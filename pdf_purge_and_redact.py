# Cursor Project: PDF "100% removal" (no blank template)
# ======================================================
# This script produces the strongest possible "no-template" cleanup:
# 1) Removes/clears ALL interactive form fields (AcroForm widgets)
# 2) Deletes ALL annotations (free-text, highlights, stamps, ink, etc.)
# 3) Removes embedded files (when supported)
# 4) Optionally applies TRUE REDACTION to user-defined zones (guaranteed removal in those areas)
#
# Usage:
#   pip install pymupdf
#
#   # Option A: purge only (forms/annotations/embedded files)
#   python pdf_purge_and_redact.py input.pdf output.pdf
#
#   # Option B: purge + true redaction by zones (recommended if typed content is "baked in")
#   python pdf_purge_and_redact.py input.pdf output.pdf --zones zones.json
#
# zones.json format (page indexes are 0-based):
# {
#   "0": [{"x1":72,"y1":120,"x2":540,"y2":170}],
#   "1": [{"x1":72,"y1":100,"x2":540,"y2":150}]
# }
#
# Coordinate system:
# - Units: PDF points (1/72 inch)
# - Origin: top-left (PyMuPDF)
#
# NOTE:
# Without a blank template, "100% removal of filled info" is only guaranteed for:
# - Form field values / widgets
# - Annotations
# - Anything inside redaction zones you specify
# If the filled text is normal page content and you don't specify zones or patterns,
# it cannot be reliably distinguished from the original template text.

import sys
import json
import argparse
import fitz  # PyMuPDF


def purge_widgets(page: fitz.Page) -> int:
    """Delete/clear AcroForm widgets (text fields, checkboxes, etc.)."""
    removed = 0
    widgets = page.widgets() or []
    for w in widgets:
        # Try to delete widget completely
        try:
            page.delete_widget(w)
            removed += 1
            continue
        except Exception:
            pass

        # Fallback: clear value
        try:
            w.field_value = ""
            w.update()
            removed += 1
        except Exception:
            pass
    return removed


def purge_annotations(page: fitz.Page) -> int:
    """Delete all annotations on the page (sticky notes, highlights, free text, stamps, etc.)."""
    removed = 0
    annot = page.first_annot
    while annot:
        nxt = annot.next
        try:
            page.delete_annot(annot)
            removed += 1
        except Exception:
            pass
        annot = nxt
    return removed


def remove_embedded_files(doc: fitz.Document) -> int:
    """Remove embedded files at document level when supported by the PDF + PyMuPDF build."""
    removed = 0
    try:
        count = doc.embfile_count()
        # Iterate by index, delete by name (best-effort)
        for i in range(count):
            try:
                info = doc.embfile_info(i) or {}
                name = info.get("name")
                if name:
                    doc.embfile_del(name)
                    removed += 1
            except Exception:
                pass
    except Exception:
        pass
    return removed


def load_zones(zones_path: str) -> dict:
    with open(zones_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("zones.json must be a JSON object mapping pageIndex -> list of rects.")
    return data


def apply_redaction_zones(doc: fitz.Document, zones: dict) -> int:
    """
    Apply TRUE redaction to specified zones.
    This removes underlying content, not just hides it.
    """
    total = 0
    for page_index_str, rects in zones.items():
        page_index = int(page_index_str)
        if page_index < 0 or page_index >= doc.page_count:
            continue
        page = doc[page_index]

        if not isinstance(rects, list):
            continue

        for r in rects:
            if not all(k in r for k in ("x1", "y1", "x2", "y2")):
                continue
            rect = fitz.Rect(r["x1"], r["y1"], r["x2"], r["y2"]) & page.rect
            if rect.is_empty:
                continue

            # Add redact annotation then apply redactions for the page
            page.add_redact_annot(rect, fill=(1, 1, 1))
            total += 1

        # Apply for this page (removes content + can remove images too)
        if rects:
            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)

    return total


def main():
    parser = argparse.ArgumentParser(description="Purge interactive PDF data and optionally true-redact zones.")
    parser.add_argument("input_pdf", help="Path to input PDF")
    parser.add_argument("output_pdf", help="Path to output PDF")
    parser.add_argument("--zones", help="Optional zones.json to true-redact (content removal)")

    args = parser.parse_args()

    doc = fitz.open(args.input_pdf)

    total_widgets = 0
    total_annots = 0

    for page in doc:
        total_widgets += purge_widgets(page)
        total_annots += purge_annotations(page)

    embedded_removed = remove_embedded_files(doc)

    redacted_zones = 0
    if args.zones:
        zones = load_zones(args.zones)
        redacted_zones = apply_redaction_zones(doc, zones)

    # Save with cleanup to drop orphaned objects and reduce the chance of recoverable remnants
    doc.save(args.output_pdf, deflate=True, garbage=4, clean=True)
    doc.close()

    print("Done.")
    print(f"Widgets removed/cleared: {total_widgets}")
    print(f"Annotations removed:     {total_annots}")
    print(f"Embedded files removed:  {embedded_removed}")
    if args.zones:
        print(f"Redaction zones applied: {redacted_zones}")
    print(f"Output: {args.output_pdf}")


if __name__ == "__main__":
    main()


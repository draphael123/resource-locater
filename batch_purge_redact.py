"""
Batch process all PDFs using pdf_purge_and_redact.py approach
and save them to a new folder.
"""

import os
import sys
from pathlib import Path
import fitz  # PyMuPDF


def purge_widgets(page: fitz.Page) -> int:
    """Delete/clear AcroForm widgets (text fields, checkboxes, etc.)."""
    removed = 0
    widgets = list(page.widgets())
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


def process_pdf(input_path: str, output_path: str) -> bool:
    """Process a single PDF file with purge and redact approach."""
    try:
        doc = fitz.open(input_path)

        total_widgets = 0
        total_annots = 0

        for page in doc:
            total_widgets += purge_widgets(page)
            total_annots += purge_annotations(page)

        embedded_removed = remove_embedded_files(doc)

        # Save with cleanup to drop orphaned objects and reduce the chance of recoverable remnants
        doc.save(output_path, deflate=True, garbage=4, clean=True)
        doc.close()

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    # Get the current directory
    current_dir = Path(".")
    output_dir = Path("purged_pdfs")
    
    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)
    
    # Find all PDF files, excluding already processed ones and test files
    pdf_files = []
    for pdf_file in current_dir.glob("*.pdf"):
        # Skip files that are already processed or test files
        if ("_cleared" not in pdf_file.name and 
            "_flattened" not in pdf_file.name and 
            "_purged" not in pdf_file.name and
            "test" not in pdf_file.name.lower() and 
            "blank" not in pdf_file.name.lower() and
            pdf_file.parent.name != "cleared_pdfs" and
            pdf_file.parent.name != "purged_pdfs"):
            pdf_files.append(pdf_file)
    
    print(f"Found {len(pdf_files)} PDF file(s) to process...\n")
    
    successful = 0
    failed = 0
    
    for pdf_file in pdf_files:
        # Create output path in the purged_pdfs folder
        output_path = output_dir / pdf_file.name
        
        print(f"Processing: {pdf_file.name}...", end=" ")
        
        if process_pdf(str(pdf_file), str(output_path)):
            print(f"[OK] -> {output_path}")
            successful += 1
        else:
            print(f"[FAILED]")
            failed += 1
    
    print(f"\nCompleted: {successful} successful, {failed} failed")
    print(f"Output folder: {output_dir.absolute()}")


if __name__ == "__main__":
    main()


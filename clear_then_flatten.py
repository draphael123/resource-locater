import sys
from pypdf import PdfReader, PdfWriter

def main():
    if len(sys.argv) < 3:
        print("Usage: python clear_then_flatten.py input.pdf output.pdf")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2]

    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Copy pages
    for page in reader.pages:
        writer.add_page(page)

    # Attempt to clear form fields
    if reader.get_fields():
        fields = reader.get_fields()
        # Update each field value to empty
        writer.update_page_form_field_values(
            writer.pages[0],  # pypdf requires a page reference; values apply across doc
            {name: "" for name in fields.keys()}
        )

    # Flatten form fields (best-effort)
    try:
        writer.flatten_annotations()
    except Exception:
        # Some versions may not have this; still save cleared values
        pass

    with open(output_pdf, "wb") as f:
        writer.write(f)

    print(f"Done. Output: {output_pdf}")

if __name__ == "__main__":
    main()


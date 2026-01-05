"""
PDF Answer Remover
Completely removes all filled-in answers from PDF forms, leaving only the blank template.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional

try:
    import pypdf
except ImportError:
    print("Error: pypdf library not found. Installing...")
    os.system(f"{sys.executable} -m pip install pypdf")
    import pypdf

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF library not found. Installing...")
    os.system(f"{sys.executable} -m pip install pymupdf")
    import fitz  # PyMuPDF


def clear_pdf_answers_pymupdf(input_path: str, output_path: Optional[str] = None) -> bool:
    """
    Completely clear all form field values from PDF using PyMuPDF.
    This method ensures all filled information is removed, leaving only the blank template.
    """
    try:
        doc = fitz.open(input_path)
        
        # Process each page to clear all form fields
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get all widgets (form fields) on this page
            widgets = list(page.widgets())
            
            for widget in widgets:
                try:
                    field_type = widget.field_type
                    
                    # Clear the field value based on its type
                    if field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                        # Text fields - completely clear
                        widget.field_value = ""
                        widget.update()
                        # Double-check and clear again
                        if widget.field_value:
                            widget.field_value = ""
                            widget.update()
                            
                    elif field_type == fitz.PDF_WIDGET_TYPE_CHECKBOX:
                        # Checkboxes - uncheck
                        widget.field_value = False
                        widget.update()
                        
                    elif field_type == fitz.PDF_WIDGET_TYPE_RADIOBUTTON:
                        # Radio buttons - unselect
                        widget.field_value = False
                        widget.update()
                        
                    elif field_type == fitz.PDF_WIDGET_TYPE_COMBOBOX:
                        # Combo boxes (dropdowns) - clear selection
                        widget.field_value = ""
                        widget.update()
                        # Try to reset choice
                        try:
                            if hasattr(widget, 'choice_values') and widget.choice_values:
                                widget.field_value = ""
                                widget.update()
                        except:
                            pass
                            
                    elif field_type == fitz.PDF_WIDGET_TYPE_LISTBOX:
                        # List boxes - clear selection
                        widget.field_value = ""
                        widget.update()
                        try:
                            if hasattr(widget, 'choice_values') and widget.choice_values:
                                widget.field_value = ""
                                widget.update()
                        except:
                            pass
                            
                    elif field_type == fitz.PDF_WIDGET_TYPE_SIGNATURE:
                        # Signature fields - clear
                        widget.field_value = ""
                        widget.update()
                        
                    else:
                        # Unknown field type - try to clear anyway
                        try:
                            widget.field_value = ""
                            widget.update()
                        except:
                            try:
                                widget.field_value = False
                                widget.update()
                            except:
                                pass
                
                except Exception as e:
                    # If clearing fails, try reset
                    try:
                        widget.reset()
                    except:
                        pass
            
            # Also clear any annotations that might contain form data
            try:
                annots = list(page.annots())
                for annot in annots:
                    annot_type = annot.type[1] if annot.type else ""
                    # Remove annotations that contain user data
                    if annot_type in ["Text", "FreeText", "Ink", "Stamp", "Highlight", "Underline", "Squiggly", "StrikeOut"]:
                        page.delete_annot(annot)
            except:
                pass
        
        # Final verification pass - ensure all fields are truly empty
        for page_num in range(len(doc)):
            page = doc[page_num]
            widgets = list(page.widgets())
            for widget in widgets:
                try:
                    # Check if field still has a value
                    current_value = widget.field_value
                    if current_value:
                        # Force clear based on type
                        if isinstance(current_value, str) and current_value.strip():
                            widget.field_value = ""
                            widget.update()
                        elif isinstance(current_value, bool) and current_value:
                            widget.field_value = False
                            widget.update()
                        elif isinstance(current_value, (list, tuple)) and current_value:
                            widget.field_value = ""
                            widget.update()
                except:
                    pass
        
        # Save the cleared PDF
        if output_path is None:
            output_path = input_path.replace(".pdf", "_cleared.pdf")
        
        # Save with garbage collection to ensure clean output
        doc.save(output_path, garbage=4, deflate=True)
        doc.close()
        
        return True
        
    except Exception as e:
        print(f"Error with PyMuPDF method: {e}")
        import traceback
        traceback.print_exc()
        return False


def clear_pdf_answers_pypdf(input_path: str, output_path: Optional[str] = None) -> bool:
    """
    Clear form fields from PDF using pypdf.
    This is a fallback method.
    """
    try:
        reader = pypdf.PdfReader(input_path)
        writer = pypdf.PdfWriter()
        
        # Clear form fields at document level
        if "/AcroForm" in reader.trailer.get("/Root", {}):
            acro_form = reader.trailer["/Root"]["/AcroForm"]
            if "/Fields" in acro_form:
                fields = acro_form["/Fields"]
                # Clear all field values
                for field_ref in fields:
                    if isinstance(field_ref, pypdf.generic.IndirectObject):
                        field = field_ref.get_object()
                        if "/V" in field:
                            del field["/V"]
                        if "/DV" in field:
                            del field["/DV"]
                        # Clear kids if present
                        if "/Kids" in field:
                            kids = field["/Kids"]
                            for kid_ref in kids:
                                if isinstance(kid_ref, pypdf.generic.IndirectObject):
                                    kid = kid_ref.get_object()
                                    if "/V" in kid:
                                        del kid["/V"]
                                    if "/DV" in kid:
                                        del kid["/DV"]
        
        # Copy pages
        for page in reader.pages:
            # Clear annotations on page
            if "/Annots" in page:
                annots = page.get("/Annots", [])
                if annots:
                    for annot_ref in annots:
                        if isinstance(annot_ref, pypdf.generic.IndirectObject):
                            annot = annot_ref.get_object()
                            if "/V" in annot:
                                annot["/V"] = pypdf.generic.TextStringObject("")
                            if "/DV" in annot:
                                annot["/DV"] = pypdf.generic.TextStringObject("")
            
            writer.add_page(page)
        
        # Create empty AcroForm
        if "/AcroForm" in reader.trailer["/Root"]:
            new_acro_form = pypdf.generic.DictionaryObject()
            writer._root_object.update({
                pypdf.generic.NameObject("/AcroForm"): new_acro_form
            })
        
        # Write output
        if output_path is None:
            output_path = input_path.replace(".pdf", "_cleared.pdf")
        
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
        
        return True
    except Exception as e:
        print(f"Error with pypdf method: {e}")
        return False


def clear_pdf_answers(input_path: str, output_path: Optional[str] = None, method: str = "auto") -> bool:
    """
    Completely clear all answers from a PDF file, leaving only the blank template.
    
    Args:
        input_path: Path to input PDF file
        output_path: Path to output PDF file (default: adds '_cleared' to filename)
        method: 'auto', 'pypdf', or 'pymupdf' - which method to use
    
    Returns:
        True if successful, False otherwise
    """
    if not os.path.exists(input_path):
        print(f"Error: File not found: {input_path}")
        return False
    
    if output_path is None:
        base_name = Path(input_path).stem
        directory = Path(input_path).parent
        output_path = str(directory / f"{base_name}_cleared.pdf")
    
    # Use PyMuPDF by default (most comprehensive)
    if method == "auto" or method == "pymupdf":
        if clear_pdf_answers_pymupdf(input_path, output_path):
            print(f"[OK] Successfully cleared: {input_path}")
            print(f"     Output: {output_path}")
            return True
        elif method == "pymupdf":
            return False
    
    # Fallback to pypdf
    if method == "auto" or method == "pypdf":
        if clear_pdf_answers_pypdf(input_path, output_path):
            print(f"[OK] Successfully cleared: {input_path}")
            print(f"     Output: {output_path}")
            return True
    
    print(f"[FAILED] Failed to clear: {input_path}")
    return False


def clear_all_pdfs_in_directory(directory: str = ".", pattern: str = "*.pdf", 
                                 exclude_cleared: bool = True) -> List[str]:
    """
    Clear answers from all PDFs in a directory.
    
    Args:
        directory: Directory to process (default: current directory)
        pattern: File pattern to match (default: "*.pdf")
        exclude_cleared: Skip files that already have "_cleared" in name
    
    Returns:
        List of successfully processed files
    """
    directory_path = Path(directory)
    pdf_files = list(directory_path.glob(pattern))
    
    if exclude_cleared:
        pdf_files = [f for f in pdf_files if "_cleared" not in f.name and "test" not in f.name.lower()]
    
    successful = []
    
    print(f"Found {len(pdf_files)} PDF file(s) to process...\n")
    
    for pdf_file in pdf_files:
        if clear_pdf_answers(str(pdf_file)):
            successful.append(str(pdf_file))
        print()  # Blank line between files
    
    print(f"\nCompleted: {len(successful)}/{len(pdf_files)} files processed successfully")
    return successful


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Completely remove all filled-in answers from PDF forms, leaving only blank templates"
    )
    parser.add_argument("input", nargs="?", help="Input PDF file (or directory if --all is used)")
    parser.add_argument("-o", "--output", help="Output PDF file path")
    parser.add_argument("-a", "--all", action="store_true", 
                       help="Process all PDFs in the current directory")
    parser.add_argument("-d", "--directory", default=".", 
                       help="Directory to process (used with --all)")
    parser.add_argument("-m", "--method", choices=["auto", "pypdf", "pymupdf"], 
                       default="auto", help="Method to use for clearing PDFs")
    
    args = parser.parse_args()
    
    if args.all:
        clear_all_pdfs_in_directory(args.directory)
    elif args.input:
        clear_pdf_answers(args.input, args.output, args.method)
    else:
        print("No input specified. Use --all to process all PDFs or provide an input file.")
        print("\nUsage examples:")
        print("  python pdf_clearer.py file.pdf")
        print("  python pdf_clearer.py file.pdf -o output.pdf")
        print("  python pdf_clearer.py --all")
        print("  python pdf_clearer.py --all -d /path/to/pdfs")

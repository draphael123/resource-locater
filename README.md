# PDF Clearer - State License Application Forms Directory

A comprehensive tool for clearing filled-in information from PDF forms and a directory website for finding blank state license application forms.

## Features

### PDF Clearing Tools
- **pdf_clearer.py**: Removes all form field values while preserving form structure
- **clear_then_flatten.py**: Clears and flattens PDF forms (makes them non-editable)
- **pdf_purge_and_redact.py**: Aggressively removes all interactive elements and annotations

### Website
- **index.html**: Interactive directory of blank state license application forms
- Search and filter by state, license type, and application type
- Direct links to official state board websites
- Search results with potential form download links

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Clear PDF Forms
```bash
# Single file
python pdf_clearer.py input.pdf

# All PDFs in directory
python pdf_clearer.py --all
```

### Website
Simply open `index.html` in your browser, or deploy to Vercel for online access.

## Deployment

This project is ready for deployment to Vercel. The website is a static HTML file with embedded data, so no server-side code is needed.

## License

MIT

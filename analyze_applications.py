"""
Analyze PDF filenames to identify states and license types,
then create a reference list for finding blank forms.
"""

import re
from pathlib import Path
from collections import defaultdict

# State abbreviations mapping
STATE_ABBREVIATIONS = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
    'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
    'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
    'WI': 'Wisconsin', 'WY': 'Wyoming'
}

def parse_filename(filename):
    """Extract state, license type, and application type from filename."""
    filename_upper = filename.upper()
    
    # Find state abbreviation
    state = None
    for abbrev in STATE_ABBREVIATIONS.keys():
        if f' {abbrev} ' in filename_upper or filename_upper.startswith(abbrev) or f'- {abbrev}' in filename_upper:
            state = abbrev
            break
    
    # Find license type
    license_type = None
    if 'NP' in filename_upper:
        license_type = 'NP'  # Nurse Practitioner
    elif 'RN' in filename_upper:
        license_type = 'RN'  # Registered Nurse
    elif 'MD' in filename_upper:
        license_type = 'MD'  # Medical Doctor
    elif 'CSR' in filename_upper:
        license_type = 'CSR'  # Controlled Substance Registration
    elif 'CDS' in filename_upper:
        license_type = 'CDS'  # Controlled Dangerous Substance
    elif 'ARNP' in filename_upper:
        license_type = 'ARNP'  # Advanced Registered Nurse Practitioner
    elif 'FNP' in filename_upper:
        license_type = 'FNP'  # Family Nurse Practitioner
    
    # Find application type
    app_type = None
    if 'INITIAL' in filename_upper or 'INITIAL' in filename_upper:
        app_type = 'Initial'
    elif 'RENEWAL' in filename_upper:
        app_type = 'Renewal'
    elif 'RX AUTH' in filename_upper or 'RX AUTH' in filename_upper:
        app_type = 'RX Authorization'
    
    return {
        'state': state,
        'state_name': STATE_ABBREVIATIONS.get(state, 'Unknown'),
        'license_type': license_type,
        'app_type': app_type,
        'filename': filename
    }

def main():
    current_dir = Path(".")
    
    # Find all original PDF files
    pdf_files = []
    for pdf_file in current_dir.glob("*.pdf"):
        if ("_cleared" not in pdf_file.name and 
            "_flattened" not in pdf_file.name and 
            "_purged" not in pdf_file.name and
            "test" not in pdf_file.name.lower() and 
            "blank" not in pdf_file.name.lower() and
            pdf_file.parent.name != "cleared_pdfs" and
            pdf_file.parent.name != "purged_pdfs"):
            pdf_files.append(pdf_file.name)
    
    print(f"Found {len(pdf_files)} original PDF files\n")
    print("=" * 80)
    
    # Parse all files
    applications = []
    for filename in sorted(pdf_files):
        info = parse_filename(filename)
        applications.append(info)
    
    # Group by state and license type
    grouped = defaultdict(list)
    for app in applications:
        key = f"{app['state']} - {app['license_type']} - {app['app_type']}"
        grouped[key].append(app)
    
    # Print summary
    print("\nAPPLICATION SUMMARY BY STATE AND LICENSE TYPE:\n")
    print(f"{'State':<15} {'License':<10} {'Type':<15} {'Count':<10}")
    print("-" * 80)
    
    for key in sorted(grouped.keys()):
        parts = key.split(' - ')
        state = parts[0] if parts[0] else 'Unknown'
        license_type = parts[1] if len(parts) > 1 else 'Unknown'
        app_type = parts[2] if len(parts) > 2 else 'Unknown'
        count = len(grouped[key])
        print(f"{state:<15} {license_type:<10} {app_type:<15} {count:<10}")
    
    # Create detailed list
    print("\n" + "=" * 80)
    print("\nDETAILED LIST FOR BLANK FORM SEARCH:\n")
    
    unique_apps = {}
    for app in applications:
        key = (app['state'], app['license_type'], app['app_type'])
        if key not in unique_apps:
            unique_apps[key] = app
    
    # Sort with None handling
    sorted_apps = sorted(unique_apps.items(), key=lambda x: (
        x[0][0] or 'ZZZ',  # state
        x[0][1] or 'ZZZ',  # license_type
        x[0][2] or 'ZZZ'   # app_type
    ))
    
    for (state, license_type, app_type), app in sorted_apps:
        print(f"\n{app['state_name']} ({state or 'Unknown'}) - {license_type or 'Unknown'} - {app_type or 'Unknown'}")
        print(f"  Search terms: '{app['state_name']} {license_type or ''} {app_type or ''} application blank form'")
        if license_type in ['RN', 'NP', 'ARNP', 'FNP']:
            print(f"  Board: {app['state_name']} Board of Nursing")
        elif license_type == 'MD':
            print(f"  Board: {app['state_name']} Board of Medical Practice")
        elif license_type in ['CSR', 'CDS']:
            print(f"  Board: {app['state_name']} Board of Pharmacy or Medical Board")
    
    # Save to file
    output_file = Path("blank_forms_needed.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("BLANK APPLICATION FORMS NEEDED\n")
        f.write("=" * 80 + "\n\n")
        for (state, license_type, app_type), app in sorted_apps:
            f.write(f"{app['state_name']} ({state}) - {license_type} - {app_type}\n")
            f.write(f"  Search: '{app['state_name']} {license_type} {app_type} application blank form'\n")
            if license_type in ['RN', 'NP', 'ARNP', 'FNP']:
                f.write(f"  Board: {app['state_name']} Board of Nursing\n")
            elif license_type == 'MD':
                f.write(f"  Board: {app['state_name']} Board of Medical Practice\n")
            elif license_type in ['CSR', 'CDS']:
                f.write(f"  Board: {app['state_name']} Board of Pharmacy or Medical Board\n")
            f.write("\n")
    
    print(f"\n\nSummary saved to: {output_file}")
    print(f"\nTotal unique application types needed: {len(unique_apps)}")

if __name__ == "__main__":
    main()


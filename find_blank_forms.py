"""
Web search helper to find blank application forms for each state and license type.
This script searches for forms and provides URLs, but cannot directly download files.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path
from urllib.parse import quote, urljoin
import re

# State board website patterns (common URLs)
STATE_BOARD_PATTERNS = {
    'AZ': {
        'nursing': 'https://www.azbn.gov',
        'medical': 'https://www.azmd.gov'
    },
    'CA': {
        'nursing': 'https://www.rn.ca.gov',
        'medical': 'https://www.mbc.ca.gov'
    },
    'CO': {
        'nursing': 'https://dora.colorado.gov/professions/nursing',
        'medical': 'https://dora.colorado.gov/professions/physicians'
    },
    'HI': {
        'nursing': 'https://cca.hawaii.gov/pvl/boards/nursing',
        'medical': 'https://cca.hawaii.gov/pvl/boards/medicine'
    },
    'IL': {
        'nursing': 'https://www.idfpr.com/profs/nursing.asp',
        'medical': 'https://www.idfpr.com/profs/medical.asp',
        'pharmacy': 'https://www.idfpr.com/profs/pharmacy.asp'
    },
    'IN': {
        'nursing': 'https://www.in.gov/pla/nursing',
        'medical': 'https://www.in.gov/pla/medical',
        'pharmacy': 'https://www.in.gov/pla/pharmacy'
    },
    'MA': {
        'nursing': 'https://www.mass.gov/orgs/board-of-registration-in-nursing',
        'medical': 'https://www.mass.gov/orgs/board-of-registration-in-medicine'
    },
    'MD': {
        'nursing': 'https://mbon.maryland.gov',
        'medical': 'https://www.mbp.state.md.us'
    },
    'ME': {
        'nursing': 'https://www.maine.gov/boardofnursing',
        'medical': 'https://www.maine.gov/md'
    },
    'MI': {
        'nursing': 'https://www.michigan.gov/lara/bureau-list/bpl/health/hp-lic-health-prof/nursing',
        'medical': 'https://www.michigan.gov/lara/bureau-list/bpl/health/hp-lic-health-prof/physicians'
    },
    'MN': {
        'nursing': 'https://mn.gov/boards/nursing',
        'medical': 'https://mn.gov/boards/medical-practice'
    },
    'ND': {
        'nursing': 'https://www.ndbon.org',
        'medical': 'https://www.ndbom.org'
    },
    'NJ': {
        'nursing': 'https://www.njconsumeraffairs.gov/nur',
        'medical': 'https://www.njconsumeraffairs.gov/med',
        'pharmacy': 'https://www.njconsumeraffairs.gov/phar'
    },
    'NM': {
        'nursing': 'https://www.rld.nm.gov/boards-and-commissions/individual-boards-and-commissions/nursing-board',
        'medical': 'https://www.rld.nm.gov/boards-and-commissions/individual-boards-and-commissions/medical-board',
        'pharmacy': 'https://www.rld.nm.gov/boards-and-commissions/individual-boards-and-commissions/pharmacy-board'
    },
    'OH': {
        'nursing': 'https://www.nursing.ohio.gov',
        'medical': 'https://www.med.ohio.gov'
    },
    'PA': {
        'nursing': 'https://www.dos.pa.gov/ProfessionalLicensing/BoardsCommissions/Nursing',
        'medical': 'https://www.dos.pa.gov/ProfessionalLicensing/BoardsCommissions/Medicine'
    },
    'SD': {
        'nursing': 'https://doh.sd.gov/boards/nursing',
        'medical': 'https://doh.sd.gov/boards/medical'
    },
    'UT': {
        'nursing': 'https://dopl.utah.gov/nursing',
        'medical': 'https://dopl.utah.gov/physician'
    },
    'VA': {
        'nursing': 'https://www.dhp.virginia.gov/nursing',
        'medical': 'https://www.dhp.virginia.gov/medicine'
    },
    'WA': {
        'nursing': 'https://www.doh.wa.gov/licensespermitsandcertificates/nursingcommission',
        'medical': 'https://www.doh.wa.gov/licensespermitsandcertificates/medicalcommission'
    }
}

def get_board_type(license_type):
    """Determine board type from license type."""
    if license_type in ['RN', 'NP', 'ARNP', 'FNP']:
        return 'nursing'
    elif license_type == 'MD':
        return 'medical'
    elif license_type in ['CSR', 'CDS']:
        return 'pharmacy'
    return 'nursing'  # default

def search_google(query, max_results=3):
    """Search Google for the query and return top results."""
    try:
        # Using DuckDuckGo HTML search as fallback (no API key needed)
        url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            for link in soup.find_all('a', class_='result__a', limit=max_results):
                href = link.get('href', '')
                text = link.get_text(strip=True)
                if href:
                    results.append({'title': text, 'url': href})
            return results
    except Exception as e:
        print(f"  Search error: {e}")
    return []

def find_form_urls(state, state_name, license_type, app_type):
    """Find URLs for blank forms."""
    results = {
        'state': state,
        'state_name': state_name,
        'license_type': license_type,
        'app_type': app_type,
        'board_url': None,
        'search_results': [],
        'suggested_urls': []
    }
    
    # Get board URL if available
    if state in STATE_BOARD_PATTERNS:
        board_type = get_board_type(license_type)
        if board_type in STATE_BOARD_PATTERNS[state]:
            results['board_url'] = STATE_BOARD_PATTERNS[state][board_type]
    
    # Create search query
    if license_type and app_type:
        query = f"{state_name} {license_type} {app_type} application blank form PDF"
    elif license_type:
        query = f"{state_name} {license_type} application blank form PDF"
    else:
        query = f"{state_name} application blank form PDF"
    
    # Search for forms
    print(f"  Searching: {query}")
    search_results = search_google(query, max_results=5)
    results['search_results'] = search_results
    
    # Create suggested URLs based on common patterns
    if results['board_url']:
        base = results['board_url']
        suggested = [
            f"{base}/applications",
            f"{base}/forms",
            f"{base}/licensing",
            f"{base}/apply",
            f"{base}/downloads"
        ]
        results['suggested_urls'] = suggested
    
    return results

def main():
    # Load the applications list
    applications_file = Path("blank_forms_needed.txt")
    if not applications_file.exists():
        print("Error: blank_forms_needed.txt not found. Run analyze_applications.py first.")
        return
    
    # Parse applications from the file
    applications = []
    with open(applications_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract application info
    pattern = r'(\w+) \((\w+)\) - (.+?) - (.+?)\n'
    matches = re.findall(pattern, content)
    
    for match in matches:
        state_name, state, license_type, app_type = match
        if state != 'Unknown' and license_type != 'Unknown':
            applications.append({
                'state': state,
                'state_name': state_name,
                'license_type': license_type,
                'app_type': app_type
            })
    
    print(f"Found {len(applications)} applications to search for\n")
    print("=" * 80)
    
    all_results = []
    
    for i, app in enumerate(applications, 1):
        print(f"\n[{i}/{len(applications)}] {app['state_name']} ({app['state']}) - {app['license_type']} - {app['app_type']}")
        result = find_form_urls(
            app['state'],
            app['state_name'],
            app['license_type'],
            app['app_type']
        )
        all_results.append(result)
        
        if result['board_url']:
            print(f"  Board URL: {result['board_url']}")
        
        if result['search_results']:
            print(f"  Found {len(result['search_results'])} search results:")
            for idx, sr in enumerate(result['search_results'][:3], 1):
                print(f"    {idx}. {sr['title'][:60]}...")
                print(f"       {sr['url']}")
        
        # Small delay to avoid rate limiting
        time.sleep(1)
    
    # Save results to JSON
    output_file = Path("form_search_results.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    # Create HTML report
    html_file = Path("form_search_results.html")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Blank Form Search Results</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .app { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
        .board-url { color: #0066cc; font-weight: bold; }
        .search-result { margin: 10px 0; padding: 10px; background: #f5f5f5; }
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Blank Application Form Search Results</h1>
""")
        
        for result in all_results:
            f.write(f"""
    <div class="app">
        <h2>{result['state_name']} ({result['state']}) - {result['license_type']} - {result['app_type']}</h2>
""")
            if result['board_url']:
                f.write(f'        <p><span class="board-url">Board URL:</span> <a href="{result["board_url"]}" target="_blank">{result["board_url"]}</a></p>\n')
            
            if result['suggested_urls']:
                f.write("        <p><strong>Suggested URLs to check:</strong></p><ul>\n")
                for url in result['suggested_urls']:
                    f.write(f'            <li><a href="{url}" target="_blank">{url}</a></li>\n')
                f.write("        </ul>\n")
            
            if result['search_results']:
                f.write("        <p><strong>Search Results:</strong></p>\n")
                for sr in result['search_results']:
                    f.write(f'        <div class="search-result">\n')
                    f.write(f'            <a href="{sr["url"]}" target="_blank">{sr["title"]}</a><br>\n')
                    f.write(f'            <small>{sr["url"]}</small>\n')
                    f.write(f'        </div>\n')
            
            f.write("    </div>\n")
        
        f.write("""
</body>
</html>
""")
    
    print(f"\n\nResults saved to:")
    print(f"  - {output_file} (JSON)")
    print(f"  - {html_file} (HTML - open in browser)")
    print(f"\nTotal applications searched: {len(all_results)}")

if __name__ == "__main__":
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.check_call(["pip", "install", "requests", "beautifulsoup4"])
        import requests
        from bs4 import BeautifulSoup
    
    main()


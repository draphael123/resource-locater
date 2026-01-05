"""
Embed JSON data directly into HTML file to avoid CORS issues
"""

import json
from pathlib import Path

# Read the JSON file
json_file = Path("form_search_results.json")
html_file = Path("index.html")

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filter out invalid entries
filtered_data = [item for item in data if item.get('state') and item.get('state') != 'None' and item.get('license_type') and item.get('license_type') != 'None']

# Read the HTML file
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Find the script section and replace the loadForms function
# We'll embed the data as a JavaScript variable
json_str = json.dumps(filtered_data, ensure_ascii=False, indent=2)

# Replace the async loadForms function with one that uses embedded data
old_load_function = """        // Load form data
        async function loadForms() {
            try {
                const response = await fetch('form_search_results.json');
                allForms = await response.json();
                
                // Filter out unknown/invalid entries
                allForms = allForms.filter(form => 
                    form.state && form.state !== 'None' && 
                    form.license_type && form.license_type !== 'None'
                );
                
                filteredForms = [...allForms];
                updateStats();
                renderForms();
                document.getElementById('lastUpdated').textContent = new Date().toLocaleDateString();
            } catch (error) {
                console.error('Error loading forms:', error);
                document.getElementById('formGrid').innerHTML = 
                    '<div class="no-results">Error loading form data. Please ensure form_search_results.json is available.</div>';
            }
        }"""

new_load_function = f"""        // Embedded form data (loaded directly to avoid CORS issues)
        const embeddedFormData = {json_str};
        
        // Load form data
        function loadForms() {{
            try {{
                allForms = embeddedFormData;
                filteredForms = [...allForms];
                updateStats();
                renderForms();
                document.getElementById('lastUpdated').textContent = new Date().toLocaleDateString();
            }} catch (error) {{
                console.error('Error loading forms:', error);
                document.getElementById('formGrid').innerHTML = 
                    '<div class="no-results">Error loading form data.</div>';
            }}
        }}"""

# Replace in HTML
html_content = html_content.replace(old_load_function, new_load_function)

# Write the updated HTML
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully embedded {len(filtered_data)} forms into {html_file}")
print(f"Filtered out {len(data) - len(filtered_data)} invalid entries")


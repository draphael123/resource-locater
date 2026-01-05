"""
Create a complete HTML file with embedded JSON data, removing suggested_urls
"""
import json
from pathlib import Path

# Read the JSON file
json_file = Path("form_search_results.json")
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filter out invalid entries
filtered_data = [item for item in data if item.get('state') and item.get('state') != 'None' and item.get('license_type') and item.get('license_type') != 'None']

# Remove suggested_urls from each item
for item in filtered_data:
    if 'suggested_urls' in item:
        del item['suggested_urls']

# Convert to JSON string for embedding
json_str = json.dumps(filtered_data, ensure_ascii=False, indent=2)

# Read the HTML template
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>State License Application Forms Directory</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            background-attachment: fixed;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            animation: fadeIn 0.6s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 4px solid transparent;
            border-image: linear-gradient(90deg, #667eea, #764ba2, #f093fb) 1;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        h1 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3em;
            margin-bottom: 15px;
            font-weight: 800;
            letter-spacing: -1px;
        }
        
        .subtitle {
            color: #666;
            font-size: 1.2em;
            margin-top: 10px;
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 25px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        
        .stat-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            transition: transform 0.3s, box-shadow 0.3s;
            min-width: 120px;
        }
        
        .stat-box:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        }
        
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            display: block;
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.95;
            margin-top: 5px;
        }
        
        .how-to-use {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 30px;
            border-radius: 15px;
            margin: 30px 0;
            border-left: 5px solid #667eea;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .how-to-use h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .how-to-use h2::before {
            content: "📖";
            font-size: 1.2em;
        }
        
        .instructions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .instruction-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .instruction-card:hover {
            transform: translateY(-3px);
        }
        
        .instruction-card .step-number {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        
        .instruction-card h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.2em;
        }
        
        .instruction-card p {
            color: #666;
            line-height: 1.6;
        }
        
        .search-box {
            margin: 30px 0;
            text-align: center;
            position: relative;
        }
        
        #searchInput {
            width: 100%;
            max-width: 600px;
            padding: 15px 25px;
            font-size: 1.1em;
            border: 3px solid #e0e0e0;
            border-radius: 30px;
            outline: none;
            transition: all 0.3s;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }
        
        #searchInput:focus {
            border-color: #667eea;
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
            transform: scale(1.02);
        }
        
        .filters {
            display: flex;
            gap: 12px;
            margin: 25px 0;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .filter-btn {
            padding: 12px 24px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 1em;
            font-weight: 600;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .filter-btn:hover {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .filter-btn.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        
        .form-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            padding: 25px;
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }
        
        .form-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 5px;
            background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        }
        
        .form-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            border-color: #667eea;
        }
        
        .form-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 20px;
        }
        
        .form-title {
            font-size: 1.4em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }
        
        .form-info {
            color: #666;
            font-size: 0.95em;
            margin-bottom: 15px;
        }
        
        .form-badge {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            white-space: nowrap;
            box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
        }
        
        .board-link {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            text-decoration: none;
            margin: 8px 8px 8px 0;
            font-size: 0.95em;
            font-weight: 600;
            transition: all 0.3s;
            box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
        }
        
        .board-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.5);
            background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
        }
        
        .search-results {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
        }
        
        .search-results-title {
            font-size: 0.9em;
            color: #667eea;
            margin-bottom: 12px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .search-link {
            display: block;
            color: #667eea;
            text-decoration: none;
            padding: 10px 0;
            font-size: 0.9em;
            border-bottom: 1px solid #f0f0f0;
            transition: all 0.3s;
            position: relative;
            padding-left: 25px;
        }
        
        .search-link::before {
            content: "🔗";
            position: absolute;
            left: 0;
        }
        
        .search-link:hover {
            color: #764ba2;
            padding-left: 30px;
            border-bottom-color: #667eea;
        }
        
        .no-results {
            text-align: center;
            padding: 60px 40px;
            color: #999;
            font-size: 1.3em;
        }
        
        .no-results::before {
            content: "🔍";
            font-size: 3em;
            display: block;
            margin-bottom: 20px;
        }
        
        footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 3px solid #e0e0e0;
            color: #666;
            font-size: 0.95em;
        }
        
        footer p {
            margin: 10px 0;
        }
        
        @media (max-width: 768px) {
            .form-grid {
                grid-template-columns: 1fr;
            }
            
            h1 {
                font-size: 2em;
            }
            
            .container {
                padding: 20px;
            }
            
            .instructions {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📋 State License Application Forms</h1>
            <p class="subtitle">Complete directory of blank application forms for healthcare professionals</p>
            <div class="stats" id="stats">
                <div class="stat-box">
                    <div class="stat-number" id="totalForms">0</div>
                    <div class="stat-label">Total Forms</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number" id="totalStates">0</div>
                    <div class="stat-label">States</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number" id="totalTypes">0</div>
                    <div class="stat-label">License Types</div>
                </div>
            </div>
        </header>
        
        <div class="how-to-use">
            <h2>How to Use This Website</h2>
            <div class="instructions">
                <div class="instruction-card">
                    <div class="step-number">1</div>
                    <h3>Search for Forms</h3>
                    <p>Use the search box to find forms by state name, license type (RN, NP, MD, etc.), or application type (Initial, Renewal).</p>
                </div>
                <div class="instruction-card">
                    <div class="step-number">2</div>
                    <h3>Filter by Category</h3>
                    <p>Click the filter buttons to quickly view forms by license type (RN, NP, MD, CSR) or application type (Initial, Renewal).</p>
                </div>
                <div class="instruction-card">
                    <div class="step-number">3</div>
                    <h3>Access Official Links</h3>
                    <p>Each form card shows the official state board website link. Click "Official Board Website" to visit the state's licensing board.</p>
                </div>
                <div class="instruction-card">
                    <div class="step-number">4</div>
                    <h3>Find Download Links</h3>
                    <p>Check the "Search Results" section in each card for potential direct download links to blank application forms.</p>
                </div>
            </div>
            <p style="margin-top: 20px; color: #666; font-style: italic;">
                💡 <strong>Tip:</strong> Always verify form versions and requirements on the official state board websites. Forms may be updated periodically.
            </p>
        </div>
        
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔍 Search by state, license type, or application type...">
        </div>
        
        <div class="filters">
            <button class="filter-btn active" data-filter="all">All Forms</button>
            <button class="filter-btn" data-filter="RN">RN</button>
            <button class="filter-btn" data-filter="NP">NP</button>
            <button class="filter-btn" data-filter="MD">MD</button>
            <button class="filter-btn" data-filter="CSR">CSR</button>
            <button class="filter-btn" data-filter="Initial">Initial</button>
            <button class="filter-btn" data-filter="Renewal">Renewal</button>
        </div>
        
        <div class="form-grid" id="formGrid">
            <!-- Forms will be inserted here by JavaScript -->
        </div>
        
        <div class="no-results" id="noResults" style="display: none;">
            No forms found matching your search criteria.
        </div>
        
        <footer>
            <p>Last updated: <span id="lastUpdated"></span></p>
            <p>This directory provides links to official state board websites and search results for blank application forms.</p>
            <p style="margin-top: 15px; font-size: 0.85em; color: #999;">
                Note: Always verify form versions and requirements on the official state board websites.
            </p>
        </footer>
    </div>
    
    <script>
        let allForms = [];
        let filteredForms = [];
        
        // Embedded form data (loaded directly to avoid CORS issues)
        const embeddedFormData = {json_data};
        
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
        }}
        
        function updateStats() {{
            const totalForms = allForms.length;
            const uniqueStates = new Set(allForms.map(f => f.state)).size;
            const uniqueTypes = new Set(allForms.map(f => f.license_type)).size;
            
            document.getElementById('totalForms').textContent = totalForms;
            document.getElementById('totalStates').textContent = uniqueStates;
            document.getElementById('totalTypes').textContent = uniqueTypes;
        }}
        
        function renderForms() {{
            const grid = document.getElementById('formGrid');
            const noResults = document.getElementById('noResults');
            
            if (filteredForms.length === 0) {{
                grid.style.display = 'none';
                noResults.style.display = 'block';
                return;
            }}
            
            grid.style.display = 'grid';
            noResults.style.display = 'none';
            
            grid.innerHTML = filteredForms.map(form => {{
                const stateName = form.state_name || form.state;
                const licenseType = form.license_type || 'Unknown';
                const appType = form.app_type || 'Application';
                const badgeColor = getBadgeColor(licenseType);
                
                let boardLinks = '';
                if (form.board_url) {{
                    const boardUrl = form.board_url.startsWith('http') ? form.board_url : `https://${{form.board_url}}`;
                    boardLinks = `<a href="${{boardUrl}}" target="_blank" class="board-link">Official Board Website</a>`;
                }}
                
                let searchLinks = '';
                if (form.search_results && form.search_results.length > 0) {{
                    searchLinks = '<div class="search-results"><div class="search-results-title">Search Results:</div>';
                    form.search_results.slice(0, 3).forEach(result => {{
                        let url = result.url;
                        if (!url.startsWith('http')) {{
                            // Decode DuckDuckGo redirect URLs
                            if (url.includes('uddg=')) {{
                                try {{
                                    const match = url.match(/uddg=([^&]+)/);
                                    if (match) {{
                                        url = decodeURIComponent(match[1]);
                                    }}
                                }} catch (e) {{
                                    // If decoding fails, just prepend https:
                                    url = 'https:' + url;
                                }}
                            }} else {{
                                url = 'https:' + url;
                            }}
                        }}
                        searchLinks += `<a href="${{url}}" target="_blank" class="search-link">${{result.title}}</a>`;
                    }});
                    searchLinks += '</div>';
                }}
                
                return `
                    <div class="form-card" data-state="${{form.state}}" data-type="${{form.license_type}}" data-app="${{form.app_type}}">
                        <div class="form-header">
                            <div>
                                <div class="form-title">${{stateName}}</div>
                                <div class="form-info">${{licenseType}} - ${{appType}}</div>
                            </div>
                            <span class="form-badge" style="background: ${{badgeColor}}">${{form.state}}</span>
                        </div>
                        ${{boardLinks}}
                        ${{searchLinks}}
                    </div>
                `;
            }}).join('');
        }}
        
        function getBadgeColor(licenseType) {{
            const colors = {{
                'RN': '#667eea',
                'NP': '#764ba2',
                'MD': '#f093fb',
                'CSR': '#4facfe',
                'CDS': '#43e97b',
                'ARNP': '#fa709a',
                'FNP': '#fee140'
            }};
            return colors[licenseType] || '#667eea';
        }}
        
        function filterForms(filter) {{
            if (filter === 'all') {{
                filteredForms = [...allForms];
            }} else {{
                filteredForms = allForms.filter(form => 
                    form.license_type === filter || 
                    form.app_type === filter ||
                    form.state === filter
                );
            }}
            renderForms();
        }}
        
        // Event listeners
        document.getElementById('searchInput').addEventListener('input', (e) => {{
            const query = e.target.value.toLowerCase();
            filteredForms = allForms.filter(form => {{
                const stateName = (form.state_name || form.state || '').toLowerCase();
                const licenseType = (form.license_type || '').toLowerCase();
                const appType = (form.app_type || '').toLowerCase();
                return stateName.includes(query) || 
                       licenseType.includes(query) || 
                       appType.includes(query);
            }});
            renderForms();
        }});
        
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', (e) => {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                filterForms(e.target.dataset.filter);
            }});
        }});
        
        // Initialize
        loadForms();
    </script>
</body>
</html>"""

# Replace the JSON data placeholder
html_content = html_template.replace('{json_data}', json_str)

# Write the complete HTML file
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully created index.html with {len(filtered_data)} forms")
print(f"   - Removed suggested_urls from all forms")
print(f"   - Added 'How to Use' section")
print(f"   - Enhanced visual design with gradients and animations")


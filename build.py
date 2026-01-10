import markdown
import os
import re

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(BASE_DIR, 'index.md')
TEMPLATE_FILE = os.path.join(BASE_DIR, 'templates', 'base.html')
OUTPUT_FILE = os.path.join(BASE_DIR, 'index.html')

def build_site():
    # 1. Read the Markdown file
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 2. Convert Markdown to HTML
    # We use 'extra' extension for better features (tables, attr_list, etc.)
    html_content = markdown.markdown(md_content, extensions=['extra'])

    # 3. Split content into Header and Main
    # We assume the first <h1> and the immediately following <p> belong to the header.
    # This is a simple regex approach to separate the title card from the body.
    header_content = ""
    main_content = html_content

    # Find the first h1 and p
    match = re.match(r'(<h1>.*?</h1>\s*<p>.*?</p>)', html_content, re.DOTALL)
    if match:
        header_content = match.group(1)
        # Remove the header content from the main content
        main_content = html_content[len(header_content):].strip()
    
    # 4. Read the Template
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template = f.read()

    # 5. Inject content
    final_html = template.replace('{{ header_content }}', header_content)
    final_html = final_html.replace('{{ main_content }}', main_content)

    # 6. Write the Output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"Successfully built {OUTPUT_FILE} from {MD_FILE}")

if __name__ == "__main__":
    build_site()
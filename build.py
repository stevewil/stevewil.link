import markdown
import os
import re
from PIL import Image

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(BASE_DIR, 'index.md')
TEMPLATE_FILE = os.path.join(BASE_DIR, 'templates', 'base.html')
OUTPUT_FILE = os.path.join(BASE_DIR, 'index.html')
IMAGE_FILE = os.path.join(BASE_DIR, 'concierge.jpg')
FAVICON_FILE = os.path.join(BASE_DIR, 'favicon.ico')

def build_site():
    # 0. Generate Favicon
    if os.path.exists(IMAGE_FILE):
        try:
            img = Image.open(IMAGE_FILE)
            # Save as ICO containing multiple sizes
            img.save(FAVICON_FILE, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
            print(f"Generated favicon at {FAVICON_FILE}")
        except Exception as e:
            print(f"Error generating favicon: {e}")

    # 1. Read the Markdown file
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 2. Convert Markdown to HTML
    # We use 'extra' extension for better features and 'toc' for the menu
    # toc_depth='2-2' ensures only ## headers are included in the menu
    md = markdown.Markdown(extensions=['extra', 'toc'], extension_configs={'toc': {'toc_depth': '2-2'}})
    html_content = md.convert(md_content)
    nav_content = md.toc

    # 3. Split content into Header and Main
    # We assume the first <h1> and the immediately following <p> belong to the header.
    # This is a simple regex approach to separate the title card from the body.
    header_content = ""
    main_content = html_content

    # Find the first h1 and p
    # Updated regex to handle attributes (like id) added by TOC extension
    match = re.match(r'(<h1.*?>.*?</h1>\s*<p.*?>.*?</p>)', html_content, re.DOTALL)
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
    final_html = final_html.replace('{{ nav_content }}', nav_content)

    # 6. Write the Output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"Successfully built {OUTPUT_FILE} from {MD_FILE}")

if __name__ == "__main__":
    build_site()
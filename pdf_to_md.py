import pdfplumber

pdf_file = "2023-24-NBA-Season-Official-Playing-Rules.pdf"

with pdfplumber.open(pdf_file) as pdf:
    markdown_text = ""
    for page in pdf.pages:
        markdown_text += page.extract_text()
    
    with open("nba_rulebook.md", "w", errors='replace') as file:
        file.write(markdown_text)
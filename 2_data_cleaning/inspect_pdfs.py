import pdfplumber, glob

for path in sorted(glob.glob("1_datasets/raw/*.pdf")):
    with pdfplumber.open(path) as pdf:
        print("=" * 70)
        print(path, "| pages:", len(pdf.pages))
        page = pdf.pages[0]
        print("--- first 15 lines of text ---")
        print("\n".join((page.extract_text() or "").split("\n")[:15]))
        tables = page.extract_tables()
        print("--- tables found on page 1:", len(tables))
        if tables:
            for row in tables[0][:5]:
                print(row)

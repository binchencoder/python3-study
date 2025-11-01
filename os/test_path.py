from pathlib import Path

path = "/mnt/work/code/extractor/pdf-extractor/output/Fanning/A.pdf"

if __name__ == '__main__':
    pdf_path = Path(path)
    print(pdf_path.parent)

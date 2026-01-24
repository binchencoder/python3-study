import os
from pathlib import Path

path = "/mnt/work/code/extractor/pdf-extractor/output/Fanning/A.pdf"

if __name__ == '__main__':
    pdf_path = Path(path)
    print(f"pdf_path.parent = {pdf_path.parent}")

    print(f"pdf_path.stem = {pdf_path.stem}")

    print(f"pdf_path.name = {pdf_path.name}")

    print(f"os.path.splitext(pdf_path) = {os.path.splitext(pdf_path)}")
    print(f"os.path.split(pdf_path) = {os.path.split(pdf_path)} ")

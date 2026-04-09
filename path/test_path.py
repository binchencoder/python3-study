from pathlib import Path

if __name__ == '__main__':
    path = Path("/Volumes/BinchenCoder/python_workspace/extractor/pdf-extractor/output/AntibioticRiverConcentration-main.md")

    print(f"path.resolve() = {path.resolve()}")
    print(f"path.stem() = {path.stem}")


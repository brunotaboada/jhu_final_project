"""Assemble the Colab upload bundles for the final project.

Produces two zips in the repo root:

  * Papers.zip          -> contains the Papers/ folder of research PDFs
                           (the notebook unzips this to /content/Papers).
  * Project_Files.zip   -> contains config.json, NOFO.pdf,
                           Research_Proposal_Template.pdf and Papers.zip
                           (the notebook unzips this first, into /content).

Usage (from repo root):

    python3 scripts/build_project_files.py

config.json (with your real Great Learning key) must exist in the repo root.
If it does not, config.example.json is bundled instead so you can fill it in
inside Colab. Neither zip is committed to git — they are build artifacts.
"""
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def build_papers_zip() -> Path:
    out = ROOT / "Papers.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for pdf in sorted((DATA / "Papers").glob("*.pdf")):
            z.write(pdf, arcname=f"Papers/{pdf.name}")
    print(f"Built {out.name} with {len(list((DATA / 'Papers').glob('*.pdf')))} papers")
    return out


def build_project_files_zip(papers_zip: Path) -> Path:
    out = ROOT / "Project_Files.zip"
    config = ROOT / "config.json"
    if not config.exists():
        config = ROOT / "config.example.json"
        print("WARNING: config.json not found, bundling config.example.json instead")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(config, arcname="config.json")
        z.write(DATA / "NOFO.pdf", arcname="NOFO.pdf")
        z.write(DATA / "Research_Proposal_Template.pdf", arcname="Research_Proposal_Template.pdf")
        z.write(papers_zip, arcname="Papers.zip")
    print(f"Built {out.name}")
    return out


if __name__ == "__main__":
    papers = build_papers_zip()
    build_project_files_zip(papers)

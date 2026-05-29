# AI for Research Proposal Automation — JHU AGAI Final Project

A generative-AI assistant that helps a researcher (Dr. Ian McCulloh) turn a large,
loosely-related body of prior work into a competitive **NIH research proposal**
aligned to a specific **Notice of Funding Opportunity (NOFO)** — here NIMH
`PAR-25-136`, *Laboratories to Optimize Digital Health* (digital mental health
interventions).

The deliverable is the notebook in [`notebook/JHU_AGAI_Final_Project.ipynb`](notebook/JHU_AGAI_Final_Project.ipynb),
which is **built to run as-is in Google Colab** and then be exported to HTML for
submission.

## Pipeline

| Step | What it does |
|------|--------------|
| Setup | Loads the API key + base URL from `config.json` and configures `gpt-4o-mini` (LangChain `ChatOpenAI`). |
| 1. Topic Extraction | LLM reads the full NOFO and returns the single funding topic. |
| 2. Relevance Assessment | Chunks + embeds all papers (`all-MiniLM-L6-v2`), indexes them in FAISS, semantic-searches for the topic, and summarises each relevant paper. |
| 3. Proposal Ideation | Generates 5 structured ideas (title, description, citation, NOFO alignment, source file path); picks one and regex-extracts its source paper path. |
| 4. Proposal Blueprint | Drafts a full proposal from the chosen idea + source paper + sample template. |
| 5. Evaluation (LLM-as-Judge) | Scores the draft 1–5 on Innovation, Significance, Approach, Investigator Expertise as JSON. |
| 6. Human Review | Checkpoint for manual refinement. |
| 7. Summary & Recommendation | Written project summary + improvement ideas (in the notebook). |

## Repository layout

```
notebook/JHU_AGAI_Final_Project.ipynb   # the completed notebook (run in Colab)
data/NOFO.pdf                           # the funding opportunity
data/Research_Proposal_Template.pdf     # sample proposal template
data/Papers/P1..P5_*.pdf                # the 5 candidate research papers
config.example.json                     # config template (copy to config.json)
scripts/fill_notebook.py                # fills the notebook's blanks (reproducible)
scripts/build_project_files.py          # builds Papers.zip / Project_Files.zip for Colab
```

## Running it in Colab

1. Create your `config.json` from the template:
   ```bash
   cp config.example.json config.json   # then paste your Great Learning key
   ```
2. Build the upload bundle:
   ```bash
   python3 scripts/build_project_files.py
   ```
   This produces `Project_Files.zip` (config + NOFO + template + `Papers.zip`).
3. Open the notebook in Colab, upload `Project_Files.zip` to the session, and run
   the cells top to bottom. The notebook unzips to `/content/` and expects:
   `/content/config.json`, `/content/NOFO.pdf`,
   `/content/Research_Proposal_Template.pdf`, and `/content/Papers/`.
4. When finished, export **File → Download → .html** and submit the HTML.

> **Note on restarts:** the install cells intentionally trigger Colab runtime
> restarts (the notebook tells you when to click *Cancel* vs *Restart*). After a
> restart, continue from the next cell.

## Security note

`config.json` holds a live API key and is **git-ignored** — it is intentionally
not committed. Only `config.example.json` (placeholders) is tracked. `Papers.zip`
and `Project_Files.zip` are build artifacts and are also git-ignored; regenerate
them with `scripts/build_project_files.py`.

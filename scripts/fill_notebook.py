"""Fill in the blanks of the JHU AGAI Final Project notebook.

This edits the target cells in place (by index) with completed config,
LLM setup, prompts and supporting code. Run from the repo root:

    python3 scripts/fill_notebook.py
"""
import json
from pathlib import Path

NB_PATH = Path("notebook/JHU_AGAI_Final_Project.ipynb")

# ---------------------------------------------------------------------------
# Cell sources (keyed by cell index in the original learner notebook)
# ---------------------------------------------------------------------------

CONFIG_CELL = '''# @title Loading the `config.json` file
import json
import os

# Load the JSON file and extract values
file_name = 'config.json'
with open(file_name, 'r') as file:
    config = json.load(file)
    os.environ['OPENAI_API_KEY'] = config.get("OPENAI_API_KEY") # Loading the API Key
    os.environ["OPENAI_BASE_URL"] = config.get("OPENAI_BASE_URL") # Loading the API Base Url
'''

LLM_CELL = '''# @title Defining the LLM Model - Use `gpt-4o-mini` Model
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
'''

NOFO_LOADER_CELL = '''from langchain.document_loaders import PyPDFLoader

# Reading the NOFO Document
pdf_file = "/content/NOFO.pdf"
pdf_loader = PyPDFLoader(pdf_file);
NOFO_pdf = pdf_loader.load()
'''

TOPIC_PROMPT_CELL = '''# Combine all NOFO pages into a single string so the model sees the full context
NOFO_text = "\\n".join(doc.page_content for doc in NOFO_pdf)

topic_extraction_Prompt = f"""
You are an expert NIH grants analyst. You are given the full text of an NIH
Notice of Funding Opportunity (NOFO) below, delimited by <NOFO> tags.

Your task:
- Carefully read the NOFO.
- Identify the single, specific research topic / scientific area for which this
  funding opportunity is offering grants.
- Ground your answer in the "Funding Opportunity Title", "Funding Opportunity
  Purpose" and "Goal(s)" sections.

Output rules (very important):
- Respond with ONLY the topic name as a short noun phrase (max ~12 words).
- Do NOT add any explanation, preamble, label, quotes, or extra text.

<NOFO>
{NOFO_text}
</NOFO>
"""
'''

PAPERS_UNZIP_CELL = '''# Unzipping the Research Papers - Replace your zip file path and extract it in the contents folder only
import zipfile
with zipfile.ZipFile("/content/Papers.zip", 'r') as zip_ref:
  zip_ref.extractall("/content/") # No changes needed here
'''

SUMMARY_PROMPT_CELL = '''summary_prompt = f"""
You are a research analyst supporting an NIH grant application on the topic:
"{topic}".

Immediately after this instruction the full text of ONE research paper from the
advisor's portfolio will be appended.

Your task:
1. Write a concise, structured summary of that paper using these labelled fields:
   - Title: (as best inferred from the text)
   - Core Problem / Objective:
   - Methods & Data:
   - Key Findings:
   - Transferable Assets: methods, models, datasets or populations that could be
     repurposed toward the funding topic above.
2. Then add a final field:
   - Relevance to "{topic}": 2-3 sentences judging how this work could be aligned
     with the funding topic, ending with a relevance rating of High / Medium / Low.

Constraints:
- Keep the whole summary under ~250 words.
- Be specific and factual; do NOT invent results that are not supported by the text.

RESEARCH PAPER TEXT:
"""
'''

GEN_IDEA_PROMPT_CELL = '''# Build a compact context block from the per-paper summaries produced in Step 2
papers_context = "\\n\\n".join(
    f"PAPER: {d['title']}\\n"
    f"FILE PATH: {d['file_path']}\\n"
    f"SUMMARY: {d['llm_response']}"
    for d in documents
)

gen_idea_prompt = f"""
You are a senior research strategist helping Dr. Ian McCulloh craft a competitive
NIH proposal for the funding topic: "{topic}".

Below, delimited by <PAPERS> tags, are summaries of his most relevant prior
research papers. Each entry includes that paper's exact FILE PATH.

Using ONLY these papers as the scientific foundation, generate EXACTLY 5 distinct,
novel and fundable research proposal ideas that align tightly with the funding
topic and NIH digital mental health priorities.

FORMATTING RULES (follow EXACTLY):
- Use a line containing only three dashes ( --- ) as a delimiter.
- Place a --- line BEFORE the first idea, and a --- line between every idea.
- For EACH idea use this exact structure (keep the bold field labels):

**Idea X:** [Concise title of the project idea]
**Description:** [3-5 sentences covering objectives, innovative elements, scientific rationale, and anticipated impact]
**Citation:** [Author(s), Year or the title of the paper that inspired this idea]
**NOFO Alignment:** [Two or more specific NOFO requirements this idea directly addresses]
**File Path of the Research Paper:** [The exact FILE PATH of the source paper, copied verbatim, ending in .pdf]

IMPORTANT:
- The "File Path of the Research Paper" MUST be copied verbatim from the matching
  paper's FILE PATH below and MUST end in .pdf.
- Output nothing before the first --- and nothing after the last idea.

<PAPERS>
{papers_context}
</PAPERS>
"""
'''

TEMPLATE_LOADER_CELL = '''# Here we need to add the full papers instead of the summary
chosen_idea_rp = PyPDFLoader(idea_generated_from_research_paper, mode="single").load()

# Loading the sample research proposal template
research_proposal_template = PyPDFLoader("/content/Research_Proposal_Template.pdf", mode="single").load()
'''

PROPOSAL_PROMPT_CELL = '''# Full text of the source research paper and the sample proposal template
source_paper_text = chosen_idea_rp[0].page_content
template_text = research_proposal_template[0].page_content

research_proposal_template_prompt = f"""
You are an expert NIH grant writer. Write a complete, well-structured research
proposal for the NIH funding topic: "{topic}".

Base the proposal on the SELECTED IDEA below, ground its science in the SOURCE
RESEARCH PAPER, and follow the section structure and academic tone of the SAMPLE
PROPOSAL TEMPLATE.

SELECTED IDEA:
{chosen_idea}

REQUIREMENTS:
1. Follow the structure of the sample template, adapting headings as appropriate:
   Title, Introduction / Background, Problem Statement, Specific Aims / Objectives,
   Research Methodology & Approach, Expected Outcomes & Impact, and a Timeline.
2. Explicitly align the proposal with the NOFO: address the reach, efficiency,
   effectiveness and quality of digital mental health interventions, and emphasize
   health-disparity / vulnerable populations where relevant.
3. Build on and cite the SOURCE RESEARCH PAPER in the text, and include a
   References section. Do NOT fabricate citations beyond the provided paper and
   well-established public knowledge.
4. Write in clear, persuasive, scientifically rigorous prose using Markdown
   headings. Target roughly 800-1200 words.

SOURCE RESEARCH PAPER (full text):
{source_paper_text}

SAMPLE PROPOSAL TEMPLATE (use for structure and tone only):
{template_text}
"""
'''

EVAL_PROMPT_CELL = """evaluation_prompt = f'''
You are acting as an NIH study-section reviewer (LLM-as-Judge). Evaluate the
research proposal below against standard NIH review criteria for the funding
topic "{topic}".

Score the proposal on EACH of these four criteria from 1 (Poor) to 5 (Excellent):
1. Innovation
2. Significance
3. Approach
4. Investigator Expertise

For each criterion provide: a justification, the integer score, at least one
strength, at least one weakness, and at least one recommendation.

Return ONLY a JSON object wrapped in a ```json code block, and nothing else
(no text before or after the code block, and no trailing newline after the
closing fence). Use EXACTLY this schema, where each of the four criteria is a
top-level key:

```json
{{
  "Innovation": {{
    "justification": "<justification>",
    "score": <1-5>,
    "strengths": "<strength>",
    "weaknesses": "<weakness>",
    "recommendations": "<recommendation>"
  }},
  "Significance": {{ "justification": "...", "score": 0, "strengths": "...", "weaknesses": "...", "recommendations": "..." }},
  "Approach": {{ "justification": "...", "score": 0, "strengths": "...", "weaknesses": "...", "recommendations": "..." }},
  "Investigator Expertise": {{ "justification": "...", "score": 0, "strengths": "...", "weaknesses": "...", "recommendations": "..." }}
}}
```

RESEARCH PROPOSAL TO EVALUATE:
{research_plan.content}
'''
"""

STEP7_MARKDOWN = """## **Step 7: Summary and Recommendation - [3 Marks]**

### Project Summary

This project built an end-to-end **generative-AI assistant for NIH research
proposal automation**, addressing Dr. Ian McCulloh's problem: a large, diverse
research portfolio that is not obviously aligned to a new NIMH Notice of Funding
Opportunity (NOFO) on **digital mental health interventions** (PAR-25-136,
*Laboratories to Optimize Digital Health*). The pipeline chains several LLM and
retrieval steps:

1. **LLM Setup** - Loaded the API key and base URL from `config.json` and
   configured `gpt-4o-mini` (temperature 0) via LangChain's `ChatOpenAI`.
2. **Topic Extraction** - Prompted the LLM over the full NOFO text to distil the
   single funding topic ("digital mental health interventions").
3. **Research Paper Relevance Assessment** - Chunked all candidate papers, embedded
   them with `all-MiniLM-L6-v2`, indexed them in a FAISS vector store, and ran a
   semantic similarity search to surface the papers most relevant to the topic.
   Each relevant paper was then summarised with a structured, topic-aware prompt.
4. **Proposal Ideation** - Fed the filtered summaries to the LLM to generate five
   structured, novel proposal ideas, each with a title, description, citation,
   explicit NOFO alignment, and the source paper's file path. One idea was selected
   and its source paper file path extracted via regex for downstream grounding.
5. **Proposal Blueprint** - Combined the chosen idea, the full source paper, and the
   sample proposal template to draft a complete, NOFO-aligned research proposal,
   optionally exported to PDF.
6. **Proposal Evaluation (LLM-as-Judge)** - Scored the draft 1-5 on Innovation,
   Significance, Approach, and Investigator Expertise, returning structured JSON with
   justifications, strengths, weaknesses, and recommendations.
7. **Human Review** - Left a checkpoint for the advisor to refine the draft.

**Key observations & learnings**

- **Prompt design dominates output quality.** Tight output contracts (delimiters,
  exact field labels, "respond with only...") were essential for the downstream
  parsing (idea splitting on `---`, regex file-path extraction, JSON evaluation).
- **Retrieval grounding reduces hallucination.** FAISS semantic filtering ensured
  ideas were anchored to the advisor's *actual* work rather than generic content,
  and carrying the source file path end-to-end kept citations traceable.
- **Context-window management matters.** Truncating papers to a safe token budget
  before summarisation avoided context-length errors while preserving the salient
  content.
- **LLM-as-Judge is a fast, structured feedback loop** that mirrors NIH review
  criteria, though it should complement - not replace - human review.

### Recommendations & Future Enhancements

- **Robust output parsing.** Replace fixed-index JSON slicing (`content[7:-3]`) and
  brittle splits with a regex / JSON-block extractor (or LangChain structured
  output / Pydantic parsers) so the pipeline tolerates formatting drift.
- **Richer relevance scoring.** Combine vector similarity with an LLM relevance
  classifier and a score threshold, and add re-ranking, rather than relying on a
  fixed top-k chunk count.
- **Whole-paper retrieval for drafting.** Use map-reduce / multi-document
  summarisation so the proposal can draw on several papers, not just one.
- **Iterative refine loop.** Feed the LLM-as-Judge feedback back into a revision
  step to automatically strengthen weak criteria before human review.
- **Stronger evaluation.** Use multiple judge prompts or models and average scores
  to reduce single-model bias, and validate against real reviewer rubrics.
- **Productization.** Add citation/reference verification, a human-in-the-loop UI,
  logging/caching of LLM calls, and config-driven paths so the tool generalises to
  other NOFOs and portfolios.
"""

# ---------------------------------------------------------------------------
# index -> (expected_cell_type, new_source_string)
# ---------------------------------------------------------------------------
REPLACEMENTS = {
    13: ("code", CONFIG_CELL),
    14: ("code", LLM_CELL),
    16: ("code", NOFO_LOADER_CELL),
    18: ("code", TOPIC_PROMPT_CELL),
    21: ("code", PAPERS_UNZIP_CELL),
    41: ("code", SUMMARY_PROMPT_CELL),
    42: ("code", CONFIG_CELL),
    43: ("code", LLM_CELL),
    49: ("code", GEN_IDEA_PROMPT_CELL),
    58: ("code", TEMPLATE_LOADER_CELL),
    59: ("code", PROPOSAL_PROMPT_CELL),
    65: ("code", EVAL_PROMPT_CELL),
    73: ("markdown", STEP7_MARKDOWN),
}


def to_source_lines(text: str):
    """Convert a string into notebook 'source' list (lines keep trailing \\n)."""
    lines = text.splitlines(keepends=True)
    return lines if lines else [""]


def main():
    nb = json.loads(NB_PATH.read_text())
    cells = nb["cells"]
    for idx, (ctype, src) in REPLACEMENTS.items():
        cell = cells[idx]
        assert cell["cell_type"] == ctype, (
            f"Cell {idx} expected {ctype} but is {cell['cell_type']}"
        )
        cell["source"] = to_source_lines(src)
        if ctype == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False))
    print(f"Updated {len(REPLACEMENTS)} cells in {NB_PATH}")


if __name__ == "__main__":
    main()

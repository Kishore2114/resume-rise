# ResumeRise

A standalone web app implementing the system in *"ResumeRise: A Truthfulness-Constrained LLM Coach for Resume–Job Matching and Interview Practice"*.

No install, no build, no dependencies, no Cursor needed.

## Run

Double-click `index.html` (or `start.bat`). Any modern browser works.

## Connect an LLM

Click **⚙ LLM settings** and pick a provider (OpenAI, Groq, OpenRouter, Ollama, or any OpenAI-compatible URL), a model, and your API key.

- Keyword baseline works fully offline, with no key.
- Fully local/private option: install [Ollama](https://ollama.com), `ollama pull llama3.1`, then start it with `OLLAMA_ORIGINS=*` (PowerShell: `$env:OLLAMA_ORIGINS="*"; ollama serve`) and choose the *Ollama* preset.
- API keys are kept in `sessionStorage` (cleared when the tab closes) unless you tick "Remember". Resumes are never stored.

## Features (matching the paper)

- **Module 1 – Resume Match**: top-20 keyword coverage baseline + LLM score (skills 40 / experience 30 / education 15 / communication 15), strengths, must-have vs nice-to-have gaps with honest actions, 3 rewrites, clarity flags. Both scores shown side by side, with a warning when they disagree strongly.
- **Anti-fabrication check**: each rewrite's quoted original must exist verbatim in the resume; new numbers in suggestions are flagged.
- **Module 2 – Mock Interview**: 5 questions (2 behavioural, 2 technical, 1 project), 1–5 scoring on relevance/structure/specificity/communication, strengths/improvements, outline using only your own facts, session average.
- **Prompt safety**: inputs treated as data (injection resistant), no length reward, no identity inference, strict JSON, all output rendered as plain text (no markup injection).
- Light/dark themes, contact-detail redaction helper, sample data.

## For the evaluation study

Set temperature in settings (default 0.2) and rerun the same pair 3–5 times for stability (E2). The app is a tool; results tables in the paper must come from your own measurements.

Source code: https://github.com/Kishore2114/resume-rise

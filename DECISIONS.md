# CivicProof decisions

Decisions describe the current plan and may be revised with evidence. Date: 2026-10-21.

## D001: Foundation before models

Build contracts, ingestion, evidence, reviewed labels, and scoring before adding an LLM. Fluent output without traceable evidence would hide upstream failures. No model server or paid API is required in Phase 1.

## D002: A small ordinary package first

Use `civicproof/` in the repository root and run it with `python -m civicproof` after confirming Python 3.12. This keeps the first lesson understandable without installation machinery. A `src/` layout can provide stronger separation between checkout imports and installed packages, but is optional until packaging needs justify it. Do not change layouts merely to look professional.

## D003: Standard library only for Lesson 1

The starter only prints a message. Introduce a virtual environment and dependency metadata before installing Pydantic, a PDF library, or other third-party tools. Python 3.12 is the declared interpreter, even though other versions are installed. Local verification found a stale Store path selected by `py -3.12`; use the working `python` command, check its version, and record an explicit executable fallback without changing global settings.

## D004: Explicit evidence and uncertainty

Retain raw evidence separately from normalized candidates. Validate each supported extracted field's source. Missing or uncertain data does not become an invented value, and schema validity does not mean factual verification.

## D005: Begin with inspectable local records

Plan JSON records and JSONL annotations initially. Decide whether SQLite is useful after learning persistence and cross-record references. Avoid adding an ORM, backend framework, or database server without a concrete need.

## D006: Review annotations and protect the test split

Begin with about 5-10 official public documents and a few clearly defined fields. Humans review labels against source pages. LLM output cannot automatically become ground truth. Group document versions and duplicates to reduce leakage. Public accessibility does not automatically grant redistribution rights.

## D007: Truthful verification and learner pacing

Record actual commands and results. Keep unimplemented work and unverified claims explicit. Do not advance lessons without the learner's readiness confirmation. Do not equate code generation with learner mastery. Provide Git commit messages at checkpoints; the first commit remains a learner activity.

## D008: Explicit local interpreter before third-party packages

Lesson 2 creates `.venv` using the verified Python 3.12.10 installation. Prefer `.\.venv\Scripts\python.exe -m ...` for reproducible terminal instructions on this laptop; PowerShell activation remains optional. This avoids the stale Windows launcher registration and ambiguity about which Python receives pip installations. Do not change global execution policy to make activation work.

Track `requirements.txt` as the dependency list; it initially contains only comments because the starter needs no third-party packages. Install actual packages only when a lesson needs them. Do not copy bundled PDF-authoring dependencies into the application environment. Revisit pins and transitive dependencies when package installation is introduced. Package isolation does not sandbox untrusted input.

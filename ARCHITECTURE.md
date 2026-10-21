# CivicProof architecture

Status: design outline, 2026-10-21. The startup package, a local virtual environment and an initially empty dependency list exist. Application components beyond startup are planned. Revise this outline as the learner implements and understands each component.

## Purpose and flow

```text
Local PDF
    -> validate input, enforce limits, calculate SHA-256, detect duplicates
    -> inspect pages and extract text/coordinates; use local OCR where needed
    -> validate document records and field candidates with data contracts
    -> check provenance against the actual source document and page
    -> persist records locally
    -> compare predictions with reviewed, versioned ground truth
    -> write an evaluation report
```

No LLM, web API, queue, cloud service, or distributed system is required in Phase 1. A command-line interface is sufficient. Local operation can be offline after tools and datasets are obtained.

## Minimal current structure

```text
CivicProof/
    .gitignore
    requirements.txt
    README.md
    ARCHITECTURE.md
    PROGRESS.md
    DECISIONS.md
    LEARNING_NOTES.md
    EVALUATION.md
    civicproof/
        __init__.py
        __main__.py
        cli.py
```

Local-only `.venv/` holds the project's Python environment and is ignored by Git. Its interpreter runs the application; it is not an application module or a security sandbox. The requirements file currently contains comments only. Add actual tested dependencies when needed, not before.

## Planned responsibilities, introduced incrementally

- `config.py`: validated local settings, including resource limits and tool paths.
- `schemas.py`: versioned Project, Document, WorkItem, Claim, Unit, and SourceLocation contracts.
- `ingestion.py`: file validation, hashing, duplicate detection, and explicit failure outcomes.
- `extraction.py`: page extraction and OCR routing with coordinate conventions recorded.
- `provenance.py`: source-reference integrity and evidence checks; evidence highlighting.
- `normalization.py`: conservative value and unit normalization with explicit unsupported outcomes.
- `storage.py`: local persistence; start with readable JSON records/JSONL and evaluate SQLite when relational integrity needs justify it.
- `evaluation.py`: reproducible scoring of frozen predictions and reviewed labels.
- `tests/`: unit and integration tests plus small synthetic fixtures.
- `data/manifest.jsonl`: planned source and permission metadata.
- `data/annotations/`: planned versioned, reviewed labels.
- `data/raw/`, `data/derived/`, `data/outputs/`: local inputs and outputs, ignored by Git.
- `pyproject.toml`: planned dependency and tool configuration once those concepts are introduced.

Do not create placeholder modules merely to match this list. Split modules further only when responsibilities become hard to understand.

## Evidence model principles

An observation records what extraction returned. A normalized candidate interprets that observation under explicit rules. A verified claim has passed a defined review or validation policy. An inference derives a conclusion from stated evidence and rules. An unsupported assertion lacks sufficient evidence. These are different epistemic states: formatting validation must not silently promote a candidate to a verified claim.

Missing, ambiguous, unreadable, and unsupported values must be explicit. The exact schema representation will be designed during the contract lessons. Never invent values to satisfy a required field. Each independently supported extracted field needs its own evidence link; a record-level citation cannot automatically justify every field in that record.

Administrative metadata such as hashes and ingestion timestamps has computational provenance. It must not be assigned a fabricated PDF bounding box. Original text and normalized values remain separate.

Pydantic can validate a record's shape and local rules. A separate integrity check must confirm that referenced documents, pages, and evidence locations actually exist. A well-shaped citation is not automatically a valid citation.

## Planned Phase 1 acceptance criteria

1. A clean Windows/Python 3.12 environment can follow documented installation commands, run the CLI on a fixture, and run the automated suite. Third-party dependencies and OCR setup are recorded reproducibly. Interpreter selection is verified before installation.
2. Digital, scanned, mixed, multipage, rotated, empty, and table-containing fixtures have declared expected behavior. Text and available coordinates are retained by page. Tables without reliable cell interpretation are explicitly limited or unsupported.
3. SHA-256 is calculated from original bytes. Identical content is detected even under a different filename. Ingesting it again does not create an unintended duplicate document.
4. Unsupported formats, corrupt files, password-protected files, configured byte/page limits, and timeouts produce explicit failure outcomes. Limits are documented and tested. A failed operation cannot silently publish partially validated supported fields.
5. Document metadata and structured records are validated, versioned, and stored locally. Originals remain immutable. Rejected or failed processing does not silently become successful extraction.
6. Every supported extracted field has the correct immutable source identity, a valid 1-based page number, a bounding box with a declared coordinate frame inside that page, exact retained supporting text, an extraction method, and a validation state. The field must actually be supported by that evidence. OCR evidence remains distinguishable from digital text and can be checked against the source image.
7. Tests reject missing evidence, wrong document references, out-of-range pages, invalid boxes, and evidence that does not justify the field. Coordinate transformations are tested with rotated/OCR fixtures; a highlight can be inspected on the original page. Unsupported outcomes explicitly state why support is unavailable.
8. Approximately 5-10 suitable official public tender documents have a source manifest recording identifiers, hashes, retrieval dates, versions, source URLs, and access/reuse findings. Public access alone does not establish redistribution rights. Do not redistribute files without an appropriate basis.
9. A versioned JSONL annotation set includes reviewed positive, missing, ambiguous, and OCR-error examples. Begin with project names and contract identifiers; expand after annotation rules are stable. Related versions and duplicate documents remain in the same split. Held-out test labels do not guide extractor tuning.
10. A deterministic baseline produces field candidates and abstains when evidence is insufficient. Evaluation compares saved predictions with a frozen label version and reports counts, precision/recall/F1, exact matches, page attribution, bounding-box alignment, coverage/abstention, and unsupported handling with explicit denominators.
11. Critical paths have meaningful positive and negative automated tests, including ingestion, contracts, units, evidence integrity, OCR failure behavior, and end-to-end evaluation. No claim of test success is made without execution evidence.
12. The final demonstration includes installation instructions, reproducible commands, fixture expectations, an evaluation report with actual results, and limitations. Numeric quality targets are agreed after a baseline is measured; no benchmark results are assumed in advance.

## Security boundaries and limitations

Never execute document text or treat it as application instructions. Use constrained parsing, controlled temporary paths, safe subprocess arguments, configurable resource limits, and minimal document content in logs. A timeout wrapper alone is not an operating-system sandbox. Detailed threat handling and implementation belong in the ingestion lessons.

Local-first processing does not imply encrypted storage or no synchronization. This repository is located under OneDrive; folder synchronization depends on the user's OneDrive settings. Revisit raw-document storage before collecting real documents.

A small evaluation collection cannot establish reliability across all tenders, layouts, languages, or scan conditions. Provenance establishes auditability; it does not establish real-world factual truth.

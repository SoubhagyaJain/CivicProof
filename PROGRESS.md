# CivicProof progress

Updated: 2026-10-21, Asia/Calcutta.

## Current session

- Repository initially contained only an empty `.git` directory on `main`.
- Python 3.12.10 and Git are available. Multiple Python versions are installed. `py -3.12` fails because it selects a stale Microsoft Store executable; `python` resolves to the working Python 3.12.10 installation. Verify `python --version` first; see README.md for the explicit executable fallback.
- Added the six continuity documents, `.gitignore`, and a three-file startup package.
- Current lesson: Day 1, Lesson 2, virtual environments and dependency basics. The learner explicitly requested the next lesson; this authorizes progression without establishing mastery.
- Lesson 1 exercise and knowledge-check answers have not been submitted or reviewed. Lesson 2 understanding is also pending. Do not infer mastery from generated code.
- Created `.venv` with the verified Python 3.12.10 executable and added `requirements.txt` containing comments only. No third-party application package has been requested.
- No PDF pipeline, schema, dataset, OCR integration, persistence layer, or metric implementation exists yet.
- The learner subsequently requested PR commands and an explanation of Git from first principles. On inspection, initial commit `64b694b` exists, the current branch is `codex/project-foundation`, and the project files are staged. The foundation commit and PR are not yet observed. Git explanation is recorded in LEARNING_NOTES.md; no learner mastery is assumed. Updating these two documents leaves their latest edits unstaged until the learner adds them again.
- First PR troubleshooting: verified that only `main` exists on the remote, and the local feature branch still points to initial commit `64b694b`; the foundation commit and feature-branch push have not completed. The learner encountered Git's `(END)` pager and then a GitHub CLI HTTP 401. `gh auth status` confirms the stored keyring token is invalid; no GH_TOKEN or GITHUB_TOKEN override is present in the inspected shell. Guide the learner to restage the two updated documents, review with `git --no-pager diff --cached --stat`, commit, push the feature branch, reauthenticate interactively with `gh auth login --hostname github.com --web`, verify authentication and retry PR creation. No credentials were changed and no commit, push or PR was performed by the mentor.
- Exported a nine-page study companion at `output/pdf/CivicProof_Phase1_Roadmap_and_Day1_Notes.pdf`, covering the overview, roadmap, acceptance checklist and Lesson 1. All nine pages were rendered with Poppler and visually inspected. Content and page-margin checks passed. This is a learning artifact, not implementation of the planned document pipeline; lesson readiness is still pending.

## Adjustable 14-day roadmap

Allow roughly 1.5-2.5 focused hours per day, with extra setup time if OCR or installation needs troubleshooting. Days are learning checkpoints, not deadlines. Each day can contain several small lessons; advance only after the learner confirms readiness.

| Day | Focus | Concrete checkpoint |
| --- | --- | --- |
| 1 | Modules, ordinary packages, imports, working directory; then environments and Git basics | Run the starter, explain its execution path, create an isolated environment, make a reviewed first commit |
| 2 | Paths, bytes versus text, file context managers, type hints, exceptions; introduce pytest | Read a local file safely and explain one passing and one failing test |
| 3 | Dictionaries versus contracts, Pydantic, optional fields, dates, IDs, schema versions | Validate initial Project, Document, and SourceLocation records with negative tests |
| 4 | PDF internals, text versus images, PyMuPDF introduction | Inspect and extract a small digital multipage fixture |
| 5 | Reading order, page coordinates, rotations, spans, tables and limitations | Save page text and boxes, inspect a source highlight |
| 6 | Local Tesseract setup, OCR routing and uncertainty, mixed documents | Detect OCR candidates and retain OCR output with page provenance |
| 7 | Secure input handling, byte/page limits, SHA-256, duplicate policy | Reject invalid inputs and recognize identical bytes under different names |
| 8 | Timeouts, failures, configuration, structured logging, local persistence | Persist explicit processing outcomes; diagnose an injected failure |
| 9 | Observation/candidate/verified/inference distinctions, claim provenance | Enforce per-field evidence and cross-record integrity |
| 10 | Units, dimensions, conservative normalization, quantity/work-item contracts | Normalize supported units and explicitly reject incompatible/unknown cases |
| 11 | Official tender collection, access/reuse review, versioning and splits | Record a diverse manifest for about 5-10 appropriate documents |
| 12 | Annotation guidelines, JSONL, manual review, ambiguity and OCR cases | Freeze a first reviewed annotation version; protect held-out examples |
| 13 | Metric arithmetic from scratch, simple deterministic baseline, pytest expansion | Produce a reproducible scored report with explicit denominators |
| 14 | Integration, regression and failure tests, installation rehearsal, limitations | Demonstrate the full pipeline and audit every supported field's evidence |

## Verification record

Environment discovery was executed. Initial launcher checks failed before application startup with error 0x80070002. The actual Python 3.12 executable was confirmed working. The following corrected checks were executed successfully on 2026-10-21:

| Command | Actual result |
| --- | --- |
| `python --version` | `Python 3.12.10` |
| `python -m civicproof` | Printed the two expected startup lines; exit code 0 |
| `python -c "import civicproof.cli; import civicproof.__main__; print('Imports completed without starting the app.')"` | Printed only the explicit confirmation message; neither import started the app; exit code 0 |
| `python -m compileall -q civicproof` | No syntax errors reported; exit code 0 |

These are Lesson 1 starter behavior and syntax checks. There is no pytest suite yet. There are no PDF/OCR/evaluation results. The launcher registration problem remains; documented commands use the working interpreter. Learner execution and understanding remain pending.

### Lesson 2 verification

Executed successfully on 2026-10-21:

| Check | Actual result |
| --- | --- |
| Create `.venv` with the verified Python executable | Exit code 0 |
| `.\.venv\Scripts\python.exe --version` | `Python 3.12.10` |
| Inspect `sys.executable` | Project-local `.venv\Scripts\python.exe` |
| Compare `sys.prefix != sys.base_prefix` | `True` |
| Inspect `pyvenv.cfg` | `include-system-site-packages = false` |
| Environment pip list with version checking disabled | Only `pip 25.0.1` installed |
| Install `requirements.txt` with `--no-index` | Exit code 0; comments-only file installs no application package |
| Environment `pip check` | `No broken requirements found.` |
| Run CivicProof with the environment interpreter | Expected two startup lines; exit code 0 |
| `git check-ignore .venv/pyvenv.cfg` | Confirmed ignored |

PowerShell activation and editor interpreter selection were not exercised. Direct interpreter commands do not require activation. There is still no pytest suite, no third-party application package and no PDF/OCR/evaluation result. Learner execution and understanding remain pending.

## Exact next task

The learner follows Lesson 2, identifies the environment interpreter, checks package isolation, runs the startup command and completes the exercise and knowledge questions. Lesson 1 answers and exercise remain available for review. Do not introduce Lesson 3 until the learner confirms readiness. The planned next lesson introduces Git snapshots and reviewing the first commit.

Suggested first checkpoint commit, after the learner reviews the starter:

```text
chore: initialize CivicProof learning foundation
```

No commit has been created by the assistant.

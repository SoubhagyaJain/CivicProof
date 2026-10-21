# CivicProof evaluation foundation

Status: planned, 2026-10-21. No dataset has been collected, no ground-truth labels have been reviewed, and no extraction or evaluation score has been measured.

## Goal

Measure extraction and source attribution separately from any future reasoning system. Evaluate a small deterministic baseline before an LLM is introduced. A high text score cannot compensate for an evidence reference that points to the wrong place.

## Planned collection and annotation

Start with about 5-10 suitable civil-infrastructure tender documents from verified official Indian government sources. Check live download access and published terms during collection. Record source URLs, retrieval dates, document versions, content hashes, and license/reuse findings. Do not invent URLs or equate public availability with unrestricted reuse. Avoid unnecessary personal information and sensitive content.

Begin with project names and contract identifiers. Add dates, work-item descriptions, quantities, and units after rules for the first fields are stable. Labels must include document ID/hash, schema and annotation versions, field name, raw evidence, expected value or explicit missing/ambiguous/unreadable state, source page and location, and review status. Define the precise JSONL schema during the annotation lessons.

Ground truth is the reviewed reference answer, not guaranteed absolute truth. Audit it against original pages. Machine suggestions may help locate evidence later, but may never become ground truth automatically. Keep synthetic test fixtures distinguishable from public tender examples.

## Dataset split policy

Training data teaches a model; development data guides implementation and tuning; held-out test data supports the final independent check. Phase 1 has no model training requirement. Reserve held-out documents before tuning extraction rules. Keep duplicates, related versions, and closely related templates grouped where needed to avoid leakage. With a tiny dataset, report raw counts and acknowledge high uncertainty.

## Planned measures

Definitions and arithmetic will be taught and implemented from scratch before libraries are considered.

- Precision: supported correct predictions divided by all predictions counted as positive under the scoring policy.
- Recall: correct recovered targets divided by all expected positive targets.
- F1: harmonic mean of precision and recall, with explicit zero-denominator handling.
- Exact-match accuracy: exact matches divided by eligible evaluated fields, with raw and normalized comparisons reported separately.
- Source-page attribution: correct document/page references divided by a declared eligible prediction count. Include coverage so abstention cannot inflate apparent success.
- Bounding-box alignment: intersection-over-union for boxes in the same declared page coordinate frame, plus evidence inspection and declared thresholds where used.
- Coverage and abstention: answered and abstained fields divided by the same declared eligible field count; separate invalid-output cases rather than hiding them.
- Unsupported handling: count unsupported predictions presented as supported and justified abstentions; missing target handling needs its own score rather than being treated as extraction success.
- Text extraction: completed/failed pages, readable text preservation on reviewed fixtures, OCR errors, and layout limitations. Nonempty text alone is not evidence of correct extraction.
- Unit normalization: exact supported conversion results and correct rejection of unknown or dimensionally incompatible units.

Define matching, duplicates, wrong-value penalties, missing-value treatment, and every denominator before using scores for comparisons. Report per-field results and counts. Do not silently drop errors or difficult examples. Bounding-box overlap alone does not prove that evidence supports the claimed value.

## Reproducibility record planned for every report

Record dataset and annotation versions, original document hashes, configuration, dependency/tool versions, baseline version or Git commit, saved predictions, run command, and scoring policy. OCR outputs may vary with tool versions, so freeze the evaluated outputs and record the environment.

## Required examples and tests

Include positive, missing, ambiguous, unreadable, OCR-error, rotated-page, duplicate, corrupted-file, invalid-schema, invalid-box, wrong-source, unknown-unit, and missing-evidence examples. Critical functionality needs positive and negative tests. Use small synthetic fixtures for controlled edge cases and reviewed public examples for realism.

## Results

Not measured. The Day 1 starter has no extraction, provenance validation, OCR, or evaluation implementation. The strict evidence gate and full acceptance checklist are in ARCHITECTURE.md.

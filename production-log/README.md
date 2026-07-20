# Production Log

This directory contains only the current English production-log material and its reproducible build tool.

## Current files

- `complete-production-log-en.md`: canonical English candidate-review source
- `complete-production-log-en.docx`: generated English Word copy
- `weekly-work-log-en.md`: continuing English weekly record
- `build_documents.py`: bilingual parity check and Word export builder

The matching Chinese files live once, under `../zh-cn/`:

- `../zh-cn/complete-production-log-zh-cn.md`
- `../zh-cn/complete-production-log-zh-cn.docx`
- `../zh-cn/weekly-work-log-zh-cn.md`

Superseded fragments and duplicate exports are excluded from the current tree. Their development remains traceable in Git history.

## Build and verify

```bash
python3 production-log/build_documents.py
python3 code/verify_project_bundle.py
```

The builder verifies that the English and Chinese sources have matching ordered pair IDs, field-row IDs, table shapes, block structure, and placeholders. It then creates both Word files and checks them by round-trip text extraction.

## Remaining administrative work

1. Obtain the candidate's correct current production-log form from the centre.
2. Review every first-person statement and complete all genuine-information placeholders.
3. Transfer only reviewed material to the official form.
4. Complete declarations, dates, signatures, presentation evidence, and supervisor-only sections with the correct people.

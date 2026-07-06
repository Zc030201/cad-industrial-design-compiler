# Privacy And Sanitization

This repository is designed to stay public-safe.

## Do Not Commit

- Private drawings, models, reports, screenshots, business files, or customer data.
- Local absolute paths.
- Production component catalogs.
- Internal project names.
- Binary CAD files or office files.

## Recommended Public Data

- Synthetic component metadata.
- Small hand-written examples.
- Publicly shareable validation reports.
- Docs that describe workflow behavior without private project context.

## Suggested Scan

Run before publishing:

```powershell
python scripts/privacy_scan.py .
```

The scan is intentionally conservative. If it flags a term, either remove it or
document why it is safe.

## Neutral Naming

Prefer neutral words:

- `synthetic`
- `demo`
- `industrial panel`
- `frame`
- `cover`
- `bracket`
- `fixture`
- `component catalog`

Avoid private product, customer, and project labels.

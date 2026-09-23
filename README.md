# Virelox copy preview

This repository contains the published static preview. The editable Next.js source is not included. `scripts/update_copy_preview.py` applies the reviewed copy to the existing exported layout and creates standalone pages so older Next.js build artifacts do not replace the preview text after loading.

To rebuild from the original export in commit `3748312`:

```sh
python3 -m pip install -r scripts/requirements.txt
python3 scripts/update_copy_preview.py
```

The homepage and About page preserve the published page order. `copy-enhancements.css` adds the small stat icons, the founder visual, and the featured channel cards.

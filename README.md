# Virelox copy preview

This repository contains the published static preview. The editable Next.js source is not included. `scripts/update_copy_preview.py` applies the reviewed copy to the existing exported layout and creates standalone pages so older Next.js build artifacts do not replace the preview text after loading.

To rebuild from the original export in commit `3748312`:

```sh
python3 -m pip install -r scripts/requirements.txt
python3 scripts/update_copy_preview.py
```

The homepage and About page preserve the published page order. `copy-enhancements.css` adds the small stat icons, the founder visual, and the featured channel cards.

## Cloudflare production build

The `codex/cloudflare-deploy` branch turns this reviewed preview into a root-hosted Cloudflare Workers site. The original preview files stay in place. `npm run build` writes a clean `dist/` with root-relative assets, production indexing, and a working `/api/contact` form endpoint. `npm run dev` runs it locally; `npm run deploy` publishes it after Wrangler authentication.

The Cloudflare Worker uses static assets for the pages and an Email Service send binding for contact submissions. Static pages are served as assets; only `/api/contact` runs Worker code. The binding is restricted to sending from `website@vireloxmedia.com` to `caleb@vireloxmedia.com`.

Before publishing, configure Cloudflare Email Service for `vireloxmedia.com` and verify `caleb@vireloxmedia.com` as a destination address. Confirm that this does not replace or disrupt the existing mailbox routing. Then deploy to the free `workers.dev` address, test both pages and a real form submission, and only then attach `vireloxmedia.com` and `www.vireloxmedia.com` to the Worker and remove the old Netlify DNS records. Keep Netlify active until both hostnames and email work on Cloudflare.

The original editable Next.js source is not present in this repository. Future content changes should be made in the preview build script and rebuilt before deploying, or the production source should be linked if it becomes available.

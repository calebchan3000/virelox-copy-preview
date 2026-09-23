import { copyFileSync, cpSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const root = new URL("../", import.meta.url).pathname;
const dist = join(root, "dist");
rmSync(dist, { recursive: true, force: true });
mkdirSync(dist, { recursive: true });

for (const dir of ["_next/static/css", "_next/static/media", "channels", "format-icons", "partners", "stat-icons", "team", "trusted", "about"]) {
  if (dir === "about") continue;
  cpSync(join(root, dir), join(dist, dir), { recursive: true });
}
for (const file of ["favicon.png", "virelox_lockup.png", "virelox_full.png", "copy-enhancements.css", "sitemap.xml"]) {
  copyFileSync(join(root, file), join(dist, file));
}
for (const css of readdirSync(join(dist, "_next/static/css"))) {
  const path = join(dist, "_next/static/css", css);
  writeFileSync(path, readFileSync(path, "utf8").replaceAll("/virelox-copy-preview/", "/"));
}

function page(source, target) {
  let html = readFileSync(join(root, source), "utf8");
  html = html.replaceAll("/virelox-copy-preview/", "/").replaceAll('href="/virelox-copy-preview"', 'href="/"');
  html = html.replace(/<meta\b[^>]*\bname="(?:robots|googlebot)"[^>]*\/>/gi, "");
  html = html.replace(/<link\b[^>]*\brel="apple-touch-icon"[^>]*\/>/gi, '<link rel="apple-touch-icon" href="/favicon.png"/>');
  html = html.replaceAll("data-netlify=\"true\" ", "").replaceAll("netlify-honeypot=\"bot-field\"", "");
  html = html.replace(/<input name="form-name"[^>]*\/>/i, "");
  html = html.replace('class="contact-form"', 'class="contact-form" action="/api/contact"');
  if (source === "index.html") {
    html = html.replaceAll("Virelox Media grows personal brands on YouTube, done for you: about an hour a week on camera, we handle the rest. Educational long-form in your voice, grown through organic reach — from the team behind Casgains Academy and a 15M+ subscriber owned network.", "Virelox Media builds educational YouTube channels for founders, experts, and companies. You record; our team researches, produces, and manages the channel.");
  } else {
    html = html.replaceAll('content="https://vireloxmedia.com" property="og:url"', 'content="https://vireloxmedia.com/about/" property="og:url"');
  }
  mkdirSync(join(dist, target, ".."), { recursive: true });
  writeFileSync(join(dist, target), html);
}

page("index.html", "index.html");
page("about/index.html", "about/index.html");
writeFileSync(join(dist, "about.html"), '<!doctype html><html lang="en"><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/about/"><link rel="canonical" href="https://vireloxmedia.com/about/"><a href="/about/">View the About page</a></html>');
writeFileSync(join(dist, "robots.txt"), "User-agent: *\nAllow: /\nSitemap: https://vireloxmedia.com/sitemap.xml\n");
writeFileSync(join(dist, "404.html"), '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | Virelox Media</title><body style="font:18px/1.6 system-ui;background:#111;color:white;max-width:38rem;margin:12vh auto;padding:2rem"><h1>Page not found</h1><p>The page you’re looking for isn’t here.</p><a style="color:#bba7f3" href="/">Return home</a></body></html>');

let js = readFileSync(join(root, "copy-preview.js"), "utf8");
js = js.slice(0, js.indexOf("  // GitHub Pages does not process")) + `  const form = document.querySelector(".contact-form");
  form?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = form.querySelector('button[type="submit"]');
    let status = form.nextElementSibling;
    if (!status?.classList.contains("form-status")) {
      status = document.createElement("p");
      status.className = "form-status";
      status.setAttribute("role", "status");
      form.insertAdjacentElement("afterend", status);
    }
    button.disabled = true;
    status.textContent = "Sending your message…";
    try {
      const response = await fetch(form.action, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(form),
      });
      const data = await response.json();
      status.textContent = data.message || "Please try again or email caleb@vireloxmedia.com.";
      if (response.ok) form.reset();
    } catch {
      status.textContent = "We couldn't send your message. Please email caleb@vireloxmedia.com directly.";
    } finally {
      button.disabled = false;
    }
  });
});
`;
writeFileSync(join(dist, "copy-preview.js"), js);
console.log("Built Cloudflare site in dist/");

const RECIPIENT = "caleb@vireloxmedia.com";
const SENDER = "website@vireloxmedia.com";

function response(body, status = 200, json = false) {
  return new Response(json ? JSON.stringify(body) : body, {
    status,
    headers: {
      "content-type": json ? "application/json; charset=utf-8" : "text/html; charset=utf-8",
      "cache-control": "no-store",
      "x-content-type-options": "nosniff",
    },
  });
}

function field(value, max) {
  return typeof value === "string" ? value.trim().slice(0, max) : "";
}

function result(request, message, status = 200) {
  if (request.headers.get("accept")?.includes("application/json")) {
    return response({ ok: status === 200, message }, status, true);
  }
  const safeMessage = message.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
  return response(`<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Contact Virelox Media</title><body style="font:18px/1.6 system-ui;background:#111;color:white;max-width:38rem;margin:12vh auto;padding:2rem"><h1>${status === 200 ? "Thank you" : "Could not send your message"}</h1><p>${safeMessage}</p><p><a style="color:#bba7f3" href="/#contact">Return to Virelox Media</a></p></body></html>`, status);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== "/api/contact") return env.ASSETS.fetch(request);
    if (request.method !== "POST") return response({ ok: false, message: "Method not allowed" }, 405, true);

    const contentLength = Number(request.headers.get("content-length") || 0);
    if (contentLength > 12000) return result(request, "Please shorten your message and try again.", 413);

    let data;
    const contentType = request.headers.get("content-type") || "";
    try {
      if (contentType.includes("application/json")) {
        data = await request.json();
      } else if (contentType.includes("application/x-www-form-urlencoded") || contentType.includes("multipart/form-data")) {
        data = Object.fromEntries(await request.formData());
      } else {
        return result(request, "Please use the contact form on the site.", 415);
      }
    } catch {
      return result(request, "Please check the form and try again.", 400);
    }

    // The hidden field catches simple automated submissions without emailing anyone.
    if (field(data["bot-field"], 200)) return result(request, "Thank you. Your message was received.");

    const name = field(data.name, 120);
    const email = field(data.email, 254);
    const company = field(data.company, 160);
    const message = field(data.message, 4000);
    if (!name || !message || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return result(request, "Please enter your name, a valid email, and a message.", 400);
    }

    if (!env.EMAIL) return result(request, `Please email ${RECIPIENT} directly.`, 503);

    try {
      await env.EMAIL.send({
        to: RECIPIENT,
        from: SENDER,
        replyTo: email,
        subject: `Virelox discovery call request from ${name.replace(/[\r\n]/g, " ")}`,
        text: `Name: ${name}\nEmail: ${email}\nCompany: ${company || "Not provided"}\n\nMessage:\n${message}`,
      });
    } catch (error) {
      console.error("Contact email failed", error);
      return result(request, `Please email ${RECIPIENT} directly.`, 503);
    }
    return result(request, "Your message was sent. We’ll be in touch soon.");
  },
};

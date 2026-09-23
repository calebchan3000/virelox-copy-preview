document.addEventListener("DOMContentLoaded", () => {
  const nav = document.querySelector(".navbar");
  const menu = document.querySelector(".nav-mobile-toggle");

  const updateNav = () => nav?.classList.toggle("scrolled", window.scrollY > 16);
  updateNav();
  window.addEventListener("scroll", updateNav, { passive: true });

  menu?.addEventListener("click", () => {
    const open = nav.classList.toggle("menu-open");
    menu.setAttribute("aria-expanded", String(open));
  });
  nav?.querySelectorAll(".nav-links a").forEach((link) => {
    link.addEventListener("click", () => {
      nav.classList.remove("menu-open");
      menu?.setAttribute("aria-expanded", "false");
    });
  });

  // GitHub Pages does not process the production form endpoint.
  const form = document.querySelector(".contact-form");
  form?.addEventListener("submit", (event) => {
    event.preventDefault();
    let status = form.nextElementSibling;
    if (!status?.classList.contains("preview-form-status")) {
      status = document.createElement("p");
      status.className = "preview-form-status";
      status.setAttribute("role", "status");
      form.insertAdjacentElement("afterend", status);
    }
    status.innerHTML = 'This is a copy preview. To contact us, email <a href="mailto:caleb@vireloxmedia.com">caleb@vireloxmedia.com</a>.';
  });
});

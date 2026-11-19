import { emailDraft, whatsappLink } from "./contact.mjs";
const config = window.KEVORO_CONFIG;
const menu = document.querySelector("#menu-toggle");
const nav = document.querySelector("#site-nav");
function closeMenu() {
  menu.setAttribute("aria-expanded", "false");
}
menu.addEventListener("click", () =>
  menu.setAttribute(
    "aria-expanded",
    String(menu.getAttribute("aria-expanded") !== "true"),
  ),
);
nav.addEventListener("click", (event) => {
  if (event.target.closest("a")) closeMenu();
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && menu.getAttribute("aria-expanded") === "true") {
    closeMenu();
    menu.focus();
  }
});
const tabs = [...document.querySelectorAll('[role="tab"]')];
function selectTab(tab) {
  tabs.forEach((item) => {
    const selected = item === tab;
    item.setAttribute("aria-selected", String(selected));
    item.tabIndex = selected ? 0 : -1;
    document.getElementById(item.getAttribute("aria-controls")).hidden =
      !selected;
  });
}
tabs.forEach((tab, index) => {
  tab.addEventListener("click", () => selectTab(tab));
  tab.addEventListener("keydown", (event) => {
    let next;
    if (event.key === "ArrowRight") next = (index + 1) % tabs.length;
    if (event.key === "ArrowLeft")
      next = (index + tabs.length - 1) % tabs.length;
    if (event.key === "Home") next = 0;
    if (event.key === "End") next = tabs.length - 1;
    if (next !== undefined) {
      event.preventDefault();
      selectTab(tabs[next]);
      tabs[next].focus();
    }
  });
});
document.querySelectorAll("[data-demo]").forEach((link) =>
  link.addEventListener("click", () => {
    document.querySelector("#producto").value = link.dataset.demo;
  }),
);
const dialog = document.querySelector("#whatsapp-dialog");
document.querySelectorAll("[data-whatsapp]").forEach((button) =>
  button.addEventListener("click", () => {
    const url = whatsappLink(config.whatsappNumber, button.dataset.whatsapp);
    if (url) window.location.assign(url);
    else dialog.showModal();
  }),
);
document
  .querySelector("#close-dialog")
  .addEventListener("click", () => dialog.close());
const form = document.querySelector("#contact-form");
const ready = document.querySelector("#draft-ready");
form.addEventListener("submit", (event) => {
  event.preventDefault();
  if (!form.reportValidity()) return;
  document.querySelector("#email-draft").href = emailDraft(
    Object.fromEntries(new FormData(form)),
    config.email,
  );
  ready.hidden = false;
  ready.focus();
});
form.addEventListener("input", () => {
  ready.hidden = true;
});

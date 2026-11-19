import test from "node:test";
import assert from "node:assert/strict";
import { emailDraft, whatsappLink } from "../assets/contact.mjs";

test("email draft preserves Spanish and reserved characters without injecting headers", () => {
  const url = new URL(
    emailDraft({
      producto: "Gestión",
      nombre: "Demo & prueba",
      mensaje: "Agenda? Sí.\nSin datos privados.",
    }),
  );
  assert.equal(url.pathname, "kevoro.company@gmail.com");
  assert.equal(url.searchParams.get("subject"), "Solicitud de demo · Gestión");
  assert.match(url.searchParams.get("body"), /Demo & prueba/);
  assert.match(
    url.searchParams.get("body"),
    /Agenda\? Sí\.\nSin datos privados\./,
  );
  assert.deepEqual([...url.searchParams.keys()], ["subject", "body"]);
});

test("WhatsApp stays unavailable without a valid international number", () => {
  for (const invalid of [
    "",
    "pendiente",
    "123",
    "+57 123",
    "https://example.com",
    "0".repeat(11),
  ]) {
    assert.equal(whatsappLink(invalid, "Basilia Connect"), null);
  }
  const url = new URL(whatsappLink("12025550123", "Basilia Connect"));
  assert.equal(url.hostname, "wa.me");
  assert.equal(url.pathname, "/12025550123"); // Reserved fictional North American number.
  assert.match(url.searchParams.get("text"), /Basilia Connect/);
});

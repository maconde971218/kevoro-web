export function emailDraft(
  { producto, nombre, mensaje },
  email = "kevoro.company@gmail.com",
) {
  const subject = `Solicitud de demo · ${producto}`;
  const body = `Hola, Kevoro.\n\nMe interesa: ${producto}.\n${nombre ? `Mi nombre: ${nombre}.\n` : ""}\n${mensaje}\n\nGracias.`;
  return `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}
export function whatsappLink(number, product) {
  if (!/^[1-9]\d{9,14}$/.test(number ?? "")) return null;
  return `https://wa.me/${number}?text=${encodeURIComponent(`Hola, Kevoro. Me gustaría conocer más sobre ${product}.`)}`;
}

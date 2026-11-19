/* Marca: preferencia temporal de esta página. No almacenamiento ni comunicaciones. */
const choices = document.querySelectorAll('[data-choice]');
const notice = document.querySelector('#selection-note');
for (const choice of choices) {
  choice.addEventListener('click', () => {
    for (const other of choices) other.setAttribute('aria-pressed', String(other === choice));
    notice.textContent = `Tu preferencia en esta vista: ${choice.dataset.choice}. No se ha guardado, enviado ni aprobado ninguna dirección.`;
  });
}

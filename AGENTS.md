# Reglas de Kevoro para esta web

- Trabaja en ramas; nunca escribas en `main`, fusiones ni publiques. Conserva cambios ajenos.
- Pruebas primero para comportamiento nuevo; verifica con evidencia antes de decir «listo».
- Solo datos ficticios en pruebas. Nunca contraseñas, claves reales ni datos de pacientes.
- No inventes testimonios, clientes, métricas, certificaciones o constitución legal.
- Usa recursos propios o con licencia compatible y conserva fuente/licencia.
- El CEO aprueba resultados, no pasos. Todo contenido social queda como borrador; no uses herramientas de publicación o mensajería.
- Todo PR de Codex pasa también por `kevoro-qa` (Claude) antes del merge. Una revisión de otro agente Codex no la sustituye. Si Claude no está disponible, entrega el PR como borrador con esa revisión pendiente.

## Si eres Codex

Lee `.agents/README.md` y el `SKILL.md` correspondiente antes de aplicarlo. Para diseño usa `frontend-design`, `emil-design-eng` y `frontend-a11y`; para revisar, `impeccable-polish` y `web-design-guidelines`. `ui-ux-pro-max` sirve de referencia local, no reemplaza la marca de `marca/guia.md`. Las skills de marketing preparan propuestas sin publicar.

La web es HTML/CSS/JS estático para GitHub Pages. `npm test` verifica lógica y servidor; el comando Python de `README.md` prueba escritorio y celular con `webapp-testing`. Prueba solo localhost, con contextos nuevos, tráfico externo bloqueado y sandbox del navegador activo. Si el entorno lo impide, usa el CI y documenta el límite; no desactives protecciones para obtener un verde. No incorpores dependencias de runtime sin una necesidad concreta.

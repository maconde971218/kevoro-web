# Kevoro · propuesta de marca, web e Instagram

**Borrador para revisión del CEO.** Rama `feat/marca-y-web`. La web publicada en GitHub Pages seguirá igual hasta una aprobación y un merge realizados por una persona autorizada.

La propuesta usa **Pulso**, verde profundo y lima, como punto de partida. La galería de marca ofrece también Claro (azul) y Cercano (coral). Todos los gráficos son originales; las interfaces son ilustraciones conceptuales sin datos de pacientes.

## Revisar la propuesta

Con Node.js instalado, ejecutar `npm run dev` y abrir `http://localhost:3000`:

- `/`: nueva web y recorrido de contacto.
- `/marca/`: tres direcciones, logos y tres posts.
- `/instagram/`: nueve posts iniciales, seis guiones de Reels y calendario de 30 días.

El servidor de revisión solo sirve archivos públicos de estas carpetas. No sirve `.git`, skills ni configuración privada. Para revisar sin entorno de desarrollo, el CI adjunta capturas y una copia estática descargable al PR. No se desplegó una segunda web pública ni se modificó la fuente de GitHub Pages.

## Contacto

El formulario prepara un borrador para `kevoro.company@gmail.com`: no guarda datos ni envía nada automáticamente. La persona revisa y envía desde su aplicación de correo. Existe también un enlace de correo directo.

Para activar WhatsApp, editar **únicamente `whatsappNumber` en `assets/config.js`** con el número comercial aprobado, incluido el código de país y solo dígitos. Vacío muestra una alternativa por correo. No se ha usado un número real o inventado como contacto.

## Qué se instaló

14 skills de fuentes oficiales de sus autores o repositorios reconocidos, con licencias y versiones documentadas en [.agents/README.md](.agents/README.md). Incluye UI UX Pro Max, Impeccable adaptado y Vercel para el estilo actual solicitado. La página no necesita esas herramientas para funcionar ni carga librerías externas. Manrope se sirve localmente bajo OFL; los gráficos SVG y PNG son propios.

## Pruebas

```sh
npm test
python3 -m pip install -r requirements-test.txt
python3 -m playwright install --with-deps chromium
python3 .agents/skills/webapp-testing/scripts/with_server.py \
  --server "exec node scripts/preview.mjs --port 8765" --port 8765 \
  -- python3 -m unittest discover -s tests -v
```

La suite comprueba móvil de 320 y 390 px, escritorio de 1440 px, menú, pestañas, contacto, WhatsApp sin configurar, teclado, movimiento reducido, errores de consola y bloqueo de red externa. Cada prueba de navegador usa un contexto nuevo y `chromium_sandbox=True`; un fallo de arranque es error, nunca una prueba omitida. El CI guarda capturas, trazas y salida real, incluidos fallos.

La máquina inicial no permite iniciar Chromium/Firefox con sandbox activo. Tampoco abrió la vista previa administrada por fallo del relay. La evidencia válida de navegador debe venir del CI; no afirmar pruebas con lector de pantalla, dispositivo físico o navegadores adicionales que no se hayan ejecutado. La inspección temprana de la galería de marca se hizo sin sandbox de proceso y no sustituye la suite.

## Decisiones del CEO

1. Elegir Pulso, Claro o Cercano y aprobar logo/tono.
2. Confirmar el número comercial de WhatsApp.
3. Aprobar textos y piezas; decidir fecha de inicio de los 30 días. Nada está programado ni publicado en redes.

El PR requiere además revisión de `kevoro-qa` (Claude) antes de merge. La aprobación de esta propuesta no implica nuevas certificaciones, garantías, precios ni compromisos comerciales.

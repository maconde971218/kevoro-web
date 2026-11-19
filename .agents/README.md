# Skills de Kevoro

Son guías y herramientas de trabajo para Codex; no forman parte del código que recibe quien visita la página. Instalación revisada el 18 de noviembre de 2026 (Bogotá). Cada carpeta conserva licencia, atribuciones y procedencia. Se fijaron versiones por commit y se documentaron las adaptaciones a las reglas del CEO.

| Skill | Fuente / licencia | Para qué sirve aquí |
| --- | --- | --- |
| frontend-design | [Anthropic](https://github.com/anthropics/skills), Apache-2.0 | Dirección visual propia, jerarquía y composición |
| webapp-testing | [Anthropic](https://github.com/anthropics/skills), Apache-2.0 | Playwright en localhost, escritorio y celular |
| emil-design-eng | [Emil Kowalski](https://github.com/emilkowalski/skills), MIT | Detalles de interacción y movimiento con propósito |
| frontend-a11y | [Mike Mai](https://github.com/mikemai2awesome/agent-skills), MIT | Teclado, foco, semántica, contraste y formularios |
| ui-ux-pro-max | [Next Level Builder](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), MIT | Catálogo de diseño y buscador Python local |
| web-design-guidelines | [Vercel Labs](https://github.com/vercel-labs/agent-skills), MIT | Revisión consistente de interfaces; referencia fijada localmente |
| impeccable-polish | [Paul Bakaus](https://github.com/pbakaus/impeccable), Apache-2.0 | Método de pulido adaptado, sin runtime, binarios ni hooks |
| product-marketing | [Corey Haines](https://github.com/coreyhaines31/marketingskills), MIT | Definir qué ofrece Kevoro y a quién |
| copywriting | Misma fuente, MIT | Textos claros para la web y piezas |
| copy-editing | Misma fuente, MIT | Quitar exageraciones y revisar el tono |
| content-strategy | Misma fuente, MIT | Temas y objetivos del calendario |
| social | Misma fuente, MIT | Borradores de posts, Stories y guiones de Reels |
| seo-audit | Misma fuente, MIT | Metadatos, estructura y descubrimiento |
| schema | Misma fuente, MIT | Datos estructurados solo cuando hay hechos que los respaldan |

Los paquetes de marketing que incorporan métodos atribuidos a Profound conservan también su aviso MIT. No instalamos herramientas de publicación, anuncios, envío de mensajes ni acceso a cuentas.

## Las populares para «vibe coding»

Se consultó la API de GitHub de los autores: UI UX Pro Max tenía 151.391 estrellas, Impeccable 112.954 y Vercel agent-skills 34.489 en la fecha de revisión. Es una muestra de proyectos muy conocidos, no un ranking mundial ni una promesa de calidad. Su utilidad se evaluó para esta página estática; no se agregó React ni una biblioteca de animación por moda.

Impeccable se instaló como **adaptación documental independiente**: no equivale a instalar el producto completo. El método de pulido aporta valor sin su descarga de binarios en ejecución. Emil cubre las decisiones de movimiento. UI UX Pro Max aporta búsquedas locales; sus ejemplos comerciales nunca se convierten en afirmaciones de Kevoro.

## Revisadas y omitidas

- `brand-guidelines` de Anthropic define la identidad de Anthropic; Kevoro necesita la suya.
- `theme-factory` ofrece temas prefabricados redundantes con las tres rutas originales de `marca/`.
- `canvas-design` está enfocada en pósters PDF/PNG y distribuye muchas fuentes que esta propuesta no requiere. Los maestros originales SVG y sus exportaciones sirven para el kit.
- [openai/skills](https://github.com/openai/skills) no tenía una skill específica de marketing, copywriting, redes o SEO en el catálogo inspeccionado. No se atribuyen las de terceros a OpenAI.
- Se omitieron referencias de marketing sin una licencia de redistribución separada comprobada (Academic Phrasebank y Plain English Campaign), automatización de publicación y servicios externos de vídeo/avatar.

Las cuatro skills pedidas expresamente sí tenían una fuente pública con licencia compatible. Los paquetes siguen la estructura del [estándar Agent Skills](https://agentskills.io/specification): carpeta con `SKILL.md`, metadatos y referencias locales. Este estándar no implica que una skill sea de OpenAI o Anthropic.

## Trazabilidad

[Fuentes de diseño](fuentes-diseno.json) y [fuentes de marketing](fuentes-marketing.json) incluyen repos, commits, hashes, licencias, modificaciones y verificaciones. Las reglas del usuario prevalecen sobre ejemplos o recomendaciones de las skills. Antes de actualizar una fuente, revisar el diff y su licencia; no descargar instrucciones remotas cambiantes durante una revisión.

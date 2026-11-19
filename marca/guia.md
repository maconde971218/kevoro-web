# Kevoro · propuesta de identidad

**Estado: borrador para aprobación del CEO.** La web y los tres ejemplos de post usan Pulso como propuesta recomendada. Esto no constituye una decisión de marca ni una autorización para publicar en redes.

Abre [la galería visual](index.html) para comparar las tres rutas. Los botones de preferencia solo cambian el estado de esa página: no guardan, envían ni aprueban una elección.

## La idea de marca

**Software sencillo para el día a día de tu negocio.** Kevoro crea software desde Bogotá: Basilia Connect para la agenda de clínicas y recordatorios por WhatsApp, aplicaciones de gestión y desarrollo a la medida. El diseño debe transmitir claridad, criterio y cercanía. Primero se entiende qué ofrece; después se aprecia cómo está hecho.

La propuesta toma recursos actuales del diseño de productos digitales — tipografía amplia, espacios generosos, módulos gráficos, contraste y pequeños estados de interacción — y les da una identidad propia. Las formas representan herramientas que encajan. No son capturas de productos reales.

## Tres direcciones para elegir

| Dirección | Personalidad | Logo propuesto | Cuándo elegirla |
| --- | --- | --- | --- |
| **A · Pulso — recomendada** | Enérgica y clara; verde profundo con lima | Una K hecha con tres piezas independientes | Si Kevoro quiere verse actual y reconocible, con una identidad que sirve tanto para clínicas como para otros negocios |
| **B · Claro** | Precisa y digital; azul vivo sobre hielo | Una K dentro de una ventana redondeada | Si se prefiere una imagen más técnica, ordenada y sobria |
| **C · Cercano** | Cálida y editorial; coral, vino y rosa | Una K de curvas suaves | Si la marca debe poner el foco en la conversación y el acompañamiento |

Recomendamos **Pulso** porque distingue a Kevoro con una combinación fácil de reconocer y permite que cada producto tenga su propio espacio. La K funciona como icono pequeño y las mismas piezas generan composiciones para la web y las redes. Claro y Cercano son alternativas reales, no variantes ya aprobadas.

## Paletas y usos

Los valores están también en [paletas.json](paletas.json).

| Ruta | Color | Valor | Uso propuesto |
| --- | --- | --- | --- |
| Pulso | Verde profundo | `#164D43` | Marca, botones y fondos oscuros |
| Pulso | Lima suave | `#D9FA79` | Acento, ilustraciones y énfasis sobre verde |
| Pulso | Blanco | `#FAFCF9` | Fondo principal y texto sobre verde |
| Pulso | Azul cielo | `#DCEAF7` | Fondos secundarios e ilustraciones |
| Pulso | Tinta | `#183B35` | Texto principal |
| Claro | Azul vivo | `#2855F9` | Marca y acento |
| Claro | Tinta azul | `#172447` | Texto principal |
| Claro | Blanco hielo | `#EFF4FF` | Fondo |
| Cercano | Coral | `#F16D57` | Formas y acentos |
| Cercano | Vino | `#442438` | Texto y marca |
| Cercano | Rosa claro | `#FFF2EC` | Fondo |

Combinaciones de texto comprobadas con el cálculo de luminancia relativa WCAG, redondeado a dos decimales:

| Texto sobre fondo | Contraste |
| --- | --- |
| Tinta Pulso sobre blanco | 11,86:1 |
| Verde sobre lima | 8,22:1 |
| Blanco sobre verde | 9,35:1 |
| Tinta Pulso sobre cielo | 10,00:1 |
| Tinta azul sobre hielo | 13,81:1 |
| Azul vivo sobre hielo | 5,07:1 |
| Vino sobre rosa | 12,32:1 |

Estas parejas superan 4,5:1 para texto normal. La tabla comprueba combinaciones de color; no equivale a certificar accesibilidad de una página completa. Evitar texto blanco sobre lima, cielo, rosa o coral. Los estados de una interfaz deben distinguirse también por texto, forma o borde, no solo por color.

## Tipografía

**Manrope variable, pesos 200–800**, es la fuente de Pulso y Claro. Se sirve desde el repo, sin petición a un proveedor externo. En titulares usamos 700–800, en cuerpo 400–500 y en botones 600–700. Conservar cuerpos de lectura cómodos, interlineado amplio y evitar párrafos largos en mayúsculas.

Cercano combina Manrope con **Georgia**, como alternativa de sistema para titulares editoriales. No se incluye ni redistribuye un archivo de Georgia; el navegador usa la fuente instalada o su alternativa serif.

Manrope es de Mikhail Sharanda y Mirko Velimirović, bajo **SIL Open Font License 1.1**. Ver [licencia](../assets/fonts/OFL.txt) y [procedencia exacta](../assets/fonts/README.md). Los logos y posts exportados llevan las letras convertidas en contornos para que se vean igual al abrirlos en otro equipo. Sus fuentes de edición conservan texto vivo.

## Logo y aplicación

- El símbolo Pulso es una K modular original: un pilar y dos diagonales. No representa un socio, integración ni certificación.
- Usar [símbolo](logos/kevoro-pulso-symbol.svg) para favicon y espacios pequeños; [logo completo](logos/kevoro-pulso.svg) cuando haya espacio para el nombre.
- La [versión monocroma](logos/kevoro-pulso-mono.svg) y el [símbolo monocromo](logos/kevoro-pulso-symbol-mono.svg) funcionan en una sola tinta.
- Mantener como margen libre, por cada lado, al menos el ancho del pilar vertical. No deformar, inclinar, añadir sombras o reconstruir la K con otra fuente.
- Como punto de partida, usar símbolo de al menos 24 px y logo completo de al menos 120 px de ancho. Revisar legibilidad en el soporte final.
- Los archivos Claro y Cercano están en la misma carpeta, con nombres `kevoro-claro*` y `kevoro-cercano*`.

## Tono de voz

Hablamos en español, de tú, con claridad y respeto. Nombramos un problema cotidiano, explicamos una posibilidad concreta y cerramos con un siguiente paso. El lenguaje puede ser cercano sin imitar jerga ni exagerar.

| Intención | Ejemplo de tono |
| --- | --- |
| Presentarnos | “Software sencillo, hecho en Bogotá.” |
| Explicar Basilia | “Una agenda para clínicas, con recordatorios por WhatsApp.” |
| Abrir una conversación | “Cuéntanos qué parte del día a día de tu negocio quieres ordenar.” |
| Invitar a una demo | “Te mostramos cómo podría funcionar para tu negocio.” |
| Desarrollo a la medida | “Tu idea merece una herramienta propia. Conversemos.” |

Evitar garantías de resultados, urgencia falsa, cifras sin evidencia y frases como “la mejor plataforma”, “duplicamos tus ventas” o “cero ausencias”. No atribuir testimonios, clientes, certificaciones, constitución legal o integraciones en funcionamiento. No mostrar datos de pacientes, ni siquiera para hacer la interfaz más creíble. Una ilustración de agenda debe identificarse como conceptual.

## Tres posts de ejemplo

Formato vertical **1080 × 1350 px (4:5)**. Son composiciones originales y borradores para revisión, no publicaciones realizadas. Los textos siguientes son propuestas de pie de foto; la planificación completa de Instagram está en la entrega de contenido.

### 1. Presentación — [PNG](posts/post-01.png) · [SVG](posts/post-01.svg)

Diseño tipográfico verde y lima, con la K modular como recurso de fondo.

**Texto de la pieza:** “Menos vueltas. Más negocio. Software sencillo, hecho en Bogotá.”

**Pie de foto propuesto:** El día a día de un negocio ya tiene suficientes tareas. En Kevoro creamos software sencillo para ayudarte a organizarlo: agenda para clínicas, herramientas de gestión y desarrollo a la medida. Cuéntanos qué necesitas ordenar.

**Texto alternativo:** Fondo verde profundo con letras lima: “Menos vueltas. Más negocio.” Debajo, “Software sencillo, hecho en Bogotá”, junto al símbolo modular de Kevoro.

### 2. Basilia Connect — [PNG](posts/post-02.png) · [SVG](posts/post-02.svg)

Composición clara con una agenda esquemática, bloques de mañana y tarde y rótulo visible “Ilustración conceptual”. No es una captura del producto.

**Texto de la pieza:** “Tu agenda, con todo en su lugar. Basilia Connect.”

**Pie de foto propuesto:** Basilia Connect reúne la agenda de citas para clínicas y los recordatorios por WhatsApp. Solicita una demo para conocer la propuesta y conversar sobre las necesidades de tu clínica. Escríbenos a kevoro.company@gmail.com. La agenda de esta pieza es una ilustración conceptual.

**Texto alternativo:** Sobre un fondo claro, el título “Tu agenda, con todo en su lugar”. Una ilustración azul muestra una agenda con bloques genéricos de mañana y tarde. No contiene datos de pacientes.

### 3. Desarrollo a la medida — [PNG](posts/post-03.png) · [SVG](posts/post-03.svg)

Composición azul cielo con tres módulos gráficos propios: idea, interfaz y Kevoro.

**Texto de la pieza:** “Tu idea merece una herramienta propia. Conversemos.”

**Pie de foto propuesto:** Cada negocio tiene una forma de trabajar. Si tienes una idea para organizar un proceso, empecemos por entenderla. En Kevoro desarrollamos herramientas a la medida. Cuéntanos qué necesitas en kevoro.company@gmail.com.

**Texto alternativo:** Fondo azul cielo con tres módulos verde, lima y blanco. El texto dice “Tu idea merece una herramienta propia” e invita a conversar con Kevoro por correo.

Antes de publicar, revisar el texto comercial y el canal de contacto. Se incluyen PNG compatibles de 1080 × 1350, exportados localmente con Inkscape desde los SVG originales. Los SVG siguen siendo los maestros vectoriales; la publicación de cualquier versión requiere aprobación.

## Archivos y procedencia

| Carpeta o archivo | Contenido |
| --- | --- |
| `index.html`, `marca.css`, `marca.js` | Galería local y adaptable de las tres direcciones |
| `logos/` | Ocho SVG autónomos de logos y símbolos; letras en contornos |
| `posts/` | Tres SVG autónomos verticales con letras en contornos y sus tres exportaciones PNG 1080 × 1350 |
| `fuentes/logos/`, `fuentes/posts/` | Las mismas piezas con texto editable; requieren Manrope para reproducir la tipografía exacta |
| `exportar-svg.py` | Herramienta reproducible para convertir las fuentes de edición a contornos |
| `paletas.json` | Valores de color, tipografía y estado de cada propuesta |
| `FUENTES.md` | Inventario de origen y licencias de los recursos |

Para volver a exportar después de editar las fuentes: `python marca/exportar-svg.py --font /ruta/a/Manrope.ttf`. Requiere `fonttools`. También admite el WOFF2 local sin argumento; en ese caso Python necesita `brotli`. El script no se ejecuta en la página y no realiza peticiones de red.

## Decisiones del CEO

1. Elegir **Pulso, Claro o Cercano** como dirección de marca. Nuestra recomendación es Pulso.
2. Aprobar o pedir ajustes al símbolo, los colores y el tono de los ejemplos.
3. Confirmar el número comercial de WhatsApp para activar ese contacto en la web.

La revisión del PR y la aprobación de contenido siguen siendo necesarias antes de publicar. Nada en la galería registra una aprobación.

## Exportar los posts a PNG

Las tres imágenes PNG se generaron con Inkscape CLI desde los SVG maestros, sin navegador ni servicio externo. Por ejemplo: `INKSCAPE_PROFILE_DIR=/tmp/kevoro-inkscape inkscape marca/posts/post-01.svg --export-type=png --export-filename=marca/posts/post-01.png`. Repetir para `02` y `03` cuando cambie el maestro.

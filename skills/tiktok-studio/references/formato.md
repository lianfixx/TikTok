# Formato de una pieza de TikTok

Cómo se arma la ficha de cada video: gancho, texto en pantalla, duración, descripción, hashtags, portada, sonido y ajustes. Cada regla dice su certeza (oficial, de terceros o criterio). Las citas están en `docs/investigacion/inv-creadores.md`.

## La ficha (JSON)

Va en `cuenta/privado/` (no se sube: el repositorio es público). Ejemplo completo: [pieza.ejemplo.json](../assets/pieza.ejemplo.json). Campos:

| Campo | Qué lleva |
|---|---|
| `id` | Único, por ejemplo `tt-2026-11-21-matriz`. |
| `fecha` | ISO con zona de México: `2026-11-21T12:00:00-06:00`. |
| `pilar` | `ia-derecho`, `lifestyle` o `politica`. |
| `formato` | `video` (grabado o animado) o `fotos` (carrusel). |
| `productora` | `vox-studio` (animado), `editor-studio` (lo graba Emi y se edita) o `emi` (lo graba y lo sube él). |
| `idea` | Una sola idea, en una línea. |
| `angulo` | La opinión o el giro de Emi. En política, con su postura (`opinion_emi`). |
| `para_quien` | Quién debería verlo (por ejemplo: «abogados jóvenes que hacen todo a mano»). |
| `gancho` | `{texto_pantalla, voz, visual}`: lo que pasa en los primeros 3 segundos. |
| `texto_pantalla` | Los rótulos principales, en orden. |
| `duracion_objetivo_s` | Duración prevista. |
| `descripcion` | El texto de la publicación, con sus hashtags al final. |
| `hashtags` | Lista (2 o 3). Debe coincidir con los de la descripción. |
| `portada` | `{segundo}` o `{archivo}` y su texto. |
| `etiqueta_ia` | `{requiere: false, motivo}`. Ver «Etiqueta de IA». |
| `medios` | `{persona_realista_ia, escena_realista_ia, voz_ia_reconocible, voz_ia_generica, origen_archivo}`. |
| `musica` | `ninguna`, `original`, `biblioteca-tiktok` o `comercial-licenciada`. |
| `divulgacion_comercial` | `true` solo si promueve un servicio o una marca (propia o pagada). |
| `fuentes` | Enlaces oficiales de toda cita legal o dato. |
| `opinion_emi` | Su postura con sus palabras (obligatoria en política). |
| `excepcion_cadencia` | Solo si Emi decidió saltarse la separación o el tope: sus palabras, fecha y dónde lo dijo. `tts semana` lo convierte de error en aviso. |
| `estado` | `idea`, `borrador`, `aprobado`, `programado` o `publicado`. |
| `aprobado_por_emi`, `aprobado_medio`, `aprobado_huella` | Los escribe `tts aprobar`, nunca a mano. |

## Gancho: los primeros 3 segundos

- **Oficial**: «Hook viewers in the first three seconds of your video» (Creator Academy, «Video traffic: the For You feed»). Otro artículo dice «ideally within the first 5 seconds». **Criterio** de la skill: 3 segundos; pasar de 5 es error.
- **Oficial**: técnicas que menciona TikTok: una pregunta que el video responde, suspenso, poner el tiempo en el título («Everything you need to know about buying a home in 2 mins»), mostrar al inicio un adelanto del resultado, y «a bold text overlay or quick voiceover in the first three seconds that tells viewers exactly what they're about to learn».
- **Criterio** (con la postura de Emi del 13/11/2026: ganchos agresivos permitidos): el gancho puede ser duro, pero **tiene que cumplir lo que promete** en el video. Un gancho que engaña hace que la gente salte, y saltar es una de las señales que el sistema predice (oficial).
- **Criterio**: el gancho va en tres capas a la vez: lo que se ve, lo que se oye y el texto en pantalla. Más del 30 % ve sin sonido según una encuesta de TikTok (oficial, sin metodología publicada), así que el texto en pantalla tiene que entenderse solo.

## Texto en pantalla y pantalla segura

- **Oficial**: mantener texto, subtítulos y lo importante dentro de la zona que no tapan los botones, el nombre, la descripción ni el audio, y «avoid placing elements around the edges of your frame». TikTok **no publica medidas en píxeles** para videos orgánicos; para anuncios ofrece plantillas descargables («Downloadable safe zone files are available below», TikTok Ads, «Video ads specifications»).
- **Oficial**: texto normal en 40-50 px a 1080×1920 («regular text in videos usually fits well in a 40 to 50 pixel font size»); los títulos, más grandes.
- **Criterio de producción** (hasta compararlo con la plantilla oficial de anuncios): en 1080×1920, el texto clave entre las alturas 160 y 1,480 px; libres unos 160 px arriba, 440 abajo, 60 a la izquierda y 140 a la derecha, donde está la columna de botones.
- **Oficial**: subtítulos automáticos disponibles en el editor. **Criterio**: si el video ya trae subtítulos quemados, no activar los automáticos encima.

## Duración

- **Oficial**: no hay duración ideal: «experiment with different lengths according to the different types of videos you're crafting». También: «Well-crafted, long-form content thrives on the For You feed». Máximo de subida: 60 minutos.
- **Oficial**: terminar un video largo es señal fuerte (Newsroom 2020).
- **Oficial**: el Creator Rewards Program (abierto en México) solo paga videos de más de 1 minuto, con cuenta personal, 10,000 seguidores y 100,000 vistas en 30 días.
- **Criterio**: para explicar algo jurídico, 45-75 s; para gym o vida diaria, lo que pida la escena. Que dure lo necesario para cumplir el gancho y ni un segundo más. Se ajusta con la curva de retención de Analytics.

## Descripción

- **Oficial**: la Búsqueda ordena por relevancia y engagement; la relevancia sale de «video captions, video text, and hashtags». Las palabras clave van en la descripción, la voz en off, los subtítulos y el texto en pantalla.
- **Oficial**: el relleno de palabras sin relación «can get your video flagged for spam».
- **Criterio**: primera línea con el gancho o el dato, en palabras que alguien buscaría («DOF», «efectivo», «Hacienda»); después, una o dos frases de contexto y, si cabe, una pregunta real. Distinta de la de X, Instagram y LinkedIn (regla común: la misma idea se adapta, nunca se pega el mismo texto).
- **No verificado**: el límite de caracteres (terceros dicen 4,000; el Centro de Ayuda no se pudo leer). La skill avisa arriba de 2,200 y no pasa de ahí.

## Hashtags

- **Oficial**: «we encourage you to use 2 to 3 relevant hashtags on each video». Muchos hashtags poco relacionados «can actually work against you».
- **De terceros**: #fyp, #foryou y apilar hashtags de moda no tuvieron efecto medible en llegar a tendencias (Klug et al., WebSci 2021). `tts revisar` avisa si aparecen #fyp o #parati.
- **Criterio**: 2 o 3 que describan el tema (#derecho, #abogado, #DOF), nunca más de 5. El tope de 5 es de la skill: TikTok no fija un máximo.

## Portada

- **Oficial**: 9:16 a 1080×1920; título simple en la portada («We highly recommend using text to add simple titles to your cover photos»); en nichos profesionales como el legal, «stay away from funky fonts».
- **Oficial**: «Avoid mixing personal and professional content on your account». **Criterio**: Emi decidió mezclar pilares; la portada y el perfil mantienen una sola identidad visual (la de su espacio `personal`) para que la mezcla se vea coherente.
- **Criterio**: elegir el cuadro donde ya se lee el titular, o la `portada.png` que deja Vox Studio. El texto debe leerse en miniatura.

## Sonido y música

- **Oficial**: las cuentas personales tienen la biblioteca «Unlimited» (más de 80,000 sonidos autorizados); las de empresa solo la Commercial Music Library.
- **Oficial**: la música de fuera de TikTok «can trigger mutes or takedowns». La biblioteca general no está liberada para promover un negocio: «If you use our General Music Library through a personal account to promote your business, you are at risk of copyright infringement».
- **Oficial** (dato interno sin método): videos con música de fondo, «+98.31% more views per video». Es una correlación publicada por TikTok; no prueba que la música cause las vistas.
- **De terceros**: no hay auditoría que mida que los sonidos de moda den alcance (ver [mitos.md](mitos.md)).
- **Criterio** (decisión de la Matriz de Redes del 13/11/2026): el máster sale sin canciones comerciales y con música original muy baja. Si Emi quiere un sonido de moda, lo agrega él en la app, desde la biblioteca de TikTok, a volumen mínimo. Nunca en una pieza que promueva a MILLA.

## Etiqueta de IA

Regla de TikTok (oficial, Creator Academy, «AI-generated content label», y Normas, «Integrity and authenticity»):

- **Obligatoria** para contenido hecho o editado de forma significativa con IA que muestre «realistic-looking people or scenes».
- **No obligatoria** para «generic text-to-speech (TTS) narration, when the TTS isn't a recognizable voice of a known individual», para ediciones menores ni para estilos artísticos.
- Activarla «won't affect the distribution of your video»; no se puede quitar después de publicar. Sin la etiqueta cuando hace falta, TikTok puede quitar, restringir o etiquetar el video.
- TikTok etiqueta por su cuenta lo que se hace con sus efectos de IA y lo que llega con metadatos C2PA de otras plataformas (informe DSA 2025), y su equipo puede etiquetar contenido que detecte sin etiqueta (Normas).

Regla de Emi (13/11/2026): ninguna pieza dice que la hizo una IA.

**Cómo se cumplen las dos** (criterio): esta skill **no encarga videos con personas, voces reconocibles ni escenas realistas hechas con IA**. Vox Studio usa ilustración o collage y voz genérica; Editor Studio trabaja con la imagen y la voz reales de Emi. Así la etiqueta no es obligatoria y nada dice quién armó el video. Si una pieza llegara a necesitarla (`medios.persona_realista_ia`, `escena_realista_ia` o `voz_ia_reconocible` en `true`), `tts revisar` da **error** y se rediseña. No se sube sin la etiqueta para esquivarla. Antes de subir se comprueba si el archivo trae metadatos C2PA (`tts archivo RUTA`; queda anotado en `medios.c2pa_revisado`). La comprobación no sirve para esquivar la regla: si el video necesita la etiqueta, se rediseña; si trae C2PA sin necesitarla, se le pide a la productora un render limpio para que TikTok no le ponga una etiqueta que no corresponde.

Caso revisado el 17/11/2026: el video del DOF «¿Adiós al efectivo?» (56 s) es collage ilustrado con voz genérica y no tiene C2PA. No requiere etiqueta.

Voz del espacio `personal` de Vox Studio («Daniel Virgen - Hyped», de la biblioteca de ElevenLabs), revisada el 18/11/2026: suena humana, pero no hay indicio de que sea la voz reconocible de una persona conocida (una búsqueda no la ligó a nadie). **Criterio**: entra en la exención de TTS genérico y no requiere la etiqueta en TikTok; se marca `voz_ia_generica: true`. Si un día se usa una voz clonada de alguien identificable, va `voz_ia_reconocible: true` y la pieza se rediseña. Para cero riesgo, la opción es la voz de Emi. Instagram tiene su propia regla, más amplia, y la decide su skill.

## Marca de agua y archivo de origen

- **Oficial**: lo que lleva marca de agua o logo de otra plataforma no entra al Para ti (informe DSA 2025).
- **Criterio**: siempre se sube el **máster** (`medios.origen_archivo: "master"`), nunca un video descargado de Instagram, X o CapCut con su marca. `tts revisar` da error con `descargado`.

## Divulgación comercial

- **Oficial**: «When you post content that promotes a brand, product, or service (including your own brand or business) … Have the content disclosure toggle turned on»; sin ella, el video puede quedar fuera del Para ti.
- **Criterio**: hablar de las herramientas que Emi construyó no es promover un servicio mientras no ofrezca venderlas. Si una pieza invita a contratar a MILLA, va con `divulgacion_comercial: true`, y la pregunta de si va en esta cuenta la decide Emi.

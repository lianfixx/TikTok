# Registro de cambios

Lo más reciente arriba. Formato en `ia/PROTOCOLO.md`, sección 3.

## 2026-11-18 · Excepciones de cadencia decididas por Emi
- Agente: Claude Code (sesión en la nube)
- Solicitud: Emi, 18/11/2026, en el chat de la Matriz de Redes (informado por esa sesión): los dos videos de The Economist 2027 salen el sábado 21 y el domingo 22, con 24 horas entre los dos.
- Cambios: campo `excepcion_cadencia` en la ficha, con las palabras, la fecha y el lugar donde lo dijo Emi. `tts semana` convierte el error de separación en aviso cuando la ficha lo trae. Documentado en `formato.md`; una prueba nueva. Las dos fichas de TikTok están en `cuenta/privado/` (no se suben) y esperan los MP4 de Vox Studio.
- Archivos: `skills/tiktok-studio/scripts/{tiktokstudio.py,test_tiktokstudio.py}`, `skills/tiktok-studio/references/formato.md` y este registro.
- Verificación: 50 pruebas → aprobado; `tts semana` con las dos fichas → sin errores, con el aviso de la excepción; `python3 ia/verificar.py ci` → aprobado.
- Pendiente: revisar los MP4 (imágenes, voz «Emilio» y C2PA) cuando lleguen al panel y dejar las dos piezas con su ficha.

## 2026-11-18 · Ficha manual de TikTok en el panel
- Agente: Claude Code (sesión en la nube)
- Solicitud: encargo de Emi del 17/11/2026 (que el panel le diga fecha, hora, descripción y le deje descargar video y portada); la Matriz de Redes desplegó la ficha manual el 18/11/2026.
- Cambios: `tiktokstudio.py entregar … --panel` imprime el JSON para `POST /api/claude/pieza` con el bloque `app` (portada y ajustes en frases), más `id` y `archivos` si la ficha trae `panel_id` y `panel_archivos`. La pieza del DOF (`eb716e244b02`) se reenvió con su bloque `app`: sigue «lista para aprobar», con el video y sin errores de revisión. Documentado en `references/entrega-y-medicion.md`.
- Archivos: `skills/tiktok-studio/scripts/{tiktokstudio.py,test_tiktokstudio.py}`, `skills/tiktok-studio/references/entrega-y-medicion.md` y este registro.
- Verificación: 49 pruebas → aprobado; respuesta del panel → `app` guardado, `revision.errores` vacío; `python3 ia/verificar.py ci` → aprobado.
- Pendiente: que Emi apruebe la pieza y la portada propuesta en el panel; el panel no manda avisos al teléfono.

## 2026-11-18 · Vox Studio aplicó el puente; regla de voz de IA aclarada
- Agente: Claude Code (sesión en la nube)
- Solicitud: aviso de la Matriz de Redes (18/11/2026): Vox Studio aplicó la petición, con la confirmación de Emi, y señaló que el puente prohibía «voces realistas hechas con IA» cuando su voz de ElevenLabs lo es.
- Cambios: `puente/PETICION-vox.md` queda en «aplicada en rama, sin fusionar» (commit `7c605c0`). El puente decía más de lo que exige TikTok y contradecía la skill; ahora pide lo mismo que la regla oficial: nada de personas o escenas realistas hechas con IA, ni voces que suenen a una persona conocida, porque la narración TTS genérica está exenta. `formato.md` anota el caso de la voz del espacio personal como TTS genérico (criterio) y la opción de la voz de Emi para cero riesgo.
- Archivos: `puente/{para-vox.md,PETICION-vox.md}`, `skills/tiktok-studio/references/formato.md` y este registro.
- Verificación: `python3 ia/verificar.py ci` → aprobado.
- Pendiente: fusionar la rama de Vox Studio a `main` (lo decide su sesión con Emi).

## 2026-11-17 · Encargo al panel: modo manual de TikTok
- Agente: Claude Code (sesión en la nube)
- Solicitud: Emi, 17/11/2026: que el panel le diga, para TikTok, la hora, la fecha, la descripción y le deje descargar el video y la portada; él publica a mano.
- Cambios: (1) Encargo enviado a la sesión de la Matriz de Redes, que mantiene el panel: fecha, hora y cuenta regresiva; descargar video y portada; copiar la descripción con contador de 2,200 caracteres; checklist de ajustes de la app; pasos; «Ya la publiqué» con enlace; recordatorio; sin reglas de X en piezas de TikTok; y un campo `tiktok` opcional en la pieza para los ajustes. (2) Portada del DOF (cuadro de 0.3 s, 1080×1920) subida al panel (`a9a6a953aba9`) y propuesta a la pieza `eb716e244b02`; Emi la acepta con «Agregar y aprobar». Este repositorio no cambia de código: cuando el panel defina el campo, se adapta la entrega.
- Archivos: este registro.
- Verificación: panel → archivo «listo» y propuesta aceptada por la API; mensaje entregado a la sesión del panel; `python3 ia/verificar.py ci` → aprobado.
- Pendiente: que la sesión del panel lo construya; probarlo con la pieza del DOF; que Emi acepte la portada propuesta.

## 2026-11-17 · Automatizar la subida a TikTok: qué se puede
- Agente: Claude Code (sesión en la nube)
- Solicitud: Emi, 17/11/2026: «Dime paso por paso lo de automatizar la subida de videos».
- Cambios: se leyó la documentación oficial de TikTok for Developers (Content Posting API, Content Sharing Guidelines, App Review Guidelines, sandbox; actualizadas el 04/08/2026) y se anotó en `references/entrega-y-medicion.md`. Publicar directo para la cuenta propia no pasa la auditoría y, sin ella, todo queda en privado. Subir como borrador también pide app aprobada (o un sandbox, que es para pruebas). Lo viable hoy es programar en TikTok Studio web o usar un programador de terceros ya auditado. Tres fuentes nuevas vigiladas.
- Archivos: `skills/tiktok-studio/references/{entrega-y-medicion,fuentes}.md`, `skills/tiktok-studio/data/fuentes.json` y este registro.
- Verificación: `tiktokstudio.py fuentes revisar --solo` en las cuatro fuentes de la API → todas las frases presentes; `python3 ia/verificar.py ci` → aprobado.
- Pendiente: decisión de Emi entre programar en TikTok Studio o probar un programador de terceros.

## 2026-11-17 · DOF aprobado, pieza en el panel y revisión mensual con sello
- Agente: Claude Code (sesión en la nube)
- Solicitud: Emi, 17/11/2026, en el chat de esta sesión: «Apruebo descripción»; «1.- Si 2.- Si» (que la revisión mensual selle sola y que Vox Studio lea el puente de TikTok); preguntó si se puede publicar por API.
- Cambios: (1) Ficha privada del DOF aprobada con `tiktokstudio.py aprobar`: huella del MP4 del panel (`archivo_sha256` igual al del archivo revisado) y sin C2PA. (2) Pieza en el panel de la Matriz de Redes como «lista para aprobar» (id `eb716e244b02`, jueves 19/11 a las 19:30); el panel no publica TikTok: Emi la aprueba, la sube desde la app y marca «Ya la publiqué». (3) La revisión mensual (`fuentes.yml`) ahora sella la fecha y la registra con un commit propio cuando nada cambió; si algo cambió, solo avisa. `ia/REGLAS.md` lo documenta como excepción autorizada. (4) Petición a Vox Studio enviada a la Matriz de Redes para que la haga llegar. (5) Publicar por API: no hoy; la API oficial deja en privado lo que publica una app sin auditar (fuente vigilada `api-publicacion`).
- Archivos: `.github/workflows/fuentes.yml`, `ia/REGLAS.md`, `skills/tiktok-studio/SKILL.md`, `docs/AUDITORIA-2026-11-17.md`, `puente/PETICION-vox.md`, `cuenta/{perfil.json,aprendizajes.md}`, `red/estado.json` y este registro.
- Verificación: `tiktokstudio.py entregar` → paquete sin errores; panel → pieza creada sin errores de revisión (181 caracteres); `python3 ia/verificar.py ci` → aprobado.
- Pendiente: que Emi apruebe la pieza en el panel y la suba el jueves 19 a las 19:30; que mande el enlace para anotarla; su decisión sobre intentar la API.

## 2026-11-17 · Revisión mensual probada en GitHub
- Agente: Claude Code (sesión en la nube)
- Solicitud: cierre de la auditoría del mismo día.
- Cambios: se lanzó a mano el workflow `fuentes.yml` para comprobar que GitHub puede leer tiktok.com; lo anota `docs/AUDITORIA-2026-11-17.md`.
- Archivos: `docs/AUDITORIA-2026-11-17.md` y este registro.
- Verificación: ejecución <https://github.com/lianfixx/TikTok/actions/runs/44237119521> → aprobado, «todas las frases siguen en su fuente»; `python3 ia/verificar.py ci` → aprobado.
- Pendiente: ninguno.

## 2026-11-17 · Auditoría independiente y correcciones (1.2.0)
- Agente: Claude Code (sesión en la nube); revisor: otro agente de Claude Code, independiente y de solo lectura.
- Solicitud: método acordado con Emi para la skill (auditoría adversarial al final y corregir todo lo que encuentre).
- Cambios: detalle en `docs/AUDITORIA-2026-11-17.md`. Vigilancia de fuentes solo dentro del artículo, con dirección final comprobada y salida distinta de 0 si una página no se lee; seis URLs actualizadas y frases más largas. Huella de aprobación que cubre fecha, ajustes y el MP4 (`archivo_sha256`, nueva orden `archivo`, que también busca C2PA). Nombre del despacho detectado aunque venga disfrazado. Regla de autoría de IA y anzuelos con más formas, sin bloquear relatos de terceros. Detección de citas legales más precisa y dominio oficial por nombre de servidor. Tope semanal en ventana móvil con lo publicado. Huella de texto igual a la de la Matriz de Redes. Textos públicos sin datos que liguen la cuenta con el despacho ni con militancia, y sin frases de borradores (las dos entradas anteriores llevan su errata). Escaneo de cookies de TikTok. Afirmaciones ajustadas a su fuente. Correcciones menores de la tabla de la auditoría. El control de GitHub exige `IA-Actor:`. La revisión mensual sigue siendo de solo lectura: hacer que selle y haga commits sola necesita el visto bueno de Emi.
- Archivos: `skills/tiktok-studio/{SKILL.md,scripts/*,data/*,assets/*,references/*}`, puentes `.claude/` y `.agents/`, `ia/{verificar.py,test_verificar.py,REGLAS.md}`, `.github/workflows/fuentes.yml`, `.gitignore`, `cuenta/aprendizajes.md`, `red/estado.json`, `docs/AUDITORIA-2026-11-17.md` y este registro.
- Verificación: 49 pruebas de la skill y 3 de verificar → aprobado; `tiktokstudio.py fuentes revisar --sellar` → 34 de 34 frases dentro de su artículo, sin cambios de dirección; ficha privada del DOF → sin errores; `python3 ia/verificar.py ci` → aprobado.
- Pendiente: que Emi decida si la revisión mensual puede sellar la fecha y hacer commits sola; aprobación de la descripción del DOF; `archivo_sha256` del MP4 antes de entregarlo.

## 2026-11-17 · Respuestas de Emi: cuenta, bio, pilares y descripción del DOF
- Agente: Claude Code (sesión en la nube)
- Solicitud: Emi, 17/11/2026, en el chat de esta sesión: respondió las preguntas de TikTok.
- Cambios: (1) Usuario `@emiliano_milla_`: ya existía; Emi confirmó que es suya y que la reusa (creada el 08/02/2020; vista pública el 17/11/2026: 1,007 seguidores, unos 55,000 likes, 1 video, sin bio). (2) Cuenta personal. (3) Bio: «Disciplina > motivación. Derecho, gym y opiniones que incomodan.» (pidió frases cortas, estilo viral y sin decir «abogado»; Pinterest no se pudo consultar sin sesión). (4) Pilares en tercios iguales después del lanzamiento, adaptados al material. (5) Grabará gym o vlogs cada semana. (6) Revisión de fuentes mensual. (7) Del video del DOF eligió la descripción B; se ajustó para que coincida con el texto del art. 15 y con quien narra, y queda pendiente de que la apruebe. [Errata del 17/11/2026: se quitaron de esta línea frases del borrador sin publicar; ver «Auditoría independiente».] Skill 1.1.0.
- Archivos: `cuenta/perfil.json`, `red/estado.json`, `skills/tiktok-studio/SKILL.md` y sus puentes, `references/{cuenta-nueva,pilares,entrega-y-medicion}.md`, `AGENTS.md`, `ia/INSTRUCCIONES_PROYECTO.md`, `puente/PETICION-vox.md`, `README.md` y este registro.
- Verificación: `tiktokstudio.py cuenta comprobar emiliano_milla_` → existe; ficha privada del DOF con la descripción B ajustada → sin errores; `python3 ia/verificar.py ci` → aprobado.
- Pendiente: que Emi apruebe la descripción ajustada, ponga la bio y el nombre en la app y decida qué hace con el video de 2020; auditoría independiente.

## 2026-11-17 · tiktok-studio 1.0.0
- Agente: Claude Code (sesión en la nube)
- Solicitud: Emi, 13/11/2026: una skill propia para TikTok con el método de x-viral (`lianfixx/X`), adaptada a que TikTok no publicó su algoritmo. Decisiones de Emi tomadas por la Matriz de Redes (13/11/2026, `lianfixx/REDES/docs/DECISIONES-EMI-2026-11-13.md`).
- Cambios: skill `tiktok-studio` con reglas, flujo, algoritmo (señales oficiales y de terceros, sin pesos), formato (gancho, pantalla segura, duración, descripción, hashtags, portada, música, etiqueta de IA, marca de agua, divulgación), mitos, cuenta nueva y calendario, pilares y límites, frontera con Vox Studio y Editor Studio, entrega y medición, fuentes, portabilidad y encargos. Script `tiktokstudio.py` (revisar, semana, aprobar con huella, entregar, balance, publicado, métricas, aprender, idea para Vox, estado para la Matriz, revisión de fuentes y comprobación pública de la cuenta) con 33 pruebas. `red/estado.json` con el contrato 0.1.1. Puentes para Claude, Codex y Gemini, instrucciones para ChatGPT y Gemini, control en GitHub Actions y revisión mensual de 35 frases oficiales en 16 fuentes. Investigación del 13/11/2026 en `docs/investigacion/`.
- Archivos: todo el repositorio salvo `README.md` inicial (reescrito).
- Verificación: `python3 ia/verificar.py ci` → aprobado; `tiktokstudio.py fuentes revisar` → 35 de 35 frases presentes (17/11/2026) [errata: eran 34]; `tiktokstudio.py cuenta comprobar emilianomilla_` → no existe; ficha real del video del DOF (privada) → sin errores; video del DOF revisado cuadro por cuadro → sin marca de otro espacio, sin personas ni escenas realistas y sin metadatos C2PA (el audio no se transcribió). [Errata del 17/11/2026: se quitó el nombre del despacho de esta línea; ver «Auditoría independiente».]
- Pendiente: auditoría independiente; que Emi abra la cuenta y elija usuario, biografía y descripción del DOF; confirmar pilares, videos propios de gym y frecuencia de la revisión de fuentes; que Vox Studio aplique `puente/PETICION-vox.md`.

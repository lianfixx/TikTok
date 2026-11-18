# Registro de cambios

Lo más reciente arriba. Formato en `ia/PROTOCOLO.md`, sección 3.

## 2026-11-17 · Respuestas de Emi: cuenta, bio, pilares y descripción del DOF
- Agente: Claude Code (sesión en la nube)
- Solicitud: Emi, 17/11/2026, en el chat de esta sesión: respondió las preguntas de TikTok.
- Cambios: (1) Usuario `@emiliano_milla_`: ya existía; Emi confirmó que es suya y que la reusa (creada el 08/02/2020; vista pública el 17/11/2026: 1,007 seguidores, unos 55,000 likes, 1 video, sin bio). (2) Cuenta personal. (3) Bio: «Disciplina > motivación. Derecho, gym y opiniones que incomodan.» (pidió frases cortas, estilo viral y sin decir «abogado»; Pinterest no se pudo consultar sin sesión). (4) Pilares en tercios iguales después del lanzamiento, adaptados al material. (5) Grabará gym o vlogs cada semana. (6) Revisión de fuentes mensual. (7) Del video del DOF eligió la descripción B. Se ajustó porque decía «la ley te manda al cheque» y el art. 15 permite efectivo o cheque, y porque decía «te lo explico» con una voz que no es la suya; queda pendiente de que la apruebe. Skill 1.1.0.
- Archivos: `cuenta/perfil.json`, `red/estado.json`, `skills/tiktok-studio/SKILL.md` y sus puentes, `references/{cuenta-nueva,pilares,entrega-y-medicion}.md`, `AGENTS.md`, `ia/INSTRUCCIONES_PROYECTO.md`, `puente/PETICION-vox.md`, `README.md` y este registro.
- Verificación: `tiktokstudio.py cuenta comprobar emiliano_milla_` → existe; ficha privada del DOF con la descripción B ajustada → sin errores; `python3 ia/verificar.py ci` → aprobado.
- Pendiente: que Emi apruebe la descripción ajustada, ponga la bio y el nombre en la app y decida qué hace con el video de 2020; auditoría independiente.

## 2026-11-17 · tiktok-studio 1.0.0
- Agente: Claude Code (sesión en la nube)
- Solicitud: Emi, 13/11/2026: una skill propia para TikTok con el método de x-viral (`lianfixx/X`), adaptada a que TikTok no publicó su algoritmo. Decisiones de Emi tomadas por la Matriz de Redes (13/11/2026, `lianfixx/REDES/docs/DECISIONES-EMI-2026-11-13.md`).
- Cambios: skill `tiktok-studio` con reglas, flujo, algoritmo (señales oficiales y de terceros, sin pesos), formato (gancho, pantalla segura, duración, descripción, hashtags, portada, música, etiqueta de IA, marca de agua, divulgación), mitos, cuenta nueva y calendario, pilares y límites, frontera con Vox Studio y Editor Studio, entrega y medición, fuentes, portabilidad y encargos. Script `tiktokstudio.py` (revisar, semana, aprobar con huella, entregar, balance, publicado, métricas, aprender, idea para Vox, estado para la Matriz, revisión de fuentes y comprobación pública de la cuenta) con 33 pruebas. `red/estado.json` con el contrato 0.1.1. Puentes para Claude, Codex y Gemini, instrucciones para ChatGPT y Gemini, control en GitHub Actions y revisión mensual de 35 frases oficiales en 16 fuentes. Investigación del 13/11/2026 en `docs/investigacion/`.
- Archivos: todo el repositorio salvo `README.md` inicial (reescrito).
- Verificación: `python3 ia/verificar.py ci` → aprobado; `tiktokstudio.py fuentes revisar` → 35 de 35 frases presentes (17/11/2026); `tiktokstudio.py cuenta comprobar emilianomilla_` → no existe; ficha real del video del DOF (privada) → sin errores; video del DOF revisado cuadro por cuadro → sin marca de Castorena, sin personas ni escenas realistas y sin metadatos C2PA (el audio no se transcribió).
- Pendiente: auditoría independiente; que Emi abra la cuenta y elija usuario, biografía y descripción del DOF; confirmar pilares, videos propios de gym y frecuencia de la revisión de fuentes; que Vox Studio aplique `puente/PETICION-vox.md`.

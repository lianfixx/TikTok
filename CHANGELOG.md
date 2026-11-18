# Registro de cambios

Lo más reciente arriba. Formato en `ia/PROTOCOLO.md`, sección 3.

## 2026-11-17 · tiktok-studio 1.0.0
- Agente: Claude Code (sesión en la nube)
- Solicitud: Emi, 13/11/2026: una skill propia para TikTok con el método de x-viral (`lianfixx/X`), adaptada a que TikTok no publicó su algoritmo. Decisiones de Emi tomadas por la Matriz de Redes (13/11/2026, `lianfixx/REDES/docs/DECISIONES-EMI-2026-11-13.md`).
- Cambios: skill `tiktok-studio` con reglas, flujo, algoritmo (señales oficiales y de terceros, sin pesos), formato (gancho, pantalla segura, duración, descripción, hashtags, portada, música, etiqueta de IA, marca de agua, divulgación), mitos, cuenta nueva y calendario, pilares y límites, frontera con Vox Studio y Editor Studio, entrega y medición, fuentes, portabilidad y encargos. Script `tiktokstudio.py` (revisar, semana, aprobar con huella, entregar, balance, publicado, métricas, aprender, idea para Vox, estado para la Matriz, revisión de fuentes y comprobación pública de la cuenta) con 33 pruebas. `red/estado.json` con el contrato 0.1.1. Puentes para Claude, Codex y Gemini, instrucciones para ChatGPT y Gemini, control en GitHub Actions y revisión mensual de 35 frases oficiales en 16 fuentes. Investigación del 13/11/2026 en `docs/investigacion/`.
- Archivos: todo el repositorio salvo `README.md` inicial (reescrito).
- Verificación: `python3 ia/verificar.py ci` → aprobado; `tiktokstudio.py fuentes revisar` → 35 de 35 frases presentes (17/11/2026); `tiktokstudio.py cuenta comprobar emilianomilla_` → no existe; ficha real del video del DOF (privada) → sin errores; video del DOF revisado cuadro por cuadro → sin marca de Castorena, sin personas ni escenas realistas y sin metadatos C2PA (el audio no se transcribió).
- Pendiente: auditoría independiente; que Emi abra la cuenta y elija usuario, biografía y descripción del DOF; confirmar pilares, videos propios de gym y frecuencia de la revisión de fuentes; que Vox Studio aplique `puente/PETICION-vox.md`.

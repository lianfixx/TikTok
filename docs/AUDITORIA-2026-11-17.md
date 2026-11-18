# Auditoría independiente · 17/11/2026

- Revisor: un agente de Claude Code distinto del que escribió la skill, con la consigna de tumbar cada afirmación y cada parte del código. Solo lectura: leyó el repositorio, corrió las pruebas y abrió las fuentes oficiales y los estudios citados.
- Versión auditada: 1.1.0 (commit `6dbae82`). Corrección: 1.2.0.
- Verificado como correcto: las citas oficiales de Newsroom, Centro de Transparencia, Normas de la Comunidad, Creator Academy, informe DSA 2025 y TikTok for Developers; la existencia y el contenido de los estudios de terceros (Boeker y Urman, Vombatkere et al., Zannettou et al., Mosnar et al., Klug et al., Baumann et al., Steel et al., Buffer); el contrato `red/estado.json` contra el validador de la Matriz de Redes; enlaces y anclas; que no haya borradores privados ni secretos en el historial.

## Hallazgos y corrección

| # | Gravedad | Hallazgo | Corrección |
|---|---|---|---|
| 1 | Alta | `fuentes revisar` daba por buena una página borrada (404) o caída si las demás se leían. | Ahora sale con 3 si alguna página no se lee y con 1 si cambió de dirección. Pruebas con páginas simuladas. |
| 2 | Alta | Varias frases vigiladas aparecían fuera del artículo (avances de otros artículos, JSON incrustado), así que nunca podían fallar. Seis páginas ya redirigían. | Se busca solo en el cuerpo del artículo (`articleData` en Creator Academy, `<main>` en las demás), con frases largas, y se comprueba la dirección final. URLs actualizadas. 34 de 34 frases verificadas en vivo. |
| 3 | Alta | La huella de aprobación no cubría la fecha, la música, los ajustes ni el MP4. | La huella cubre todo lo que imprime la entrega, más `archivo_sha256` (nueva orden `archivo`, que también busca C2PA). Sin la huella del MP4 no se entrega. |
| 4 | Alta | `#CastorenaAbogados`, `Castorena_Abogados`, `Castoreña` o `C4storena` pasaban. | Búsqueda sobre texto sin acentos, sin guiones bajos y con sustitución de letras. |
| 5 | Media | La regla «ninguna pieza dice que la hizo una IA» se saltaba con «La IA escribió este guion», «lo hice con IA», «Guion: ChatGPT», y bloqueaba relatos de terceros («lo que generó ChatGPT eran citas falsas»). | Más formas cubiertas como error; lo que cuenta lo que hizo una IA en otro caso queda como aviso. |
| 6 | Media | Anzuelos en mayúscula inicial («Comenta LEY para…») y metas («si llegamos a 10 mil likes…») pasaban; «lo que sigue… y te doy» se bloqueaba. | Patrones corregidos; pedir guardar o compartir queda como aviso. |
| 7 | Media | «Reforma tu rutina» o «Paseo de la Reforma» exigían fuente legal; «art 123», «LFT» o «la Corte» no. Un enlace como `evil.com/dof.gob.mx` contaba como oficial. | Detección de derecho más precisa y dominio oficial comprobado por el nombre del servidor. |
| 8 | Media | El tope semanal contaba semanas de calendario e ignoraba lo publicado. | Ventana móvil de 7 días que incluye `cuenta/publicados.jsonl`. |
| 9 | Media | `huella_texto` no coincidía con la de la Matriz de Redes, así que no servía para detectar textos repetidos entre redes. | Misma fórmula que `redes.py` y x-viral (SHA-256 del texto NFC sin espacios a los lados, 12 hex). El id `tiktok-studio` coincide con la configuración de la Matriz y se conserva. |
| 10 | Media | El repositorio público ligaba la cuenta personal con el despacho y con su militancia, y el registro citaba frases de un borrador sin publicar. | Texto neutralizado en aprendizajes, referencias y registro (las entradas corregidas del registro llevan la marca de errata). |
| 11 | Media | El control de secretos no reconocía las cookies de sesión de TikTok. | Patrones nuevos (`sessionid`, `sid_guard`, `msToken`, `tt_csrf_token`, exportaciones de cookies) y `.gitignore` ampliado. |
| 12 | Media | Exageraciones: «TikTok etiqueta **solo**…», tope de 5 hashtags marcado como oficial, «a más tardar 5 s» como oficial. | Redactado según la fuente; lo que es de la skill quedó marcado como criterio. |
| — | Baja | Conteo de hashtags pegados y con acento; 35 frases cuando eran 34; sábado a las 12:00 contra el calendario de 19:30; frase vieja sobre la cuenta; cita atribuida a las Normas que es de Creator Academy; fila de «shadowban» contradictoria; Klug sin su hallazgo sobre horarios; años de Baumann y Steel (2025); cifra de Forbes omitida; nombres de métricas marcados como oficiales; `nan` en métricas; fechas con «Z» en Python 3.9; sin pruebas de salida de `fuentes`; la revisión mensual no sellaba la fecha; `IA-Actor` no se comprobaba. | Todo corregido. El control de GitHub exige `IA-Actor:`. La revisión mensual sigue siendo de solo lectura: que selle la fecha y haga commits por sí sola requiere el visto bueno de Emi, así que el sello lo deja una sesión al revisar. |

## Lo que sigue sin probar

- Probado el 17/11/2026: la revisión mensual sí lee tiktok.com desde GitHub (ejecución manual <https://github.com/lianfixx/TikTok/actions/runs/44237119521>, 34 de 34 frases). Si un día TikTok la bloquea, falla con salida 2 y se corre desde box o desde una sesión de Claude.
- El límite de caracteres de la descripción y el requisito de seguidores para LIVE: el Centro de Ayuda no se deja leer de forma automática.
- La comprobación de C2PA busca marcas en los bytes del MP4; no es un lector completo de Content Credentials.
- GitHub desactiva las tareas programadas de un repositorio público tras 60 días sin actividad; si eso pasa, se reactiva en la pestaña Actions.
- `aprobar` no registra quién aprobó: la regla de que solo se corre con el visto bueno de Emi se cumple a mano.

# Entregar, anotar y medir

## Entregar

Ninguna IA publica en TikTok ni entra a la cuenta de Emi. Hoy el modo es manual (ver «Automatizar la subida» abajo):

1. `tts revisar ARCHIVO --para entrega` sin errores. Exige que la pieza esté aprobada y que la huella del texto coincida con la aprobada.
2. Antes de aprobar, `tts archivo RUTA.mp4` da el `archivo_sha256` del MP4 (y busca C2PA). Va en la ficha, así la aprobación queda atada a ese archivo exacto y a la fecha, la música y los ajustes; si cualquiera cambia, hay que aprobar de nuevo.
3. `tts entregar ARCHIVO ID` imprime el paquete:
   - fecha y hora (hora del centro de México);
   - archivo de video (nombre y dónde está: Drive o la computadora en la nube);
   - descripción completa, lista para copiar;
   - portada (segundo o archivo) y su texto;
   - ajustes: etiqueta de IA (apagada y por qué), divulgación comercial, música, subtítulos automáticos (no, si ya trae).
4. Emi lo sube desde su teléfono o lo programa en TikTok Studio web, que permite programar hasta 30 días antes (oficial, Creator Academy). Confirma en el chat con el enlace del video.

## Automatizar la subida (revisado el 17/11/2026, TikTok for Developers)

- **Publicar directo por API (Content Posting API, Direct Post)**: sin auditoría, lo publicado queda en privado («Unaudited API Clients can only post contents in SELF_ONLY viewership», oficial). La auditoría no acepta una herramienta para subir a la cuenta propia: «Not acceptable: A utility tool to help upload contents to the account(s) you or your team manages», y la revisión de apps exige que no sea «for private or personal use» (oficial). Con el panel de Emi, que es de uso personal, **no es viable**.
- **Subir como borrador (Upload, `video.upload`)**: el video llega a la bandeja de TikTok de Emi y él lo termina y publica desde la app (oficial). También pide una app aprobada; en modo sandbox, que es para pruebas, funciona sin revisión con hasta 10 cuentas propias (oficial). **Criterio**: usar un sandbox de pruebas como herramienta diaria va contra su propósito y puede dejar de funcionar; no se recomienda como base.
- **Lo viable hoy**: programar en TikTok Studio web, hasta 30 días antes (oficial). Con más de 1,000 seguidores se pueden subir hasta 30 videos a la vez (oficial; Emi tenía 1,007 el 17/11/2026). Un rato a la semana: subir los videos aprobados y dejarlos programados.
- **Programadores de terceros ya auditados** (Buffer, Metricool, Later y similares): Emi conecta su TikTok en ellos y ellos publican. No verificado aquí: si publican directo o como borrador en México, su costo y si tienen API para que el panel les pase las piezas. Requiere decisión de Emi (costo y dar acceso a un tercero).

## Anotar

```bash
tts publicado --id tt-2026-11-20-dof --fecha 2026-11-20T19:30:00-06:00 --pilar ia-derecho \
  --formato video --url https://www.tiktok.com/@emiliano_milla_/video/... --archivo cuenta/privado/semana.json
```

Guarda una línea en `cuenta/publicados.jsonl` con la huella de la descripción (para que la Matriz de Redes detecte textos repetidos entre redes) y regenera `red/estado.json`. El texto completo solo se guarda una vez publicado: lo publicado ya es público.

## Medir

Las métricas las trae Emi: capturas de TikTok Studio → Analytics, cada domingo (decisión del 13/11/2026). Cada video se mide a los **7 días** (criterio: suficiente para que pase su primer recorrido y comparable entre videos). Qué pedir de cada video. Los nombres en inglés son los que se usan en la app; la Creator Academy describe retención, tiempo promedio, «Watched full video» y fuentes de tráfico (oficial), pero el nombre exacto de cada etiqueta se confirma con la primera captura de Emi:

| Métrica | En TikTok Studio | Clave en `valores` |
|---|---|---|
| Vistas | Post views | `vistas` |
| Tiempo promedio | Average watch time | `tiempo_promedio_s` |
| Lo vio completo | Watched full video (%) | `vio_completo_pct` |
| Retención | Retention rate y curva (dónde se van) | `retencion_nota` |
| Me gusta, comentarios, compartidos, guardados | Likes, Comments, Shares, Saves | `likes`, `comentarios`, `compartidos`, `guardados` |
| Nuevos seguidores | New followers | `nuevos_seguidores` |
| Fuentes de tráfico | For You, Following, Search, Profile, Sound… (%) | `trafico_para_ti_pct`, `trafico_busqueda_pct`, `trafico_perfil_pct`, `trafico_siguiendo_pct` |
| Búsquedas | Search queries (últimos 90 días) | `busquedas` (lista) |
| Elegibilidad | Aviso de «no elegible para el Para ti» | `no_elegible` (true/false) |

```bash
tts metricas tt-2026-11-20-dof --capturado 2026-11-27 vistas=1520 tiempo_promedio_s=21.4 vio_completo_pct=18 nuevos_seguidores=7
```

**Qué mirar primero** (oficial: «We suggest keeping an eye on your retention rate … Next, check your engagement»):

1. La curva de retención: dónde se va la gente. Si se va en los primeros 3 segundos, falló el gancho; si se va a la mitad, sobra video.
2. Compartidos y guardados frente a likes.
3. Fuentes de tráfico: mucho «Para ti», el sistema lo está mostrando a desconocidos; mucha «Búsqueda», la descripción y las palabras clave funcionan.
4. Si TikTok marcó el video como no elegible, se lee el motivo y se anota la lección.

La demografía aparece con al menos 100 espectadores en el periodo y «Followers viewed» con 1,000 seguidores (oficial). Los rangos de fechas llegan a 365 días (oficial); por eso las capturas se guardan cada semana y no se depende de lo que quede en la app.

**Criterio**: no se comparan números absolutos con otras redes (cada red mide distinto). Se compara cada video contra la mediana de los videos anteriores de la propia cuenta.

## Lección

Cada video medido deja una lección con `tts aprender`, por ejemplo: «El gancho con la pregunta del DOF retuvo al 60 % a los 3 s; el de la Matriz, al 35 %. Probar preguntas directas». Si sirve para video, también `tts vox idea`.

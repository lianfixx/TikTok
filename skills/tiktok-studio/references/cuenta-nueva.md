# Cuenta nueva y calendario

Plan para abrir la cuenta y las primeras semanas. Lo decidido por Emi lleva fecha; lo demás es propuesta de la skill con su certeza.

## Fase 0: abrir la cuenta (le toca a Emi)

1. Crear la cuenta desde su teléfono. Usuario: `@emilianomilla_`, igual que en X (propuesta; pendiente de que Emi lo confirme). Comprobar después, sin sesión: `tts cuenta comprobar emilianomilla_` (abre la página pública desde box o desde cualquier navegador).
2. Tipo: **personal** (oficial: las dos tienen Analytics; la de empresa pierde la biblioteca de sonidos «Unlimited» y el Creator Rewards Program). Sin teléfono ni correo de MILLA en el perfil: el programa de recompensas excluye perfiles con «personal or business contact information» (oficial).
3. Nombre visible y biografía: lo que Emi elija. El nombre y la biografía son lo que más lleva gente al perfil («your nickname and your bio are the most important for driving profile traffic», oficial).
4. Foto: la profesional que ya tiene.
5. Avisar en el chat. La skill anota el usuario en `cuenta/perfil.json`, regenera `red/estado.json` y deja la petición a Vox Studio para que escriba el @ en su perfil `personal`.

Ninguna IA crea la cuenta, inicia sesión ni la configura: lo hace Emi.

## Fase 1: lanzamiento (decidido por Emi el 13/11/2026)

Cinco videos del espacio personal, pilar IA + Derecho, tesis «la IA reemplaza tareas, no criterio»:

| Orden | Pieza | Productora | Nota |
|---|---|---|---|
| 1 | Video animado del DOF «¿Adiós al efectivo?», **tal cual** | ya hecho (Vox Studio) | Emi pidió subirlo en cuanto tenga cuenta y no volver a discutirlo. |
| 2 | Video 1 · Matriz | Editor Studio (lo graba Emi) | Pregunta final: «¿Tu despacho sabe qué tiene pendiente hoy sin preguntarle a nadie?» |
| 3 | Video 2 · DOF | Editor Studio | Cinco días después del animado, para no repetir tema seguido. |
| 4 | Video 3 · Boletines (datos de ejemplo) | Editor Studio | Rotulado «datos de ejemplo». |
| 5 | Video 4 · Vox | Editor Studio | Con la voz de Emi. Si se muestra un fragmento de Vox, que sea ilustrado. |

Calendario propuesto el 17/11/2026 (sujeto a que la cuenta exista y a que Editor Studio entregue): primer video el día en que se abra la cuenta, a las 19:30; sábado 21 a las 12:00; martes 24, jueves 26 y sábado 28 o lunes 30 a las 19:30. La Matriz de Redes acomoda las fechas en `lianfixx/REDES` (`calendario/`).

## Cadencia (criterio, ajustable)

Mientras se aprende qué funciona: **máximo 1 video por día, al menos 48 horas entre videos y no más de 3 por semana**. Está en `data/reglas.json` y lo valida `tts semana`.

Por qué: TikTok dice «Post more often» y, a la vez, que la cadencia es decisión del creador y que importa más la constancia (oficial). Publicar más sube la probabilidad de un video atípico, no las vistas del típico (Buffer, de terceros). Emi tiene 120 minutos por semana para todas las redes (decisión del 13/11/2026), y cada video grabado le cuesta tiempo. Tres buenos a la semana, sostenidos, valen más que siete que no puede sostener.

Se revisa al cumplir 4 semanas con métricas: si la retención y las vistas aguantan y Emi tiene material, se sube a 4 o 5.

## Fase 2: después del lanzamiento (propuesta, pendiente de Emi)

- **Pilares**: 50 % IA + Derecho, 25 % gym y estilo de vida y 25 % opinión política durante el primer mes; después, según las métricas. En X decidió tercios iguales; en TikTok el lanzamiento ya carga IA + Derecho.
- **Videos que graba él** (gym, vlogs): pendiente de que diga si los hará.
- **Formatos que vale la pena probar** (oficial, Creator Academy): responder un comentario con un video («Respond to comments with a video») y hacer Stitch a una buena pregunta. Los Stitch y Duet no cuentan para el programa de recompensas (oficial).

## Hora de publicación

No hay hora oficial. Mientras no haya datos: 19:30 entre semana y 12:00 en sábado (criterio: después del trabajo y a media mañana del fin de semana en el centro de México). Cuando Analytics tenga datos, se usa «Most active times» de su audiencia: «Use it to help plan when to post, then check back to see what works best for you» (oficial).

## Mismo video en TikTok y en Reels

Sí, con el máster limpio, sin marca de agua de Instagram (oficial: la marca ajena saca el video del Para ti). Que sea idéntico al de Reels no tiene castigo publicado: es contenido original de Emi (criterio). La descripción se escribe para TikTok. Si en una red salió antes y funcionó, la lección se anota en las dos.

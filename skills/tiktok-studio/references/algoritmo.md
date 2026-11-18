# Cómo recomienda TikTok

TikTok **no ha publicado el código ni los pesos** de su sistema de recomendación. Esta página junta lo que TikTok dice oficialmente, lo que terceros midieron con método explícito y lo que es solo criterio, con su grado de certeza en cada línea. Investigación completa, con todas las citas: `docs/investigacion/`. Las frases que vigila la revisión mensual están en [`data/fuentes.json`](../data/fuentes.json).

**Grados de certeza**

- **oficial**: lo dice TikTok en una página suya (Newsroom, Centro de Transparencia, Normas de la Comunidad, Creator Academy, informe DSA). Una página oficial puede ser vieja: se anota su fecha.
- **de terceros**: estudio revisado por pares, periodismo con método o empresa con datos y método declarados. Mide lo que pasa por fuera; no ve el modelo. Los propios investigadores advierten que las auditorías de TikTok «often hold only in the short term» (Mosnar et al., SIGIR 2025).
- **criterio**: decisión de esta skill con base en lo anterior. Se puede cambiar con datos de la cuenta.

## Las etapas (oficial)

Centro de Transparencia, «Introduction to the TikTok recommendation system» (sin fecha visible; leída el 13/11/2026):

1. **Recuperación**: «the system retrieves a large number of videos».
2. **Predicción**: «Predictions estimate the likelihood you will interact with a given video».
3. **Ranking**: «sorts videos by their prediction scores». La puntuación final combina las predicciones («By combining prediction scores for each of these interactions, we can arrive at an overall score»). **Cómo las combina no se publica.**
4. **Diversidad** y reglas adicionales: evitar videos seguidos demasiado parecidos e incluir creadores de la región del espectador.

## Lo que el sistema predice (oficial)

Mismo documento, apéndice. Para cada espectador y cada video, la probabilidad de:

| Acción | Cita |
|---|---|
| Like, compartir, comentar, «No me interesa» | «Like, share, comment on, or mark a video as ‘Not Interested.’» |
| Seguir al autor o entrar a su perfil | «Follow the video’s author or interact with their profile.» |
| Terminar, saltar o guardar en favoritos | «Finish, skip, or favorite a video.» |
| Ver cierto tiempo | «Spend a certain amount of time viewing a video.» |
| Tocar el sonido | «Tap the video’s soundtrack.» |

Lo que pesa más, en palabras de TikTok (sin números):

- Terminar un video largo: «A strong indicator of interest, such as whether a user finishes watching a longer video from beginning to end» (Newsroom, 18/06/2020).
- Tiempo de visualización: «watch time is a key driver for our content recommendation system» (Creator Academy, «Creating high-quality videos on TikTok»).
- Idioma, país y tipo de dispositivo: «receive lower weight in the recommendation system relative to other data points we measure» (Newsroom 2020).

**De terceros**: una filtración de 2021 («TikTok Algo 101», reportada por The New York Times y confirmada como auténtica por TikTok) describía la puntuación como una suma de like, comentario, tiempo de reproducción y reproducción previstos, cada uno con un valor, y la retención y el tiempo de uso como objetivos. Era una versión simplificada para personal no técnico, de 2020-2021, y no da los valores. Sirve para entender la forma, no para calcular nada.

## Lo que el sistema lee del video (oficial)

Centro de Transparencia, apéndice: la hora de publicación, la región desde donde se publicó, el idioma del autor, el sonido, **la duración** y los hashtags. El informe DSA de TikTok de 2025 añade «number of views» como información del video. Newsroom 2020: «captions, sounds, and hashtags».

Que la duración sea una señal **no** dice cuál es la buena: TikTok pide experimentar («experiment with different lengths», Creator Academy).

## Lo que no es factor directo (oficial)

- **Seguidores y éxitos anteriores**: «neither follower count nor whether the account has had previous high-performing videos are direct factors» (Newsroom 2020). Una cuenta nueva no arranca castigada.
- **De terceros**: del lado del espectador, seguir a alguien es lo que más personaliza su feed (Boeker y Urman, WWW 2022; Vombatkere et al., WWW 2024), y la gente da más likes a cuentas que sigue (Zannettou et al., CHI 2024). Los seguidores ayudan **indirectamente**.

## Diversidad (oficial)

- «your For You feed generally won't show two videos in a row made with the same sound or by the same creator» (Newsroom 2020; repetido en Newsroom 16/03/2023).
- «We also don't recommend duplicated content, content you've already seen before, or any content that's considered spam» (Newsroom 2020).
- Modelos que evitan series de videos parecidos en temas sensibles («dispersion techniques», informe DSA 2025).
- **De terceros**: entre el 30 % y el 50 % de lo que ve un usuario en sus primeros mil videos es «explotación» de intereses conocidos; el resto es exploración (Vombatkere et al. 2024). Por eso un video puede llegar a quien no sigue a Emi.

**Criterio**: no publicar dos videos casi iguales; si se repite un tema, cambiar ángulo, gancho y texto.

## Lo que queda fuera del Para ti (oficial)

Normas de la Comunidad vigentes (publicadas el 25/08/2026, en vigor desde el 24/09/2026) e informe DSA 2025. El contenido no elegible **sigue** en el perfil y en la Búsqueda, y TikTok avisa en Analytics si un video quedó fuera.

| Qué | Cita |
|---|---|
| No original o reutilizado sin aportar nada | «ineligible for the FYF if it includes unoriginal or reused material without anything new» |
| Marca de agua o logo de otra plataforma | «(such as content with someone else’s visible watermark or superimposed logo) is ineligible for the FYF» (DSA 2025) |
| Cebo de interacción | «Content that tries to manipulate people into giving gifts or inflating likes or follows isn't eligible for the FYF.» |
| Interacción falsa | «we'll remove fake likes, followers, or other inflated signals» |
| Desinformación de daño moderado; afirmaciones no verificadas sobre elecciones | «ineligible for the FYF if it contains misinformation that may cause moderate harm»; ineligible: «Statements that misrepresent authoritative civic information, such as a false claim about the text of a parliamentary bill» |
| Publicidad política pagada (o sospecha) | «suspected paid political advertising is ineligible for the For You feed» |
| Contenido comercial sin divulgar | «All commercial content must be disclosed using the content disclosure setting.» |
| IA realista sin etiqueta | «Unlabeled content may be removed, restricted, or labeled by our team» |
| Cuenta con mucho contenido no elegible | TikTok puede hacer «the account and its content ineligible for the FYF and harder to find» |

Para un abogado esto se traduce en: citar el texto oficial de la ley o la tesis (un error sobre el texto de una ley es justo el ejemplo de TikTok), nada de pedir likes a cambio de algo, nunca cobrar por hablar de política y divulgar cuando se promueva un servicio propio (MILLA). **Criterio**: esta cuenta personal no promueve a MILLA; si algún día lo hace, se activa la divulgación.

## Intervención humana (de terceros, con respuesta oficial)

Forbes (20/01/2023) documentó el «heating»: empleados que empujan videos al Para ti a mano. TikTok lo confirmó y dijo que afecta a cerca del 0.002 % de los videos. El informe DSA 2025 dice además que TikTok revisa a mano todo contenido que alcanza cierto nivel de popularidad. **Criterio**: nada de esto lo controla Emi; no entra en la estrategia.

## Política (oficial)

- El contenido político orgánico **está permitido** y no es «no elegible» por sí mismo: «our community can share political content organically as long as it's in line with our Community Guidelines. However, we do not allow paid political advertising» (Creator Academy, «Political ads»).
- Prohibido cobrar por contenido político: «if you're getting paid to create anything political, you're breaking our rules».
- Las cuentas de gobierno, políticos y partidos (GPPPA: «elected officials, candidates, government agencies, cabinet ministers, and official spokespeople») pierden anuncios y monetización. **Criterio**: la cuenta de Emi es personal; militar en Acción Juvenil no la vuelve GPPPA. Si Emi fuera candidato o funcionario, se revisa.

## Lo que TikTok no dice (no inventar)

Pesos, porcentajes o umbrales (por ejemplo «70 % de retención»); la mejor hora; cuántos videos por semana; la duración ideal; si la etiqueta de IA baja el alcance (dice que no: «won't affect the distribution»); que exista un «lote de prueba» de N vistas. Ver [mitos.md](mitos.md).

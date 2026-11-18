# Investigación de terceros: sistema de recomendación de TikTok

Fecha de consulta de todas las fuentes: **2026-11-13**.
Las citas van en su idioma original. Ninguna cifra se calculó ni se estimó aquí: todas salen de la fuente citada.

**Etiquetas de certeza**
- **de terceros**: investigadores, periodistas o empresas ajenas a TikTok/ByteDance, con método explícito.
- **oficial (ByteDance)**: escrito por TikTok o por ingenieros de ByteDance.
- **filtración**: documento interno de TikTok publicado por periodistas. TikTok confirmó su autenticidad, pero no lo publicó.

**Advertencia general.** TikTok no ha publicado su código de ranking. Las auditorías externas miden lo que pasa en el feed de cuentas reales o de bots, pero no pueden ver el modelo. Además, Mosnar et al. (SIGIR 2025, de terceros) concluyen que estos hallazgos envejecen rápido: *"these one-shot audit findings often hold only in the short term"* (https://doi.org/10.1145/3726302.3730293). Cualquier hallazgo de 2021-2022 se debe tratar como histórico.

Casi todas las auditorías miden **el lado del espectador** (qué le recomiendan a quien mira). Casi ninguna mide **el lado del creador** (cómo se reparte el alcance de un video nuevo). Para la estrategia de un creador, lo segundo se infiere de lo primero; no se ha demostrado de forma directa.

---

## 1. Estudios

### 1.1 Boeker y Urman (2022): "An Empirical Investigation of Personalization Factors on TikTok"
- **Certeza:** de terceros (Universidad de Zúrich / TU Múnich), revisado por pares.
- **Publicación:** The Web Conference (WWW '22). DOI 10.1145/3485447.3512102. arXiv: https://arxiv.org/abs/2201.12271
- **Método:** auditoría con cuentas falsas (*sock puppets*): bots con guion que siguen, dan like o miran más tiempo, accediendo desde distintas ubicaciones (proxies) e idiomas, por la web de TikTok.
- **Cita:** *"We provide evidence that all the tested factors influence the content recommended to TikTok users. Further, we identified that the follow-feature has the strongest influence, followed by the like-feature and video view rate."*
- **Cita (sobre ubicación e idioma, cuerpo del PDF):** *"This also implies that language does not influence the RS as strong as the location does."*
- **Qué prueba:** que seguir, dar like y el tiempo de visualización del **espectador** cambian su feed, y que la ubicación pesa más que el idioma configurado.
- **Qué no prueba:** cómo se distribuye el video de un creador. Usó la versión web (no la app), en 2021, con bots.

### 1.2 Vombatkere et al. (2024): "TikTok and the Art of Personalization: Investigating Exploration and Exploitation on Social Media Feeds"
- **Certeza:** de terceros (BU, TU Delft, U. Washington, MPI-SWS), revisado por pares.
- **Publicación:** **WWW '24**, no IMC (corrijo el encargo). DOI 10.1145/3589334.3645600. arXiv: https://arxiv.org/abs/2403.12410
- **Método:** datos donados por usuarios reales (vía GDPR) de 347 usuarios, de los cuales se analizan 220 líneas de tiempo. Se validan contra 5 bots y contra una base aleatoria. Cada video se clasifica como "explotación" (afín a intereses previos) o "exploración".
- **Cita:** *"the algorithm exploits users' interests in between 30% and 50% of all recommended videos in the first thousand videos of users' tenure on TikTok."*
- **Cita:** *"our results show that liking and following are the primary drivers of personalization."*
- **Cita (interpretación de los autores):** *"this finding indicates that the TikTok algorithm opts to recommend a large number of explore videos"*
- **Limitación declarada:** *"the sample of real traces from TikTok users is not necessarily representative"*.
- **Para el creador:** una fracción grande del feed es exploración. Esto es coherente con que el contenido llegue a personas que no siguen al creador, pero el estudio no mide el alcance de los creadores.

### 1.3 Klug, Qin, Evans y Kaufman (2021): "Trick and Please. A Mixed-Method Study On User Assumptions About the TikTok Algorithm"
- **Certeza:** de terceros, revisado por pares. ACM WebSci '21. DOI 10.1145/3447535.3462512 (verificado en OpenAlex; dl.acm.org devolvió 403).
- **Método:** 28 entrevistas y análisis de 300,617 videos de la **sección de tendencias** (no del FYP personal).
- **Cita (resumen):** *"Our data analysis confirms that higher video engagement through comments, likes, and shares leads to a higher chance of the algorithm pushing a video to the trending section. We also find that posting videos at certain times increases the chances of it trending and reaching higher popularity. In contrast, the highly common assumption that using trending hashtags, algorithm related hashtags (e.g. #fyp, #foryou), and piling up trending hashtags would significantly push videos to the trending section was found not applicable."*
- **Límite:** son datos de 2020-2021, de la sección de tendencias y de carácter observacional.

### 1.4 Zannettou et al. (2024): "Analyzing User Engagement with TikTok's Short Format Video Recommendations using Data Donations"
- **Certeza:** de terceros. CHI 2024. DOI 10.1145/3613904.3642433. arXiv: https://arxiv.org/abs/2301.04945
- **Método:** donación de datos de 347 usuarios, con 9.2 millones de recomendaciones.
- **Cita:** *"the average daily usage time increases over the users' lifetime while the user attention remains stable at around 45%. We also find that users like more videos uploaded by people they follow than those recommended by people they do not follow."*

### 1.5 Baumann et al. (2026): "Dynamics of algorithmic content amplification on TikTok"
- **Certeza:** de terceros. EPJ Data Science. DOI 10.1140/epjds/s13688-026-00629-2 (verificado en OpenAlex).
- **Método:** auditoría con bots que tienen intereses distintos.
- **Cita:** *"content aligned with the bots' interests undergoes strong amplification, with rapid reinforcement typically occurring within the first 200 videos watched."*
- **Ojo:** "200" se refiere a los **videos que mira el espectador**. **No** es un "lote de 200 vistas" para el video de un creador. No debe usarse como prueba del mito de los lotes.

### 1.6 Kaplan et al. (2026): "When 'For You' Isn't for You: Measuring User Agency in TikTok's Algorithmic Feed"
- **Certeza:** de terceros. ICWSM 2026. DOI 10.1609/icwsm.v20i1.42688
- **Método:** experimentos controlados en la **app móvil** con cuentas propias.
- **Cita:** *"We find that the FYP algorithm is sensitive to both types of signals"* (explícitas e implícitas). También: *"the most effective explicit signal---marking a video as `Not Interested'---is unintuitively buried in the interface."*

### 1.7 Mosnar et al. (2025): "Revisiting Algorithmic Audits of TikTok: Poor Reproducibility and Short-term Validity of Findings"
- **Certeza:** de terceros. SIGIR 2025. DOI 10.1145/3726302.3730293
- **Cita:** *"these one-shot audit findings often hold only in the short term"*. Es la advertencia metodológica que aplica a todo este documento.

### 1.8 Steel, Schirmer, Ruths y Pfeffer (2025/2026): "Just Another Hour on TikTok: ID sampling to obtain a complete slice of TikTok"
- **Certeza:** de terceros. Journal of Quantitative Description: Digital Media, vol. 6 (2026). DOI 10.51685/jqd.2026.002. arXiv: https://arxiv.org/abs/2504.13279
- **Método:** muestreo por ID de más del 99% de las publicaciones de una hora (10 de abril de 2024, de 17:00 a 18:00 UTC), más un minuto por cada hora de un día. Es lo más cercano a datos del **lado del creador** que encontré.
- **Cita (distribución de vistas):** *"view count and like count show a mode at ∼100 views and ∼50 likes respectively"*
- **Cita (publicación programada):** *"there is a 14% higher posting volume at the 0th second of each minute, implying scheduled posts, or bot activity. View counts for posts posted at the zeroth second get significantly more views (p-value: 7e-5), with an mean of 3,899 views at the zeroth second vs. 2,502 views for all other seconds."* Es una correlación: no prueba que programar cause más vistas.
- **Cita (sur global):** *"the global south ... accounts for 81% of posts but only receive mean view counts of 1.5k (compared to a baseline of 2.2k)."*
- **Cita (idioma de comentarios):** *"15% are in English, 9% are in Spanish, and 5% are in Arabic."*
- **Cita (volumen):** *"we estimate a total of 269 million posts produced on the day we looked at"*.

### 1.9 Pew Research Center (2024): "How U.S. Adults Use TikTok"
- **Certeza:** de terceros, con encuesta y observación directa de cuentas.
- **URL:** https://www.pewresearch.org/internet/2024/02/22/how-u-s-adults-use-tiktok/ (PDF: https://www.pewresearch.org/wp-content/uploads/sites/20/2024/02/PL_2024.02.22_TikTok-Users_REPORT.pdf)
- **Método:** encuesta del 7 al 27 de agosto de 2023 a 2,745 adultos de EE. UU. usuarios de TikTok; 869 compartieron su usuario para observar sus cuentas.
- **Cita:** *"The top 25% of U.S. adults on TikTok by posting volume produce 98% of all publicly accessible videos from this group."*
- **Cita:** *"The median poster has put up a total of six public videos in the life of their accounts and received a total of 149 likes in return."*
- **Límite:** mide la concentración de **publicaciones** y de likes totales, no de vistas. Solo cubre EE. UU.

### 1.10 Monolith (2022): "Real Time Recommendation System With Collisionless Embedding Table"
- **Certeza:** **oficial (ByteDance), sistema genérico; no prueba que sea el ranking de TikTok.**
- **Autores:** Zhuoran Liu, Youlong Cheng y otros (Bytedance Inc., más un autor de Fudan). ORSUM@ACM RecSys 2022. arXiv: https://arxiv.org/abs/2209.07663
- **Cita:** *"Building a scalable and real-time recommendation system is vital for many businesses driven by time-sensitive customer feedback, such as short-videos ranking or online ads."*
- **Cita:** *"Monolith has successfully landed in the BytePlus Recommend product."*
- **Qué sugiere:** ByteDance diseña para entrenar en línea, casi en tiempo real, con la retroalimentación reciente del usuario. **Qué no prueba:** el paper no dice que TikTok use Monolith ni describe objetivos de ranking ni señales de TikTok. El texto extraído no menciona "TikTok" ni "Douyin".

### 1.11 Otros estudios relevantes, menos centrales
- **Mousavi et al. (ICWSM 2024), "Auditing Algorithmic Explanations of Social Media Feeds: A Case Study of TikTok Video Explanations"** (de terceros). Cita del resumen en Consensus: *"an account that made zero comments on the platform, was presented with the explanation 'You commented on similar videos' in 34% of all recommended videos."* Conclusión: las explicaciones de "por qué ves esto" que da TikTok no son confiables como fuente.
- **Delmonaco et al. (2024), "'What are you doing, TikTok?': How Marginalized Social Media Users Perceive, Theorize, and 'Prove' Shadowbanning"** (de terceros, cualitativo). DOI 10.1145/3637431. Cita: *"marginalized social media users collaboratively develop and test algorithmic folk theories to make sense of their unclear experiences with shadowbanning."* Documenta creencias y experiencias; no mide la supresión.
- **Masood et al. (CHI 2026), "Counting How the Seconds Count"** (de terceros). arXiv: https://arxiv.org/abs/2503.20030. Usa análisis de video con modelos de visión y lenguaje, donación de datos y entrevistas. Los propios autores dicen: *"it is not our goal to reverse-engineer TikTok's recommendation algorithm"*. No extraje cifras de resultados: las que circulan en agregadores no las verifiqué.

---

## 2. Periodismo con método explícito

### 2.1 The Wall Street Journal (julio de 2021): "Inside TikTok's Highly Secretive Algorithm" / "How TikTok's Algorithm Figures Out Your Deepest Desires"
- **Certeza:** de terceros (experimento periodístico).
- **Fuente primaria:** wsj.com, **no accesible** (bloqueado). Verificado mediante fuentes secundarias:
  - Popular Science, 7 de diciembre de 2021: https://www.popsci.com/technology/tiktok-algorithm/. Cita: *"used 100 automated "bot" accounts"*. Cita: *"the most important element the app analyzed was the watch time on a video"*. Respuesta de TikTok: *"isn't representative of real user behavior because humans have a diverse set of interests."*
  - Tubefilter, 21 de julio de 2021: https://tubefilter.com/2021/07/21/tiktok-recommendation-algorithm-wall-street-journal-guillaume-chaslot/. Cita: los bots *"gave TikTok no other information aside from a location and a birthdate."*
- **Método:** 100 bots con intereses asignados que se quedaban en los videos afines o los volvían a ver, y pasaban de largo los demás.
- **Qué prueba:** que el tiempo de visualización del **espectador** basta para personalizar su feed rápido, sin likes ni follows.
- **Qué no prueba:** los pesos internos ni la distribución del lado del creador. Son bots, no humanos.
- **No verificado:** la cifra de "menos de 2 horas / 40 minutos" para aprender los intereses aparece solo en resúmenes secundarios; no la cito como dato.

### 2.2 The New York Times (5 de diciembre de 2021), Ben Smith: "How TikTok Reads Your Mind"
- **Certeza:** filtración de un documento interno ("TikTok Algo 101") reportada por un tercero. TikTok confirmó la autenticidad.
- **Fuente primaria:** https://www.nytimes.com/2021/12/05/business/media/tiktok-algorithm.html, **no accesible** (bloqueado). Verificado mediante:
  - Gizmodo (Shoshana Wodinsky, 6 de diciembre de 2021): https://gizmodo.com/leaked-tiktok-doc-reveals-its-obvious-secret-to-an-addi-1848166901
    - Fórmula, citada del NYT: *"Plike X Vlike + Pcomment X Vcomment + Eplaytime X Vplaytime + Pplay X Vplay"*
    - Objetivos: el sistema *"has chosen to optimize for two closely related metrics in the stream of videos it serves"*: *"retention"* y *"time spent"*. El "ultimate goal" es sumar usuarios activos diarios.
    - Gizmodo no obtuvo copia; un vocero de TikTok confirmó que el documento es auténtico.
  - The Batch / DeepLearning.AI (15 de diciembre de 2021): https://www.deeplearning.ai/the-batch/what-makes-tiktok-tick. Describe la fórmula como una forma simplificada y dice que el Times no definió sus términos. Cita a Julian McAuley (UCSD): *"There seems to be some perception (by the media? or the public?) that they've cracked some magic code for recommendation"*.
- **Qué prueba (con límites):** que en 2020-2021 el documento describía la puntuación de un video como una suma ponderada de predicciones (probabilidad de like, de comentario, tiempo de reproducción esperado y probabilidad de reproducción), con retención y tiempo de uso como objetivos de negocio.
- **Qué no prueba:** los valores de los pesos V, si la fórmula sigue vigente o cómo actúa el filtro previo de candidatos. El documento fue escrito para personal no técnico y, según la cobertura, era una simplificación.

### 2.3 Forbes (20 de enero de 2023), Emily Baker-White: "TikTok's Secret 'Heating' Button Can Make Anyone Go Viral"
- **Certeza:** de terceros (fuentes internas y documentos). TikTok confirmó la práctica.
- **URL original:** https://www.forbes.com/sites/emilybaker-white/2023/01/20/tiktoks-secret-heating-button-can-make-anyone-go-viral/ (**403**). Se leyó la sindicación de Forbes Australia: https://www.forbes.com.au/news/innovation/tiktoks-secret-heating-button-can-make-anyone-go-viral
- **Método:** seis empleados actuales y anteriores de TikTok y ByteDance, más documentos internos.
- **Cita (documento interno "MINT Heating Playbook"):** *"The heating feature refers to boosting videos into the For You feed through operation intervention"*
- **Dato de Forbes:** los videos "calentados" representaban *"around 1-2%"* de las vistas diarias totales.
- **Respuesta de TikTok (Jamie Favazza):** *"that content makes up approximately .002% of videos in For You feeds."* También: *"We promote some videos to help diversify the content experience."*
- **Qué prueba:** que existe una intervención humana manual sobre la distribución, además del algoritmo.
- **Qué no prueba:** a quién se le aplica hoy ni con qué criterio. Las cifras de Forbes (porcentaje de **vistas**) y de TikTok (porcentaje de **videos**) usan denominadores distintos y no son comparables entre sí.

### 2.4 The Intercept (16 de marzo de 2020), Biddle, Ribeiro y Dias: supresión en el FYP
- **Certeza:** de terceros (documentos internos de moderación y fuentes anónimas).
- **URL:** https://theintercept.com/2020/03/16/tiktok-app-moderators-users-discrimination/
- **Contenido:** se indicaba a los moderadores excluir del FYP videos con, por ejemplo, *"ugly facial looks"*, porque podían *"decrease the short-term new user retention rate."*
- **Respuesta de TikTok (Josh Gartner):** las reglas *"represented an early blunt attempt at preventing bullying, but are no longer in place, and were already out of use when The Intercept obtained them."*
- **Qué prueba:** que hubo, al menos hasta 2019 según la fuente, una restricción de alcance por decisión de moderación, distinta de eliminar el video.

### 2.5 Fuente oficial usada como contraste
- **TikTok Newsroom (18 de junio de 2020), "How TikTok recommends videos #ForYou".** Oficial (ByteDance). https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you
  - *"neither follower count nor whether the account has had previous high-performing videos are direct factors"*
  - Señal fuerte: *"whether a user finishes watching a longer video from beginning to end"*
  - Idioma y país: *"they receive lower weight in the recommendation system relative to other data points we measure."*
  - Diversidad: el feed *"generally won't show two videos in a row made with the same sound or by the same creator."*
- **TikTok, "For You feed Eligibility Standards"** (oficial; la página indica *"Effective September 24, 2026"*). https://www.tiktok.com/community-guidelines/en/fyf-standards
  - *"We make ineligible for the FYF certain content that may not be suitable for a broad audience."*
  - *"Creators can check TikTok's analytics to see how their videos are performing, including if there were any made ineligible for recommendation."*
  - *"Even if a video doesn't make it to the FYF, people may still find it through search or by going to a creator's account."*

---

## 3. Mitos

| Mito | Evidencia | Fuente (certeza) | Veredicto |
|---|---|---|---|
| Los hashtags #fyp / #parati ayudan | En 300,617 videos de tendencias, el supuesto de que #fyp/#foryou o apilar hashtags empuja el video *"was found not applicable"*. Steel et al. observan que quienes programan publicaciones usan más #fyp, pero es una correlación con la programación, no con el hashtag. | Klug et al. 2021, DOI 10.1145/3447535.3462512 (de terceros); Steel et al. 2026, arXiv 2504.13279 (de terceros) | **Falso / sin efecto demostrado.** Los datos son de 2021 y de la sección de tendencias. |
| Existe una "mejor hora" para publicar | Klug: publicar *"at certain times increases the chances of it trending"*. Buffer (empresa, observacional) publica rankings de horarios, y otro estudio comercial (Sprout Social) llega a horarios distintos, según cobertura secundaria. Steel: los posts publicados en el segundo 0 tienen más vistas, pero es una correlación (programación o bots). | Klug 2021 (de terceros); https://buffer.com/resources/best-time-to-post-on-tiktok (de terceros, comercial; no lo abrí directamente); Steel 2026 (de terceros) | **Parcial.** El horario se asocia con el rendimiento, pero no hay una hora universal; los estudios se contradicen y son mayormente de EE. UU. Conviene probar con las analíticas propias (actividad de la audiencia). |
| "Shadowban" | Oficial: TikTok declara videos **no elegibles para el FYF** y lo muestra en las analíticas. Histórico: The Intercept documentó la supresión en el FYP por decisión de moderación (2019-2020). Delmonaco et al.: los creadores lo perciben y teorizan, sin medición cuantitativa. | Página oficial de elegibilidad FYF (oficial); The Intercept 2020 (de terceros); Delmonaco 2024, DOI 10.1145/3637431 (de terceros) | **Parcialmente cierto, pero mal nombrado.** La restricción de alcance por video existe y es pública (no elegible para FYF). Un castigo secreto a toda la cuenta **no** está demostrado con método por terceros. |
| Borrar videos daña la cuenta | No encontré auditoría, estudio ni documento oficial verificable. | — | **Sin evidencia** en ningún sentido. |
| Hay un "pool de prueba" o "lotes" de 200-500 vistas | TikTok no publica tamaños de lote. Baumann et al. hablan de "200 videos", pero vistos **por el espectador**, no de vistas de un creador. Steel et al.: la moda de vistas en una muestra casi completa es ~100, una descripción de la distribución y no de un mecanismo. | Newsroom 2020 (oficial, sin cifras); Baumann 2026 (de terceros); Steel 2026 (de terceros) | **No verificado.** Que haya distribución escalonada es plausible, pero la cifra concreta no tiene fuente primaria. |
| Hay que publicar 3 veces al día | Buffer (11.4 M de posts, 150 mil cuentas, regresión de efectos fijos): más frecuencia da *"up to 34% more views per post"* (11+ por semana contra 1 por semana), pero *"the median views per post stay pretty flat"*, y *"Posting more helps — but mostly because it increases your chances of getting lucky."* | https://buffer.com/resources/how-often-should-you-post-on-tiktok/ (de terceros, comercial, 8 de octubre de 2025) | **Falso como regla.** La frecuencia sube las probabilidades de un video atípico con muchas vistas, pero no mejora el video típico. No encontré en una página oficial la cifra de "1-4 al día" atribuida a TikTok. |
| El número de seguidores determina el alcance | Oficial: *"neither follower count nor ... previous high-performing videos are direct factors"*. Del lado del espectador, seguir es el factor de personalización más fuerte (Boeker; Vombatkere), y los usuarios dan más likes a cuentas que siguen (Zannettou). | Newsroom 2020 (oficial); Boeker 2022, Vombatkere 2024, Zannettou 2024 (de terceros) | **No es un factor directo (según la versión oficial)**, pero tiene un efecto indirecto: los seguidores reciben más contenido de la cuenta y responden mejor. |
| Los links o las menciones fuera de la plataforma se penalizan | No encontré evidencia de terceros ni texto oficial verificado. | — | **Sin evidencia.** |
| Editar el texto tras publicar "reinicia" el video | No encontré evidencia. | — | **Sin evidencia.** |
| El watch time de más de 100% (las revisiones) importa | El tiempo de reproducción es señal: *"Eplaytime"* en la fórmula filtrada (NYT, vía Gizmodo); para el WSJ, el watch time es el elemento más importante; oficial: terminar un video largo pesa. Boeker: la tasa de visualización influye en el feed. | NYT/Gizmodo 2021 (filtración); WSJ vía PopSci 2021 (de terceros); Newsroom 2020 (oficial); Boeker 2022 (de terceros) | **El tiempo de visualización como señal: respaldado.** Que el "más de 100%" o las revisiones sean una métrica con peso propio: **no verificado.** |
| Los videos de menos de 15 s ganan | No encontré auditoría que lo pruebe. La única referencia oficial habla de terminar un video **largo** como señal fuerte. | Newsroom 2020 (oficial) | **Sin evidencia de terceros.** No hay base para una regla de duración. |
| TikTok penaliza los Reels resubidos con marca de agua | La página oficial vigente de elegibilidad FYF que pude leer **no** menciona "watermark", "unoriginal" ni "reupload". Solo blogs de creadores lo afirman. | Página FYF oficial (sin mención); blogs (no confiables) | **No verificado.** El contenido no original puede quedar fuera del FYF, pero no encontré el texto oficial vigente. |
| Pasar a cuenta de empresa mata el alcance | No encontré evidencia de terceros ni oficial. | — | **Sin evidencia.** |
| Usar sonidos en tendencia da alcance | No hay auditoría que lo mida. Oficial: el feed *"generally won't show two videos in a row made with the same sound"* (diversificación). | Newsroom 2020 (oficial) | **Sin evidencia de terceros.** |

**Hallazgos transversales útiles para la estrategia**
- El sistema reacciona rápido a la conducta del espectador: tiempo de visualización, likes y follows (Boeker; Vombatkere; Baumann; WSJ).
- Una fracción grande del feed es exploración, según la estimación de Vombatkere (*"30% and 50%"* de explotación).
- El alcance es muy desigual: la moda está en ~100 vistas por video (Steel), y la mediana de un "poster" en EE. UU. es de 149 likes en total (Pew).
- Además del algoritmo, existe intervención humana (heating; moderación del FYP).

---

## 4. México

| Dato | Valor | Fuente (certeza) |
|---|---|---|
| Audiencia publicitaria de TikTok, 18 años o más | *"TikTok had 99.0 million users aged 18 and above"* *"in Mexico in late 2025."* | DataReportal / Kepios, "Digital 2026: Mexico", publicado el 8 de noviembre de 2025. https://datareportal.com/reports/digital-2026-mexico (de terceros, basado en las herramientas publicitarias de TikTok) |
| Alcance frente a adultos | *"TikTok ads reached 105.7 percent\*"* *"of all adults aged 18 and above in Mexico"*. Más del 100% es un artefacto de la fuente publicitaria. | ídem |
| Alcance frente a usuarios de internet | *"equivalent to 89.7 percent of the local internet user base"* | ídem |
| Crecimiento | *"increased by 17.9 million"* *"(+22.0 percent) between the end of 2024 and late 2025."* | ídem |
| Género (audiencia adulta) | *"43.9 percent ... female, whereas 56.1 percent was male."* | ídem |
| Contexto | Población: 132 millones; usuarios de internet: 110 millones (*"83.5 percent"*); identidades en redes sociales: 99.0 millones. | ídem |
| Advertencia metodológica | Son datos de alcance publicitario, no de usuarios activos mensuales: *"trends in TikTok's ad reach figures may not necessarily match changes in the platform's overall user base."* | ídem |
| Español en la plataforma (global) | *"9% are in Spanish"*: comentarios en español en una hora de abril de 2024, a nivel mundial y no solo en México. | Steel et al. 2026 (de terceros) |
| Sur global | Concentra el 81% de los posts, con una media de vistas de 1.5 mil contra 2.2 mil de la base. México no se desglosa. | Steel et al. 2026 (de terceros) |

**No verificado para México:** la cifra de Statista de *"80.8"* por ciento de alcance publicitario a inicios de 2024 (https://statista.com/statistics/1458188/social-media-advertising-reach-mexico) la vi solo en un fragmento de búsqueda. No encontré auditorías del algoritmo hechas específicamente en México o con contenido en español mexicano.

---

## 5. URLs fallidas o no accesibles
- https://www.nytimes.com/2021/12/05/business/media/tiktok-algorithm.html: fetch bloqueado (se usaron Gizmodo y The Batch).
- https://www.wsj.com/video/series/inside-tiktoks-highly-secretive-algorithm/... y https://www.wsj.com/articles/tiktok-algorithm-video-investigation-11626877477: bloqueado (se usaron Popular Science y Tubefilter).
- https://www.forbes.com/sites/emilybaker-white/2023/01/20/tiktoks-secret-heating-button-can-make-anyone-go-viral/: HTTP 403 (se usó forbes.com.au).
- https://dl.acm.org/doi/fullHtml/10.1145/3447535.3462512 (Klug): HTTP 403 (se usaron el resumen vía Consensus y OpenAlex).
- https://support.tiktok.com/en/using-tiktok/exploring-videos/how-tiktok-recommends-content: redirige a https://www.tiktok.com/support/faq_detail?id=7655285288050104852, que devolvió la página vacía (renderizada con JS).
- Página oficial de TikTok con "post 1-4 times a day": no encontrada.
- Buffer, mejor hora (https://buffer.com/resources/best-time-to-post-on-tiktok): no la abrí; las cifras citadas son de fragmentos de búsqueda y no las uso como dato.

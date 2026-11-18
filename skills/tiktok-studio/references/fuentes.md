# Fuentes y cómo se mantienen

## Orden de autoridad

1. Documentación oficial de TikTok: Normas de la Comunidad, Centro de Transparencia (incluidos los informes que exige la Ley de Servicios Digitales de la UE), Creator Academy, Newsroom, TikTok for Business y TikTok for Developers.
2. Declaraciones de directivos de TikTok en canales oficiales.
3. Estudios de terceros con método explícito (revisados por pares, periodismo con método, empresas con datos y método declarados), siempre marcados «de terceros».
4. Criterio de esta skill, marcado como tal.

Blogs de «gurús», cifras sin método y lo que «todo el mundo dice» no cuentan: van a [mitos.md](mitos.md).

## Dónde está cada cosa

- `docs/investigacion/inv-oficial.md`: lo que dice TikTok sobre su recomendación, con citas, URL y fechas (lectura del 13/11/2026).
- `docs/investigacion/inv-creadores.md`: guías oficiales para creadores (formato, búsqueda, analítica, música, cuentas, IA, política).
- `docs/investigacion/inv-terceros.md`: estudios, periodismo y la tabla de mitos.
- [`data/fuentes.json`](../data/fuentes.json): las frases exactas que sostienen cada regla y que se revisan cada mes.

## Fuentes que no se pueden vigilar en automático

- **Centro de Ayuda** (`support.tiktok.com`, que redirige a `tiktok.com/support/faq_detail`): devuelve la página vacía a lectores automáticos. Por eso el límite de caracteres de la descripción y el requisito de seguidores para LIVE quedan **no verificados**.
- **Informe DSA 2025** (PDF en el CDN de TikTok): de ahí sale que la marca de agua ajena saca un video del Para ti. Se relee a mano cuando TikTok publique el informe siguiente (índice: <https://www.tiktok.com/transparency/en/dsa-transparency/>).
- Las fuentes de terceros no cambian una vez publicadas; lo que cambia es TikTok, y por eso envejecen: «these one-shot audit findings often hold only in the short term» (Mosnar et al., SIGIR 2025).

## Revisión mensual

`tiktokstudio.py fuentes revisar` (y el workflow `fuentes.yml`, el primer domingo de cada mes) abre cada página oficial y busca cada frase. Resultados:

- `ok`: la frase sigue; la regla se sostiene.
- `FALTA`: la frase ya no aparece. Puede ser un cambio de redacción o de regla: leer la página y actualizar la regla, la frase y la versión.
- `NO SE LEYÓ`: la página no respondió. No cuenta como cambio. Si ninguna respondió (salida 2), probablemente TikTok bloqueó la lectura desde GitHub; repetir a mano o desde box.

Última revisión completa: 17/11/2026, 38 de 38 frases presentes en 19 fuentes, buscadas solo dentro del artículo (no en menús ni en avances de otros artículos). La revisión también falla si una página cambia de dirección o no se puede leer.

Cuando aparezca una página oficial nueva que importe (por ejemplo, un cambio en las Normas de la Comunidad), se añade a `data/fuentes.json` con su frase y la regla que sostiene.

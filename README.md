# TikTok · tiktok-studio

Skill de la cuenta personal de Emi en TikTok: decide qué video hacer, para quién y cómo engancha en los primeros segundos; prepara la descripción, los hashtags, la portada y el calendario; entrega el paquete aprobado para que Emi lo publique, y mide.

TikTok, a diferencia de X, **no publicó el código de su algoritmo**. Por eso cada regla de esta skill dice de dónde sale y qué tan segura es: **oficial** (lo dice TikTok), **de terceros** (estudio con método) o **criterio** (decisión de la skill). Lo que circula sin sustento está en [mitos](skills/tiktok-studio/references/mitos.md).

## Qué hay aquí

| Ruta | Qué es |
|---|---|
| [`skills/tiktok-studio/SKILL.md`](skills/tiktok-studio/SKILL.md) | La skill: reglas, flujo y lo esencial de TikTok. |
| `skills/tiktok-studio/references/` | Algoritmo, formato, mitos, cuenta nueva, pilares, frontera con video, entrega y medición, fuentes, portabilidad y encargos. |
| `skills/tiktok-studio/scripts/tiktokstudio.py` | Revisor de fichas y semanas, aprobación con huella, entrega, registro, estado para la Matriz y vigilancia de fuentes. Python sin dependencias. |
| `skills/tiktok-studio/data/` | Frases oficiales vigiladas (`fuentes.json`) y parámetros (`reglas.json`). |
| `cuenta/` | Estado de la cuenta, publicados, aprendizajes. `privado/` no se sube. |
| `red/estado.json` | Lo que lee la Matriz de Redes (`lianfixx/REDES`), contrato 0.1.1. |
| `puente/` | Ideas para Vox Studio y la petición para que las lea. |
| `docs/investigacion/` | La investigación completa con citas, URL y fechas. |
| `ia/` | Reglas, protocolo común, control (`verificar.py`), revisor de SKILL.md e instrucciones para ChatGPT y Gemini. |

## Uso rápido

```bash
python3 ia/verificar.py inicio
python3 skills/tiktok-studio/scripts/tiktokstudio.py revisar skills/tiktok-studio/assets/pieza.ejemplo.json
python3 skills/tiktok-studio/scripts/tiktokstudio.py fuentes revisar
python3 ia/verificar.py ci
```

Ninguna IA entra a la cuenta de TikTok de Emi. Emi aprueba y publica.

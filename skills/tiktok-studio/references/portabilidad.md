# Usar la skill en cualquier IA

La skill es Markdown plano, JSON y un script de Python sin dependencias. No usa funciones propias de ninguna plataforma.

| Dónde | Cómo |
|---|---|
| Claude Code, Codex, Gemini CLI, Cursor | Clonar `lianfixx/tiktok`. Cargan `CLAUDE.md`, `AGENTS.md` o `GEMINI.md` y el puente de `.claude/skills/` o `.agents/skills/`. Empezar con `python3 ia/verificar.py inicio`. |
| claude.ai | Subir la carpeta `skills/tiktok-studio` como skill (zip). `python3 ia/check_skill.py skills/tiktok-studio` comprueba que el frontmatter lo acepte. |
| ChatGPT (Proyecto), Gemini (Gem) u otra IA sin terminal | Pegar `ia/INSTRUCCIONES_PROYECTO.md` en las instrucciones y adjuntar o enlazar `SKILL.md` y sus referencias. Las revisiones del script se aplican a mano con [formato.md](formato.md). |

Sin escritura en el repositorio, la IA termina con un bloque «Registro pendiente para el repositorio» con la entrada de `CHANGELOG.md` y los cambios exactos (`ia/PROTOCOLO.md`).

Python 3.9 o más reciente. El script solo usa la red en `fuentes revisar` y `cuenta comprobar`, y solo para leer páginas públicas.

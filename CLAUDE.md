@AGENTS.md

# Claude Code en este repositorio

- La skill canónica está en `skills/tiktok-studio/` y se carga desde el puente `.claude/skills/tiktok-studio` (invocable como `/tiktok-studio`).
- Este repositorio no tiene frenos automáticos: las reglas de `ia/REGLAS.md` se cumplen a mano. Registra cada cambio con `Agente: Claude Code`.
- No se inicia sesión en TikTok desde box ni desde ninguna otra máquina. Lo aprobado se le entrega a Emi listo para copiar (`tiktokstudio.py entregar`). Box sí sirve para ver páginas públicas (`browser_fetch`).

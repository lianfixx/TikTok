#!/usr/bin/env python3
"""Arranque y control de este repositorio (versión ligera del protocolo común entre IA).

  python3 ia/verificar.py inicio   resume rama, último commit, registro, estado de la cuenta y vigencia de las fuentes
  python3 ia/verificar.py ci       pruebas, SKILL.md y puentes, estado para la Matriz, registro con «Agente:»,
                                   secretos y borradores privados

Solo biblioteca estándar. No instala frenos ni hooks: eso lo decide Emi (ver ia/REGLAS.md).
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SKILL = "skills/tiktok-studio"
SKILLS = [SKILL, ".claude/skills/tiktok-studio", ".agents/skills/tiktok-studio"]
SCRIPT = f"{SKILL}/scripts/tiktokstudio.py"
SECRETOS = [
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----", r"\bsk-[A-Za-z0-9_-]{20,}", r"\bgh[pousr]_[A-Za-z0-9]{30,}",
    r"\bAKIA[0-9A-Z]{16}\b", r"\bxox[baprs]-[A-Za-z0-9-]{10,}", r"\bAIza[0-9A-Za-z_-]{35}\b",
    r"(?i)\b(auth_token|sessionid(?:_ss)?|sid_tt|sid_guard|sid_ucp_v1|ssid_ucp_v1|uid_tt|mstoken|tt_csrf_token|tt_chain_token|odin_tt|ct0|password|contraseña|access_token|refresh_token|client_secret)['\"]?\s*[=:]\s*['\"]?[A-Za-z0-9%+/=_|-]{16,}",
    r"(?i)['\"]name['\"]\s*:\s*['\"](?:sessionid|sid_tt|sid_guard|mstoken|tt_csrf_token)['\"]\s*,\s*['\"]value['\"]\s*:\s*['\"][^'\"]{16,}",
    r"\b[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d\b",
]
CAMPOS_ESTADO = ("contrato", "skill", "red", "version_skill", "actualizado", "cuentas", "cadencia", "formatos",
                 "minutos_emi_por_pieza", "publicados", "lecciones", "ideas_para_otras", "pendientes_de_emi", "fuentes")


def git(*args: str) -> str:
    r = subprocess.run(["git", "-C", str(RAIZ), *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def edad_fuentes() -> tuple[str, int | None]:
    try:
        d = json.loads((RAIZ / SKILL / "data/fuentes.json").read_text(encoding="utf-8"))
        maximo = json.loads((RAIZ / SKILL / "data/reglas.json").read_text(encoding="utf-8"))["dias_max_sin_verificar_fuentes"]
        hoy_mx = dt.datetime.now(dt.timezone(dt.timedelta(hours=-6))).date()
        dias = (hoy_mx - dt.date.fromisoformat(d["verificado"])).days
        return f"{len(d['fuentes'])} fuentes oficiales, verificadas el {d['verificado']} (hace {dias} días; máximo {maximo})", dias - maximo
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return f"no se pudieron leer ({exc})", None


def inicio() -> int:
    print(f"Repositorio: lianfixx/tiktok · rama {git('rev-parse', '--abbrev-ref', 'HEAD') or '?'}")
    print(f"Último commit: {git('log', '-1', '--format=%h %cs %s') or 'ninguno'}")
    actor = re.search(r"^IA-Actor:\s*(.+)$", git("log", "-1", "--format=%B"), re.M)
    print(f"Última IA: {actor.group(1) if actor else 'no declarada'}")
    sucio = git("status", "--porcelain")
    print("Cambios sin commit: " + (f"{len(sucio.splitlines())} archivo(s)" if sucio else "ninguno"))
    try:
        pf = json.loads((RAIZ / "cuenta/perfil.json").read_text(encoding="utf-8"))
        print(f"Cuenta: {('@' + pf['usuario']) if pf.get('usuario') else 'sin usuario'} · {pf.get('estado', '?')}")
        for p in pf.get("pendientes_de_emi", []):
            print(f"  Pendiente de Emi: {p.get('que')}")
    except (OSError, ValueError) as exc:
        print(f"Cuenta: no se pudo leer cuenta/perfil.json ({exc})")
    texto, exceso = edad_fuentes()
    print(f"Fuentes: {texto}")
    if exceso is None or exceso > 0:
        print("  AVISO: correr «tiktokstudio.py fuentes revisar --sellar» antes de afirmar reglas de TikTok.")
    registro = RAIZ / "CHANGELOG.md"
    if registro.is_file():
        titulos = [l for l in registro.read_text(encoding="utf-8").splitlines() if l.startswith("## ")][:3]
        print("Registro reciente:\n  " + "\n  ".join(titulos))
    print(f"Leer: AGENTS.md → ia/REGLAS.md → {SKILL}/SKILL.md → cuenta/")
    return 0


def rastreados() -> list[Path]:
    salida = git("ls-files", "-z", "--cached", "--others", "--exclude-standard")
    if salida:
        return [RAIZ / p for p in salida.split("\0") if p]
    return [p for p in RAIZ.rglob("*") if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts]


def ci() -> int:
    fallas: list[str] = []

    def correr(nombre: str, cmd: list[str]) -> None:
        r = subprocess.run(cmd, cwd=RAIZ, capture_output=True, text=True)
        print(f"{'ok   ' if r.returncode == 0 else 'FALLA'} {nombre}")
        if r.returncode != 0:
            fallas.append(nombre)
            print((r.stdout + r.stderr).strip()[-2000:])

    correr("pruebas de tiktokstudio", [sys.executable, "-m", "unittest", "discover", "-s", f"{SKILL}/scripts", "-p", "test_*.py"])
    correr("pruebas de verificar", [sys.executable, "-m", "unittest", "discover", "-s", "ia", "-p", "test_*.py"])
    correr("SKILL.md y puentes", [sys.executable, "ia/check_skill.py", *SKILLS])
    correr("fuentes legibles", [sys.executable, SCRIPT, "fuentes", "ver"])
    correr("perfil de la cuenta legible", [sys.executable, SCRIPT, "balance"])
    correr("ficha de ejemplo sin errores", [sys.executable, SCRIPT, "revisar", f"{SKILL}/assets/pieza.ejemplo.json"])
    correr("semana de ejemplo sin errores", [sys.executable, SCRIPT, "semana", f"{SKILL}/assets/semana.ejemplo.json"])

    canon = (RAIZ / SKILLS[0] / "SKILL.md").read_text(encoding="utf-8")
    desc = re.search(r"^description: (.+)$", canon, re.M)
    for puente in SKILLS[1:]:
        d2 = re.search(r"^description: (.+)$", (RAIZ / puente / "SKILL.md").read_text(encoding="utf-8"), re.M)
        if not desc or not d2 or desc.group(1) != d2.group(1):
            fallas.append(f"{puente}: la descripción no coincide con la skill canónica")
    version = re.search(r'version: "([^"]+)"', canon)
    try:
        estado = json.loads((RAIZ / "red/estado.json").read_text(encoding="utf-8"))
        faltan = [c for c in CAMPOS_ESTADO if c not in estado]
        if faltan:
            fallas.append("red/estado.json: faltan " + ", ".join(faltan))
        if not version or estado.get("version_skill") != version.group(1):
            fallas.append("red/estado.json: version_skill no coincide con SKILL.md (correr «tiktokstudio.py estado»)")
        n_pub = sum(1 for l in (RAIZ / "cuenta/publicados.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())
        if len(estado.get("publicados", [])) != n_pub:
            fallas.append("red/estado.json desactualizado frente a cuenta/publicados.jsonl (correr «tiktokstudio.py estado»)")
    except (OSError, ValueError) as exc:
        fallas.append(f"red/estado.json o cuenta/publicados.jsonl ilegible ({exc})")

    if os.environ.get("GITHUB_ACTIONS") == "true":
        mensaje = git("log", "-1", "--format=%B")
        if mensaje and not re.search(r"^IA-Actor:\s*\S", mensaje, re.M) and not mensaje.startswith("Merge "):
            fallas.append("el último commit no termina con «IA-Actor: <agente>» (ia/PROTOCOLO.md)")

    registro = RAIZ / "CHANGELOG.md"
    texto = registro.read_text(encoding="utf-8") if registro.is_file() else ""
    entradas = re.split(r"^## ", texto, flags=re.M)[1:]
    if not entradas:
        fallas.append("CHANGELOG.md sin entradas")
    for e in entradas:
        if not re.search(r"^- Agente: \S", e, re.M):
            fallas.append(f"CHANGELOG.md: la entrada «{e.splitlines()[0]}» no tiene línea «Agente:»")

    for ruta in rastreados():
        rel = ruta.relative_to(RAIZ).as_posix()
        if rel.startswith("cuenta/privado/") and rel != "cuenta/privado/.gitkeep":
            fallas.append(f"{rel}: los borradores privados no se suben (repositorio público)")
        if re.search(r"(^|/)(borradores?|drafts?)/|\.cookies$|(^|/)\.env$|\.(mp4|mov|m4a|wav)$", rel, re.I):
            fallas.append(f"{rel}: borrador, archivo de sesión o video; no va en un repositorio público")
        if not ruta.is_file() or ruta.stat().st_size > 2_000_000:
            continue
        try:
            contenido = ruta.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for patron in SECRETOS:
            if re.search(patron, contenido):
                fallas.append(f"{rel}: posible secreto o dato personal ({patron[:24]}…)")
    for f in fallas:
        print(f"FALLA {f}")
    print("Control: " + ("aprobado" if not fallas else f"{len(fallas)} falla(s)"))
    return 1 if fallas else 0


if __name__ == "__main__":
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    sys.exit({"inicio": inicio, "ci": ci}.get(orden, lambda: (print(__doc__), 2)[1])())

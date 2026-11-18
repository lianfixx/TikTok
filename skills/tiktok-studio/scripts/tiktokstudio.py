#!/usr/bin/env python3
"""tiktok-studio: utilidades de la skill de TikTok de Emi. Solo biblioteca estándar de Python 3.9+.

Órdenes (ver `tiktokstudio.py -h` y skills/tiktok-studio/SKILL.md):

  revisar ARCHIVO.json [--para entrega]   revisa una ficha, una lista o una semana contra las reglas
  semana ARCHIVO.json                     revisa además separación, tope semanal y balance de pilares
  aprobar ARCHIVO.json ID --medio "…"     anota el visto bueno de Emi y la huella del texto aprobado
  entregar ARCHIVO.json ID                imprime el paquete aprobado listo para copiar
  balance                                 reparto de pilares de lo publicado y qué pilar toca
  publicado --id … --fecha … …            anota un video publicado
  metricas ID --capturado FECHA k=v …     anota métricas de TikTok Studio de un video publicado
  aprender "lección"                      guarda una lección en cuenta/aprendizajes.md
  vox idea "texto"                        deja una idea para Vox Studio en puente/para-vox.md
  estado                                  regenera red/estado.json (contrato de la Matriz de Redes)
  fuentes revisar [--sellar]              comprueba que las fuentes oficiales sigan diciendo lo citado
  fuentes ver                             lista las fuentes y su última verificación
  archivo RUTA.mp4                        sha256 del video (para la aprobación) y búsqueda de metadatos C2PA
  cuenta comprobar USUARIO                mira la página pública de TikTok: ¿existe la cuenta?

Nada aquí publica, programa ni entra a TikTok: eso lo hace Emi, siempre con su visto bueno.
La red solo se usa para leer páginas públicas (fuentes y cuenta).
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import html
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
RAIZ = SKILL.parent.parent
DATA = SKILL / "data"
CUENTA = RAIZ / "cuenta"
PUENTE = RAIZ / "puente"
RED = RAIZ / "red"

PILARES = ("ia-derecho", "lifestyle", "politica")
FORMATOS = ("video", "fotos")
PRODUCTORAS = ("vox-studio", "editor-studio", "emi")
ESTADOS = ("idea", "borrador", "aprobado", "programado", "publicado")
MUSICA = ("ninguna", "original", "biblioteca-tiktok", "comercial-licenciada")
TZ_MX = dt.timezone(dt.timedelta(hours=-6))
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

# Límites de Emi (10 y 13/11/2026). El despacho vetado nunca se nombra: se busca sobre el texto
# «aplanado» (sin acentos, sin guiones bajos y con 4→a, 0→o…), así que tampoco pasa en un hashtag.
DESPACHO_VETADO = r"castorena"
LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s", "_": " "})
ASUNTOS = [
    r"\b(?:mis?|nuestr[oa]s?|un|una|unos|unas|el|la|los|las|ese|esa|este|esta)\s+client[ea]s?\b",
    r"\b(?:expediente|exp\.)\s*(?:n[uú]m(?:ero|\.)?\s*)?\d",
    r"\b(?:amparo|juicio|toca|asunto|causa)\s+(?:(?:directo|indirecto|laboral|penal|civil|en revisi[oó]n)\s+)?(?:n[uú]m(?:ero|\.)?\s*)?\d+/\d{4}\b",
    r"\ben el despacho\s+(?:llevamos|tenemos|vimos|lleg[oó]|atendimos)\b",
]
# Regla absoluta de Emi del 13/11/2026: ninguna pieza dice que la hizo una IA. Error cuando habla de
# esta pieza o de Emi; solo aviso cuando narra lo que una IA hizo en otro lado (eso es tema del pilar).
_IA = r"(?:una\s+|la\s+|el\s+)?(?:ia|i\.a\.|inteligencia artificial|chatgpt|claude|gemini|grok|copilot|un modelo de lenguaje|la m[aá]quina)\b"
_VERBO = r"(?:hizo|arm[oó]|escribi[oó]|gener[oó]|cre[oó]|edit[oó]|redact[oó]|dise[nñ][oó]|produjo|narr[oó]|anim[oó]|grab[oó]|mont[oó])"
_PIEZA = r"(?:este|esta|el|la|mi|nuestro|nuestra)\s+(?:video|v[ií]deo|guion|gui[oó]n|texto|post|voz|imagen|im[aá]genes|edici[oó]n|tiktok|pieza|descripci[oó]n|narraci[oó]n|portada)"
AUTORIA_IA = [
    r"\b(?:escrit|redactad|generad|cread|hech|armad|editad|producid|dise[nñ]ad|narrad|animad)[oa]s?\s+(?:100\s*%\s+|totalmente\s+|todo\s+|completamente\s+)?(?:por|desde|con)\s+" + _IA,
    rf"\b(?:lo|la|los|las|me\s+lo|me\s+la|esto|{_PIEZA})\s+(?:lo\s+|la\s+)?{_VERBO}\s+" + _IA,
    rf"\b{_IA}\s+(?:me\s+)?{_VERBO}\s+(?:{_PIEZA}|esto|todo|lo\s+que\s+ves|lo\s+que\s+escuchas)",
    r"\b(?:lo|la)?\s*(?:hice|hicimos|arm[eé]|cre[eé]|gener[eé]|edit[eé]|escrib[ií])\s+(?:todo\s+|100\s*%\s+)?con\s+" + _IA,
    r"\b(?:texto|post|video|imagen|voz|guion|guión|edici[oó]n|narraci[oó]n)\s*(?:[:=]|por|de|hech[oa]\s+con|generad[oa]\s+con)\s*(?:una\s+)?(?:ia|chatgpt|claude|gemini|grok|copilot)\b",
    r"\bvoz\s+(?:sint[eé]tica|artificial|clonada)\b",
]
AUTORIA_IA_TERCEROS = [rf"\b{_VERBO}\s+" + _IA, rf"\b{_IA}\s+{_VERBO}\b"]
# Anzuelos: el trueque o la orden de interacción dirigida al espectador (Normas: «manipulate people
# into giving gifts or inflating likes or follows»). No se castiga una pregunta real.
_ACCION = r"(?:like|likes|me gusta|coraz[oó]n|corazones|follow|s[ií]gueme|regalo|regalos|rosa|rosas|gu[aá]rd(?:a|alo|ala)|comp[aá]rt(?:e|elo|ela))"
ANZUELOS = [
    rf"\b(?:dale|denle|dame|denme|deme|reg[aá]lame|m[aá]ndame)\s+(?:un\s+|tu\s+|una\s+|tus\s+)?{_ACCION}",
    r"\b(?i:comenta|comenten|escribe|escriban|pon|pongan|responde|respondan)\s+(?i:la\s+palabra\s+)?[\"«“']?[A-ZÁÉÍÓÚÑ0-9]{2,}[\"»”']?\s+(?i:y|para|si)\b",
    rf"\b(?:{_ACCION}|comenta\w*|s[ií]g(?:ue|a)n?me\w*)\b[^.\n]{{0,45}}\by\s+(?:te|les)\s+(?:l[oa]s?\s+)?(?:mando|paso|env[ií]o|regalo|comparto|sigo|doy)\b",
    rf"(?:^|[.!?¿¡\n]\s*)(?:{_ACCION}|dale like|dale coraz[oó]n)\s+si\b",
    r"(?:^|[.!?¿¡\n]\s*)etiqueta(?:n)?\s+a\s+(?:ese|esa|tu|tus|un|una|alguien|quien|\d)",
    r"\bs[ií]g(?:ue|a)n?me(?:n)?\s+(?:para|y)\s+(?:m[aá]s|la\s+parte|parte|ver)",
    r"\bfollow\s*(?:x|por)\s*follow\b|\bsigo\s+de\s+vuelta\b",
    r"\bsi\s+(?:llega(?:mos|s)?|pasa(?:mos)?|junta(?:mos)?)\s+(?:a\s+)?[\d.,]+\s*(?:mil|k)?\s*(?:likes|me gusta|seguidores|comentarios|corazones)",
]
ANZUELOS_LEVES = [r"\bcomp[aá]rt(?:e|elo|ela)\s+con\s+(?:alguien|quien|tu|tus)\b", r"\bgu[aá]rd(?:a|alo|ala)\s+(?:para|este|esto)\b"]
INSULTOS = r"\b(?:idiotas?|imb[eé]cil(?:es)?|pendej[oa]s?|est[uú]pid[oa]s?|tarad[oa]s?|mierdas?)\b"
INSULTOS_LEVES = r"\b(?:rat(?:a|ero|era)s?|payas[oa]s?|inept[oa]s?|basuras?|delincuentes?|c[ií]nic[oa]s?|vendid[oa]s?)\b"
MODISMOS_VETADOS = r"\bg[uü]e[yi]\b|\bwey\b"  # Emi, 13/11/2026: «quítalo, suena horrible»
PLANTILLA_IA = [
    r"\ben el mundo actual\b", r"\ben la era (digital|de la)\b", r"\bes importante destacar\b",
    r"\bcabe (destacar|mencionar|señalar)\b", r"\bsum[eé]rgete\b", r"\bdescubre c[oó]mo\b",
    r"\ben resumen\b", r"\ben conclusi[oó]n\b", r"\bno se trata (solo )?de\b[^.\n]{0,60}\bsino\b",
    r"\bun antes y un despu[eé]s\b", r"\bcambi[oó] las reglas del juego\b", r"\bdesbloquea\b", r"\bpotencia tu\b",
]
DERECHO = re.compile(
    r"\bart[ií]culos?\s+\d+|\barts?\.?\s*\d+|\btesis\b|\bjurisprudencia\b|\bconstituci[oó]n\b|\bconstitucional(?:es)?\b"
    r"|\bley\s+(?:federal|general|org[aá]nica|nacional|de|del|para)\b|\bc[oó]digo\s+(?:civil|penal|fiscal|nacional|de\s+comercio|de\s+procedimientos|federal)\b"
    r"|\bdof\b|\bdiario oficial\b|\bscjn\b|\bsuprema corte\b|\bla corte\b|\btribunal(?:es)?\s+colegiad|\btransitorio\b"
    r"|\breforma\s+(?:constitucional|judicial|laboral|electoral|fiscal|a\s+la\s+ley|al?\s+(?:art|c[oó]digo))"
    r"|\b(?:lft|cpeum|cff|cnpcf|lisr|lamparo|ley de amparo|ine|tepjf|tfja)\b", re.I)
MILLA = re.compile(r"\bmilla\s*abogados\b|\bmillabogados\b|\bcontr[aá]ta(?:me|nos)\b|\bagenda\s+(?:tu|una)\s+(?:cita|asesor[ií]a)\b", re.I)
HASHTAG = re.compile(r"[#＃]([^\s#＃.,;:!?¡¿()\[\]{}\"'«»“”]+)")


# ------------------------------------------------------------------ utilidades

def leer_json(ruta: Path):
    return json.loads(ruta.read_text(encoding="utf-8"))


def escribir_json(ruta: Path, datos) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def reglas() -> dict:
    return leer_json(DATA / "reglas.json")


def perfil() -> dict:
    ruta = CUENTA / "perfil.json"
    return leer_json(ruta) if ruta.is_file() else {}


def normalizar(texto: str) -> str:
    t = unicodedata.normalize("NFKC", texto or "").lower()
    return re.sub(r"\s+", " ", t).strip()


def aplanar(texto: str) -> str:
    """Minúsculas, sin acentos y con sustituciones de letras (4→a, 0→o, _→espacio), para nombres vetados."""
    t = unicodedata.normalize("NFD", normalizar(texto))
    return "".join(c for c in t if unicodedata.category(c) != "Mn").translate(LEET)


def fecha(valor: str) -> dt.datetime:
    texto = str(valor).strip()
    if texto.endswith(("Z", "z")):  # Python < 3.11 no acepta «Z»
        texto = texto[:-1] + "+00:00"
    d = dt.datetime.fromisoformat(texto)
    if d.tzinfo is None:
        raise ValueError("sin zona horaria")
    return d


def piezas_de(datos) -> list[dict]:
    if isinstance(datos, dict) and isinstance(datos.get("piezas"), list):
        return datos["piezas"]
    if isinstance(datos, list):
        return datos
    if isinstance(datos, dict):
        return [datos]
    raise ValueError("el archivo debe ser una ficha, una lista de fichas o {\"piezas\": [...]}")


def textos(p: dict) -> str:
    """Todo lo que se verá o se oirá en la publicación."""
    g = p.get("gancho") or {}
    partes = [p.get("descripcion", ""), p.get("idea", ""), p.get("angulo", ""),
              g.get("texto_pantalla", "") if isinstance(g, dict) else str(g),
              g.get("voz", "") if isinstance(g, dict) else "",
              (p.get("portada") or {}).get("texto", "") if isinstance(p.get("portada"), dict) else ""]
    tp = p.get("texto_pantalla") or []
    partes += tp if isinstance(tp, list) else [str(tp)]
    return "\n".join(str(x) for x in partes if x)


CAMPOS_APROBADOS = ("descripcion", "gancho", "texto_pantalla", "portada", "archivo", "archivo_sha256", "fecha", "musica",
                    "subtitulos_quemados", "etiqueta_ia", "divulgacion_comercial", "fuentes", "medios")


def huella(p: dict) -> str:
    """Huella de todo lo que Emi aprueba y de lo que el paquete de entrega imprime, incluido el MP4 (su sha256)."""
    base = {k: p.get(k) for k in CAMPOS_APROBADOS}
    return hashlib.sha256(json.dumps(base, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def huella_texto(descripcion: str) -> str:
    """Huella para la Matriz de Redes, igual que su `redes.py` y x-viral: SHA-256 del texto NFC sin espacios a los
    lados, primeros 12 hex. Así la Matriz puede detectar el mismo texto en varias redes."""
    return hashlib.sha256(unicodedata.normalize("NFC", descripcion or "").strip().encode("utf-8")).hexdigest()[:12]


def publicados() -> list[dict]:
    ruta = CUENTA / "publicados.jsonl"
    if not ruta.is_file():
        return []
    return [json.loads(l) for l in ruta.read_text(encoding="utf-8").splitlines() if l.strip()]


def hashtags_de(texto: str) -> list[str]:
    return [h.lower() for h in HASHTAG.findall(unicodedata.normalize("NFC", texto or ""))]


def es_oficial(url: str, dominios: tuple) -> bool:
    try:
        partes = urllib.parse.urlsplit(url)
    except ValueError:
        return False
    host = (partes.hostname or "").lower().rstrip(".")
    return partes.scheme in ("http", "https") and any(host == d or host.endswith("." + d) for d in dominios)


# ------------------------------------------------------------------ revisar

def revisar_pieza(p: dict, para: str = "", previas: list[str] | None = None, hoy: dt.datetime | None = None) -> tuple[list[str], list[str]]:
    errores: list[str] = []
    avisos: list[str] = []
    r = reglas()
    hoy = hoy or dt.datetime.now(TZ_MX)

    for campo in ("id", "fecha", "pilar", "formato", "productora", "idea", "descripcion"):
        if not p.get(campo):
            errores.append(f"falta «{campo}»")
    if p.get("pilar") and p["pilar"] not in PILARES:
        errores.append(f"pilar «{p['pilar']}» no es uno de {', '.join(PILARES)}")
    if p.get("formato") and p["formato"] not in FORMATOS:
        errores.append(f"formato «{p['formato']}» no es uno de {', '.join(FORMATOS)}")
    if p.get("productora") and p["productora"] not in PRODUCTORAS:
        errores.append(f"productora «{p['productora']}» no es una de {', '.join(PRODUCTORAS)}")
    if p.get("estado") and p["estado"] not in ESTADOS:
        errores.append(f"estado «{p['estado']}» no es uno de {', '.join(ESTADOS)}")
    cuando = None
    if p.get("fecha"):
        try:
            cuando = fecha(p["fecha"])
        except ValueError:
            errores.append("fecha inválida: usar ISO con zona, por ejemplo 2026-11-21T12:00:00-06:00")

    # Gancho
    g = p.get("gancho")
    if not isinstance(g, dict) or not str(g.get("texto_pantalla", "")).strip():
        errores.append("falta el gancho con su texto en pantalla («gancho.texto_pantalla»): lo que se lee en los primeros 3 s")
    else:
        seg = g.get("segundos")
        if isinstance(seg, (int, float)):
            if seg > r["gancho_s"]["max"]:
                errores.append(f"el gancho llega a los {seg} s; TikTok habla de los primeros 3 s y, en otra guía, «ideally within the first 5 seconds» (oficial); pasar de 5 es criterio de esta skill")
            elif seg > r["gancho_s"]["ideal"]:
                avisos.append(f"el gancho termina a los {seg} s; lo ideal son 3 (oficial)")
    if p.get("formato") == "video" and not p.get("duracion_objetivo_s"):
        avisos.append("falta «duracion_objetivo_s»: la productora necesita saber cuánto debe durar")

    texto = textos(p)
    plano = normalizar(texto)

    # Límites de Emi
    if re.search(DESPACHO_VETADO, aplanar(texto)):
        errores.append("menciona a Castorena: prohibido en la cuenta personal")
    for patron in ASUNTOS:
        if re.search(patron, plano):
            errores.append("parece hablar de clientes o asuntos de un despacho: prohibido, ni anonimizados")
            break
    if any(re.search(patron, plano) for patron in AUTORIA_IA):
        errores.append("dice o sugiere que una IA hizo la pieza: regla absoluta de Emi (13/11/2026)")
    elif any(re.search(patron, plano) for patron in AUTORIA_IA_TERCEROS):
        avisos.append("habla de lo que hizo una IA: está bien si es de otro caso, nunca de esta pieza (regla absoluta de Emi)")
    if re.search(INSULTOS, plano):
        errores.append("insulto: sin ataques personales")
    elif re.search(INSULTOS_LEVES, plano):
        avisos.append("calificativo fuerte contra alguien: criticar la decisión, no a la persona")
    if re.search(MODISMOS_VETADOS, plano):
        errores.append("«güey» y modismos así están fuera (Emi, 13/11/2026)")
    for i, patron in enumerate(ANZUELOS):
        if re.search(patron, texto) if i == 1 else re.search(patron, plano, re.I):  # el 1 distingue la palabra clave en mayúsculas
            errores.append("anzuelo de interacción: TikTok saca del Para ti lo que manipula para inflar likes, follows o regalos (oficial)")
            break
    else:
        if any(re.search(patron, plano) for patron in ANZUELOS_LEVES):
            avisos.append("pide guardar o compartir: que sea una invitación que aporte, no un trueque (criterio)")
    for patron in PLANTILLA_IA:
        if re.search(patron, plano):
            avisos.append("frase de plantilla («" + re.search(patron, plano).group(0) + "»): que Emi la reescriba con su voz")
            break
    if re.search(r"[^\d\s]:\s", p.get("descripcion", "")):
        avisos.append("la descripción usa dos puntos; a Emi le suenan «muy IA» (dicho para LinkedIn, por confirmar en TikTok)")

    # Derecho y política
    if DERECHO.search(texto):
        dominios = tuple(r["dominios_oficiales"])
        oficiales = [f for f in (p.get("fuentes") or []) if es_oficial(str(f), dominios)]
        if not oficiales:
            errores.append("cita derecho (artículo, ley, DOF, tesis o reforma) sin fuente oficial verificada en «fuentes»")
    if p.get("pilar") == "politica" and not str(p.get("opinion_emi", "")).strip():
        errores.append("pieza política sin «opinion_emi»: primero se le pregunta su postura")
    if MILLA.search(texto) and p.get("divulgacion_comercial") is not True:
        errores.append("promueve un servicio (MILLA o «contrátame»): requiere «divulgacion_comercial»: true y que Emi decida si va en esta cuenta")
    if "divulgacion_comercial" not in p:
        avisos.append("falta «divulgacion_comercial» (true solo si promueve un servicio o una marca)")

    # Descripción y hashtags
    desc = p.get("descripcion", "") or ""
    if len(desc) > r["descripcion_max"]:
        errores.append(f"descripción de {len(desc)} caracteres; la skill no pasa de {r['descripcion_max']} (límite oficial no verificado)")
    tags = hashtags_de(desc)
    if len(tags) > r["hashtags"]["max"]:
        errores.append(f"{len(tags)} hashtags; TikTok recomienda 2 o 3 relevantes (oficial) y esta skill no pasa de 5 (criterio)")
    elif len(tags) > r["hashtags"]["recomendados_max"]:
        avisos.append(f"{len(tags)} hashtags; TikTok recomienda 2 o 3 (oficial)")
    elif not tags:
        avisos.append("sin hashtags; TikTok recomienda 2 o 3 relevantes (oficial)")
    mitos = [t for t in tags if t in r["hashtags_mito"]]
    if mitos:
        avisos.append("hashtags sin efecto demostrado (#" + ", #".join(mitos) + "): ver mitos.md")
    if p.get("hashtags") is not None:
        declarados = [str(h).lstrip("#").lower() for h in p["hashtags"]]
        if sorted(declarados) != sorted(tags):
            avisos.append("«hashtags» no coincide con los de la descripción")
    if len(set(tags)) != len(tags):
        avisos.append("hashtag repetido en la descripción")

    # IA, archivo y música
    medios = p.get("medios")
    etiqueta = p.get("etiqueta_ia")
    if not isinstance(medios, dict):
        errores.append("falta «medios» (persona_realista_ia, escena_realista_ia, voz_ia_reconocible, origen_archivo)")
        medios = {}
    if not isinstance(etiqueta, dict) or "requiere" not in etiqueta:
        errores.append("falta «etiqueta_ia» con «requiere» y «motivo»")
        etiqueta = {}
    realista = [k for k in ("persona_realista_ia", "escena_realista_ia", "voz_ia_reconocible") if medios.get(k) is True]
    if realista or etiqueta.get("requiere") is True:
        errores.append("lleva personas, escenas o voces realistas hechas con IA (" + (", ".join(realista) or "etiqueta_ia.requiere") +
                       "): TikTok exige la etiqueta de IA y Emi prohíbe decir que lo hizo una IA; se rediseña "
                       "(ilustración, voz genérica o la imagen y voz de Emi). Ver formato.md, «Etiqueta de IA»")
    elif etiqueta.get("requiere") is False and not str(etiqueta.get("motivo", "")).strip():
        avisos.append("«etiqueta_ia.requiere» es false sin «motivo»: anotar por qué no hace falta")
    origen = medios.get("origen_archivo")
    if origen == "descargado":
        errores.append("archivo descargado de otra red: la marca de agua ajena saca el video del Para ti (oficial); subir el máster")
    elif origen != "master":
        avisos.append("«medios.origen_archivo» debe ser «master» (el archivo original, sin marca de agua)")
    if p.get("productora") in ("vox-studio", "editor-studio") and medios.get("c2pa_revisado") is not True:
        avisos.append("falta comprobar que el MP4 no traiga metadatos C2PA («medios.c2pa_revisado»: true)")
    musica = p.get("musica")
    if musica is not None and musica not in MUSICA:
        errores.append(f"música «{musica}» no es una de {', '.join(MUSICA)}; nada de canciones comerciales sin licencia")
    if musica == "biblioteca-tiktok" and p.get("divulgacion_comercial") is True:
        errores.append("sonido de la biblioteca general en una pieza que promueve un servicio: riesgo de derechos (oficial)")

    # Duplicados contra lo publicado y entre fichas
    for previa in previas or []:
        sim = difflib.SequenceMatcher(None, normalizar(desc), normalizar(previa)).ratio()
        if sim >= r["similitud"]["error"]:
            errores.append(f"descripción casi igual a otra ({sim:.0%}): TikTok no recomienda contenido duplicado (oficial)")
            break
        if sim >= r["similitud"]["aviso"]:
            avisos.append(f"descripción parecida a otra ({sim:.0%}): cambiar ángulo y texto")
            break

    if cuando and cuando < hoy and p.get("estado") not in ("publicado",):
        avisos.append("la fecha ya pasó")

    if para == "entrega":
        if p.get("estado") not in ("aprobado", "programado"):
            errores.append("para entregar, la pieza tiene que estar aprobada por Emi (tts aprobar)")
        if p.get("aprobado_huella") != huella(p):
            errores.append("el texto cambió después de la aprobación (o no hay aprobación): Emi tiene que aprobar esta versión")
        if not p.get("archivo"):
            errores.append("falta «archivo»: el MP4 aprobado (nombre y dónde está)")
        if not re.fullmatch(r"[0-9a-f]{64}", str(p.get("archivo_sha256", ""))):
            errores.append("falta «archivo_sha256» (tiktokstudio.py archivo RUTA): sin él no se sabe si el MP4 es el que Emi aprobó")
    return errores, avisos


def imprimir(p: dict, errores: list[str], avisos: list[str]) -> None:
    print(f"{'ERROR' if errores else 'ok   '} {p.get('id', '(sin id)')}")
    for e in errores:
        print(f"  error: {e}")
    for a in avisos:
        print(f"  aviso: {a}")


def cmd_revisar(args) -> int:
    piezas = piezas_de(leer_json(Path(args.archivo)))
    previas = [x.get("descripcion", "") for x in publicados() if x.get("descripcion")]
    total = 0
    for i, p in enumerate(piezas):
        otras = previas + [q.get("descripcion", "") for j, q in enumerate(piezas) if j != i and q.get("descripcion")]
        e, a = revisar_pieza(p, args.para, otras)
        imprimir(p, e, a)
        total += len(e)
    print("Revisión: " + ("sin errores" if not total else f"{total} error(es)"))
    return 1 if total else 0


def revisar_semana(piezas: list[dict], previas: list[dict] | None = None) -> tuple[list[str], list[str]]:
    """Cadencia sobre las piezas nuevas y lo ya publicado: por día, separación y tope en cualquier ventana de 7 días."""
    errores: list[str] = []
    avisos: list[str] = []
    c = reglas()["cadencia"]
    ids = {p.get("id") for p in piezas}
    todas = list(piezas) + [x for x in (publicados() if previas is None else previas) if x.get("id") not in ids]
    con_fecha = []
    for p in todas:
        try:
            con_fecha.append((fecha(p["fecha"]), p))
        except (KeyError, ValueError):
            pass
    con_fecha.sort(key=lambda x: x[0])
    por_dia: dict[str, int] = {}
    for f, p in con_fecha:
        dia = f.astimezone(TZ_MX).date().isoformat()
        por_dia[dia] = por_dia.get(dia, 0) + 1
    for dia, n in por_dia.items():
        if n > c["max_por_dia"]:
            errores.append(f"{dia}: {n} videos; máximo {c['max_por_dia']} por día (criterio)")
    semana = dt.timedelta(days=7)
    for i, (f, p) in enumerate(con_fecha):
        dentro = [q for g, q in con_fecha[i:] if g - f < semana]
        if len(dentro) > c["max_por_semana"]:
            errores.append(f"del {f.astimezone(TZ_MX):%d/%m} en 7 días: {len(dentro)} videos ({', '.join(str(q.get('id')) for q in dentro)}); "
                           f"máximo {c['max_por_semana']} en cualquier ventana de 7 días mientras se aprende (criterio)")
            break
    for (f1, p1), (f2, p2) in zip(con_fecha, con_fecha[1:]):
        horas = (f2 - f1).total_seconds() / 3600
        if horas < c["separacion_min_h"]:
            errores.append(f"{p1.get('id')} → {p2.get('id')}: {horas:.0f} h de separación; mínimo {c['separacion_min_h']} (criterio)")
    pilares = [p.get("pilar") for p in piezas if p.get("pilar") in PILARES]
    bal = perfil().get("balance") or {}
    if len(pilares) >= 4 and bal:
        tol = perfil().get("tolerancia_balance", 0.15)
        for pil, meta in bal.items():
            real = pilares.count(pil) / len(pilares)
            if abs(real - meta) > tol:
                avisos.append(f"pilar {pil}: {real:.0%} de la semana contra {meta:.0%} acordado")
    return errores, avisos


def cmd_semana(args) -> int:
    datos = leer_json(Path(args.archivo))
    piezas = piezas_de(datos)
    codigo = cmd_revisar(argparse.Namespace(archivo=args.archivo, para=""))
    e, a = revisar_semana(piezas)
    for x in e:
        print(f"error de semana: {x}")
    for x in a:
        print(f"aviso de semana: {x}")
    print("Semana: " + ("sin errores" if not e and not codigo else "con errores"))
    return 1 if e or codigo else 0


# ------------------------------------------------------------------ aprobar y entregar

def buscar(piezas: list[dict], ident: str) -> dict:
    for p in piezas:
        if p.get("id") == ident:
            return p
    raise SystemExit(f"no hay una pieza con id «{ident}»")


def cmd_aprobar(args) -> int:
    ruta = Path(args.archivo)
    datos = leer_json(ruta)
    piezas = piezas_de(datos)
    p = buscar(piezas, args.id)
    e, _ = revisar_pieza(p)
    if e:
        imprimir(p, e, [])
        print("No se aprueba con errores.")
        return 1
    if not args.medio.strip():
        print("Falta --medio: dónde aprobó Emi (por ejemplo «chat de Claude, 18/11/2026 20:10»).")
        return 1
    p["estado"] = "aprobado"
    p["aprobado_por_emi"] = True
    p["aprobado_medio"] = args.medio
    p["aprobado_fecha"] = dt.datetime.now(TZ_MX).isoformat(timespec="minutes")
    p["aprobado_huella"] = huella(p)
    escribir_json(ruta, datos)
    print(f"Aprobada {p['id']} · huella {p['aprobado_huella'][:12]}. Si cambia el texto, la aprobación deja de valer.")
    return 0


def paquete(p: dict) -> str:
    cuando = fecha(p["fecha"]).astimezone(TZ_MX)
    portada = p.get("portada") or {}
    if portada.get("archivo"):
        port = f"subir {portada['archivo']}"
    elif portada.get("segundo") is not None:
        port = f"elegir el cuadro del segundo {portada['segundo']}"
    else:
        port = "elegir el cuadro donde se lea el titular"
    et = p.get("etiqueta_ia") or {}
    lineas = [
        f"TikTok · {p['id']}",
        f"Cuándo: {cuando:%d/%m/%Y} a las {cuando:%H:%M} (hora del centro de México)",
        f"Archivo: {p.get('archivo', '(falta)')}",
        "",
        "Descripción (copiar tal cual):",
        "-----",
        p.get("descripcion", ""),
        "-----",
        "",
        f"Portada: {port}" + (f" · texto: {portada['texto']}" if portada.get("texto") else ""),
        "Ajustes:",
        "  · Etiqueta de contenido generado con IA: " + ("ACTIVAR" if et.get("requiere") else f"apagada ({et.get('motivo', 'no aplica')})"),
        "  · Divulgar contenido comercial: " + ("ACTIVAR" if p.get("divulgacion_comercial") else "apagado"),
        "  · Subtítulos automáticos: " + ("no (el video ya trae)" if p.get("subtitulos_quemados") else "sí"),
        "  · Música en la app: " + {"biblioteca-tiktok": "sonido de la biblioteca de TikTok, volumen mínimo",
                                   "ninguna": "ninguna", "original": "no agregar (ya trae música original)",
                                   "comercial-licenciada": "no agregar (ya trae música con licencia)"}.get(p.get("musica"), "no agregar"),
        "",
        "Después de publicar: mandar el enlace del video para anotarlo.",
    ]
    return "\n".join(lineas)


def cmd_entregar(args) -> int:
    p = buscar(piezas_de(leer_json(Path(args.archivo))), args.id)
    e, a = revisar_pieza(p, "entrega")
    if e:
        imprimir(p, e, a)
        print("No se entrega con errores.")
        return 1
    print(paquete(p))
    return 0


# ------------------------------------------------------------------ registro

def cmd_balance(args) -> int:
    pubs = publicados()
    bal = perfil().get("balance") or {}
    n = len(pubs)
    print(f"Publicados: {n}")
    faltas = {}
    for pil in PILARES:
        k = sum(1 for x in pubs if x.get("pilar") == pil)
        meta = bal.get(pil, 0)
        faltas[pil] = meta * (n + 1) - k
        print(f"  {pil}: {k} ({(k / n if n else 0):.0%}) · acordado {meta:.0%}")
    if bal:
        print(f"Toca: {max(faltas, key=faltas.get)}")
    else:
        print("Sin balance acordado en cuenta/perfil.json")
    return 0


def cmd_publicado(args) -> int:
    try:
        fecha(args.fecha)
    except ValueError:
        print("fecha inválida: ISO con zona, por ejemplo 2026-11-20T19:30:00-06:00")
        return 1
    if args.pilar not in PILARES:
        print(f"pilar inválido: {', '.join(PILARES)}")
        return 1
    if any(x.get("id") == args.id for x in publicados()):
        print(f"ya está anotado: {args.id}")
        return 1
    desc = args.descripcion
    if args.archivo:
        p = buscar(piezas_de(leer_json(Path(args.archivo))), args.id)
        desc = desc or p.get("descripcion", "")
    if not desc:
        print("falta la descripción (--descripcion o --archivo)")
        return 1
    if args.url and not re.match(r"^https://(?:www\.)?tiktok\.com/@[\w.]+/(?:video|photo)/\d+", args.url):
        print("url no parece de un video de TikTok (https://www.tiktok.com/@usuario/video/…)")
        return 1
    reg = {"id": args.id, "fecha": args.fecha, "espacio": args.espacio, "pilar": args.pilar, "formato": args.formato,
           "url": args.url or "", "idea_matriz": args.idea or "", "descripcion": desc, "huella_texto": huella_texto(desc)}
    CUENTA.mkdir(exist_ok=True)
    with (CUENTA / "publicados.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(reg, ensure_ascii=False) + "\n")
    print(f"Anotado {args.id}.")
    return cmd_estado(args)


def _valor(v: str):
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    try:
        return int(v)
    except ValueError:
        try:
            n = float(v)
        except ValueError:
            return v
        if n != n or n in (float("inf"), float("-inf")):
            raise ValueError(f"«{v}» no es un número válido")
        return n


def cmd_metricas(args) -> int:
    ruta = CUENTA / "publicados.jsonl"
    pubs = publicados()
    reg = next((x for x in pubs if x.get("id") == args.id), None)
    if not reg:
        print(f"no está anotado: {args.id}")
        return 1
    try:
        dt.date.fromisoformat(args.capturado)
    except ValueError:
        print("--capturado debe ser una fecha AAAA-MM-DD")
        return 1
    valores = {}
    for par in args.valores:
        if "=" not in par:
            print(f"«{par}» no es clave=valor")
            return 1
        k, v = par.split("=", 1)
        if not re.match(r"^[a-z][a-z0-9_]*$", k):
            print(f"clave «{k}»: usar snake_case")
            return 1
        try:
            valores[k] = _valor(v)
        except ValueError as exc:
            print(exc)
            return 1
    reg["metricas"] = {"capturado": args.capturado, "fuente": args.fuente, "valores": valores}
    ruta.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in pubs), encoding="utf-8")
    print(f"Métricas de {args.id} anotadas.")
    return cmd_estado(args)


def cmd_aprender(args) -> int:
    texto = " ".join(args.texto).strip()
    if not texto:
        print("falta la lección")
        return 1
    ruta = CUENTA / "aprendizajes.md"
    previo = ruta.read_text(encoding="utf-8") if ruta.is_file() else "# Aprendizajes de la cuenta de TikTok\n\n"
    hoy = dt.datetime.now(TZ_MX).date().isoformat()
    ruta.write_text(previo.rstrip("\n") + f"\n- {hoy} · {texto}\n", encoding="utf-8")
    print("Lección guardada.")
    return 0


def cmd_vox(args) -> int:
    if args.accion != "idea":
        print("uso: vox idea \"texto\"")
        return 2
    texto = " ".join(args.texto).strip()
    if not texto:
        print("falta la idea")
        return 1
    ruta = PUENTE / "para-vox.md"
    previo = ruta.read_text(encoding="utf-8")
    hoy = dt.datetime.now(TZ_MX).date().isoformat()
    ruta.write_text(previo.rstrip("\n") + f"\n- {hoy} · espacio `{args.espacio}` · {texto}\n", encoding="utf-8")
    print("Idea para Vox Studio guardada.")
    return 0


# ------------------------------------------------------------------ estado para la Matriz de Redes

FORMATOS_ESTADO = [
    {"id": "video", "que_premia": "Que lo terminen y lo vean más tiempo; likes, compartidos, comentarios, guardados y seguir al autor (sin pesos publicados).",
     "fuente": "skills/tiktok-studio/references/algoritmo.md", "certeza": "oficial"},
    {"id": "fotos", "que_premia": "Las mismas interacciones; TikTok mide retención en carruseles de 2 fotos o más. Sin dato oficial de que rinda más o menos que el video.",
     "fuente": "skills/tiktok-studio/references/formato.md", "certeza": "oficial"},
]


def lecciones() -> list[dict]:
    ruta = CUENTA / "aprendizajes.md"
    out = []
    if ruta.is_file():
        for l in ruta.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^- (\d{4}-\d{2}-\d{2}) · (.+)$", l)
            if m:
                out.append({"fecha": m.group(1), "texto": m.group(2), "evidencia": "cuenta/aprendizajes.md", "alcance": "red"})
    return out


def ideas_vox() -> list[dict]:
    ruta = PUENTE / "para-vox.md"
    out = []
    if ruta.is_file():
        for l in ruta.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^- (\d{4}-\d{2}-\d{2}) · espacio `([\w-]+)` · (.+)$", l)
            if m:
                out.append({"fecha": m.group(1), "para": "vox-studio", "tema": m.group(3), "por_que": f"espacio {m.group(2)}"})
    return out


def construir_estado() -> dict:
    pf = perfil()
    r = reglas()
    c = r["cadencia"]
    version = re.search(r'version: "([^"]+)"', (SKILL / "SKILL.md").read_text(encoding="utf-8"))
    pubs = []
    for x in publicados():
        reg = {k: x.get(k, "") for k in ("id", "fecha", "espacio", "pilar", "formato", "url", "idea_matriz", "huella_texto")}
        if x.get("metricas"):
            reg["metricas"] = x["metricas"]
        pubs.append(reg)
    usuario = pf.get("usuario", "")
    return {
        "contrato": "redes-estado/0.1.1",
        "skill": "tiktok-studio",
        "red": "tiktok",
        "version_skill": version.group(1) if version else "",
        "actualizado": dt.datetime.now(TZ_MX).date().isoformat(),
        "cuentas": [{"espacio": "personal", "usuario": ("@" + usuario) if usuario else "", "activa": bool(pf.get("activa")),
                     "notas": pf.get("estado", "")}],
        "cadencia": {"max_por_dia": c["max_por_dia"], "separacion_min_h": c["separacion_min_h"],
                     "max_por_semana": c["max_por_semana"], "dias_preferidos": [], "fuente": c["fuente"], "certeza": c["certeza"]},
        "formatos": FORMATOS_ESTADO,
        "minutos_emi_por_pieza": r["minutos_emi_por_pieza"],
        "publicados": pubs,
        "lecciones": lecciones(),
        "ideas_para_otras": ideas_vox(),
        "pendientes_de_emi": pf.get("pendientes_de_emi", []),
        "fuentes": {"publicados": "cuenta/publicados.jsonl", "lecciones": "cuenta/aprendizajes.md",
                    "ideas_vox": "puente/para-vox.md", "perfil": "cuenta/perfil.json",
                    "fuentes_oficiales": "skills/tiktok-studio/data/fuentes.json"},
    }


def cmd_estado(args) -> int:
    escribir_json(RED / "estado.json", construir_estado())
    print("red/estado.json actualizado.")
    return 0


# ------------------------------------------------------------------ fuentes y cuenta (solo lectura de páginas públicas)

def cuerpo(crudo: str) -> str:
    """Solo el texto del artículo o de la página, sin menús ni avances de otros artículos.

    Creator Academy trae el artículo en JSON («articleData» → «content»); las demás páginas, en <main>.
    """
    i = crudo.find('"articleData":{"article":')
    if i >= 0:
        j = crudo.find('"content":', i)
        if j >= 0:
            try:
                contenido, _ = json.JSONDecoder().raw_decode(crudo, j + len('"content":'))
                if isinstance(contenido, str):
                    return texto_visible(contenido)
            except ValueError:
                pass
    m = re.search(r"(?is)<main\b[^>]*>(.*)</main>", crudo)
    zona = m.group(1) if m else crudo
    zona = re.sub(r"(?is)<(script|style|noscript)\b[^>]*>.*?</\1>", " ", zona)
    return texto_visible(zona)


def texto_visible(crudo: str) -> str:
    # Se conserva el texto de los <script>: varias páginas de TikTok traen el artículo como JSON incrustado.
    for esc, car in (("\\u002F", "/"), ("\\u003c", "<"), ("\\u003e", ">"), ("\\u0026", "&"), ("\\u0027", "'"), ('\\"', '"')):
        crudo = crudo.replace(esc, car).replace(esc.upper().replace("\\U", "\\u"), car)
    t = html.unescape(re.sub(r"<[^>]+>", " ", crudo))
    t = t.replace("\\u2019", "'").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace(" ", " ")
    return re.sub(r"\s+", " ", t)


def contiene(pagina: str, frase: str) -> bool:
    norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'").replace("‘", "'").replace("\\u2019", "'")).lower()
    return norm(frase) in norm(pagina)


def bajar(url: str, tiempo: int = 30) -> tuple[str, str]:
    """Devuelve (texto crudo, dirección final después de redirecciones)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=tiempo) as resp:
        return resp.read().decode("utf-8", errors="ignore"), resp.geturl()


def misma_direccion(a: str, b: str) -> bool:
    limpiar = lambda u: urllib.parse.urlsplit(u)._replace(query="", fragment="").geturl().rstrip("/").lower()
    return limpiar(a) == limpiar(b)


def revisar_fuentes(datos: dict, leer=bajar, solo: str = "") -> tuple[list, list, list, list[str]]:
    """Devuelve (frases que faltan, páginas sin leer, direcciones que cambiaron, líneas de informe)."""
    faltan, sin_leer, movidas, informe = [], [], [], []
    for f in datos["fuentes"]:
        if solo and f["id"] != solo:
            continue
        try:
            crudo, final = leer(f["url"])
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            sin_leer.append(f["id"])
            informe.append(f"NO SE LEYÓ {f['id']}: {exc}")
            continue
        if not misma_direccion(final, f["url"]):
            movidas.append((f["id"], final))
            informe.append(f"MOVIDA {f['id']}: ahora responde {final}")
        pagina = cuerpo(crudo)
        for fr in f["frases"]:
            ok = contiene(pagina, fr["texto"])
            informe.append(f"{'ok   ' if ok else 'FALTA'} {f['id']}: «{fr['texto']}»")
            if not ok:
                faltan.append((f["id"], fr))
    return faltan, sin_leer, movidas, informe


def cmd_fuentes(args) -> int:
    ruta = DATA / "fuentes.json"
    datos = leer_json(ruta)
    if args.accion == "ver":
        print(f"Última verificación sellada: {datos.get('verificado', 'nunca')}")
        for f in datos["fuentes"]:
            print(f"- {f['id']}: {f['titulo']} ({len(f['frases'])} frase(s))\n  {f['url']}")
        return 0
    faltan, sin_leer, movidas, informe = revisar_fuentes(datos, solo=args.solo)
    print("\n".join(informe))
    for fid, fr in faltan:
        print(f"Revisar regla → {fr['regla']} (fuente {fid})")
    total = sum(1 for f in datos["fuentes"] if not args.solo or f["id"] == args.solo)
    if faltan or movidas:
        print(f"Resultado: {len(faltan)} frase(s) ya no aparecen y {len(movidas)} página(s) cambiaron de dirección. "
              "La regla puede haber cambiado: leer la página y actualizar data/fuentes.json y la referencia.")
        return 1
    if sin_leer and len(sin_leer) == total:
        print("Resultado: no se pudo leer ninguna página (¿bloqueo de red?). Repetir desde otra conexión.")
        return 2
    if sin_leer:
        print(f"Resultado: {len(sin_leer)} página(s) sin leer ({', '.join(sin_leer)}): una página borrada no se puede "
              "distinguir de una caída pasajera, así que no se da por buena. Repetir; si sigue, abrirla a mano.")
        return 3
    print("Resultado: todas las frases siguen en su fuente.")
    if args.sellar and not args.solo:
        datos["verificado"] = dt.datetime.now(TZ_MX).date().isoformat()
        escribir_json(ruta, datos)
        print(f"Sellado: {datos['verificado']}.")
    return 0


def estado_cuenta(pagina: str, usuario: str) -> str:
    """Lee el JSON que TikTok incrusta en la página pública. Heurística: no es una API documentada."""
    m = re.search(r'"statusCode":(\d+)', pagina)
    if re.search(r'"uniqueId":"' + re.escape(usuario) + r'"', pagina, re.I) and (not m or m.group(1) == "0"):
        return "existe"
    if (m and m.group(1) != "0") or "Couldn't find this account" in pagina:
        return "no existe"
    return "no concluyente"


def cmd_cuenta(args) -> int:
    usuario = args.usuario.lstrip("@")
    if not re.match(r"^[\w.]{2,24}$", usuario):
        print("usuario inválido")
        return 2
    try:
        pagina, _ = bajar(f"https://www.tiktok.com/@{usuario}")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"No se pudo leer la página pública: {exc}")
        return 2
    res = estado_cuenta(pagina, usuario)
    print(f"@{usuario}: {res} (lectura de la página pública; confirmar abriéndola en un navegador)")
    return {"existe": 0, "no existe": 1}.get(res, 2)


def cmd_archivo(args) -> int:
    """Huella del MP4 y búsqueda de metadatos C2PA (Content Credentials), que harían que TikTok lo etiquete solo."""
    ruta = Path(args.ruta)
    if not ruta.is_file():
        print(f"no existe: {ruta}")
        return 1
    h = hashlib.sha256()
    c2pa = False
    with ruta.open("rb") as f:
        previo = b""
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
            ventana = (previo + bloque).lower()
            c2pa = c2pa or any(m in ventana for m in (b"c2pa", b"jumbf", b"contentauth", b"jumd"))
            previo = bloque[-16:]
    print(f"archivo_sha256: {h.hexdigest()}")
    print(f"tamaño: {ruta.stat().st_size:,} bytes")
    print("C2PA: " + ("ENCONTRADO: TikTok podría etiquetarlo como IA; pedir a la productora un render sin esos metadatos"
                      if c2pa else "no se encontraron marcas (c2pa, jumbf); revisión por bytes, no exhaustiva"))
    return 2 if c2pa else 0


# ------------------------------------------------------------------ CLI

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tiktokstudio.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="orden", required=True)
    s = sub.add_parser("revisar"); s.add_argument("archivo"); s.add_argument("--para", choices=["entrega"], default=""); s.set_defaults(f=cmd_revisar)
    s = sub.add_parser("semana"); s.add_argument("archivo"); s.set_defaults(f=cmd_semana)
    s = sub.add_parser("aprobar"); s.add_argument("archivo"); s.add_argument("id"); s.add_argument("--medio", required=True); s.set_defaults(f=cmd_aprobar)
    s = sub.add_parser("entregar"); s.add_argument("archivo"); s.add_argument("id"); s.set_defaults(f=cmd_entregar)
    s = sub.add_parser("balance"); s.set_defaults(f=cmd_balance)
    s = sub.add_parser("publicado")
    for k in ("--id", "--fecha", "--pilar"):
        s.add_argument(k, required=True)
    s.add_argument("--formato", default="video", choices=FORMATOS); s.add_argument("--url", default="")
    s.add_argument("--espacio", default="personal"); s.add_argument("--idea", default="")
    s.add_argument("--archivo", default=""); s.add_argument("--descripcion", default=""); s.set_defaults(f=cmd_publicado)
    s = sub.add_parser("metricas"); s.add_argument("id"); s.add_argument("--capturado", required=True)
    s.add_argument("--fuente", default="captura de TikTok Studio de Emi"); s.add_argument("valores", nargs="+"); s.set_defaults(f=cmd_metricas)
    s = sub.add_parser("aprender"); s.add_argument("texto", nargs="+"); s.set_defaults(f=cmd_aprender)
    s = sub.add_parser("vox"); s.add_argument("accion", choices=["idea"]); s.add_argument("texto", nargs="+")
    s.add_argument("--espacio", default="personal"); s.set_defaults(f=cmd_vox)
    s = sub.add_parser("estado"); s.set_defaults(f=cmd_estado)
    s = sub.add_parser("fuentes"); s.add_argument("accion", choices=["revisar", "ver"]); s.add_argument("--sellar", action="store_true")
    s.add_argument("--solo", default=""); s.set_defaults(f=cmd_fuentes)
    s = sub.add_parser("archivo"); s.add_argument("ruta"); s.set_defaults(f=cmd_archivo)
    s = sub.add_parser("cuenta"); s.add_argument("accion", choices=["comprobar"]); s.add_argument("usuario"); s.set_defaults(f=cmd_cuenta)
    args = ap.parse_args(argv)
    return args.f(args)


if __name__ == "__main__":
    sys.exit(main())

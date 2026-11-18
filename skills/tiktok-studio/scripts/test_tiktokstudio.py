"""Pruebas de tiktokstudio.py. Sin red: las órdenes que leen páginas se prueban con texto local."""
from __future__ import annotations

import argparse
import contextlib
import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tiktokstudio as t  # noqa: E402

EJEMPLO = json.loads((t.SKILL / "assets" / "pieza.ejemplo.json").read_text(encoding="utf-8"))


def pieza(**cambios) -> dict:
    p = copy.deepcopy(EJEMPLO)
    p.pop("_nota", None)
    p.update(cambios)
    return p


def errores(p: dict, **kw) -> list[str]:
    return t.revisar_pieza(p, **kw)[0]


def avisos(p: dict, **kw) -> list[str]:
    return t.revisar_pieza(p, **kw)[1]


class Aislado(unittest.TestCase):
    """Cada prueba escribe en un directorio temporal, nunca en cuenta/ ni en red/ del repositorio."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.orig = (t.CUENTA, t.PUENTE, t.RED)
        t.CUENTA, t.PUENTE, t.RED = base / "cuenta", base / "puente", base / "red"
        t.CUENTA.mkdir()
        t.PUENTE.mkdir()
        (t.PUENTE / "para-vox.md").write_text("# Para Vox Studio\n", encoding="utf-8")
        (t.CUENTA / "perfil.json").write_text(json.dumps({
            "usuario": "", "activa": False, "estado": "prueba",
            "balance": {"ia-derecho": 0.5, "lifestyle": 0.25, "politica": 0.25}, "tolerancia_balance": 0.15,
            "pendientes_de_emi": [{"que": "abrir cuenta", "desde": "2026-11-13", "bloquea": "todo"}]}), encoding="utf-8")

    def tearDown(self):
        t.CUENTA, t.PUENTE, t.RED = self.orig
        self.tmp.cleanup()

    def correr(self, argv: list[str]) -> tuple[int, str]:
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            codigo = t.main(argv)
        return codigo, salida.getvalue()


class Revisar(Aislado):
    def test_ejemplo_sin_errores(self):
        self.assertEqual(errores(pieza()), [])

    def test_campos_obligatorios(self):
        e = errores(pieza(id="", pilar="memes", formato="reel", productora="capcut"))
        self.assertTrue(any("«id»" in x for x in e))
        self.assertTrue(any("pilar «memes»" in x for x in e))
        self.assertTrue(any("formato «reel»" in x for x in e))
        self.assertTrue(any("productora «capcut»" in x for x in e))

    def test_fecha_sin_zona(self):
        self.assertTrue(any("fecha inválida" in x for x in errores(pieza(fecha="2099-01-06 19:30"))))

    def test_gancho_tarde_y_sin_texto(self):
        self.assertTrue(any("gancho llega" in x for x in errores(pieza(gancho={"texto_pantalla": "x", "segundos": 8}))))
        self.assertTrue(any("ideal son 3" in x for x in avisos(pieza(gancho={"texto_pantalla": "x", "segundos": 4}))))
        self.assertTrue(any("falta el gancho" in x for x in errores(pieza(gancho={"voz": "hola"}))))

    def test_castorena_prohibido(self):
        self.assertTrue(any("Castorena" in x for x in errores(pieza(descripcion="Lo que aprendí en Castorena #derecho #abogado"))))

    def test_clientes_y_asuntos(self):
        self.assertTrue(any("clientes" in x for x in errores(pieza(descripcion="Un cliente me preguntó esto #derecho #abogado"))))
        self.assertTrue(any("clientes" in x for x in errores(pieza(descripcion="En el amparo 123/2026 pasó algo #derecho #abogado"))))

    def test_autoria_ia_prohibida(self):
        for d in ("Este video lo hizo una IA #derecho #abogado", "Guion generado por ChatGPT #derecho #abogado",
                  "Lo armó Claude en dos minutos #derecho #abogado", "Narrado con voz sintética #derecho #abogado"):
            self.assertTrue(any("regla absoluta" in x for x in errores(pieza(descripcion=d))), d)

    def test_nombrar_la_herramienta_si_se_permite(self):
        p = pieza(descripcion="Uso Claude y ChatGPT para revisar boletines, el criterio es mío. #derecho #abogado")
        self.assertFalse(any("regla absoluta" in x for x in errores(p)))

    def test_anzuelos(self):
        for d in ("Comenta DOF y te mando la ley #derecho #abogado", "Dale like si estás de acuerdo #derecho #abogado",
                  "Sígueme para la parte 2 #derecho #abogado", "Etiqueta a tu amigo abogado #derecho #abogado",
                  "Regálame una rosa #derecho #abogado"):
            self.assertTrue(any("anzuelo" in x for x in errores(pieza(descripcion=d))), d)

    def test_pregunta_real_no_es_anzuelo(self):
        p = pieza(descripcion="¿Tú pagas en efectivo o con el celular? Te leo. #derecho #abogado")
        self.assertFalse(any("anzuelo" in x for x in errores(p)))

    def test_insultos_y_modismos(self):
        self.assertTrue(any("insulto" in x for x in errores(pieza(descripcion="Son unos pendejos #derecho #abogado"))))
        self.assertTrue(any("calificativo" in x for x in avisos(pieza(descripcion="Unos payasos legislando #derecho #abogado"))))
        self.assertTrue(any("güey" in x for x in errores(pieza(descripcion="No manches güey #gym #abogado"))))

    def test_hashtags(self):
        muchos = "Texto #a #b #c #d #e #f"
        self.assertTrue(any("6 hashtags" in x for x in errores(pieza(descripcion=muchos, hashtags=None))))
        self.assertTrue(any("4 hashtags" in x for x in avisos(pieza(descripcion="Texto #a #b #c #d", hashtags=None))))
        self.assertTrue(any("sin efecto demostrado" in x for x in avisos(pieza(descripcion="Texto #fyp #abogado", hashtags=None))))
        self.assertTrue(any("no coincide" in x for x in avisos(pieza(descripcion="Texto #gym #abogado", hashtags=["gym"]))))
        self.assertTrue(any("sin hashtags" in x for x in avisos(pieza(descripcion="Texto sin nada", hashtags=None))))

    def test_descripcion_larga(self):
        self.assertTrue(any("caracteres" in x for x in errores(pieza(descripcion="a" * 2300, hashtags=None))))

    def test_derecho_sin_fuente_oficial(self):
        d = "El artículo 13 de la ley cambia todo #derecho #abogado"
        self.assertTrue(any("fuente oficial" in x for x in errores(pieza(descripcion=d, fuentes=[]))))
        self.assertTrue(any("fuente oficial" in x for x in errores(pieza(descripcion=d, fuentes=["https://blog.ejemplo.com/dof"]))))
        self.assertTrue(any("fuente oficial" in x for x in errores(pieza(descripcion=d, fuentes=["https://dof.gob.mx.falso.com/x"]))))
        self.assertFalse(any("fuente oficial" in x for x in errores(pieza(descripcion=d, fuentes=["https://dof.gob.mx/nota_detalle.php?codigo=1"]))))
        self.assertFalse(any("fuente oficial" in x for x in errores(pieza(descripcion=d, fuentes=["https://www.diputados.gob.mx/LeyesBiblio/x.pdf"]))))

    def test_politica_sin_postura(self):
        self.assertTrue(any("opinion_emi" in x for x in errores(pieza(pilar="politica"))))
        self.assertFalse(any("opinion_emi" in x for x in errores(pieza(pilar="politica", opinion_emi="Mi postura, con mis palabras"))))

    def test_promocion_de_servicio(self):
        p = pieza(descripcion="Contrátame en MILLA Abogados #derecho #abogado")
        self.assertTrue(any("divulgacion_comercial" in x for x in errores(p)))
        p["divulgacion_comercial"] = True
        self.assertTrue(any("biblioteca general" in x for x in errores(p)))  # el ejemplo usa biblioteca-tiktok
        p["musica"] = "original"
        self.assertEqual(errores(p), [])

    def test_ia_realista_obliga_a_redisenar(self):
        for campo in ("persona_realista_ia", "escena_realista_ia", "voz_ia_reconocible"):
            p = pieza()
            p["medios"][campo] = True
            self.assertTrue(any("se rediseña" in x for x in errores(p)), campo)
        p = pieza(etiqueta_ia={"requiere": True, "motivo": "x"})
        self.assertTrue(any("se rediseña" in x for x in errores(p)))
        self.assertTrue(any("motivo" in x for x in avisos(pieza(etiqueta_ia={"requiere": False}))))
        self.assertTrue(any("etiqueta_ia" in x for x in errores(pieza(etiqueta_ia=None))))

    def test_archivo_descargado_y_c2pa(self):
        p = pieza()
        p["medios"]["origen_archivo"] = "descargado"
        self.assertTrue(any("marca de agua" in x for x in errores(p)))
        p = pieza(productora="vox-studio")
        self.assertTrue(any("C2PA" in x for x in avisos(p)))

    def test_musica_invalida(self):
        self.assertTrue(any("música" in x for x in errores(pieza(musica="cancion-de-moda"))))

    def test_duplicados(self):
        d = pieza()["descripcion"]
        self.assertTrue(any("casi igual" in x for x in errores(pieza(), previas=[d])))
        self.assertFalse(any("casi igual" in x for x in errores(pieza(), previas=["Algo totalmente distinto sobre leyes"])))

    def test_dos_puntos_aviso(self):
        self.assertTrue(any("dos puntos" in x for x in avisos(pieza(descripcion="Ojo: esto cambia #gym #abogado"))))
        self.assertFalse(any("dos puntos" in x for x in avisos(pieza(descripcion="A las 5:40 entreno #gym #abogado"))))


class Semana(Aislado):
    def test_separacion_y_topes(self):
        p1 = pieza(id="a", fecha="2099-01-06T19:30:00-06:00")
        p2 = pieza(id="b", fecha="2099-01-07T12:00:00-06:00", descripcion="Otra cosa #gym #abogado")
        e, _ = t.revisar_semana([p1, p2])
        self.assertTrue(any("separación" in x for x in e))
        mismo_dia = [pieza(id="c", fecha="2099-01-06T08:00:00-06:00"), pieza(id="d", fecha="2099-01-06T20:00:00-06:00")]
        self.assertTrue(any("por día" in x for x in t.revisar_semana(mismo_dia)[0]))
        cuatro = [pieza(id=f"s{i}", fecha=f"2099-01-{5 + 2 * i:02d}T10:00:00-06:00") for i in range(4)]  # lun 5 a dom 11
        self.assertTrue(any("por semana" in x for x in t.revisar_semana(cuatro)[0]))

    def test_balance(self):
        ps = [pieza(id=f"x{i}", fecha=f"2099-02-{1 + 3 * i:02d}T10:00:00-06:00") for i in range(4)]  # todo lifestyle
        self.assertTrue(any("pilar lifestyle" in x for x in t.revisar_semana(ps)[1]))

    def test_ejemplo_de_semana_limpio(self):
        codigo, salida = self.correr(["semana", str(t.SKILL / "assets" / "semana.ejemplo.json")])
        self.assertEqual(codigo, 0, salida)


class AprobarEntregar(Aislado):
    def test_aprobar_y_cambio_invalida(self):
        ruta = Path(self.tmp.name) / "p.json"
        ruta.write_text(json.dumps(pieza()), encoding="utf-8")
        codigo, _ = self.correr(["entregar", str(ruta), "tt-2099-01-06-ejemplo"])
        self.assertEqual(codigo, 1)  # sin aprobación no se entrega
        codigo, salida = self.correr(["aprobar", str(ruta), "tt-2099-01-06-ejemplo", "--medio", "chat, prueba"])
        self.assertEqual(codigo, 0, salida)
        codigo, salida = self.correr(["entregar", str(ruta), "tt-2099-01-06-ejemplo"])
        self.assertEqual(codigo, 0, salida)
        self.assertIn("Descripción (copiar tal cual)", salida)
        self.assertIn("Etiqueta de contenido generado con IA: apagada", salida)
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        datos["descripcion"] += " cambio"
        ruta.write_text(json.dumps(datos), encoding="utf-8")
        codigo, salida = self.correr(["entregar", str(ruta), "tt-2099-01-06-ejemplo"])
        self.assertEqual(codigo, 1)
        self.assertIn("cambió después de la aprobación", salida)

    def test_no_aprueba_con_errores_ni_sin_medio(self):
        ruta = Path(self.tmp.name) / "p.json"
        ruta.write_text(json.dumps(pieza(descripcion="Castorena #a #b")), encoding="utf-8")
        self.assertEqual(self.correr(["aprobar", str(ruta), "tt-2099-01-06-ejemplo", "--medio", "x"])[0], 1)
        ruta.write_text(json.dumps(pieza()), encoding="utf-8")
        self.assertEqual(self.correr(["aprobar", str(ruta), "tt-2099-01-06-ejemplo", "--medio", "  "])[0], 1)

    def test_entregar_exige_archivo(self):
        ruta = Path(self.tmp.name) / "p.json"
        ruta.write_text(json.dumps(pieza(archivo="")), encoding="utf-8")
        self.correr(["aprobar", str(ruta), "tt-2099-01-06-ejemplo", "--medio", "chat"])
        codigo, salida = self.correr(["entregar", str(ruta), "tt-2099-01-06-ejemplo"])
        self.assertEqual(codigo, 1)
        self.assertIn("falta «archivo»", salida)


class Registro(Aislado):
    def test_publicado_metricas_estado(self):
        url = "https://www.tiktok.com/@emilianomilla_/video/7300000000000000000"
        codigo, salida = self.correr(["publicado", "--id", "tt-1", "--fecha", "2026-11-19T19:30:00-06:00", "--pilar", "ia-derecho",
                                      "--url", url, "--descripcion", "¿Adiós al efectivo? #derecho #DOF"])
        self.assertEqual(codigo, 0, salida)
        self.assertEqual(self.correr(["publicado", "--id", "tt-1", "--fecha", "2026-11-19T19:30:00-06:00", "--pilar", "ia-derecho",
                                      "--descripcion", "x"])[0], 1)  # duplicado
        self.assertEqual(self.correr(["publicado", "--id", "tt-2", "--fecha", "2026-11-19T19:30:00-06:00", "--pilar", "ia-derecho",
                                      "--url", "https://x.com/a/status/1", "--descripcion", "x"])[0], 1)  # url ajena
        codigo, _ = self.correr(["metricas", "tt-1", "--capturado", "2026-11-26", "vistas=1520", "vio_completo_pct=18.5", "no_elegible=false"])
        self.assertEqual(codigo, 0)
        self.assertEqual(self.correr(["metricas", "tt-1", "--capturado", "2026-11-26", "Vistas=3"])[0], 1)
        estado = json.loads((t.RED / "estado.json").read_text(encoding="utf-8"))
        for campo in ("contrato", "skill", "red", "version_skill", "actualizado", "cuentas", "cadencia", "formatos",
                      "minutos_emi_por_pieza", "publicados", "lecciones", "ideas_para_otras", "pendientes_de_emi", "fuentes"):
            self.assertIn(campo, estado)
        self.assertEqual(estado["contrato"], "redes-estado/0.1.1")
        pub = estado["publicados"][0]
        self.assertEqual(pub["metricas"]["valores"], {"vistas": 1520, "vio_completo_pct": 18.5, "no_elegible": False})
        self.assertEqual(pub["huella_texto"], t.huella_texto("¿Adiós al efectivo? #derecho #DOF"))
        self.assertNotIn("descripcion", pub)
        self.assertIn(estado["cadencia"]["certeza"], ("oficial", "terceros", "criterio"))
        for f in estado["formatos"]:
            self.assertIn(f["certeza"], ("oficial", "terceros", "criterio"))

    def test_aprender_y_vox(self):
        self.assertEqual(self.correr(["aprender", "El", "gancho", "con", "pregunta", "retuvo", "más"])[0], 0)
        self.assertEqual(self.correr(["vox", "idea", "Explicar", "el", "artículo", "16"])[0], 0)
        self.correr(["estado"])
        estado = json.loads((t.RED / "estado.json").read_text(encoding="utf-8"))
        self.assertEqual(estado["lecciones"][0]["texto"], "El gancho con pregunta retuvo más")
        self.assertEqual(estado["ideas_para_otras"][0]["para"], "vox-studio")

    def test_balance_toca(self):
        codigo, salida = self.correr(["balance"])
        self.assertEqual(codigo, 0)
        self.assertIn("Toca: ia-derecho", salida)


class Paginas(unittest.TestCase):
    def test_texto_visible_y_frases(self):
        crudo = '<p>TikTok won&#39;t show</p><script>{"x":"\\u003cstrong\\u003e40 to 50\\u003c/strong\\u003e pixel"}</script><p>it won’t affect the distribution</p>'
        visible = t.texto_visible(crudo)
        self.assertTrue(t.contiene(visible, "40 to 50 pixel"))
        self.assertTrue(t.contiene(visible, "won't affect the distribution"))
        self.assertTrue(t.contiene(visible, "won't show"))
        self.assertFalse(t.contiene(visible, "algo que no está"))

    def test_estado_cuenta(self):
        self.assertEqual(t.estado_cuenta('{"statusCode":10221}', "emilianomilla_"), "no existe")
        self.assertEqual(t.estado_cuenta('{"statusCode":0,"uniqueId":"tiktok"}', "tiktok"), "existe")
        self.assertEqual(t.estado_cuenta("<html></html>", "x"), "no concluyente")

    def test_fuentes_json_valido(self):
        datos = json.loads((t.DATA / "fuentes.json").read_text(encoding="utf-8"))
        ids = [f["id"] for f in datos["fuentes"]]
        self.assertEqual(len(ids), len(set(ids)))
        for f in datos["fuentes"]:
            self.assertTrue(f["url"].startswith("https://"))
            self.assertTrue(f["frases"])
            for fr in f["frases"]:
                self.assertTrue(fr["texto"].strip() and fr["regla"].strip())


if __name__ == "__main__":
    unittest.main()

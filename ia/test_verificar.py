#!/usr/bin/env python3
"""Pruebas de ia/verificar.py. Correr: python3 -m unittest discover -s ia -p 'test_*.py'"""
import re
import unittest

import verificar as v


class Secretos(unittest.TestCase):
    def detecta(self, texto: str) -> bool:
        return any(re.search(p, texto) for p in v.SECRETOS)

    def test_detecta(self):
        # Las muestras se arman al vuelo para que este archivo no dispare el propio escaneo.
        for texto in ("-----BEGIN RSA " + "PRIVATE KEY-----", "sk" + "-" + "a" * 30, "gh" + "p_" + "A1" * 18,
                      "session" + "id=" + "ab12" * 6, "client" + "_secret: " + "Zz9" * 8, "GAME" + "900101" + "HDFRRL09"):
            self.assertTrue(self.detecta(texto), texto)

    def test_no_marca_texto_normal(self):
        for texto in ("La sesión de TikTok nunca se guarda aquí.", "https://www.tiktok.com/@tiktok/video/7300000000000000000",
                      "sha256 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08", "password: nunca se guarda"):
            self.assertFalse(self.detecta(texto), texto)

    def test_edad_de_fuentes(self):
        texto, exceso = v.edad_fuentes()
        self.assertIsInstance(exceso, int)
        self.assertIn("verificadas el", texto)


if __name__ == "__main__":
    unittest.main()

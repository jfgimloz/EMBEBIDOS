#!/usr/bin/env python3
"""Contrato del odómetro Bash completo con entrada CSV preparada."""
from pathlib import Path
import os
import subprocess
import tempfile
import unittest

RAIZ = Path(__file__).resolve().parents[1]
SCRIPTS = (RAIZ / "1_bash/ejercicio/odometro.sh",)




class BashOdometro(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scripts = SCRIPTS
        cls.resuelto = SCRIPTS[0]  # Plantilla completada por el estudiantado.

    def ejecutar(self, script, filas):
        with tempfile.TemporaryDirectory() as temporal:
            entrada = Path(temporal) / "entrada.csv"
            salida = Path(temporal) / "salida.csv"
            entrada.write_text(filas, encoding="utf-8")
            resultado = subprocess.run(
                ["bash", str(script), "--reproducir", str(entrada), "--salida", str(salida)],
                capture_output=True, text=True, timeout=10,
            )
            return resultado, salida.read_text(encoding="utf-8") if salida.exists() else ""

    def test_trayectoria_con_ultima_fila_sin_salto(self):
        for script in self.scripts:
            with self.subTest(script=script):
                r, csv = self.ejecutar(script, "x,y\n0,0\n3,4\n6,8")
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertEqual(r.stdout.strip(), "muestras=3 distancia=10.000")
                self.assertEqual(csv, "x,y\n0,0\n3,4\n6,8\n")

    def test_tramo_no_entero_e_inmovilidad(self):
        for script in self.scripts:
            with self.subTest(script=script):
                r, _ = self.ejecutar(script, "x,y\n0,0\n1,1\n1,1\n")
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertEqual(r.stdout.strip(), "muestras=3 distancia=1.414")

    def test_cien_tramos_no_enteros_sin_perder_precision(self):
        filas = "x,y\n" + "\n".join(f"{i},{i}" for i in range(101)) + "\n"
        for script in self.scripts:
            with self.subTest(script=script):
                r, _ = self.ejecutar(script, filas)
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertEqual(r.stdout.strip(), "muestras=101 distancia=141.421")

    def test_sin_muestras_y_una_muestra(self):
        for script in self.scripts:
            for filas, esperado in (("x,y\n", "muestras=0 distancia=0.000"),
                                    ("x,y\n-5,3\n", "muestras=1 distancia=0.000")):
                with self.subTest(script=script, filas=filas):
                    r, _ = self.ejecutar(script, filas)
                    self.assertEqual(r.returncode, 0, r.stderr)
                    self.assertEqual(r.stdout.strip(), esperado)

    def test_fila_no_valida_se_rechaza(self):
        for script in self.scripts:
            with self.subTest(script=script):
                r, _ = self.ejecutar(script, "x,y\n1,2\n3,z\n")
                self.assertNotEqual(r.returncode, 0)
                self.assertIn("CSV", r.stderr)

    def test_plantilla_resuelta_con_los_tres_pasos_del_enunciado(self):
        r, _ = self.ejecutar(self.resuelto, "x,y\n100,100\n103,104\n100,100\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.strip(), "muestras=3 distancia=10.000")

    def test_bc_con_error_y_estado_cero_no_produce_resumen(self):
        with tempfile.TemporaryDirectory() as temporal:
            carpeta = Path(temporal)
            bc_falso = carpeta / "bc"
            bc_falso.write_text("#!/bin/sh\nprintf 'divide by zero\\n'\n", encoding="utf-8")
            bc_falso.chmod(0o755)
            entrada = carpeta / "entrada.csv"
            entrada.write_text("x,y\n0,0\n1,1\n", encoding="utf-8")
            for script in self.scripts:
                with self.subTest(script=script):
                    r = subprocess.run(
                        ["bash", str(script), "--reproducir", str(entrada),
                         "--salida", str(carpeta / "salida.csv")],
                        capture_output=True, text=True, timeout=10,
                        env={**os.environ, "PATH": f"{carpeta}:{os.environ.get('PATH', '')}"},
                    )
                    self.assertNotEqual(r.returncode, 0)
                    self.assertIn("Cálculo no válido", r.stderr)
                    self.assertNotIn("muestras=", r.stdout)

    def test_dependencias_y_sesion_se_validan_antes_de_truncar(self):
        with tempfile.TemporaryDirectory() as temporal:
            carpeta = Path(temporal)
            entrada = carpeta / "entrada.csv"
            entrada.write_text("0,0\n", encoding="utf-8")
            sin_xdotool = carpeta / "bin"
            sin_xdotool.mkdir()
            (sin_xdotool / "bc").symlink_to(subprocess.run(
                ["bash", "-c", "command -v bc"], capture_output=True, text=True,
                check=True, timeout=10).stdout.strip())
            casos = (
                ({"PATH": str(sin_xdotool)}, [], "Falta xdotool"),
                ({"XDG_SESSION_TYPE": "wayland"}, [], "sesión X11"),
                ({"PATH": str(carpeta / "sin-herramientas")},
                 ["--reproducir", str(entrada)], "Falta bc"),
            )
            for script in self.scripts:
                for entorno, opciones, mensaje in casos:
                    with self.subTest(script=script, mensaje=mensaje):
                        salida = carpeta / "salida.csv"
                        salida.write_text("salida anterior\n", encoding="utf-8")
                        r = subprocess.run(
                            ["/bin/bash", str(script), "--salida", str(salida), *opciones],
                            capture_output=True, text=True, timeout=10,
                            env={**os.environ, "DISPLAY": ":0", "XDG_SESSION_TYPE": "x11",
                                 **entorno},
                        )
                        self.assertNotEqual(r.returncode, 0)
                        self.assertIn(mensaje, r.stderr)
                        self.assertEqual(salida.read_text(), "salida anterior\n")


if __name__ == "__main__":
    unittest.main()

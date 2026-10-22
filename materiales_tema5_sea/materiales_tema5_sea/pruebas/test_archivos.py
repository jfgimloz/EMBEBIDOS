#!/usr/bin/env python3
"""Regresiones de archivos; todas las escrituras se hacen en un temporal."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


RAIZ = Path(__file__).resolve().parents[1]
CLI = str(Path(sys.argv.pop(1)).resolve())
DATOS = "x,y\n100,100\n103,104\n100,100\n"


class Archivos(unittest.TestCase):

    def ejecutar(self, orden):
        return subprocess.run(orden, capture_output=True, text=True, timeout=10)

    def ordenes(self, entrada, salida):
        return [[CLI, '--csv', str(entrada), '--salida', str(salida),
                 '--intervalo-ms', '0', '--silencioso']]

    def test_ultima_fila_sin_salto(self):
        with tempfile.TemporaryDirectory() as temporal:
            entrada = Path(temporal) / "entrada.csv"
            entrada.write_text(DATOS.rstrip("\n"))
            for orden in self.ordenes(entrada, Path(temporal) / "salida.csv")[:3]:
                with self.subTest(programa=orden[0:2]):
                    resultado = self.ejecutar(orden)
                    self.assertEqual(resultado.returncode, 0, resultado.stderr)
                    self.assertIn("muestras=3 distancia=10.000", resultado.stdout)

    def test_no_sobrescribir_entrada_ni_alias(self):
        with tempfile.TemporaryDirectory() as temporal:
            entrada = Path(temporal) / "entrada.csv"
            enlace = Path(temporal) / "enlace.csv"
            entrada.write_text(DATOS)
            enlace.symlink_to(entrada)
            duro = Path(temporal) / "duro.csv"
            os.link(entrada, duro)
            for salida in (entrada, enlace, duro):
                for orden in self.ordenes(entrada, salida):
                    with self.subTest(salida=salida.name, programa=orden[0:2]):
                        entrada.write_text(DATOS)
                        resultado = self.ejecutar(orden)
                        self.assertNotEqual(resultado.returncode, 0)
                        self.assertIn("archivos distintos", resultado.stderr)
                        self.assertEqual(entrada.read_text(), DATOS)

    def test_entrada_ausente_no_trunca_salida(self):
        with tempfile.TemporaryDirectory() as temporal:
            entrada = Path(temporal) / "ausente.csv"
            salida = Path(temporal) / "salida.csv"
            for orden in self.ordenes(entrada, salida):
                with self.subTest(programa=orden[0:2]):
                    salida.write_text("salida anterior\n")
                    resultado = self.ejecutar(orden)
                    self.assertNotEqual(resultado.returncode, 0)
                    self.assertEqual(salida.read_text(), "salida anterior\n")


    @unittest.skipUnless(Path("/dev/full").exists(), "requiere /dev/full")
    def test_cli_rechaza_fallo_de_escritura_y_cierre(self):
        with tempfile.TemporaryDirectory() as temporal:
            entrada = Path(temporal) / "entrada.csv"
            # Una salida pequeña falla al vaciar el buffer en fclose; una larga,
            # durante fprintf. Ambas deben impedir el resumen de éxito.
            for filas in (DATOS, "x,y\n" + "0,0\n" * 1000):
                with self.subTest(muestras=filas.count("\n") - 1):
                    entrada.write_text(filas)
                    resultado = self.ejecutar(self.ordenes(entrada, Path("/dev/full"))[0])
                    self.assertNotEqual(resultado.returncode, 0)
                    self.assertIn("/dev/full", resultado.stderr)
                    self.assertNotIn("muestras=", resultado.stdout)

    def test_paridad_csv_valido(self):
        casos = (
            ("x,y\r\n# comentario\r\n \r\n +0 , 00 \r\n3,4\r\n6,8", 3, "10.000"),
            ("X,Y\n0,0\n  # comentario\n3,4\n6,8\n", 3, "10.000"),
            ("\n\t \n# comentario\n", 0, "0.000"),
            ("-2147483648,2147483647\n", 1, "0.000"),
            ("2147483647,-2147483648\n", 1, "0.000"),
            ("0002147483647,-0002147483648\n", 1, "0.000"),
        )
        with tempfile.TemporaryDirectory() as temporal:
            entrada = Path(temporal) / "entrada.csv"
            for filas, muestras, distancia in casos:
                entrada.write_text(filas)
                for orden in self.ordenes(entrada, Path(temporal) / "salida.csv"):
                    with self.subTest(programa=orden[0:2], filas=filas):
                        resultado = self.ejecutar(orden)
                        self.assertEqual(resultado.returncode, 0, resultado.stderr)
                        self.assertEqual(resultado.stdout.strip(),
                                         f"muestras={muestras} distancia={distancia}")

    def test_paridad_csv_invalido(self):
        filas_invalidas = (
            "1,2,", "1,2,3", "1,,2", ",2", "1,", "1.0,2", "0x1,2",
            "x,z", "X,y", "x,Y", " x,y", "x,y ",
            "x,y\nx,y", "\nx,y", "# comentario\nX,Y",
            "2147483648,0", "0,-2147483649", "999999999999999999999999,0",
            "-999999999999999999999999,0", "0002147483648,0",
        )
        with tempfile.TemporaryDirectory() as temporal:
            entrada = Path(temporal) / "entrada.csv"
            for filas in filas_invalidas:
                entrada.write_text(filas + "\n")
                for orden in self.ordenes(entrada, Path(temporal) / "salida.csv"):
                    with self.subTest(programa=orden[0:2], filas=filas):
                        resultado = self.ejecutar(orden)
                        self.assertNotEqual(resultado.returncode, 0)
                        self.assertIn("CSV", resultado.stderr)
                        self.assertNotIn("muestras=", resultado.stdout)


if __name__ == "__main__":
    unittest.main()

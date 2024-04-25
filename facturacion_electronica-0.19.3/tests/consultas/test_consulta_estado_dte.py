# -#- coding: utf-8 -#-
from facturacion_electronica import facturacion_electronica as fe
from facturacion_electronica.firma import Firma
import json
from lxml import etree
import unittest

token_no_existe = 'TOKEN NO EXISTE'

def limpiar_errores(errores, glosa):
    for x in [
            "No hay Token en consulta DTE",
            "('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))",
            "No hay Token en consulta cesion DTE relac",
            "No hay Token en consulta DTE",
            ]:
        if x in errores :
            glosa = token_no_existe
            errores.remove(x)
    return glosa

class TestEjemploEstadoDTE(unittest.TestCase):
    """
    Test Consulta estado DTE
    """
    def test_consulta_certificado_vencido(self):
        """
        Test Consulta de estado DTE con certificado vencido
        """
        print("Se inicia test consulta estado DTE")
        f = open("facturacion_electronica/ejemplos/ejemplo_estado_documento.json")
        txt_json = f.read()
        f.close()
        ejemplo = json.loads(txt_json)
        firma_electronica = ejemplo['firma_electronica'].copy()
        result = fe.consulta_estado_dte(ejemplo)
        self.assertEqual(len(result), 2)
        for k, v in result.items():
            errores = v.get('errores', [])
            glosa = limpiar_errores(errores, v.get('glosa', False))
            self.assertFalse(errores)
            self.assertEqual((glosa or '').upper(), token_no_existe)

    """
    Test Consulta estado cesión DTE relac
    """
    def test_consulta_cesion_dte_relac_certificado_vencido(self):
        """
        Test Consulta de estado cesion DTE relac con certificado vencido
        """
        print("Se inicia test consulta estado cesion DTE relac")
        f = open("facturacion_electronica/ejemplos/ejemplo_estado_documento_cesion.json")
        txt_json = f.read()
        f.close()
        ejemplo = json.loads(txt_json)
        firma_electronica = ejemplo['firma_electronica'].copy()
        result = fe.consulta_estado_cesion_relac(ejemplo)
        self.assertEqual(len(result), 2)
        for k, v in result.items():
            errores = v.get('errores', [])
            glosa = limpiar_errores(errores, v.get('glosa', False))
            self.assertFalse(errores)
            self.assertEqual((glosa or '').upper(), token_no_existe)

    """
    Test Consulta estado cesión DTE
    """
    def test_consulta_cesion_dte_certificado_vencido(self):
        """
        Test Consulta de estado cesion DTE con certificado vencido
        """
        print("Se inicia test consulta estado cesion DTE")
        f = open("facturacion_electronica/ejemplos/ejemplo_estado_documento_cesion.json")
        txt_json = f.read()
        f.close()
        ejemplo = json.loads(txt_json)
        firma_electronica = ejemplo['firma_electronica'].copy()
        result = fe.consulta_estado_dte(ejemplo)
        self.assertEqual(len(result), 2)
        for k, v in result.items():
            errores = v.get('errores', [])
            glosa = limpiar_errores(errores, v.get('glosa', False))
            self.assertFalse(errores)
            self.assertEqual((glosa or '').upper(), token_no_existe)


if __name__ == '__main__':
    unittest.main()

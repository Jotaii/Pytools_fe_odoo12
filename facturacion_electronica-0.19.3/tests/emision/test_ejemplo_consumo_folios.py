# -#- coding: utf-8 -#-
from facturacion_electronica import facturacion_electronica as fe
from facturacion_electronica.firma import Firma
import json
from lxml import etree
import unittest


def verificar_firma_xml(firma_electronica, xml):
    firma = Firma(firma_electronica)
    result = firma.verificar_firma_xml(xml)
    return result


class TestEjemploConsumoFolios(unittest.TestCase):

    """
        Test Consumo Folios
    """
    def test_timbrar_y_enviar(self):
        """
        Test Correcto Consumo Folios
        """
        print("Se inicia test básico consumo folios")
        f = open("facturacion_electronica/ejemplos/ejemplo_consumo_folios_resumen.json")
        txt_json = f.read()
        f.close()
        ejemplo = json.loads(txt_json)
        firma_electronica = ejemplo['firma_electronica'].copy()
        result = fe.consumo_folios(ejemplo)
        self.assertFalse(result[0].get('errores', False))
        self.assertTrue(result[0].get('sii_xml_request', False))
        """
            verificar firma Envio
        """
        result_firma = verificar_firma_xml(
            firma_electronica.copy(),
            result[0]['sii_xml_request'])
        self.assertEqual((0,''), result_firma)
        """
            Verifico Integridad XML
        """
        xml = etree.fromstring(
            result[0]['sii_xml_request'].replace('xmlns="http://www.sii.cl/SiiDte"',
                                             '').encode('ISO-8859-1'))
        query = "SetDTE/Caratula/SubTotDTE"




if __name__ == '__main__':
    unittest.main()

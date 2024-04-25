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

class TestEjemploCesion(unittest.TestCase):
    """
        Test Ejemplo Cesion
    """
    def test_timbrar_y_enviar(self):
        """
        Test Correcto Cesion
        """
        print("Se inicia test Cesion")
        f = open("facturacion_electronica/ejemplos/ejemplo_cesion_de_creditos.json")
        txt_json = f.read()
        f.close()
        ejemplo = json.loads(txt_json)
        firma_electronica = ejemplo['firma_electronica'].copy()
        result = fe.timbrar_y_enviar_cesion(ejemplo)
        self.assertFalse(result.get('errores', False))
        self.assertTrue(result.get('sii_xml_request', False))
        """
            verificar firma Envio
        """
        result_firma = verificar_firma_xml(
            firma_electronica.copy(),
            result['sii_xml_request'])
        self.assertEqual((0,''), result_firma)
        """
            Verifico Integridad XML
        """
        xml = etree.fromstring(
            result['sii_xml_request'].replace('xmlns="http://www.sii.cl/SiiDte"',
                                             '').encode('ISO-8859-1'))
        self.assertIsNotNone(xml.find('DocumentoAEC'))
        query = "DocumentoAEC/Cesiones"
        Cesiones = xml.findall(query)
        self.assertEqual(len(Cesiones), 1)
        for Cesion in Cesiones:
            """
                Verifico cantidades en carátula
            """
            self.assertIsNotNone(Cesion.find('DTECedido'))
            DocumentoDTECedido = Cesion.find('DTECedido/DocumentoDTECedido')
            self.assertIsNotNone(DocumentoDTECedido)
            self.assertIsNotNone(Cesion.find('Cesion'))
            DocumentoCesion = Cesion.find('Cesion/DocumentoCesion')
            self.assertIsNotNone(DocumentoCesion)
            self.assertEqual(DocumentoCesion.find("IdDTE/Folio").text, "41")

if __name__ == '__main__':
    unittest.main()

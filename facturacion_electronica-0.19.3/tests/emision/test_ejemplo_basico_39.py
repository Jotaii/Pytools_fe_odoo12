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

class TestEjemploBasico39(unittest.TestCase):
    """
    Test Set Básico 39
    """
    def test_timbrar_y_enviar(self):
        """
        Test Set Básico 39
        """
        print("Se inicia test básico 39")
        f = open("facturacion_electronica/ejemplos/ejemplo_basico_39.json")
        txt_json = f.read()
        f.close()
        ejemplo_33 = json.loads(txt_json)
        firma_electronica = ejemplo_33['firma_electronica'].copy()
        result = fe.timbrar_y_enviar(ejemplo_33)
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
        query = "SetDTE/Caratula/SubTotDTE"
        SubTotDTEs = xml.findall(query)
        self.assertEqual(len(SubTotDTEs), 1)
        for SubTotDTE in SubTotDTEs:
            """
                Verifico cantidades en carátula
            """
            if SubTotDTE.find("TpoDTE").text == '39':
                self.assertEqual(
                    SubTotDTE.find("NroDTE").text, "2")
        query = "SetDTE/DTE"
        DTEs = xml.findall(query)
        self.assertEqual(len(DTEs), 2)
        self.assertEqual(len(result.get('detalles', [])), 2)
        for dte in result['detalles']:
            """
                Verifico DTE individuales
            """
            self.assertTrue(dte.get('NroDTE'))
            self.assertTrue(dte.get('sii_barcode_img'))
            self.assertTrue(dte.get('sii_xml_dte'))
            string_xml_dte = '<?xml version="1.0" encoding="ISO-8859-1"?>' + \
                                dte['sii_xml_dte']
            """
                Verifico Firma DTE
            """
            result_firma = verificar_firma_xml(
                firma_electronica.copy(),
                string_xml_dte)
            self.assertEqual((0,''), result_firma)
            xml_dte = etree.fromstring(
                string_xml_dte.replace('xmlns="http://www.sii.cl/SiiDte"',
                                             '').encode('ISO-8859-1'))
            Receptor = xml_dte.find('Documento/Encabezado/Receptor')
            self.assertEqual(Receptor.find("RUTRecep").text, "66666666-6")
            IdDoc = xml_dte.find('Documento/Encabezado/IdDoc')
            Totales = xml_dte.find('Documento/Encabezado/Totales')
            if dte['NroDTE'] == 1:
                self.assertEqual(dte['TipoDTE'], 39)
                self.assertEqual(IdDoc.find('TipoDTE').text, '39')
                self.assertEqual(dte['Folio'], 37)
                self.assertEqual(IdDoc.find('Folio').text, '37')
                self.assertEqual(dte['MntExe'], 0)
                self.assertIsNone(Totales.find('MntExe'))
                self.assertEqual(dte['MntNeto'], 105042)
                self.assertEqual(Totales.find('MntNeto').text, '105042')
                self.assertEqual(dte['MntIVA'], 19958)
                self.assertEqual(Totales.find('IVA').text, '19958')
                self.assertEqual(dte['MntTotal'], 125000)
                self.assertEqual(Totales.find('MntTotal').text, '125000')
                self.assertEqual(dte['ImptoReten'], 0)
                self.assertIsNone(Totales.find('ImptoReten'))
            elif dte['NroDTE'] == 2:
                self.assertEqual(dte['TipoDTE'], 39)
                self.assertEqual(IdDoc.find('TipoDTE').text, '39')
                self.assertEqual(dte['Folio'], 38)
                self.assertEqual(IdDoc.find('Folio').text, '38')
                self.assertEqual(dte['MntExe'], 250000)
                self.assertEqual(Totales.find('MntExe').text, '250000')
                self.assertEqual(dte['MntNeto'], 315126)
                self.assertEqual(Totales.find('MntNeto').text, '315126')
                self.assertEqual(dte['MntIVA'], 59874)
                self.assertEqual(Totales.find('IVA').text, '59874')
                self.assertEqual(dte['MntTotal'], 625000)
                self.assertEqual(Totales.find('MntTotal').text, '625000')
                self.assertEqual(dte['ImptoReten'], 0)
                self.assertIsNone(Totales.find('ImptoReten'))

if __name__ == '__main__':
    unittest.main()

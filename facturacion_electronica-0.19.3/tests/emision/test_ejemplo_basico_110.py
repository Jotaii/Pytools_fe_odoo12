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

class TestEjemploBasico110(unittest.TestCase):
    """
    Test Correcto Set Básico 110 Factura Exportación
    """
    def test_timbrar_y_enviar(self):
        """
        Test Correcto Set Básico 110 Factura Exportación
        """
        print("Se inicia test básico correcto 110")
        f = open("facturacion_electronica/ejemplos/ejemplo_basico_110.json")
        txt_json = f.read()
        f.close()
        ejemplo = json.loads(txt_json)
        firma_electronica = ejemplo['firma_electronica'].copy()
        result = fe.timbrar_y_enviar(ejemplo)
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
        self.assertEqual(len(SubTotDTEs), 3)
        for SubTotDTE in SubTotDTEs:
            """
                Verifico cantidades en carátula
            """
            if SubTotDTE.find("TpoDTE").text == '110':
                self.assertEqual(
                    SubTotDTE.find("NroDTE").text, "1")
            if SubTotDTE.find("TpoDTE").text == '111':
                self.assertEqual(
                    SubTotDTE.find("NroDTE").text, "1")
            if SubTotDTE.find("TpoDTE").text == '112':
                self.assertEqual(
                    SubTotDTE.find("NroDTE").text, "1")
        query = "SetDTE/DTE"
        DTEs = xml.findall(query)
        self.assertEqual(len(DTEs), 3)
        self.assertEqual(len(result.get('detalles', [])), 3)
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
            Receptor = xml_dte.find('Exportaciones/Encabezado/Receptor')
            self.assertEqual(Receptor.find("RUTRecep").text, "55555555-5")
            IdDoc = xml_dte.find('Exportaciones/Encabezado/IdDoc')
            Totales = xml_dte.find('Exportaciones/Encabezado/Totales')
            OtraMoneda = xml_dte.findall('Exportaciones/Encabezado/OtraMoneda')
            self.assertEqual(len(OtraMoneda), 1)
            self.assertEqual(OtraMoneda[0].find('TpoMoneda').text, 'PESO CL')
            self.assertEqual(len(OtraMoneda[0]), 4)
            if dte['NroDTE'] == 1:
                self.assertEqual(Totales.find('TpoMoneda').text, 'DOLAR USA')
                self.assertEqual(OtraMoneda[0].find('TpoCambio').text, '500.0')
                self.assertEqual(dte['TipoDTE'], 110)
                self.assertEqual(IdDoc.find('TipoDTE').text, '110')
                self.assertEqual(dte['Folio'], 1)
                self.assertEqual(IdDoc.find('Folio').text, '1')
                self.assertEqual(dte['MntExe'], 187012)
                self.assertEqual(Totales.find('MntExe').text, '187012')
                self.assertEqual(OtraMoneda[0].find('MntExeOtrMnda').text, '93506075')
                self.assertEqual(dte['MntNeto'], 0)
                self.assertIsNone(Totales.find('MntNeto'))
                self.assertEqual(dte['MntIVA'], 0)
                self.assertIsNone(Totales.find('IVA'))
                self.assertEqual(dte['MntTotal'], 187012)
                self.assertEqual(Totales.find('MntTotal').text, '187012')
                self.assertEqual(OtraMoneda[0].find('MntTotOtrMnda').text, '93506075')
                self.assertEqual(dte['ImptoReten'], 0)
                self.assertIsNone(Totales.find('ImptoReten'))
            elif dte['NroDTE'] == 2:
                self.assertEqual(Totales.find('TpoMoneda').text, 'YEN')
                self.assertEqual(OtraMoneda[0].find('TpoCambio').text, '600.0')
                self.assertEqual(dte['TipoDTE'], 112)
                self.assertEqual(IdDoc.find('TipoDTE').text, '112')
                self.assertEqual(dte['Folio'], 1)
                self.assertEqual(IdDoc.find('Folio').text, '1')
                self.assertEqual(dte['MntExe'], 59520)
                self.assertEqual(Totales.find('MntExe').text, '59520')
                self.assertEqual(OtraMoneda[0].find('MntExeOtrMnda').text, '35712000')
                self.assertEqual(dte['MntNeto'], 0)
                self.assertIsNone(Totales.find('MntNeto'))
                self.assertEqual(dte['MntIVA'], 0)
                self.assertIsNone(Totales.find('IVA'))
                self.assertEqual(dte['MntTotal'], 59520)
                self.assertEqual(Totales.find('MntTotal').text, '59520')
                self.assertEqual(OtraMoneda[0].find('MntTotOtrMnda').text, '35712000')
                self.assertEqual(dte['ImptoReten'], 0)
                self.assertIsNone(Totales.find('ImptoReten'))
            elif dte['NroDTE'] == 3:
                self.assertEqual(Totales.find('TpoMoneda').text, 'YEN')
                self.assertEqual(OtraMoneda[0].find('TpoCambio').text, '700.0')
                self.assertEqual(dte['TipoDTE'], 111)
                self.assertEqual(IdDoc.find('TipoDTE').text, '111')
                self.assertEqual(dte['Folio'], 1)
                self.assertEqual(IdDoc.find('Folio').text, '1')
                self.assertEqual(dte['MntExe'], 59520)
                self.assertEqual(Totales.find('MntExe').text, '59520')
                self.assertEqual(OtraMoneda[0].find('MntExeOtrMnda').text, '41664000')
                self.assertEqual(dte['MntNeto'], 0)
                self.assertIsNone(Totales.find('MntNeto'))
                self.assertEqual(dte['MntIVA'], 0)
                self.assertIsNone(Totales.find('IVA'))
                self.assertEqual(dte['MntTotal'], 59520)
                self.assertEqual(Totales.find('MntTotal').text, '59520')
                self.assertEqual(OtraMoneda[0].find('MntTotOtrMnda').text, '41664000')
                self.assertEqual(dte['ImptoReten'], 0)
                self.assertIsNone(Totales.find('ImptoReten'))


if __name__ == '__main__':
    unittest.main()

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

class TestEjemploBasico46(unittest.TestCase):
    """
        Test Set Básico 46 Factura Compras
    """
    def test_timbrar_y_enviar(self):
        """
        Test Correcto Set Básico 46 Factura Compras
        """
        print("Se inicia test básico correcto 46")
        f = open("facturacion_electronica/ejemplos/ejemplo_basico_46.json")
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
            if SubTotDTE.find("TpoDTE").text == '46':
                self.assertEqual(
                    SubTotDTE.find("NroDTE").text, "2")
            elif SubTotDTE.find("TpoDTE").text == '61':
                self.assertEqual(
                    SubTotDTE.find("NroDTE").text, "1")
            elif SubTotDTE.find("TpoDTE").text == '56':
                self.assertEqual(
                    SubTotDTE.find("NroDTE").text, "1")
        query = "SetDTE/DTE"
        DTEs = xml.findall(query)
        self.assertEqual(len(DTEs), 4)
        self.assertEqual(len(result.get('detalles', [])), 4)
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
            self.assertEqual(Receptor.find("RUTRecep").text, "16291998-9")
            IdDoc = xml_dte.find('Documento/Encabezado/IdDoc')
            Totales = xml_dte.find('Documento/Encabezado/Totales')
            if dte['NroDTE'] == 1:
                self.assertEqual(dte['TipoDTE'], 46)
                self.assertEqual(IdDoc.find('TipoDTE').text, '46')
                self.assertEqual(dte['Folio'], 1)
                self.assertEqual(IdDoc.find('Folio').text, '1')
                self.assertEqual(dte['MntExe'], 0)
                self.assertIsNone(Totales.find('MntExe'))
                self.assertEqual(dte['MntNeto'], 6659079)
                self.assertEqual(Totales.find('MntNeto').text, '6659079')
                self.assertEqual(dte['MntIVA'], 1265225)
                self.assertEqual(Totales.find('IVA').text, '1265225')
                self.assertEqual(dte['MntTotal'], 6659079)
                self.assertEqual(Totales.find('MntTotal').text, '6659079')
                self.assertEqual(dte['ImptoReten'], -1265225)
                ImptoReten = Totales.findall('ImptoReten/MontoImp')
                self.assertEqual(len(ImptoReten), 1)
                self.assertEqual(ImptoReten[0].text, "1265225")
            elif dte['NroDTE'] == 2:
                self.assertEqual(dte['TipoDTE'], 46)
                self.assertEqual(IdDoc.find('TipoDTE').text, '46')
                self.assertEqual(dte['Folio'], 2)
                self.assertEqual(IdDoc.find('Folio').text, '2')
                self.assertEqual(dte['MntExe'], 0)
                self.assertIsNone(Totales.find('MntExe'))
                self.assertEqual(dte['MntNeto'], 10550)
                self.assertEqual(Totales.find('MntNeto').text, '10550')
                self.assertEqual(dte['MntIVA'], 2005)
                self.assertEqual(Totales.find('IVA').text, '2005')
                self.assertEqual(dte['MntTotal'], 10550)
                self.assertEqual(Totales.find('MntTotal').text, '10550')
                self.assertEqual(dte['ImptoReten'], -2005)
                ImptoReten = Totales.findall('ImptoReten/MontoImp')
                self.assertEqual(len(ImptoReten), 1)
                self.assertEqual(ImptoReten[0].text, "2005")
            elif dte['NroDTE'] == 3:
                self.assertEqual(dte['TipoDTE'], 61)
                self.assertEqual(IdDoc.find('TipoDTE').text, '61')
                self.assertEqual(dte['Folio'], 22)
                self.assertEqual(IdDoc.find('Folio').text, '22')
                self.assertEqual(dte['MntExe'], 0)
                self.assertIsNone(Totales.find('MntExe'))
                self.assertEqual(dte['MntNeto'], 2220751)
                self.assertEqual(Totales.find('MntNeto').text, '2220751')
                self.assertEqual(dte['MntIVA'], 421943)
                self.assertEqual(Totales.find('IVA').text, '421943')
                self.assertEqual(dte['MntTotal'], 2220751)
                self.assertEqual(Totales.find('MntTotal').text, '2220751')
                self.assertEqual(dte['ImptoReten'], -421943)
                ImptoReten = Totales.findall('ImptoReten/MontoImp')
                self.assertEqual(len(ImptoReten), 1)
                self.assertEqual(ImptoReten[0].text, "421943")
            elif dte['NroDTE'] == 4:
                self.assertEqual(dte['TipoDTE'], 56)
                self.assertEqual(IdDoc.find('TipoDTE').text, '56')
                self.assertEqual(dte['Folio'], 8)
                self.assertEqual(IdDoc.find('Folio').text, '8')
                self.assertEqual(dte['MntExe'], 0)
                self.assertIsNone(Totales.find('MntExe'))
                self.assertEqual(dte['MntNeto'], 2220751)
                self.assertEqual(Totales.find('MntNeto').text, '2220751')
                self.assertEqual(dte['MntIVA'], 421943)
                self.assertEqual(Totales.find('IVA').text, '421943')
                self.assertEqual(dte['MntTotal'], 2220751)
                self.assertEqual(Totales.find('MntTotal').text, '2220751')
                self.assertEqual(dte['ImptoReten'], -421943)
                ImptoReten = Totales.findall('ImptoReten/MontoImp')
                self.assertEqual(len(ImptoReten), 1)
                self.assertEqual(ImptoReten[0].text, "421943")


if __name__ == '__main__':
    unittest.main()

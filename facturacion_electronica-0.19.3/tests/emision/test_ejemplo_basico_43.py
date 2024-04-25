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

def _cabezera_NroDTE1(self, dte, IdDoc, Totales):
    self.assertEqual(dte['TipoDTE'], 43)
    self.assertEqual(IdDoc.find('TipoDTE').text, '43')
    self.assertEqual(dte['Folio'], 1)
    self.assertEqual(IdDoc.find('Folio').text, '1')
    self.assertEqual(dte['MntExe'], 180844)
    self.assertEqual(Totales.find('MntExe').text, "180844")
    self.assertEqual(dte['MntNeto'], 506765)
    self.assertEqual(Totales.find('MntNeto').text, '506765')
    self.assertEqual(dte['MntIVA'], 96285)
    self.assertEqual(Totales.find('IVA').text, '96285')
    self.assertEqual(dte['MntTotal'], 783894)
    self.assertEqual(Totales.find('MntTotal').text, '783894')
    self.assertEqual(dte['ImptoReten'], 0)
    self.assertIsNone(Totales.find('ImptoReten'))
    self.assertIsNone(Totales.find('Comisiones/ValComExe'))
    self.assertIsNone(Totales.find('Comisiones/ValComNet'))
    self.assertIsNone(Totales.find('Comisiones/ValComIVA'))

class TestEjemploBasico43(unittest.TestCase):

    """
        Test Set Básico 43 Liqudación Factura
    """
    def test_timbrar_y_enviar(self):
        """
        Test Correcto Set Básico 43 Liquidación Factura
        """
        print("Se inicia test básico correcto 43")
        f = open("facturacion_electronica/ejemplos/ejemplo_basico_43.json")
        txt_json = f.read()
        f.close()
        ejemplo = json.loads(txt_json)
        firma_electronica = ejemplo['firma_electronica'].copy()
        result = fe.timbrar_y_enviar(ejemplo)
        #print(result)
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
            if SubTotDTE.find("TpoDTE").text == '43':
                self.assertEqual(
                    SubTotDTE.find("NroDTE").text, "4")
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
            Receptor = xml_dte.find('Liquidacion/Encabezado/Receptor')
            self.assertEqual(Receptor.find("RUTRecep").text, "16291998-9")
            IdDoc = xml_dte.find('Liquidacion/Encabezado/IdDoc')
            Totales = xml_dte.find('Liquidacion/Encabezado/Totales')
            Referencia = xml_dte.findall('Liquidacion/Referencia')
            if dte['NroDTE'] == 1:
                _cabezera_NroDTE1(self, dte, IdDoc, Totales)
            elif dte['NroDTE'] == 2:
                self.assertEqual(dte['TipoDTE'], 43)
                self.assertEqual(IdDoc.find('TipoDTE').text, '43')
                self.assertEqual(dte['Folio'], 2)
                self.assertEqual(IdDoc.find('Folio').text, '2')
                self.assertEqual(dte['MntExe'], 241411)
                self.assertEqual(Totales.find('MntExe').text, "241411")
                self.assertEqual(dte['MntNeto'], 4391558)
                self.assertEqual(Totales.find('MntNeto').text, '4391558')
                self.assertEqual(dte['MntIVA'], 834396)
                self.assertEqual(Totales.find('IVA').text, '834396')
                self.assertEqual(dte['MntTotal'], 5467365)
                self.assertEqual(Totales.find('MntTotal').text, '5467365')
                self.assertEqual(dte['ImptoReten'], 0)
                self.assertIsNone(Totales.find('ImptoReten'))
                self.assertIsNone(Totales.find('ImptoReten'))
                self.assertIsNone(Totales.find('Comisiones/ValComExe'))
                self.assertIsNone(Totales.find('Comisiones/ValComNet'))
                self.assertIsNone(Totales.find('Comisiones/ValComIVA'))
            elif dte['NroDTE'] == 3:
                self.assertEqual(dte['TipoDTE'], 43)
                self.assertEqual(IdDoc.find('TipoDTE').text, '43')
                self.assertEqual(dte['Folio'], 3)
                self.assertEqual(IdDoc.find('Folio').text, '3')
                self.assertEqual(dte['MntExe'], 77353)
                self.assertEqual(Totales.find('MntExe').text, '77353')
                self.assertEqual(dte['MntNeto'], 341244)
                self.assertEqual(Totales.find('MntNeto').text, '341244')
                self.assertEqual(dte['MntIVA'], 64836)
                self.assertEqual(Totales.find('IVA').text, '64836')
                self.assertIsNone(Totales.find('Comisiones/ValComExe'))
                self.assertEqual(Totales.find('Comisiones/ValComNeto').text, '6927')
                self.assertEqual(Totales.find('Comisiones/ValComIVA').text, '1316')
                self.assertEqual(dte['MntTotal'], 475190)
                self.assertEqual(Totales.find('MntTotal').text, '475190')
                self.assertEqual(dte['ImptoReten'], 0)
                self.assertIsNone(Totales.find('ImptoReten'))
                for c in xml_dte.findall('Liquidacion/Comisiones'):
                    if c.find("NroLinCom").text == "2":
                        self.assertEqual(c.find("TasaComision").text, "1.42")
            elif dte['NroDTE'] == 4:
                self.assertEqual(dte['TipoDTE'], 43)
                self.assertEqual(IdDoc.find('TipoDTE').text, '43')
                self.assertEqual(dte['Folio'], 4)
                self.assertEqual(IdDoc.find('Folio').text, '4')
                self.assertEqual(dte['MntExe'], 1098416)
                self.assertEqual(Totales.find('MntExe').text, '1098416')
                self.assertEqual(dte['MntNeto'], 694760)
                self.assertEqual(Totales.find('MntNeto').text, '694760')
                self.assertEqual(dte['MntIVA'], 132004)
                self.assertEqual(Totales.find('IVA').text, '132004')
                self.assertIsNone(Totales.find('Comisiones/ValComExe'))
                self.assertEqual(Totales.find('Comisiones/ValComNeto').text, '-3301')
                self.assertEqual(Totales.find('Comisiones/ValComIVA').text, '-627')
                self.assertEqual(dte['MntTotal'], 1929108)
                self.assertEqual(Totales.find('MntTotal').text, '1929108')
                self.assertEqual(dte['ImptoReten'], 0)
                self.assertIsNone(Totales.find('ImptoReten'))


if __name__ == '__main__':
    unittest.main()

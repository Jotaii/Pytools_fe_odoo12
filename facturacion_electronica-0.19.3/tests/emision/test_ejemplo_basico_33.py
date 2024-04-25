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
    self.assertEqual(dte['TipoDTE'], 33)
    self.assertEqual(IdDoc.find('TipoDTE').text, '33')
    self.assertEqual(dte['Folio'], 41)
    self.assertEqual(IdDoc.find('Folio').text, '41')
    self.assertEqual(dte['MntExe'], 0)
    self.assertIsNone(Totales.find('MntExe'))
    self.assertEqual(dte['MntNeto'], 1085752)
    self.assertEqual(Totales.find('MntNeto').text, '1085752')
    self.assertEqual(dte['MntIVA'], 206293)
    self.assertEqual(Totales.find('IVA').text, '206293')
    self.assertEqual(dte['MntTotal'], 1292045)
    self.assertEqual(Totales.find('MntTotal').text, '1292045')
    self.assertEqual(dte['ImptoReten'], 0)
    self.assertIsNone(Totales.find('ImptoReten'))

class TestEjemploBasico33(unittest.TestCase):

    """
        Test Set Básico 33 Factura Afecta
    """
    def test_timbrar_y_enviar(self):
        """
        Test Correcto Set Básico 33 Factura Afecta
        """
        print("Se inicia test básico correcto 33")
        f = open("facturacion_electronica/ejemplos/ejemplo_basico_33.json")
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
            if SubTotDTE.find("TpoDTE").text == '33':
                self.assertEqual(
                    SubTotDTE.find("NroDTE").text, "4")
            elif SubTotDTE.find("TpoDTE").text == '61':
                self.assertEqual(
                    SubTotDTE.find("NroDTE").text, "3")
            elif SubTotDTE.find("TpoDTE").text == '56':
                self.assertEqual(
                    SubTotDTE.find("NroDTE").text, "1")
        query = "SetDTE/DTE"
        DTEs = xml.findall(query)
        self.assertEqual(len(DTEs), 8)
        self.assertEqual(len(result.get('detalles', [])), 8)
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
            Referencia = xml_dte.findall('Documento/Referencia')
            if dte['NroDTE'] == 1:
                _cabezera_NroDTE1(self, dte, IdDoc, Totales)
            elif dte['NroDTE'] == 2:
                self.assertEqual(dte['TipoDTE'], 33)
                self.assertEqual(IdDoc.find('TipoDTE').text, '33')
                self.assertEqual(dte['Folio'], 42)
                self.assertEqual(IdDoc.find('Folio').text, '42')
                self.assertEqual(dte['MntExe'], 0)
                self.assertIsNone(Totales.find('MntExe'))
                self.assertEqual(dte['MntNeto'], 7519476)
                self.assertEqual(Totales.find('MntNeto').text, '7519476')
                self.assertEqual(dte['MntIVA'], 1428700)
                self.assertEqual(Totales.find('IVA').text, '1428700')
                self.assertEqual(dte['MntTotal'], 8948176)
                self.assertEqual(Totales.find('MntTotal').text, '8948176')
                self.assertEqual(dte['ImptoReten'], 0)
                self.assertIsNone(Totales.find('ImptoReten'))
            elif dte['NroDTE'] == 3:
                self.assertEqual(dte['TipoDTE'], 33)
                self.assertEqual(IdDoc.find('TipoDTE').text, '33')
                self.assertEqual(dte['Folio'], 43)
                self.assertEqual(IdDoc.find('Folio').text, '43')
                self.assertEqual(dte['MntExe'], 35344)
                self.assertEqual(Totales.find('MntExe').text, '35344')
                self.assertEqual(dte['MntNeto'], 1510824)
                self.assertEqual(Totales.find('MntNeto').text, '1510824')
                self.assertEqual(dte['MntIVA'], 287057)
                self.assertEqual(Totales.find('IVA').text, '287057')
                self.assertEqual(dte['MntTotal'], 1833225)
                self.assertEqual(Totales.find('MntTotal').text, '1833225')
                self.assertEqual(dte['ImptoReten'], 0)
                self.assertIsNone(Totales.find('ImptoReten'))
            elif dte['NroDTE'] == 4:
                self.assertEqual(dte['TipoDTE'], 33)
                self.assertEqual(IdDoc.find('TipoDTE').text, '33')
                self.assertEqual(dte['Folio'], 44)
                self.assertEqual(IdDoc.find('Folio').text, '44')
                self.assertEqual(dte['MntExe'], 13678)
                self.assertEqual(Totales.find('MntExe').text, '13678')
                self.assertEqual(dte['MntNeto'], 3226933)
                self.assertEqual(Totales.find('MntNeto').text, '3226933')
                self.assertEqual(dte['MntIVA'], 613117)
                self.assertEqual(Totales.find('IVA').text, '613117')
                self.assertEqual(dte['MntTotal'], 3853728)
                self.assertEqual(Totales.find('MntTotal').text, '3853728')
                self.assertEqual(dte['ImptoReten'], 0)
                self.assertIsNone(Totales.find('ImptoReten'))
            elif dte['NroDTE'] == 5:
                self.assertEqual(dte['TipoDTE'], 61)
                self.assertEqual(IdDoc.find('TipoDTE').text, '61')
                self.assertEqual(dte['Folio'], 21)
                self.assertEqual(IdDoc.find('Folio').text, '21')
                self.assertEqual(dte['MntExe'], 0)
                self.assertIsNone(Totales.find('MntExe'))
                self.assertEqual(dte['MntNeto'], 0)
                self.assertIsNone(Totales.find('MntNeto'))
                self.assertEqual(dte['MntIVA'], 0)
                self.assertIsNone(Totales.find('IVA'))
                self.assertEqual(dte['MntTotal'], 0)
                self.assertEqual(Totales.find('MntTotal').text, '0')
                self.assertEqual(dte['ImptoReten'], 0)
                self.assertIsNone(Totales.find('ImptoReten'))
                self.assertIsNotNone(Referencia)
                self.assertEqual(len(Referencia), 2)
                self.assertEqual(Referencia[1].find('CodRef').text, "2")
                self.assertEqual(Referencia[1].find('RazonRef').text, "Dice: y debe decir:")

            elif dte['NroDTE'] == 6:
                self.assertEqual(dte['TipoDTE'], 61)
                self.assertEqual(IdDoc.find('TipoDTE').text, '61')
                self.assertEqual(dte['Folio'], 22)
                self.assertEqual(IdDoc.find('Folio').text, '22')
                self.assertEqual(dte['MntExe'], 0)
                self.assertIsNone(Totales.find('MntExe'))
                self.assertEqual(dte['MntNeto'], 3698268)
                self.assertEqual(Totales.find('MntNeto').text, '3698268')
                self.assertEqual(dte['MntIVA'], 702671)
                self.assertEqual(Totales.find('IVA').text, '702671')
                self.assertEqual(dte['MntTotal'], 4400939)
                self.assertEqual(Totales.find('MntTotal').text, '4400939')
                self.assertEqual(dte['ImptoReten'], 0)
                self.assertIsNone(Totales.find('ImptoReten'))
            elif dte['NroDTE'] == 7:
                self.assertEqual(dte['TipoDTE'], 61)
                self.assertEqual(IdDoc.find('TipoDTE').text, '61')
                self.assertEqual(dte['Folio'], 23)
                self.assertEqual(IdDoc.find('Folio').text, '23')
                self.assertEqual(dte['MntExe'], 35344)
                self.assertEqual(Totales.find('MntExe').text, '35344')
                self.assertEqual(dte['MntNeto'], 1510824)
                self.assertEqual(Totales.find('MntNeto').text, '1510824')
                self.assertEqual(dte['MntIVA'], 287057)
                self.assertEqual(Totales.find('IVA').text, '287057')
                self.assertEqual(dte['MntTotal'], 1833225)
                self.assertEqual(Totales.find('MntTotal').text, '1833225')
                self.assertEqual(dte['ImptoReten'], 0)
                self.assertIsNone(Totales.find('ImptoReten'))
            elif dte['NroDTE'] == 8:
                self.assertEqual(dte['TipoDTE'], 56)
                self.assertEqual(IdDoc.find('TipoDTE').text, '56')
                self.assertEqual(dte['Folio'], 7)
                self.assertEqual(IdDoc.find('Folio').text, '7')
                self.assertEqual(dte['MntExe'], 0)
                self.assertIsNone(Totales.find('MntExe'))
                self.assertEqual(dte['MntNeto'], 1085752)
                self.assertEqual(Totales.find('MntNeto').text, '1085752')
                self.assertEqual(dte['MntIVA'], 206293)
                self.assertEqual(Totales.find('IVA').text, '206293')
                self.assertEqual(dte['MntTotal'], 1292045)
                self.assertEqual(Totales.find('MntTotal').text, '1292045')
                self.assertEqual(dte['ImptoReten'], 0)
                self.assertIsNone(Totales.find('ImptoReten'))

    def test_timbrar_varios(self):
        """
        Test Varios Básico 33 Factura Afecta
        """
        print("Se inicia test varios básico 33")
        f = open("facturacion_electronica/ejemplos/ejemplo_basico_33_varios.json")
        txt_json = f.read()
        f.close()
        ejemplo = json.loads(txt_json)
        firma_electronica = ejemplo['firma_electronica'].copy()
        result = fe.timbrar(ejemplo)
        for dte in result:
            """
                Verifico DTE individuales
            """
            self.assertFalse(dte.get('error', False))
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
            Detalle = xml_dte.find('Documento/Detalle')
            if dte['NroDTE'] == 1:
                _cabezera_NroDTE1(self, dte, IdDoc, Totales)
                for detalle in Detalle:
                    NroLinDet = Totales.findall('NroLinDet')
                    CdgItem = Totales.findall('CdgItem')
                    self.assertIsNotNone(CdgItem)
                    if NroLinDet == 1:
                        self.assertEqual(len(CdgItem), 2)
                        self.assertEqual(len(CdgItem[0]), 2)
                        self.assertEqual(CdgItem[0][0].text, 'INT1')
                        self.assertEqual(CdgItem[0][1].text, '02')
                        self.assertEqual(CdgItem[1][0].text, 'EAN13')
                        self.assertEqual(CdgItem[1][1].text, '0123456789102')
                    if NroLinDet == 2:
                        self.assertEqual(len(CdgItem), 1)
                        self.assertEqual(len(CdgItem[0]), 2)
                        self.assertEqual(CdgItem[0][0].text, 'INT1')
                        self.assertEqual(CdgItem[0][1].text, '013')
            elif dte['NroDTE'] == 2:
                self.assertEqual(dte['MntTotal'], 380)
                self.assertEqual(Totales.find('MntTotal').text, '380')
                self.assertEqual(Totales.find('MontoNF').text, '-2')
            elif dte['NroDTE'] == 3:
                self.assertEqual(dte['MntNeto'], 16578687)
                self.assertEqual(Totales.find('MntNeto').text, '16578687')
                self.assertEqual(dte['MntIVA'], 3149951)
                self.assertEqual(Totales.find('IVA').text, '3149951')
                self.assertEqual(Totales.find('CredEC').text, '2047468')
                self.assertEqual(dte['MntTotal'], 17681170)
                self.assertEqual(Totales.find('MntTotal').text, '17681170')
            elif dte['NroDTE'] == 4:
                self.assertEqual(dte['MntNeto'], 112000)
                self.assertEqual(Totales.find('MntNeto').text, '112000')
                self.assertEqual(dte['MntIVA'], 21280)
                self.assertEqual(Totales.find('IVA').text, '21280')
                self.assertEqual(dte['MntTotal'], 144480)
                self.assertEqual(Totales.find('MntTotal').text, '144480')
                self.assertEqual(dte['ImptoReten'], 11200)
                ImptoReten = Totales.findall("ImptoReten")
                self.assertEqual(len(ImptoReten), 2)
                self.assertEqual(ImptoReten[0].find('TipoImp').text, '26')
                self.assertEqual(ImptoReten[0].find('TasaImp').text, '10')
                self.assertEqual(ImptoReten[0].find('MontoImp').text, '1200')
                self.assertEqual(ImptoReten[1].find('TipoImp').text, '24')
                self.assertEqual(ImptoReten[1].find('TasaImp').text, '10')
                self.assertEqual(ImptoReten[1].find('MontoImp').text, '10000')

if __name__ == '__main__':
    unittest.main()

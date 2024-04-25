# -#- coding: utf-8 -#-
from facturacion_electronica import facturacion_electronica as fe
from facturacion_electronica.firma import Firma
import json
from lxml import etree
import unittest


class TestEjemploRespuestasIntercambio(unittest.TestCase):
    """
    Test Ejemplo Respuestas Intercambio
    """
    def test_respuesta_recepcion(self):
        """
        Test Ejemplo Respuesta Recepción XML
        """
        print("Se inicia test Respuesta Recepción XML")
        f = open("facturacion_electronica/ejemplos/ejemplo_recepcion_dte.json")
        txt_json = f.read()
        f.close()
        ejemplo = json.loads(txt_json)
        firma_electronica = ejemplo['firma_electronica'].copy()
        result = fe.recepcion_xml(ejemplo)
        """
            Verifico Integridad XML
        """
        self.assertEqual(len(result), 1)
        for r in result:
            self.assertFalse(r.get('error', False))
            xml = etree.fromstring(
                r['respuesta_xml'].replace('xmlns="http://www.sii.cl/SiiDte"',
                                                 '').encode('ISO-8859-1'))
            self.assertEqual(xml.find("Resultado").get('ID'), 'RespRecep')
            Caratula = xml.find("Resultado/Caratula")
            self.assertEqual(Caratula.find("RutResponde").text, "76883241-2")
            self.assertEqual(Caratula.find("RutRecibe").text, "96722400-6")
            self.assertEqual(Caratula.find("NroDetalles").text, "1")
            query = "Resultado/RecepcionEnvio"
            RecepcionEnvio = xml.findall(query)
            self.assertEqual(len(RecepcionEnvio), 1)
            self.assertEqual(RecepcionEnvio[0].find('RutEmisor').text, "96722400-6")
            self.assertEqual(RecepcionEnvio[0].find('RutReceptor').text, "76883241-2")
            self.assertEqual(RecepcionEnvio[0].find('EstadoRecepEnv').text, "0")
            self.assertEqual(RecepcionEnvio[0].find('NroDTE').text, "1")
            query = "RecepcionDTE"
            RecepcionDTE = RecepcionEnvio[0].findall(query)
            self.assertEqual(len(RecepcionDTE), 1)
            self.assertEqual(RecepcionDTE[0].find('TipoDTE').text, "33")
            self.assertEqual(RecepcionDTE[0].find('Folio').text, "418506")
            self.assertEqual(RecepcionDTE[0].find('RUTEmisor').text, "96722400-6")
            self.assertEqual(RecepcionDTE[0].find('RUTRecep').text, "76883241-2")
            self.assertEqual(RecepcionDTE[0].find('EstadoRecepDTE').text, "0")

    """
    Test Resuesta Recepción Mercaderías
    """
    def test_respuesta_rececpion_mercaderias(self):
        """
        Test Ejemplo Reenvío Correo de Envío
        """
        print("Se inicia test Reenvío Correo de Envío")
        f = open("facturacion_electronica/ejemplos/ejemplo_validacion_mercaderias.json")
        txt_json = f.read()
        f.close()
        ejemplo = json.loads(txt_json)
        firma_electronica = ejemplo['firma_electronica'].copy()
        result = fe.recepcion_mercaderias(ejemplo)
        self.assertFalse(result.get('error', False))
        """
            Verifico Integridad XML
        """
        self.assertFalse(result.get('errores', False))
        xml = etree.fromstring(
            result['respuesta_xml'].replace('xmlns="http://www.sii.cl/SiiDte"',
                                             '').encode('ISO-8859-1'))
        Caratula  = xml.find("SetRecibos/Caratula")
        self.assertEqual(Caratula.find("RutResponde").text, "76883241-2")
        self.assertEqual(Caratula.find("RutRecibe").text, "88888888-8")
        Recibo = xml.findall("SetRecibos/Recibo")
        self.assertEqual(len(Recibo), 2)
        DocumentoRecibo = Recibo[0].find("DocumentoRecibo")
        self.assertEqual(DocumentoRecibo.find('TipoDoc').text, "33")
        self.assertEqual(DocumentoRecibo.find('Folio').text, "14")
        self.assertEqual(DocumentoRecibo.find('RUTEmisor').text, "88888888-8")
        self.assertEqual(DocumentoRecibo.find('RUTRecep').text, "76883241-2")
        self.assertIsNotNone(DocumentoRecibo.find('Declaracion'))
        DocumentoRecibo = Recibo[1].find("DocumentoRecibo")
        self.assertEqual(DocumentoRecibo.find('TipoDoc').text, "33")
        self.assertEqual(DocumentoRecibo.find('Folio').text, "15")
        self.assertEqual(DocumentoRecibo.find('RUTEmisor').text, "88888888-8")
        self.assertEqual(DocumentoRecibo.find('RUTRecep').text, "76883241-2")
        self.assertIsNotNone(DocumentoRecibo.find('Declaracion'))

    def test_respuesta_rececpion_comercial(self):
        """
        Test Ejemplo Respuesta Recepción Comercial
        """
        print("Se inicia test Respuesta Recepción Comercial")
        f = open("facturacion_electronica/ejemplos/ejemplo_validacion_comercial.json")
        txt_json = f.read()
        f.close()
        ejemplo = json.loads(txt_json)
        firma_electronica = ejemplo['firma_electronica'].copy()
        result = fe.validacion_comercial(ejemplo)
        self.assertFalse(result.get('errores', False))
        """
            Verifico Integridad XML
        """
        self.assertFalse(result.get('errores', False))
        xml = etree.fromstring(
            result['respuesta_xml'].replace('xmlns="http://www.sii.cl/SiiDte"',
                                             '').encode('ISO-8859-1'))
        Caratula  = xml.find("Resultado/Caratula")
        self.assertEqual(Caratula.find("RutResponde").text, "76883241-2")
        self.assertEqual(Caratula.find("RutRecibe").text, "88888888-8")
        self.assertEqual(Caratula.find("NroDetalles").text, "2")
        ResultadoDTE = xml.findall("Resultado/ResultadoDTE")
        self.assertEqual(len(ResultadoDTE), 2)
        self.assertEqual(ResultadoDTE[0].find('TipoDTE').text, "33")
        self.assertEqual(ResultadoDTE[0].find('Folio').text, "14")
        self.assertEqual(ResultadoDTE[0].find('RUTEmisor').text, "88888888-8")
        self.assertEqual(ResultadoDTE[0].find('RUTRecep').text, "76883241-2")
        self.assertEqual(ResultadoDTE[0].find('EstadoDTE').text, "0")
        self.assertIsNone(ResultadoDTE[0].find('CodRchDsc'))
        self.assertEqual(ResultadoDTE[1].find('TipoDTE').text, "33")
        self.assertEqual(ResultadoDTE[1].find('Folio').text, "15")
        self.assertEqual(ResultadoDTE[1].find('RUTEmisor').text, "88888888-8")
        self.assertEqual(ResultadoDTE[1].find('RUTRecep').text, "76883241-2")
        self.assertEqual(ResultadoDTE[1].find('EstadoDTE').text, "2")
        self.assertEqual(ResultadoDTE[1].find('CodRchDsc').text, "-1")


if __name__ == '__main__':
    unittest.main()

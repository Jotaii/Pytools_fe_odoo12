from facturacion_electronica import facturacion_electronica as fe
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
import os, re
from dotenv import load_dotenv;load_dotenv()
import xmlrpc.client

# Odoo connection
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(os.getenv("ODOO_URL")))
uid = common.authenticate(os.getenv("ODOO_DB"), os.getenv("ODOO_USER"), os.getenv("ODOO_PW"), {})



# CONFIG SETTINGS

companies = ['Kaya']
yearmonth = '202402'
files_to_check = ['202402.json']
dates = ['2023-11-30'] #False
type_doc = [39]

folio_range = (2669901, 2719900)
folio_range = (182472, 745972)

# END CONFIG



BASE_DATA = {
    'Kaya':{
        'Emisor': {
            'RUTEmisor': '76962000-1', 
            'RznSocEmisor': 'GANDAYA SPA', 
            'GiroEmisor': 'VENTA AL POR MENOR DE PRENDAS Y ACCESORIOS DE VESTIR EN COMERCIOS ESPECIALIZADOS', 
            'DirOrigen': 'AVDA APOQUINDO 4411 LOCAL 177', 
            'CmnaOrigen': 'Las Condes', 
            'CiudadOrigen': 'Santiago', 
            'Modo': 'produccion', 
            'NroResol': '8', 
            'FchResol': '2014-01-16', 
            'ValorIva': 19}, 
        'firma_electronica': {
            'priv_key': re.sub(r'\\n', '\n', os.getenv('GANDPK')),
            'cert': re.sub(r'\\n', '\n', os.getenv('GANDCERT')), 
            'rut_firmante': '16359565-6', 
            'init_signature': False}, 
        'Documento': [{
            'TipoDTE': 39, 
            'documentos': [{
                'Encabezado': {
                    'IdDoc': {
                        'TipoDTE': 39, 
                        'Folio': 424486},
                    'Receptor': {}, 
                    'Totales': {
                        'MntTotal': 62970}}}]}], 
        'api': True},
    'Adagio':{
        'Emisor': {
            'RUTEmisor': '76375855-9', 
            'RznSocEmisor': 'TEA GROUP SPA', 
            'GiroEmisor': 'VENTA AL POR MENOR DE ALIMENTOS EN COMERCIOS ESPECIALIZADOS (ALMACENES', 
            'DirOrigen': 'MALL COSTANERA CENTER , ANDRES BELLO 2447 ', 
            'CmnaOrigen': 'Providencia', 
            'CiudadOrigen': 'SANTIAGO', 
            'Modo': 'produccion', 
            'NroResol': '80', 
            'FchResol': '2014-08-22', 
            'ValorIva': 19}, 
        'firma_electronica': {
            'priv_key': re.sub(r'\\n', '\n', os.getenv('TEAPK')),
            'cert': re.sub(r'\\n', '\n', os.getenv('TEACERT')),
            'rut_firmante': '17082984-0', 
            'init_signature': False}, 
        'Documento': [{
            'TipoDTE': 39, 
            'documentos': [{
                'Encabezado': {
                    'IdDoc': {
                        'TipoDTE': 39, 
                        'Folio': 2680235},
                    'Receptor': {},
                    'Totales': {
                        'MntTotal': 39960}}}]}], 
        'api': True}}



def ask_for_dte_status(tipo_dte, folio, monto_total, company):
    if company not in ['Kaya', 'Adagio']:
        raise ValueError('Company not identified')
    BASE_DATA[company]['Documento'][0]['TipoDTE'] = tipo_dte
    BASE_DATA[company]['Documento'][0]['documentos'][0]['Encabezado']['IdDoc']['TipoDTE'] = tipo_dte
    BASE_DATA[company]['Documento'][0]['documentos'][0]['Encabezado']['IdDoc']['Folio'] = folio
    BASE_DATA[company]['Documento'][0]['documentos'][0]['Encabezado']['Totales']['MntTotal'] = monto_total
    resultado = fe.consulta_estado_dte(BASE_DATA[company])
    key = [k for k in resultado.keys()]
    return(f"folio: {folio}({resultado[key[0]]['status']}) -> {resultado[key[0]]['glosa']}")


def progress_bar(current, total, bar_length=20):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '
    ending = '\n' if current >= total else '\r'

    print(f'Progress: [{arrow}{padding}] {int(fraction*100)}%', end=ending)


for company in companies:

    print("[*] Configuraciones")
    print("[*] \tCompania: {}".format(company))
    print("[*] \tAnioMes: {}".format(yearmonth))
    print("[*] \tArchivos: {}\n\n\n".format(files_to_check))

    for filename in files_to_check:
        sended = []
        to_query = []
        with open('data/{}.json'.format(yearmonth)) as json_file:
            data = json.load(json_file)
            print("{}".format(len([x for x in data if x["folio"]== None])))
            
            data = [x for x in data if
                x["compania"] == company and
                int(x["folio"] if type(x["folio"]) == str else 0) >=folio_range[0] and 
                int(x["folio"] if type(x["folio"]) == str else 0)<=folio_range[1] and 
                x["tipodte"] in type_doc]
            
            print (f'archivo fuente: {filename}\ncantidad de documentos a revisar: {len(data)}')
            counter = 1
            data = sorted(data, key=lambda rec:rec['folio'])
            folios = [int(d['folio']) for d in data]
            #for d in data[:100]: print(d)
            folios_to_be_checked = []
            folios_to_be_checked = [648460,646910,646923,604786,182572,182573,529756,646916,582111,646914,646915,604781,529755,604783,582107,646913,646912,701282,524533,701279,582120,646917,505382,447417,646933,628235,604789,693901,510585,693905,529757,604779,582105,646918,529754,646911,608606,505377,505378,608604,510584,604787,693900,604795,510586,646919,447418,505384,604784,582109,524534,182571,646920,505379,646926,505380,505381,524532,604785,505385,604790,693903,616203,637521,616204,182575,604792,693904,608602,182574,604788,646934,582112,646925,608603,646930,637520,646924,646922,646921,582106,604780,646927,628234,604782,646928,693906,604794,582121,693912,628244,582125,693917,628249,582131,608617,616207,637519,604796,447419,447420,693907,604797,608607,646929,646931,646932,582110,693902,505383,510587,628237,693913,608612,646940,604800,582117,705406,582118,582134,693920,524538,701284,646937,646936,628236,705405,701280,608608,693908,701281,604791,646935,637522,646938,608613,524535,616205,582114,608605,582116,582113,604793,705404,582128,582129,646947,646946,604805,546565,582115,705411,705410,628246,608615,524537,646942,646941,182581,582127,182576,182579,582119,608610,524536,693910,604801,693921,447421,182577,604798,637523,608609,182578,604799,693909,646939,693923,705407,705408,693911,616206,604806,637525,701283,582122,182580,628238,604802,628239,604803,701285,646943,546566,637524,608611,693914,628240,604804,646944,693915,582123,628241,693918,646954,582126,628245,608614,646953,693919,646945,646948,582124,693916,628242,628243,693922,693924,705409,505386,182582,510588,701287,582130,646951,693925,447422,701286,604824,608616,693937,447424,524539,701290,447425,646967,604825,524543,582146,646949,646950,628247,505387,604807,604808,693926,701297,705412,693927,604816,705417,505389,546570,693930,646955,693928,604809,582135,510590,604814,616209,582136,701295,646970,646952,701288,705415,646956,646959,705413,616210,705414,646958,646957,604817,510591,608618,628248,646960,582132,604820,604810,646965,646964,646963,505390,505388,701289,510589,646962,646961,182587,546568,608620,182588,510592,701298,693932,701304,693929,705416,616208,628250,701291,608619,546567,582139,604821,701302,529760,582133,604811,701292,529758,582137,705418,701293,701294,604812,604813,646966,693931,604815,701296,182583,604826,646990,182584,604818,182585,616211,182586,705423,524540,604819,582140,693933,646968,705419,524541,705420,529759,582138,693934,701300,546571,701301,546572,505391,705421,447423,608621,546569,701299,582144,693935,582141,646969,646978,646981,646980,510593,582142,546573,182589,604822,608622,582143,505392,582145,701306,646976,646989,628251,701308,646975,646983,646979,646982,693936,604823,582147,608624,546574,705422,646972,705424,701305,608623,524542,646971,701303,182590,646973,701307,705425,646974,646984,646977,647014,647272,647412]
            
            prev_missing_folio = data[0]
            
            #Descomentar despues de probar lo otro!!
            
            #print([x['folio'] for x in data if '268040' in x['folio']])
            #while len(folios)>1:
            #    if 0 < (folios[1] - folios[0]) <= 5:
            #        folios_to_be_checked += [x for x in range(folios[0]+1, folios[1])]
            #        folios.remove(folios[0])
            #        continue
            #    folios.remove(folios[0])
            
            
            for folio in folios_to_be_checked:
                progress_bar(counter, len(folios_to_be_checked), bar_length=100)
                out = ask_for_dte_status(39, folio,9990, company)

                if "Rechazado" not in out:
                    to_query.append(folio)
                    sended.append(out)
                counter +=1

            comp_id = 1 if company == "Adagio" else 2
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(os.getenv("ODOO_URL")))
            record_ids = models.execute_kw(os.getenv("ODOO_DB"), uid, os.getenv("ODOO_PW"),
                'account.invoice', 'search',
                [[('company_id', '=', comp_id), ('sii_document_number', 'in', to_query) ,('document_class_id.sii_code','=',39)]])
            
            records = models.execute_kw(os.getenv("ODOO_DB"), uid, os.getenv("ODOO_PW"), 'account.invoice', 'read', [record_ids])
            
            docs_in_sii_not_in_odoo = list(set(to_query).difference([x['sii_document_number'] for x in records]))

            print('\n[*] Resumen:')
            print(f'[*] Compañía: {company}')
            print(f'[*] Fecha: {filename.replace(".json","")}')
            print(f'[*] Cantidad de documentos revisados: {len(folios_to_be_checked)}')
            print(f'[*] Cantidad de documentos de diferencia SII -> Odoo: {len(docs_in_sii_not_in_odoo)}')
            print('[*] Resultados:')
            if len(sended) == 0: 
                print('[O] No se detectan folios en SII que no estén en Odoo.')
                exit()
            else:
                for ns in docs_in_sii_not_in_odoo: print("\t{}".format(ns))
            out_query =  ','.join([str(f) for f in docs_in_sii_not_in_odoo])
            print(f"[*] To paste Query -> ({out_query})")
            print('\n')

from facturacion_electronica import facturacion_electronica as fe
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
import os, re
from dotenv import load_dotenv;load_dotenv()




# CONFIG SETTINGS
companies = ['Kaya','Adagio']
yearmonth = '202403'
doc_types_to_check = ['BELEC']  #Supported doc_types: NC - FELEC - BELEC - LIQ - ND
dates_to_check = ['2024-02-01']
hard_check = 'NoProcesadas' # opciones: 'All'|'NoProcesadas'|'NoRecibidas'
month_report = 'All' # '1stMid' '2ndMid' None 'All'
# END CONFIG


# GLOBAL
max_day_month = {
    '01':31, '02':28 if (int(yearmonth[:4])-2020)%4 != 0 else 29,
    '03':31, '04':30, '05':31, '06':30, '07':31,
    '08':31, '09':30, '10':31, '11':30, '12':31,}
doc_types_translated = {
    "NC": 61,
    "BELEC": 39,
    "FELEC": 33,
    "LIQ": 43,
    "ND": 56
}
trans_code = {
                'BELEC':'boletas electrónicas',
                'FELEC':'facturas electrónicas',
                'NC':'notas de crédito',
                'ND':'notas de débito',
                'LIQ':'liquidación de factura'
            }
# END GLOBAL


if month_report:
    #Overwrite files to check for all monthly
    if month_report == '1stMid':
        dates_to_check = [f'{yearmonth[:4]}-{yearmonth[-2:]}-0{day}' for day in range(1,10)] + \
                     [f'{yearmonth[:4]}-{yearmonth[-2:]}-{day}' for day in range(10,16)]
    elif month_report == '2ndMid':
        dates_to_check = [f'{yearmonth[:4]}-{yearmonth[-2:]}-{day}' for day in range(15,max_day_month[yearmonth[-2:]]+1)]
    elif month_report == 'All':
        dates_to_check = [f'{yearmonth[:4]}-{yearmonth[-2:]}-0{day}' for day in range(1,10)] + \
                         [f'{yearmonth[:4]}-{yearmonth[-2:]}-{day}' for day in range(10,max_day_month[yearmonth[-2:]]+1)]
    else:
        print(f"El reporte ingresado no es una opcion valida. Se ingresó {month_report} y las opciones son ['1stMid', '2ndMid', None, 'Full']")
        exit()


BASE_DATA = {
    'Kaya':{
        'Emisor': {
            'RUTEmisor': os.getenv('RUTCOMP2'), 
            'Modo': 'produccion'}, 
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
                        'Folio': 585340, 
                        'FchEmis': '2023-08-01'}, 
                    'Emisor': {}, 
                    'Receptor': {
                        'RUTRecep': '19616942-3'}, 
                    'Totales': { 
                        'MntTotal': 59990}}, 
                'Detalle': []}]}]},
    'Adagio':{
        'Emisor': {
            'RUTEmisor': os.getenv('RUTCOMP1'), 
            'Modo': 'produccion'}, 
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
                        'Folio': 2680235,
                        'FchEmis': '2023-08-01'},
                    'Receptor': {
                        'RUTRecep': '19616942-3'},
                    'Totales': {
                        'MntTotal': 39960}},
                'Detalle':[]}]}]}}



def ask_for_dte_status(tipo_dte, folio, fch_emision, rut_receptor, monto_total, company, channel):
    if company not in ['Kaya', 'Adagio']:
        raise ValueError('Company not identified')
    BASE_DATA[company]['Documento'][0]['TipoDTE'] = tipo_dte
    BASE_DATA[company]['Documento'][0]['documentos'][0]['Encabezado']['IdDoc']['TipoDTE'] = tipo_dte
    BASE_DATA[company]['Documento'][0]['documentos'][0]['Encabezado']['IdDoc']['Folio'] = folio
    BASE_DATA[company]['Documento'][0]['documentos'][0]['Encabezado']['IdDoc']['FchEmis'] = fch_emision
    BASE_DATA[company]['Documento'][0]['documentos'][0]['Encabezado']['Receptor']['RUTRecep'] = rut_receptor
    BASE_DATA[company]['Documento'][0]['documentos'][0]['Encabezado']['Totales']['MntTotal'] = abs(monto_total)
    resultado = fe.consulta_estado_dte(BASE_DATA[company])
    key = [k for k in resultado.keys()]
    #print(resultado[key[0]])
    return (f"{channel} | folio: {folio}({resultado[key[0]]['status']}) -> {resultado[key[0]]['glosa']}")

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
    print("[*] \tTipos Documentos: {}".format([doc_types_translated[x] for x in doc_types_to_check]))
    print("[*] \tFechas: {}\n".format(dates_to_check))
    sii_rechazado = []
    with open('data/{}.json'.format(yearmonth)) as json_file:
        data_raw = [rec for rec in json.load(json_file)]
        data = [rec for rec in data_raw if rec['compania'] == company and rec['fchemis'] in dates_to_check and rec['tipodte'] in [doc_types_translated[x] for x in doc_types_to_check]]
        data.sort(key = lambda r:r['fchemis'])
        
        for doc_type in doc_types_to_check:
            resumen_mensual = []
            for date in dates_to_check:
                not_sended = []
                count_by_state = {}
                rec = [dat for dat in data if dat['tipodte'] == doc_types_translated[doc_type] and dat['fchemis']==date]
                counter = 1
                for order in rec:
                    out = ask_for_dte_status(order['tipodte'],int(order['folio']),order['fchemis'],order['rutrecep'],int(float(order['monto_total'])), company, order['channel'])
                    sii_result = re.sub('\).*','',re.sub('.*\(','',out))
                    
                    if sii_result not in count_by_state.keys():
                        count_by_state[sii_result] = 0
                    count_by_state[sii_result] += 1

                    if hard_check in ['NoProcesadas','All']:
                        if hard_check == 'All':
                            not_sended.append(out)
                        elif sii_result != 'Proceso':
                            not_sended.append(out)
                    elif hard_check == 'NoRecibidas':
                        if "No Recibido" in out:
                            not_sended.append(out)
                    progress_bar(counter, len(rec), bar_length=100)
                    counter +=1
            
                print('\n[*] Resumen:')
                print(f'[*] Compañía: {company}')
                print(f'[*] Fecha: {date}')
                print(f'[*] Tipo Documento: {doc_type}')
                print(f'[*] Cantidad de documentos revisados: {len(rec)}')
                print(f'[*] Agrupacion por estado de resultado SII:')
                for k in count_by_state.keys():
                    print(f'[*]\t{k}: {count_by_state[k]}')
                print('[*] Resultados:')
                if len(not_sended) == 0: print(f'[O]\tNo se detecta diferencia de {trans_code[doc_type]}.')
                else:
                    for ns in not_sended: print(f'\t{ns}')
                print('\n\n')
                
                resumen_mensual.append((date,len(rec),len(not_sended)))


            if month_report:
                
                with open('data/{}_{}_{}_{}.txt'.format(month_report,yearmonth,company,doc_type),'w+') as monthly_report_file:

                    # print("\n-- BEGIN REPORT -- Please copy-paste to send an email\n")
                    monthly_report_file.write(f'Estimados,\n\nAdjunto el reporte mensual de diferencias en cantidad de {trans_code[doc_type]} Odoo -> SII\n\n\n')
                    monthly_report_file.write(f"Reporte Mensual - {yearmonth[-2:]}/{yearmonth[:4]}\n")
                    monthly_report_file.write('Fecha\t\tRevisadas\tNo enviadas\n')
                    for rec in resumen_mensual:
                        monthly_report_file.write(f"{rec[0]}\t  {rec[1]}\t\t  {rec[2]}\n")

                    monthly_report_file.write(f"\nRecuerdo tambien que este reporte entrega exclusivamente el estado de {trans_code[doc_type]} en Odoo que NO han sido enviados al SII.\n")
                    monthly_report_file.write("\nSin nada mas que agregar, se despide atte.\n")



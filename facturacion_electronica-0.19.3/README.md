# Facturación Electrónica

Librería para la facturación Electrónica Chilena

Librería Creada en Base al conocimiento obtenido en https://gitlab.com/dansanti/l10n_cl_fe , la idea de separarla del proyecto original, es facilitar el desarrollo de ambos proyectos, y permitir que esta librería sea integrada en otros sistemas similares

| Tipo Documento            | Códigos        | Envío | Consulta | Certificación |
|---------------------------|----------------|-------|----------|---------------|
| Factura                   | FAC 33, FNA 34 |   OK  |    OK    |       OK      |
| Nota de Crédito           |       61       |   OK  |    OK    |       Ok      |
| Nota de Débito            |       56       |   OK  |    OK    |       OK      |
| Recepción XML Intercambio | Env, Merc, Com |   OK  |    OK    |       OK      |
| Libro de Compra-Venta     |  Compra, Venta |   OK  |    OK    |       OK      |
| Boleta                    | BEL 39, BNA 41 |   OK  |    OK    |       OK      |
| Consumo de Folios Boletas |       CF       |   OK  |    OK    |       OK      |
| Guía de Despacho          |       52       |   OK  |    OK    |       OK      |
| Libro de Guías            |       LG       |   OK  |    OK    |       OK      |
| Cesión de Créditos        |       CES      |   OK  |    OK    |       OK      |
| Factura Exportación       |       110      |   OK  |    OK    |       OK      |
| Nota Crédito Exportación  |       112      |   OK  |    OK    |       OK      |
| Nota Débito Exportación   |       111      |   OK  |    OK    |       OK      |
| Factura de Compras        |       46       |   OK  |    OK    |       OK      |
| Liquidación de facturas   |       43       |   OK  |    OK    |       X       |


 - Impuestos Soportados Para Ventas(Probados en emisión):

  A = Anticipado
  N = Normal
  R = Retención
  D = Adicional
  E = Específico

 | Código |               Nombre              |   %  | Tipo | Envío | Observación                                                                                        |
 |:------:|:---------------------------------:|:----:|:----:|:-----:|----------------------------------------------------------------------------------------------------|
 |   14   | IVA                               |  19  |   N  |   OK  |                                                                                                    |
 |   15   | IVA Retención total               |  19  |   R  |   OK  |                                                                                                    |
 |   17   | IVA al faenamiento de carnes      |   5  |   A  |   OK  |                                                                                                    |
 |   18   | IVA a las carnes                  |   5  |   A  |   OK  |                                                                                                    |
 |   19   | IVA a la Harina                   |  12  |   A  |   X   |                                                                                                    |
 |   23   | Impuesto adicional                |  15  |   A  |   X   | a) artículos oro, platino, marfil b) Joyas, piedras preciosas c) Pieles finas                      |
 |   24   | DL 825/74, ART. 42, letra b)      | 31.5 |   D  |   OK  | Licores, Piscos, whisky, aguardiente, y vinos licorosos o aromatizados.                            |
 |   25   | Vinos                             | 20.5 |   D  |   OK  |                                                                                                    |
 |   26   | Cervezas y bebidas alcohólicas    | 20.5 |   D  |   OK  |                                                                                                    |
 |   27   | Bebidas analcohólicas y minerales |  10  |   D  |   OK  |                                                                                                    |
 |   271  | Bebidas azucaradas                |  18  |   D  |   OK  | Bebidas analcohólicas y Minerales con elevado contenido de azúcares. (según indica la ley)         |
 |   28   | Impuesto especifico diesel        |      |   E  |   OK  | Compuesto                                                                                          |
 |   30   | IVA Legumbres                     |      |   R  |   X   |                                                                                                    |
 |   31   | IVA Silvestre                     |      |   R  |   X   |                                                                                                    |
 |   32   | IVA al Ganado                     |   8  |   R  |   X   |                                                                                                    |
 |   33   | IVA a la Madera                   |   8  |   R  |   X   |                                                                                                    |
 |   34   | IVA al Trigo                      |  11  |   R  |   X   |                                                                                                    |
 |   35   | Impuesto Específico Gasolinas     |      |   E  |   OK  | Compuesto                                                                                          |
 |   36   | IVA Arroz                         |  10  |   R  |   X   |                                                                                                    |
 |   37   | IVA Hidrobiológicas               |  10  |   R  |   X   |                                                                                                    |
 |   38   | IVA Chatarras                     |  19  |   R  |   X   |                                                                                                    |
 |   39   | IVA PPA                           |  19  |   R  |   X   |                                                                                                    |
 |   41   | IVA Construcción                  |  19  |   R  |   X   | Solo factura compras                                                                               |
 |   44   | IMPUESTO art 37 Letras e, h, I, l |  15  |   A  |   X   | Tasa del 15% en 1era venta a) Alfombras, tapices b) Casa rodantes c) Caviar d) Armas de aire o gas |
 |   45   | Impuesto Pirotecnia               |  50  |   A  |   X   |                                                                                                    |
 |   46   | IVA ORO                           |  19  |   R  |   X   |                                                                                                    |
 |   47   | IVA Cartones                      |  19  |   R  |   X   |                                                                                                    |
 |   48   | IVA Frambuesas                    |  14  |   R  |   X   |                                                                                                    |
 |   49   | IVA factura Compra sin Retención  |   0  |   R  |   X   | hoy utilizada sólo por Bolsa de Productos de Chile, lo cual es validado por el sistema             |
 |   50   | IVA instrumentos de prepago       |  19  |   N  |   X   |                                                                                                    |
 |   51   | IVA gas natural                   |      |   E  |   X   | Compuesto                                                                                          |
 |   53   | Impuesto Suplementos              |  0.5 |   R  |   X   |                                                                                                    |

<a href='https://www.flow.cl/btn.php?token=uuv7ekg' target='_blank'>
  <img src='https://www.flow.cl/img/botones/btn-donar-negro.png'>
</a>

"""
Módulo para generar la receta médica en formato HTML
"""

from datetime import datetime
from typing import Dict
import os
import base64

def generar_receta_html(pauta: Dict, observaciones: str = "", producto_recetado: str = "") -> str:
    """
    Genera una receta médica en formato HTML para visualización web e impresión
    """
    
    # Verificar si tiene gotas
    tiene_gotas = "dosis_por_toma_gotas" in pauta
    
    # Cargar el logo en base64 si existe
    logo_base64 = ""
    logo_paths = [
        "assets/images/Logo empresa.JPG",
        "assets/images/logo-empresa.JPG",
        "assets/images/logo-greenmed.png"
    ]
    for path in logo_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    logo_base64 = base64.b64encode(f.read()).decode()
                break
            except:
                pass
    
    # Calcular para Xatiplex
    from productos import CatalogoProductos
    from calculos import CalculadoraCBD
    
    catalogo = CatalogoProductos()
    
    # Obtener la dosis por toma en mg
    mg_por_toma = pauta['dosis_por_toma_mg']
    
    # Calcular equivalencias
    xpectra = catalogo.get_producto("Xpectra 10")
    calc_xpectra = CalculadoraCBD(xpectra)
    gotas_xpectra = calc_xpectra.convertir_a_gotas(mg_por_toma)
    
    xatiplex_5 = catalogo.get_producto("Xatiplex 5")
    calc_5 = CalculadoraCBD(xatiplex_5)
    ml_5 = calc_5.convertir_a_ml(mg_por_toma)
    
    xatiplex_10 = catalogo.get_producto("Xatiplex 10")
    calc_10 = CalculadoraCBD(xatiplex_10)
    ml_10 = calc_10.convertir_a_ml(mg_por_toma)
    
    xatiplex_15 = catalogo.get_producto("Xatiplex 15")
    calc_15 = CalculadoraCBD(xatiplex_15)
    ml_15 = calc_15.convertir_a_ml(mg_por_toma)
    
    xatiplex_20 = catalogo.get_producto("Xatiplex 20")
    calc_20 = CalculadoraCBD(xatiplex_20)
    ml_20 = calc_20.convertir_a_ml(mg_por_toma)
    
    # Determinar la cantidad para el producto seleccionado
    producto_nombre = pauta['producto']
    if "Xpectra" in producto_nombre:
        cantidad_seleccionada = f"{gotas_xpectra:.1f} gotas" if gotas_xpectra else f"{pauta['dosis_por_toma_ml']:.3f} ml"
    else:
        cantidad_seleccionada = f"{pauta['dosis_por_toma_ml']:.3f} ml"
    
    # Construir HTML
    fecha = datetime.now().strftime("%d/%m/%Y")
    
    # Logo HTML
    logo_html = ""
    if logo_base64:
        logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" alt="Greenmed" style="height: 50px;">'
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Receta Greenmed</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: Arial, Helvetica, sans-serif;
                background: white;
                margin: 0;
                padding: 15px;
            }}
            .receta {{
                max-width: 850px;
                margin: 0 auto;
                background: white;
                padding: 20px 25px;
                border: 2px solid #2E7D32;
                border-radius: 10px;
                page-break-after: avoid;
                font-size: 14px;
            }}
            /* Header */
            .header {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-bottom: 2px solid #2E7D32;
                padding-bottom: 10px;
                margin-bottom: 12px;
            }}
            .header-left {{
                display: flex;
                align-items: center;
                gap: 12px;
            }}
            .header-left img {{
                height: 50px;
            }}
            .header-title h1 {{
                color: #2E7D32;
                font-size: 18px;
                margin: 0;
            }}
            .header-title p {{
                color: #666;
                font-size: 11px;
                margin: 0;
            }}
            .header-right {{
                text-align: right;
                font-size: 11px;
                color: #555;
                line-height: 1.4;
            }}
            /* Secciones */
            .seccion {{
                margin-bottom: 10px;
                padding: 8px 12px;
                background: #f9f9f9;
                border-radius: 6px;
                border-left: 4px solid #2E7D32;
            }}
            .seccion-titulo {{
                font-weight: bold;
                font-size: 13px;
                color: #2E7D32;
                margin-bottom: 4px;
            }}
            .seccion-contenido {{
                font-size: 13px;
                color: #333;
                line-height: 1.5;
            }}
            /* Recuadro verde (dosis principal) */
            .dosis-principal {{
                background-color: #e8f5e9;
                padding: 12px 15px;
                border-radius: 8px;
                border: 2px solid #4CAF50;
                text-align: center;
                margin-bottom: 12px;
            }}
            .dosis-principal .producto {{
                font-size: 18px;
                font-weight: bold;
                color: #2E7D32;
            }}
            .dosis-principal .dosis {{
                font-size: 16px;
                color: #333;
                margin-top: 4px;
            }}
            .dosis-principal .detalle {{
                font-size: 12px;
                color: #666;
                margin-top: 2px;
            }}
            /* Tabla de equivalencias */
            .tabla-equivalencias {{
                width: 100%;
                border-collapse: collapse;
                font-size: 12px;
                margin-top: 4px;
            }}
            .tabla-equivalencias th {{
                background-color: #2E7D32;
                color: white;
                padding: 5px 8px;
                text-align: left;
                font-size: 11px;
            }}
            .tabla-equivalencias td {{
                padding: 4px 8px;
                border-bottom: 1px solid #ddd;
            }}
            .tabla-equivalencias .resaltado {{
                background-color: #fff3e0;
                font-weight: bold;
                border-left: 3px solid #FF9800;
            }}
            /* Observaciones */
            .observaciones {{
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 8px 10px;
                min-height: 50px;
                font-size: 13px;
                background: white;
                margin-top: 2px;
            }}
            .observaciones p {{
                margin: 0;
            }}
            .observaciones .placeholder {{
                color: #999;
                font-style: italic;
            }}
            /* Firma */
            .firma {{
                text-align: center;
                margin-top: 12px;
                padding-top: 10px;
                border-top: 1px solid #ddd;
            }}
            .firma-linea {{
                display: inline-block;
                width: 200px;
                border-bottom: 2px solid #333;
                padding-bottom: 3px;
                font-size: 12px;
                margin-top: 5px;
            }}
            .firma-sello {{
                display: inline-block;
                width: 100px;
                height: 60px;
                border: 2px dashed #999;
                margin-top: 8px;
                font-size: 10px;
                color: #999;
                line-height: 60px;
            }}
            .footer-receta {{
                text-align: center;
                font-size: 9px;
                color: #999;
                margin-top: 10px;
                padding-top: 6px;
                border-top: 1px solid #eee;
            }}
            /* Responsive */
            @media print {{
                body {{
                    padding: 0;
                }}
                .receta {{
                    border: 1px solid #2E7D32;
                    border-radius: 5px;
                    padding: 15px 20px;
                    max-width: 100%;
                }}
                .no-print {{
                    display: none !important;
                }}
                .firma-linea {{
                    border-bottom: 2px solid #333;
                }}
                .tabla-equivalencias .resaltado {{
                    background-color: #fff3e0 !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }}
                .dosis-principal {{
                    background-color: #e8f5e9 !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }}
                .seccion {{
                    background: #f9f9f9 !important;
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }}
            }}
            @media screen and (max-width: 600px) {{
                .receta {{
                    padding: 12px 15px;
                }}
                .header {{
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 6px;
                }}
                .header-right {{
                    text-align: left;
                    width: 100%;
                }}
                .dosis-principal .producto {{
                    font-size: 16px;
                }}
                .dosis-principal .dosis {{
                    font-size: 14px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="receta">
            <!-- HEADER -->
            <div class="header">
                <div class="header-left">
                    {logo_html}
                    <div class="header-title">
                        <h1>Greenmed</h1>
                        <p>Prescripción de Cannabinoides</p>
                    </div>
                </div>
                <div class="header-right">
                    <div><strong>Fecha:</strong> {fecha}</div>
                    <div><strong>Receta Nº:</strong> {datetime.now().strftime("%Y%m%d%H%M")}</div>
                </div>
            </div>
            
            <!-- PACIENTE -->
            <div class="seccion">
                <div class="seccion-titulo">Datos del Paciente</div>
                <div class="seccion-contenido">
                    <strong>Nombre:</strong> {pauta.get('paciente_nombre', 'No especificado')}
                    &nbsp;&nbsp;|&nbsp;&nbsp;
                    <strong>Peso:</strong> {pauta['peso']:.1f} kg
                    &nbsp;&nbsp;|&nbsp;&nbsp;
                    <strong>Edad:</strong> _____
                </div>
            </div>
            
            <!-- DOSIS PRINCIPAL (Recuadro Verde) -->
            <div class="dosis-principal">
                <div class="producto">✅ {pauta['producto']} ({pauta['concentracion']}%)</div>
                <div class="dosis">{cantidad_seleccionada} • {pauta['tomas_por_dia']} veces al día</div>
                <div class="detalle">Presentación: {pauta['presentacion']}</div>
            </div>
            
            <!-- EQUIVALENCIAS -->
            <div class="seccion">
                <div class="seccion-titulo">Equivalencias (por toma)</div>
                <div class="seccion-contenido">
                    <table class="tabla-equivalencias">
                        <thead>
                            <tr>
                                <th>Producto</th>
                                <th>Cantidad por toma</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="{'resaltado' if 'Xpectra' in producto_nombre else ''}">
                                <td>Xpectra 10</td>
                                <td>{f"{gotas_xpectra:.1f} gotas" if gotas_xpectra else f"{pauta['dosis_por_toma_ml']:.3f} ml"}</td>
                            </tr>
                            <tr class="{'resaltado' if producto_nombre == 'Xatiplex 5' else ''}">
                                <td>Xatiplex 5</td>
                                <td>{ml_5:.3f} ml</td>
                            </tr>
                            <tr class="{'resaltado' if producto_nombre == 'Xatiplex 10' else ''}">
                                <td>Xatiplex 10</td>
                                <td>{ml_10:.3f} ml</td>
                            </tr>
                            <tr class="{'resaltado' if producto_nombre == 'Xatiplex 15' else ''}">
                                <td>Xatiplex 15</td>
                                <td>{ml_15:.3f} ml</td>
                            </tr>
                            <tr class="{'resaltado' if producto_nombre == 'Xatiplex 20' else ''}">
                                <td>Xatiplex 20</td>
                                <td>{ml_20:.3f} ml</td>
                            </tr>
                        </tbody>
                    </table>
                    <div style="font-size: 11px; color: #888; margin-top: 4px;">
                        💡 El paciente debe usar SOLO UNO de estos productos.
                    </div>
                </div>
            </div>
            
            <!-- OBSERVACIONES -->
            <div class="seccion" style="margin-bottom: 8px;">
                <div class="seccion-titulo">Observaciones</div>
                <div class="observaciones">
                    {f'<p>{observaciones}</p>' if observaciones else '<p class="placeholder">(Espacio para observaciones del médico)</p>'}
                </div>
            </div>
            
            <!-- FIRMA -->
            <div class="firma">
                <div style="margin-bottom: 8px;">
                    <div class="firma-linea">Firma del Médico</div>
                </div>
                <div>
                    <div class="firma-sello">[SELLO]</div>
                </div>
            </div>
            
            <!-- FOOTER -->
            <div class="footer-receta">
                Documento generado por Calculadora CBD Greenmed v1.0 - {datetime.now().strftime("%d/%m/%Y %H:%M")}
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def generar_receta_texto(pauta: Dict, observaciones: str = "", producto_recetado: str = "") -> str:
    """Versión en texto plano (para compatibilidad)"""
    return "Receta generada. Use la versión HTML para visualizar."

"""
Módulo para generar la receta médica en formato texto
"""

from datetime import datetime
from typing import Dict

def generar_receta_texto(pauta: Dict, observaciones: str = "", producto_recetado: str = "") -> str:
    """
    Genera una receta médica en formato texto
    
    Args:
        pauta: Diccionario con la pauta de administración
        observaciones: Observaciones del médico
        producto_recetado: Producto específico que el médico receta
    
    Returns:
        String con la receta formateada
    """
    # Verificar si tiene gotas
    tiene_gotas = "dosis_por_toma_gotas" in pauta
    
    # Construir tabla de equivalencias
    tabla = """
┌────────────────────┬────────────────────┬───────────────────────────┐
│     PRODUCTO       │    POR TOMA        │   ADMINISTRACIÓN          │
├────────────────────┼────────────────────┼───────────────────────────┤
"""
    
    # Xpectra 10
    if tiene_gotas:
        tabla += f"""│  Xpectra 10        │  {pauta['dosis_por_toma_ml']:.2f} ml           │  {pauta['dosis_por_toma_gotas']:.1f} gotas (gotero)    │
│  (10% Full Spec.)  │                    │                           │
├────────────────────┼────────────────────┼───────────────────────────┤
"""
    else:
        tabla += f"""│  Xpectra 10        │  {pauta['dosis_por_toma_ml']:.2f} ml           │  Gotero                   │
│  (10% Full Spec.)  │                    │                           │
├────────────────────┼────────────────────┼───────────────────────────┤
"""
    
    # Calcular para todos los Xatiplex
    from productos import CatalogoProductos
    from calculos import CalculadoraCBD
    
    catalogo = CatalogoProductos()
    
    # Xatiplex 5
    prod = catalogo.get_producto("Xatiplex 5")
    calc = CalculadoraCBD(prod)
    ml_5 = calc.convertir_a_ml(pauta['dosis_por_toma_mg'])
    tabla += f"""│  Xatiplex 5        │  {ml_5:.2f} ml           │  Jeringa                  │
│  (5% Isolado)      │                    │                           │
├────────────────────┼────────────────────┼───────────────────────────┤
"""
    
    # Xatiplex 10
    prod = catalogo.get_producto("Xatiplex 10")
    calc = CalculadoraCBD(prod)
    ml_10 = calc.convertir_a_ml(pauta['dosis_por_toma_mg'])
    tabla += f"""│  Xatiplex 10       │  {ml_10:.2f} ml           │  Jeringa                  │
│  (10% Isolado)     │                    │                           │
├────────────────────┼────────────────────┼───────────────────────────┤
"""
    
    # Xatiplex 15
    prod = catalogo.get_producto("Xatiplex 15")
    calc = CalculadoraCBD(prod)
    ml_15 = calc.convertir_a_ml(pauta['dosis_por_toma_mg'])
    tabla += f"""│  Xatiplex 15       │  {ml_15:.2f} ml           │  Jeringa                  │
│  (15% Isolado)     │                    │                           │
├────────────────────┼────────────────────┼───────────────────────────┤
"""
    
    # Xatiplex 20
    prod = catalogo.get_producto("Xatiplex 20")
    calc = CalculadoraCBD(prod)
    ml_20 = calc.convertir_a_ml(pauta['dosis_por_toma_mg'])
    tabla += f"""│  Xatiplex 20       │  {ml_20:.2f} ml           │  Jeringa                  │
│  (20% Isolado)     │                    │                           │
└────────────────────┴────────────────────┴───────────────────────────┘
"""
    
    # Construir la receta completa
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    receta = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                         🌿 GREENMED LABORATORIOS                            ║
║                   PRESCRIPCIÓN DE CANNABINOIDES                             ║
║                                                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────────┐
│  📋 DATOS DEL PACIENTE                                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│  Nombre:  {pauta.get('paciente_nombre', 'No especificado')}{' ' * (50 - len(pauta.get('paciente_nombre', 'No especificado')))}Fecha: {fecha[:10]} │
│  Peso:    {pauta['peso']:.1f} kg{' ' * (50 - len(f'{pauta["peso"]:.1f} kg'))}Edad:  ____           │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│  💊 INDICACIÓN                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  Dosis:  {pauta['dosis_por_kg']:.1f} mg/kg/día{' ' * (15)}→   {pauta['dosis_diaria_mg']:.0f} mg/día{' ' * (10)}│
│  Administrar:  {pauta['dosis_por_toma_mg']:.0f} mg cada 12 horas (BID)                 │
│                                                                            │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│  📊 EQUIVALENCIAS SEGÚN PRODUCTO                                           │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
{tabla}
│                                                                            │
│  💡 El paciente debe usar SOLO UNO de estos productos.                      │
│                                                                            │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│  📝 OBSERVACIONES                                                           │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  {observaciones if observaciones else '  __________________________________________________________________________'}
│  {'' if observaciones else '  __________________________________________________________________________'}
│  {'' if observaciones else '  __________________________________________________________________________'}
│  {'' if observaciones else '  __________________________________________________________________________'}
│                                                                            │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                          FIRMA Y SELLO                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│                              _________________________                     │
│                              Firma del Médico                               │
│                                                                            │
│                              [         SELLO         ]                     │
│                                                                            │
└──────────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
📱 Generado por Calculadora CBD Greenmed v1.0 - {fecha}
────────────────────────────────────────────────────────────────────────────────
"""
    
    return receta

def generar_receta_html(pauta: Dict, observaciones: str = "", producto_recetado: str = "") -> str:
    """
    Genera una receta médica en formato HTML para visualización web
    
    Args:
        pauta: Diccionario con la pauta de administración
        observaciones: Observaciones del médico
        producto_recetado: Producto específico que el médico receta
    
    Returns:
        String con la receta en HTML
    """
    # Verificar si tiene gotas
    tiene_gotas = "dosis_por_toma_gotas" in pauta
    
    # Construir tabla HTML
    tabla_html = """
    <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
        <thead>
            <tr style="background-color: #2E7D32; color: white;">
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">PRODUCTO</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: center;">POR TOMA</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: center;">ADMINISTRACIÓN</th>
            </tr>
        </thead>
        <tbody>
    """
    
    # Xpectra 10
    if tiene_gotas:
        tabla_html += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Xpectra 10</strong><br><span style="font-size: 0.8rem; color: #666;">(10% Full Spectrum)</span></td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">{pauta['dosis_por_toma_ml']:.2f} ml</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">{pauta['dosis_por_toma_gotas']:.1f} gotas (gotero)</td>
            </tr>
        """
    else:
        # Si el producto actual es Xpectra, mostrar gotas
        if pauta.get('producto') == "Xpectra 10":
            tabla_html += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Xpectra 10</strong><br><span style="font-size: 0.8rem; color: #666;">(10% Full Spectrum)</span></td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">{pauta['dosis_por_toma_ml']:.2f} ml</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">Gotero</td>
            </tr>
            """
    
    # Calcular para Xatiplex
    from productos import CatalogoProductos
    from calculos import CalculadoraCBD
    
    catalogo = CatalogoProductos()
    
    xatiplex_list = [
        ("Xatiplex 5", "5% Isolado"),
        ("Xatiplex 10", "10% Isolado"),
        ("Xatiplex 15", "15% Isolado"),
        ("Xatiplex 20", "20% Isolado")
    ]
    
    for nombre, desc in xatiplex_list:
        prod = catalogo.get_producto(nombre)
        calc = CalculadoraCBD(prod)
        ml = calc.convertir_a_ml(pauta['dosis_por_toma_mg'])
        tabla_html += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>{nombre}</strong><br><span style="font-size: 0.8rem; color: #666;">({desc})</span></td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">{ml:.2f} ml</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">Jeringa</td>
            </tr>
        """
    
    tabla_html += """
        </tbody>
    </table>
    """
    
    # Construir HTML completo
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: white; border: 2px solid #2E7D32; border-radius: 10px;">
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #2E7D32, #4CAF50); color: white; border-radius: 8px; margin-bottom: 20px;">
            <h1 style="margin: 0; font-size: 2rem;">🌿 GREENMED LABORATORIOS</h1>
            <p style="margin: 5px 0 0 0; font-size: 1.2rem;">PRESCRIPCIÓN DE CANNABINOIDES</p>
        </div>
        
        <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="margin: 0 0 10px 0; color: #2E7D32;">📋 DATOS DEL PACIENTE</h3>
            <div style="display: flex; justify-content: space-between;">
                <span><strong>Nombre:</strong> {pauta.get('paciente_nombre', 'No especificado')}</span>
                <span><strong>Fecha:</strong> {fecha[:10]}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                <span><strong>Peso:</strong> {pauta['peso']:.1f} kg</span>
                <span><strong>Edad:</strong> _____</span>
            </div>
        </div>
        
        <div style="background: #e8f5e9; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 5px solid #2E7D32;">
            <h3 style="margin: 0 0 10px 0; color: #2E7D32;">💊 INDICACIÓN</h3>
            <p style="margin: 5px 0;">
                <strong>Dosis:</strong> {pauta['dosis_por_kg']:.1f} mg/kg/día → {pauta['dosis_diaria_mg']:.0f} mg/día
            </p>
            <p style="margin: 5px 0;">
                <strong>Administrar:</strong> {pauta['dosis_por_toma_mg']:.0f} mg cada 12 horas (BID)
            </p>
        </div>
        
        <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="margin: 0 0 10px 0; color: #2E7D32;">📊 EQUIVALENCIAS SEGÚN PRODUCTO</h3>
            {tabla_html}
            <p style="margin-top: 10px; font-size: 0.9rem; color: #666;">
                💡 El paciente debe usar SOLO UNO de estos productos.
            </p>
        </div>
        
        <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="margin: 0 0 10px 0; color: #2E7D32;">📝 OBSERVACIONES</h3>
            <div style="min-height: 80px; padding: 10px; background: white; border: 1px solid #ddd; border-radius: 5px;">
                {observaciones if observaciones else '<span style="color: #999;">(Escriba aquí sus observaciones)</span>'}
            </div>
        </div>
        
        <div style="text-align: center; padding: 20px; border-top: 2px solid #2E7D32; margin-top: 20px;">
            <div style="margin: 20px 0;">
                <div style="display: inline-block; width: 250px; border-bottom: 2px solid #333; padding-bottom: 5px;">
                    Firma del Médico
                </div>
                <br>
                <div style="display: inline-block; width: 150px; height: 80px; border: 2px dashed #999; margin-top: 10px; padding: 10px;">
                    [SELLO]
                </div>
            </div>
        </div>
        
        <div style="text-align: center; font-size: 0.8rem; color: #999; margin-top: 20px; padding-top: 10px; border-top: 1px solid #ddd;">
            📱 Generado por Calculadora CBD Greenmed v1.0 - {fecha}
        </div>
    </div>
    """
    
    return html

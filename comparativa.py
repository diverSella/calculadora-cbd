"""
Tabla comparativa entre Xpectra y Xatiplex
Muestra equivalencias de gotas de Xpectra a ml de Xatiplex
"""

import pandas as pd
from productos import CatalogoProductos
from calculos import CalculadoraCBD

def tabla_equivalencias():
    """
    Genera tabla de equivalencias donde las columnas son gotas de Xpectra
    y las filas son los productos Xatiplex mostrando ml equivalentes
    """
    catalogo = CatalogoProductos()
    
    # Obtener productos
    xpectra = catalogo.get_producto("Xpectra 10")
    xatiplex_5 = catalogo.get_producto("Xatiplex 5")
    xatiplex_10 = catalogo.get_producto("Xatiplex 10")
    xatiplex_15 = catalogo.get_producto("Xatiplex 15")
    xatiplex_20 = catalogo.get_producto("Xatiplex 20")
    
    # Calcular mg por gota de Xpectra
    calc_xpectra = CalculadoraCBD(xpectra)
    mg_por_gota = calc_xpectra.mg_por_gota
    
    # Definir las gotas a mostrar (por toma)
    gotas = [1, 2, 5, 10, 15, 20, 25, 30, 40, 50, 56, 60, 70, 80, 90, 100]
    
    # Calcular mg para cada cantidad de gotas
    mg_por_gotas = [gota * mg_por_gota for gota in gotas]
    
    # Preparar datos para cada producto Xatiplex
    datos = {}
    
    # Xpectra (primera fila - muestra gotas)
    datos["Xpectra 10"] = [f"{g} gotas" for g in gotas]
    
    # Xatiplex 5
    calc_5 = CalculadoraCBD(xatiplex_5)
    datos["Xatiplex 5"] = [f"{calc_5.convertir_a_ml(mg):.2f} mL" for mg in mg_por_gotas]
    
    # Xatiplex 10
    calc_10 = CalculadoraCBD(xatiplex_10)
    datos["Xatiplex 10"] = [f"{calc_10.convertir_a_ml(mg):.2f} mL" for mg in mg_por_gotas]
    
    # Xatiplex 15
    calc_15 = CalculadoraCBD(xatiplex_15)
    datos["Xatiplex 15"] = [f"{calc_15.convertir_a_ml(mg):.2f} mL" for mg in mg_por_gotas]
    
    # Xatiplex 20
    calc_20 = CalculadoraCBD(xatiplex_20)
    datos["Xatiplex 20"] = [f"{calc_20.convertir_a_ml(mg):.2f} mL" for mg in mg_por_gotas]
    
    # Crear DataFrame
    df = pd.DataFrame(datos)
    
    # Reordenar columnas: Xpectra primero, luego Xatiplex
    columnas = ["Xpectra 10", "Xatiplex 5", "Xatiplex 10", "Xatiplex 15", "Xatiplex 20"]
    df = df[columnas]
    
    return df, gotas

def mostrar_comparativa():
    """Mostrar la tabla comparativa formateada"""
    df, gotas = tabla_equivalencias()
    
    print("=" * 80)
    print("TABLA DE EQUIVALENCIAS")
    print("=" * 80)
    print("\n📊 Correspondencia entre gotas de Xpectra 10 y ml de Xatiplex (por toma)")
    print(f"\n{df.to_string(index=False)}")
    
    print("\n" + "=" * 80)
    print("📌 NOTAS:")
    print("• Xpectra 10: 32 gotas/ml (Full Spectrum)")
    print("• Xatiplex: Administración con jeringa")
    print("• Los valores están redondeados a 2 decimales")
    print("• Las dosis son por TOMA (cada 12 horas)")
    print("=" * 80)

if __name__ == "__main__":
    mostrar_comparativa()

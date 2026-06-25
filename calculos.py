"""
Módulo de cálculos para dosificación de CBD
"""

from typing import Dict, Tuple, Optional
from productos import Producto

class CalculadoraCBD:
    """Calculadora de dosis de CBD"""
    
    # Rango terapéutico según Epidiolex® (mg/kg/día)
    DOSIS_MINIMA = 2.5  # mg/kg/día
    DOSIS_MAXIMA = 20.0  # mg/kg/día
    DOSIS_INICIAL = 2.5  # mg/kg/día
    DOSIS_MANTENIMIENTO = 5.0  # mg/kg/día
    
    def __init__(self, producto: Producto):
        self.producto = producto
        self.mg_por_ml = self._calcular_mg_por_ml()
        self.mg_por_gota = self._calcular_mg_por_gota() if producto.gotas_por_ml else None
    
    def _calcular_mg_por_ml(self) -> float:
        """Calcular mg de CBD por ml según concentración"""
        # 1 ml = 1000 mg, concentración en porcentaje
        return (self.producto.concentracion / 100) * 1000
    
    def _calcular_mg_por_gota(self) -> Optional[float]:
        """Calcular mg de CBD por gota (solo para goteros)"""
        if self.producto.gotas_por_ml:
            return self.mg_por_ml / self.producto.gotas_por_ml
        return None
    
    def calcular_dosis_diaria(self, peso_kg: float, dosis_por_kg: float) -> Dict:
        """
        Calcular dosis diaria total en mg
        
        Args:
            peso_kg: Peso del paciente en kg
            dosis_por_kg: Dosis en mg/kg/día
            
        Returns:
            Diccionario con dosis total diaria en mg
        """
        dosis_mg = peso_kg * dosis_por_kg
        return {
            "dosis_mg": round(dosis_mg, 2),
            "dosis_por_kg": dosis_por_kg
        }
    
    def convertir_a_ml(self, mg: float) -> float:
        """Convertir mg a ml"""
        return mg / self.mg_por_ml
    
    def convertir_a_gotas(self, mg: float) -> Optional[float]:
        """Convertir mg a gotas (solo para goteros)"""
        if self.mg_por_gota:
            return mg / self.mg_por_gota
        return None
    
    def calcular_dosis_por_toma(self, mg_diarios: float, tomas_por_dia: int = 2) -> Dict:
        """
        Calcular dosis por toma
        
        Args:
            mg_diarios: Dosis diaria total en mg
            tomas_por_dia: Número de tomas al día
            
        Returns:
            Diccionario con dosis por toma en mg, ml y gotas (si aplica)
        """
        mg_por_toma = mg_diarios / tomas_por_dia
        ml_por_toma = self.convertir_a_ml(mg_por_toma)
        gotas_por_toma = self.convertir_a_gotas(mg_por_toma) if self.mg_por_gota else None
        
        resultado = {
            "mg_por_toma": round(mg_por_toma, 2),
            "ml_por_toma": round(ml_por_toma, 3),
        }
        
        if gotas_por_toma is not None:
            resultado["gotas_por_toma"] = round(gotas_por_toma, 1)
        
        return resultado
    
    def calcular_pauta_completa(self, peso_kg: float, dosis_por_kg: float) -> Dict:
        """
        Calcular pauta completa de administración
        
        Args:
            peso_kg: Peso del paciente en kg
            dosis_por_kg: Dosis en mg/kg/día
            
        Returns:
            Diccionario con toda la información de la pauta
        """
        # Calcular dosis diaria
        dosis_diaria = self.calcular_dosis_diaria(peso_kg, dosis_por_kg)
        mg_diarios = dosis_diaria["dosis_mg"]
        
        # Calcular dosis por toma (BID)
        dosis_toma = self.calcular_dosis_por_toma(mg_diarios, 2)
        
        # Calcular volumen total mensual (30 días)
        ml_mensual = self.convertir_a_ml(mg_diarios * 30)
        
        resultado = {
            "peso": peso_kg,
            "dosis_por_kg": dosis_por_kg,
            "dosis_diaria_mg": mg_diarios,
            "dosis_por_toma_mg": dosis_toma["mg_por_toma"],
            "dosis_por_toma_ml": dosis_toma["ml_por_toma"],
            "tomas_por_dia": 2,
            "ml_por_dia": self.convertir_a_ml(mg_diarios),
            "ml_mensual": round(ml_mensual, 2),
            "mg_por_ml": round(self.mg_por_ml, 2),
            "producto": self.producto.nombre,
            "concentracion": self.producto.concentracion,
            "tipo": self.producto.tipo,
            "presentacion": self.producto.presentacion
        }
        
        # Agregar información de gotas si está disponible
        if "gotas_por_toma" in dosis_toma:
            resultado["dosis_por_toma_gotas"] = dosis_toma["gotas_por_toma"]
            resultado["mg_por_gota"] = round(self.mg_por_gota, 3)
        
        return resultado
    
    def obtener_rangos_recomendados(self) -> Dict:
        """Obtener rangos de dosis recomendados"""
        return {
            "inicial": self.DOSIS_INICIAL,
            "mantenimiento": self.DOSIS_MANTENIMIENTO,
            "minimo": self.DOSIS_MINIMA,
            "maximo": self.DOSIS_MAXIMA
        }

def validar_dosis(dosis_por_kg: float, peso_kg: float) -> Tuple[bool, str]:
    """
    Validar que la dosis esté dentro del rango terapéutico
    
    Returns:
        (es_valido, mensaje)
    """
    if peso_kg <= 0:
        return False, "El peso debe ser mayor a 0 kg"
    
    if dosis_por_kg < CalculadoraCBD.DOSIS_MINIMA:
        return False, f"La dosis es menor al mínimo recomendado ({CalculadoraCBD.DOSIS_MINIMA} mg/kg/día)"
    
    if dosis_por_kg > CalculadoraCBD.DOSIS_MAXIMA:
        return False, f"La dosis excede el máximo recomendado ({CalculadoraCBD.DOSIS_MAXIMA} mg/kg/día)"
    
    if dosis_por_kg < CalculadoraCBD.DOSIS_INICIAL:
        return True, "Dosis inicial baja. Considere titulación gradual."
    
    if dosis_por_kg <= CalculadoraCBD.DOSIS_MANTENIMIENTO:
        return True, "Dosis dentro del rango de mantenimiento estándar."
    
    return True, "Dosis alta. Requiere monitoreo estrecho."

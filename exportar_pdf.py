"""
Módulo para exportar recetas a PDF
"""

from weasyprint import HTML
from datetime import datetime
import tempfile
import os

def exportar_pdf(html_content: str, nombre_paciente: str = "paciente") -> str:
    """
    Convierte HTML a PDF y guarda en archivo temporal
    
    Args:
        html_content: Contenido HTML de la receta
        nombre_paciente: Nombre del paciente para el nombre del archivo
    
    Returns:
        Ruta del archivo PDF generado
    """
    # Limpiar nombre para el archivo
    nombre_limpio = nombre_paciente.replace(' ', '_') if nombre_paciente else "paciente"
    fecha = datetime.now().strftime('%Y%m%d_%H%M')
    nombre_archivo = f"receta_{nombre_limpio}_{fecha}.pdf"
    
    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        pdf_path = tmp.name
    
    # Generar PDF con mejor formato
    HTML(string=html_content).write_pdf(
        pdf_path,
        stylesheets=None,
        presentational_hints=True,
        optimize_size=('fonts', 'images')
    )
    
    return pdf_path

def generar_pdf_bytes(html_content: str) -> bytes:
    """
    Genera PDF en memoria (bytes) para descarga directa
    
    Args:
        html_content: Contenido HTML de la receta
    
    Returns:
        Bytes del archivo PDF
    """
    return HTML(string=html_content).write_pdf(
        presentational_hints=True,
        optimize_size=('fonts', 'images')
    )

"""
Calculadora de Dosis de CBD - Greenmed
Aplicación para profesionales de la salud
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from productos import CatalogoProductos
from calculos import CalculadoraCBD, validar_dosis
from comparativa import tabla_equivalencias
from receta import generar_receta_html
from exportar_pdf import generar_pdf_bytes


# Configuración de la página
st.set_page_config(
    page_title="Calculadora CBD - Greenmed",
    page_icon="💊",
    layout="wide"
)

# Título principal
st.title("💊 Calculadora de Dosis de CBD")
st.subheader("Laboratorios Greenmed - Basado en posología de Epidiolex®")
st.markdown("---")

# Inicializar catálogo
catalogo = CatalogoProductos()

# Inicializar variables en session_state
if 'dosis_personalizada' not in st.session_state:
    st.session_state.dosis_personalizada = 5.0
if 'dosis_comparativa' not in st.session_state:
    st.session_state.dosis_comparativa = 50.0
if 'observaciones' not in st.session_state:
    st.session_state.observaciones = ""
if 'receta_generada' not in st.session_state:
    st.session_state.receta_generada = False
if 'receta_html' not in st.session_state:
    st.session_state.receta_html = ""

# Sidebar - Datos del paciente
with st.sidebar:
    st.header("📋 Datos del Paciente")
    
    paciente_nombre = st.text_input("Nombre del paciente", placeholder="Ej: Juan Pérez")
    peso = st.number_input(
        "Peso (kg)",
        min_value=0.5,
        max_value=300.0,
        value=70.0,
        step=0.5,
        help="Ingrese el peso del paciente en kilogramos"
    )
    
    st.divider()
    
    st.subheader("💊 Producto Greenmed")
    producto_nombre = st.selectbox(
        "Seleccione el producto",
        catalogo.listar_productos()
    )
    
    producto = catalogo.get_producto(producto_nombre)
    
    if producto:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Concentración", f"{producto.concentracion}%")
        with col2:
            st.metric("Presentación", producto.presentacion)
        
        st.info(f"**Descripción:** {producto.descripcion}")
    
    st.divider()
    
    st.subheader("⚙️ Configuración")
    tomas_por_dia = st.selectbox(
        "Tomas por día",
        [1, 2, 3, 4],
        index=1,
        help="Número de administraciones diarias"
    )

# Área principal - Pestañas
tab1, tab2, tab3 = st.tabs(["📋 Calculadora de Dosis", "📊 Tabla de Equivalencias", "📝 Receta Médica"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 Selección de Dosis")
        
        dosis_tipo = st.radio(
            "Tipo de dosis",
            ["Dosis estándar (Epidiolex®)", "Dosis personalizada"],
            horizontal=True
        )
        
        if dosis_tipo == "Dosis estándar (Epidiolex®)":
            dosis_por_kg = st.select_slider(
                "Dosis (mg/kg/día)",
                options=[2.5, 5.0, 10.0, 15.0, 20.0],
                value=5.0
            )
            
            st.info("""
            **Rango terapéutico Epidiolex®:**
            - Dosis inicial: 2.5 mg/kg/día
            - Dosis de mantenimiento: 5-10 mg/kg/día
            - Dosis máxima: 20 mg/kg/día
            """)
        else:
            st.markdown("**Dosis rápidas:**")
            col_rapidas = st.columns(5)
            
            dosis_rapidas = [2.5, 5.0, 10.0, 15.0, 20.0]
            for i, dosis in enumerate(dosis_rapidas):
                with col_rapidas[i]:
                    if st.button(f"{dosis} mg/kg", key=f"dosis_{dosis}"):
                        st.session_state.dosis_personalizada = float(dosis)
                        st.rerun()
            
            dosis_por_kg = st.number_input(
                "Dosis personalizada (mg/kg/día)",
                min_value=0.5,
                max_value=30.0,
                value=st.session_state.dosis_personalizada,
                step=0.5,
                help="Ingrese la dosis en mg/kg/día según su criterio clínico",
                key="dosis_input"
            )
            st.session_state.dosis_personalizada = float(dosis_por_kg)
    
    with col2:
        st.header("📊 Información del Producto")
        
        if producto:
            calculadora = CalculadoraCBD(producto)
            st.metric("CBD por ml", f"{calculadora.mg_por_ml:.2f} mg")
            
            if calculadora.mg_por_gota:
                st.metric("CBD por gota", f"{calculadora.mg_por_gota:.3f} mg")
                st.metric("Gotas por ml", f"{producto.gotas_por_ml} gotas")
            else:
                st.info("💉 Administración con jeringa - No aplican gotas")
    
    # Calcular y mostrar resultados
    if peso > 0 and producto:
        st.divider()
        
        es_valido, mensaje_validacion = validar_dosis(dosis_por_kg, peso)
        
        if not es_valido:
            st.error(f"⚠️ {mensaje_validacion}")
        else:
            st.success(f"✅ {mensaje_validacion}")
        
        calculadora = CalculadoraCBD(producto)
        pauta = calculadora.calcular_pauta_completa(peso, dosis_por_kg)
        
        st.header("📋 Pauta de Administración")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Dosis Diaria Total",
                f"{pauta['dosis_diaria_mg']:.1f} mg",
                help=f"{pauta['dosis_por_kg']:.1f} mg/kg/día"
            )
            st.metric(
                "Dosis por Toma",
                f"{pauta['dosis_por_toma_mg']:.2f} mg",
                help=f"{tomas_por_dia} tomas al día"
            )
        
        with col2:
            st.metric(
                "Volumen por Toma",
                f"{pauta['dosis_por_toma_ml']:.3f} ml"
            )
            if "dosis_por_toma_gotas" in pauta:
                st.metric(
                    "Gotas por Toma",
                    f"{pauta['dosis_por_toma_gotas']:.1f} gotas"
                )
            else:
                st.info("💉 Administrar con jeringa")
        
        with col3:
            st.metric(
                "Volumen Diario",
                f"{pauta['ml_por_dia']:.2f} ml"
            )
            st.metric(
                "Volumen Mensual (30 días)",
                f"{pauta['ml_mensual']:.1f} ml"
            )
        
        st.markdown("---")
        st.subheader("📋 Instrucciones de Administración")
        
        tiene_gotas = "dosis_por_toma_gotas" in pauta
        
        instrucciones = f"""
        **Producto:** {pauta['producto']} ({pauta['concentracion']}%, {pauta['tipo']})
        
        **Paciente:** {paciente_nombre if paciente_nombre else "No especificado"}
        **Peso:** {peso} kg
        
        **Dosis prescrita:** {pauta['dosis_por_kg']:.1f} mg/kg/día = {pauta['dosis_diaria_mg']:.1f} mg totales/día
        
        **Administración:** {tomas_por_dia} veces al día (cada {24/tomas_por_dia:.0f} horas)
        
        **Por toma administrar:**
        - {pauta['dosis_por_toma_mg']:.2f} mg de CBD
        - {pauta['dosis_por_toma_ml']:.3f} ml
        """
        
        if tiene_gotas:
            instrucciones += f"\n        - {pauta['dosis_por_toma_gotas']:.1f} gotas"
        
        instrucciones += f"\n\n        **Presentación:** {pauta['presentacion']}"
        
        st.markdown(instrucciones)
        
        # Tabla de titulación
        with st.expander("📊 Ver esquema de titulación sugerido"):
            st.markdown("**Titulación semanal (Epidiolex®):**")
            
            datos_titulacion = []
            for semana in range(1, 5):
                dosis_semana = min(pauta['dosis_por_kg'], 2.5 * semana)
                mg_diarios = peso * dosis_semana
                
                if tiene_gotas:
                    gotas_por_toma = (mg_diarios / tomas_por_dia) / calculadora.mg_por_gota
                    datos_titulacion.append({
                        "Semana": f"Semana {semana}",
                        "Dosis (mg/kg/día)": round(dosis_semana, 1),
                        "mg/día": round(mg_diarios, 1),
                        "ml/toma": round((mg_diarios / tomas_por_dia) / calculadora.mg_por_ml, 3),
                        "Gotas/toma": round(gotas_por_toma, 1)
                    })
                else:
                    datos_titulacion.append({
                        "Semana": f"Semana {semana}",
                        "Dosis (mg/kg/día)": round(dosis_semana, 1),
                        "mg/día": round(mg_diarios, 1),
                        "ml/toma": round((mg_diarios / tomas_por_dia) / calculadora.mg_por_ml, 3),
                        "Gotas/toma": "N/A (jeringa)"
                    })
            
            df_titulacion = pd.DataFrame(datos_titulacion)
            st.dataframe(df_titulacion, use_container_width=True, hide_index=True)

with tab2:
    st.header("📊 Tabla de Equivalencias")
    st.markdown("""
    Esta tabla muestra la correspondencia entre **gotas de Xpectra 10** y **ml de Xatiplex**.
    Útil para convertir rápidamente entre productos.
    """)
    
    # Generar tabla de equivalencias
    df_equivalencias, gotas = tabla_equivalencias()
    
    # Mostrar tabla con estilo mejorado
    st.dataframe(
        df_equivalencias,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Xpectra 10": st.column_config.TextColumn(
                "Xpectra 10 (10%)",
                help="Gotas de Xpectra 10 (32 gotas/ml)"
            ),
            "Xatiplex 5": st.column_config.TextColumn(
                "Xatiplex 5",
                help="ml de Xatiplex 5%"
            ),
            "Xatiplex 10": st.column_config.TextColumn(
                "Xatiplex 10",
                help="ml de Xatiplex 10%"
            ),
            "Xatiplex 15": st.column_config.TextColumn(
                "Xatiplex 15",
                help="ml de Xatiplex 15%"
            ),
            "Xatiplex 20": st.column_config.TextColumn(
                "Xatiplex 20",
                help="ml de Xatiplex 20%"
            )
        }
    )
    
    # Información adicional
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **💊 Xpectra 10 (Gotero)**
        - 32 gotas = 1 ml
        - Full Spectrum
        - Administración con gotero
        """)
    
    with col2:
        st.markdown("""
        **💉 Xatiplex (Jeringa)**
        - Administración con jeringa
        - Isolado de CBD
        - Mayor precisión en la dosis
        """)
    
    # Ejemplo práctico
    with st.expander("📖 Ver ejemplo de uso"):
        st.markdown("""
        **Ejemplo práctico:**
        
        Si el médico prescribe **10 gotas de Xpectra 10** y la farmacia solo tiene **Xatiplex 20**:
        
        1. Buscar en la tabla la columna "Xpectra 10" → fila "10 gotas"
        2. Leer el valor en la columna "Xatiplex 20" → **0.16 mL**
        3. Administrar **0.16 mL** de Xatiplex 20 con jeringa
        
        **Equivalencia:** 10 gotas de Xpectra 10 = 0.16 mL de Xatiplex 20
        """)

with tab3:
    st.header("📝 Receta Médica")
    st.markdown("""
    Complete los datos del paciente y la dosis en la pestaña **Calculadora de Dosis**,
    luego agregue sus observaciones y genere la receta.
    """)
    
    # Verificar que tenemos los datos necesarios
    if peso > 0 and producto:
        # Calcular pauta
        calculadora = CalculadoraCBD(producto)
        pauta = calculadora.calcular_pauta_completa(peso, dosis_por_kg)
        pauta['paciente_nombre'] = paciente_nombre if paciente_nombre else "No especificado"
        
        # Campo de observaciones
        st.subheader("📝 Observaciones")
        observaciones = st.text_area(
            "Escriba aquí sus observaciones, indicaciones adicionales o advertencias:",
            value=st.session_state.observaciones,
            height=100,
            placeholder="Ej: Iniciar con dosis baja. Evaluar respuesta en 2 semanas. Contraindicado con warfarina.",
            key="observaciones_input"
        )
        st.session_state.observaciones = observaciones
        
        # Botón para generar receta
        if st.button("🔄 Generar Receta", type="primary"):
            with st.spinner("Generando receta..."):
                receta_html = generar_receta_html(pauta, observaciones)
                st.session_state.receta_html = receta_html
                st.session_state.receta_generada = True
        
        # Mostrar receta si existe
        if st.session_state.get('receta_generada', False):
            st.divider()
            st.subheader("📋 Receta Generada")
            
            # Mostrar HTML
            st.components.v1.html(
                st.session_state.receta_html,
                height=600,
                scrolling=True
            )
            
            # Botones de acción
            st.divider()
            st.subheader("📤 Exportar")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                # Descargar HTML
                nombre_limpio = paciente_nombre.replace(' ', '_') if paciente_nombre else "paciente"
                fecha_actual = datetime.now().strftime('%Y%m%d')
                nombre_archivo_html = f"receta_{nombre_limpio}_{fecha_actual}.html"
                
                st.download_button(
                    label="📄 Descargar HTML",
                    data=st.session_state.receta_html,
                    file_name=nombre_archivo_html,
                    mime="text/html",
                    use_container_width=True
                )
            
            with col2:
                # Descargar PDF
                try:
                    pdf_bytes = generar_pdf_bytes(st.session_state.receta_html)
                    nombre_archivo_pdf = f"receta_{nombre_limpio}_{fecha_actual}.pdf"
                    
                    st.download_button(
                        label="📥 Descargar PDF",
                        data=pdf_bytes,
                        file_name=nombre_archivo_pdf,
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary"
                    )
                except Exception as e:
                    st.error(f"Error al generar PDF: {e}")
                    st.info("💡 Asegúrate de tener instalado weasyprint: pip install weasyprint")
            
            with col3:
                st.info("💡 El PDF se puede compartir directamente con el paciente por email o WhatsApp.")
    else:
        st.warning("⚠️ Primero complete los datos del paciente y seleccione un producto en la pestaña 'Calculadora de Dosis'.")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>⚠️ Esta herramienta es de apoyo para profesionales de la salud.</p>
    <p>La decisión final de prescripción es responsabilidad del médico tratante.</p>
    <p style="font-size: 0.8rem;">Greenmed | Basado en posología de Epidiolex® (FDA/EMA)</p>
</div>
""", unsafe_allow_html=True)

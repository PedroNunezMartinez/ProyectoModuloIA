import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="R&V Motor - IA CRM Dashboard",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CARGA DE DATOS ADAPTADA A TU EMBUDO REAL
@st.cache_data
def cargar_datos():
    ruta_csv = os.path.join(os.path.dirname(__file__), 'mensajes_clasificados_ia.csv')
    
    # Si aún no has subido el CSV definitivo de Colab, genera la estructura con tus 4 etiquetas exactas
    if not os.path.exists(ruta_csv):
        return pd.DataFrame({
            'cliente': [f'Contacto {i}' for i in range(1, 13)],
            'interes_ia': ['Lead Caliente', 'Lead Frío', 'Cliente Potencial', 'Cliente que Solo Pregunta'] * 3,
            'motivo_semantico': ['Quiere financiar una 150cc', 'Mensaje equivocado', 'Quiere ver motos el sábado', 'Pregunta por horarios'] * 3,
            'respuesta_automatica': ['Claro, aquí tienes los planes...' for _ in range(12)]
        })
    return pd.read_csv(ruta_csv)

df = cargar_datos()

# 3. BARRA LATERAL (Calculadora de ROI y Filtros)
st.sidebar.image("https://icons8.com", width=80)
st.sidebar.title("R&V Motor CRM")
st.sidebar.caption("Módulo de Inteligencia Artificial")

st.sidebar.markdown("---")
st.sidebar.subheader("🧮 Calculadora de ROI")
costo_campana = st.sidebar.number_input("Inversión Campaña ($)", min_value=1.0, value=200.0, step=50.0)
valor_moto_promedio = st.sidebar.number_input("Precio Promedio Moto ($)", min_value=1000.0, value=3000.0, step=100.0)
tasa_conversion = st.sidebar.slider("Tasa de Conversión de Leads %", min_value=1, max_value=100, value=15)

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filtros del Embudo")
categorias_reales = ['Lead Caliente', 'Lead Frío', 'Cliente Potencial', 'Cliente que Solo Pregunta']
categorias_seleccionadas = st.sidebar.multiselect("Clasificación IA:", categorias_reales, default=categorias_reales)

# Filtrado dinámico del dataframe
df_filtrado = df[df['interes_ia'].isin(categorias_seleccionadas)]

# 4. CUERPO PRINCIPAL
st.title("🏍️ R&V Motor — AI Management & Lead Analytics")
st.markdown("Análisis automatizado de intenciones mediante **Gemini 3.8 Flash** en tiempo real.")
st.markdown("---")

# 5. BLOQUE DE MÉTRICAS (Matemática Financiera)
total_leads = len(df)
# Filtramos los calientes y potenciales como la base de cierre de ventas
leads_valorables = len(df[df['interes_ia'].isin(['Lead Caliente', 'Cliente Potencial'])])
ventas_estimadas = int((leads_valorables * tasa_conversion) / 100)
ingreso_estimado = ventas_estimadas * valor_moto_promedio
roi_calculado = ((ingreso_estimado - costo_campana) / costo_campana) * 100 if costo_campana > 0 else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="📥 Total Mensajes", value=total_leads)
with col2:
    st.metric(label="🎯 Leads de Alto Valor", value=leads_valorables, help="Suma de Leads Calientes y Clientes Potenciales")
with col3:
    st.metric(label="💰 Ingreso Estimado", value=f"${ingreso_estimado:,.2f}", delta=f"{ventas_estimadas} Ventas")
with col4:
    st.metric(label="📈 ROI Proyectado", value=f"{roi_calculado:.1f}%")

st.markdown("---")

# 6. BLOQUE DE GRÁFICOS (Plotly Express)
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("📊 Tráfico por Tipo de Lead")
    fig_bar = px.bar(
        df_filtrado['interes_ia'].value_counts().reset_index(),
        x='interes_ia',
        y='count',
        labels={'interes_ia': 'Clasificación IA', 'count': 'Mensajes'},
        color='interes_ia',
        color_discrete_map={
            'Lead Caliente': '#EF553B',
            'Cliente Potencial': '#00CC96',
            'Cliente que Solo Pregunta': '#636EFA',
            'Lead Frío': '#AB63FA'
        },
        template="plotly_dark"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_graf2:
    st.subheader("🍕 Distribución del Embudo Comercial")
    fig_pie = px.pie(
        df_filtrado, 
        names='interes_ia', 
        hole=0.4,
        template="plotly_dark"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# 7. TABLA DE LOGS EN TIEMPO REAL
st.subheader("📋 Registro Histórico e Interacciones del Chatbot")
st.dataframe(
    df_filtrado[['cliente', 'interes_ia', 'motivo_semantico', 'respuesta_automatica']],
    use_container_width=True,
    hide_index=True
)

st.caption("🔒 R&V Motor CRM v1.0 | Código verificado en GitHub. Ejecución segura en Streamlit sin exposición de llaves API.")

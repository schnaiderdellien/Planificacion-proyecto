import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración de la página
st.set_page_config(layout="wide", page_title="Dashboard de Gestión de Proyecto")

# Título principal
st.title("Dashboard de Gestión de Proyecto")

# Carga de datos
@st.cache_data  # Cachear datos para mejor rendimiento
def load_data():
    grantt = pd.read_excel('Grantt.xlsx').sort_values(by='Task')
    riesgo = pd.read_excel('Tabla_de_riesgos.xlsx')
    planificacion = pd.read_excel('Planificacion_de_recursos.xlsx')
    costos = pd.read_excel('Estimacion_de_costos.xlsx')
    return grantt, riesgo, planificacion, costos

grantt, riesgo, planificacion, costos = load_data()

# Sidebar con información resumida
with st.sidebar:
    st.header("Resumen del Proyecto")
    total_costos = costos['Costo estimado'].sum()
    st.metric("Costo Total Estimado", f"${total_costos:,.2f}")
    
    progreso_promedio = grantt['progress'].mean() * 100
    st.metric("Progreso Promedio", f"{progreso_promedio:.1f}%")
    
    st.download_button(
        label="Descargar Datos Completos",
        data=pd.concat([grantt, riesgo, planificacion, costos]).to_csv(index=False).encode('utf-8'),
        file_name='datos_proyecto_completos.csv',
        mime='text/csv'
    )

# Pestañas principales
tab1, tab2, tab3, tab4 = st.tabs(["Diagrama de Gantt", "Riesgos", "Planificación", "Costos"])

with tab1:
    st.header("Diagrama de Gantt")
    
    # Gráfico de Gantt
    fig = px.timeline(
        grantt,
        x_start="start",
        x_end="end",
        y="Task",
        color="progress",
        color_continuous_scale=["red", "yellow", "green"],
        title="Cronograma del Proyecto"
    )
    
    fig.update_traces(
        text=grantt["Agent"],
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(color="black", size=12)
    )
    
    fig.update_yaxes(categoryorder="total ascending")
    fig.update_layout(
        height=600,
        hovermode="y unified",
        coloraxis_colorbar=dict(
            title="Progreso",
            tickformat=".0%",
        ),
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Gestión de Riesgos")
    st.dataframe(riesgo.style.highlight_max(axis=0, color='#ffcccc'), use_container_width=True)
    
    # Gráfico de riesgos por categoría
    if 'Categoría' in riesgo.columns:
        fig_riesgos = px.bar(
            riesgo['Categoría'].value_counts().reset_index(),
            x='index',
            y='Categoría',
            title="Riesgos por Categoría"
        )
        st.plotly_chart(fig_riesgos, use_container_width=True)

with tab3:
    st.header("Planificación de Recursos")
    st.dataframe(planificacion, use_container_width=True)
    
    # Gráfico de asignación de recursos
    if 'Recurso' in planificacion.columns:
        fig_recursos = px.pie(
            planificacion,
            names='Recurso',
            values='Horas asignadas',
            title="Distribución de Horas por Recurso"
        )
        st.plotly_chart(fig_recursos, use_container_width=True)

with tab4:
    st.header("Estimación de Costos")
    st.dataframe(costos, use_container_width=True)
    
    # Gráfico de distribución de costos
    if 'Concepto' in costos.columns:
        fig_costos = px.treemap(
            costos,
            path=['Concepto'],
            values='Costo estimado',
            title="Distribución de Costos"
        )
        st.plotly_chart(fig_costos, use_container_width=True)
        
        # Mostrar el total de costos
        st.subheader(f"Total estimado: ${total_costos:,.2f}")
import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración básica
st.set_page_config(layout="centered")
st.title("Dashboard de Proyecto")

# Cargar los datos
def cargar_datos():
    gantt = pd.read_excel('Grantt.xlsx').sort_values(by='Task')
    riesgo = pd.read_excel('Tabla_de_riesgos.xlsx')
    planificacion = pd.read_excel('Planificacion_de_recursos.xlsx')
    costos = pd.read_excel('Estimacion_de_costos.xlsx')
    return gantt, costos, riesgo, planificacion

gantt_df, costos_df, riesgo_df, planificacion_df = cargar_datos()

col1, col2 = st.columns(2)

with col1:
    # Calcular costo total
    total = costos_df['Costo estimado'].sum()
    st.info(f" **Costo Total Estimado:** ${total:,.2f}")

with col2:
    # Calcular progreso promedio
    progreso = gantt_df['progress'].mean() * 100
    st.info(f" **Progreso Promedio:** {progreso:.1f}%")

# Gráfico de Gantt
st.subheader("Diagrama de Gantt")
fig = px.timeline(
    gantt_df,
    x_start="start",
    x_end="end",
    y="Task",
    color="progress",
    color_continuous_scale=["red", "yellow", "green"],
    height=400
)

fig.update_traces(
    text=gantt_df["Agent"],
    textposition="inside",
    textfont=dict(color="black", size=10)
)

fig.update_layout(
    coloraxis_colorbar=dict(title="Progreso", tickformat=".0%"),
)

# Mostrar el gráfico
st.plotly_chart(fig, use_container_width=True)


st.subheader("Planificación de Recursos")
st.dataframe(planificacion_df, hide_index=True)

st.subheader("Riesgos")
st.dataframe(riesgo_df, hide_index=True)

st.subheader("Detalle de Costos")
st.dataframe(costos_df, hide_index=True)

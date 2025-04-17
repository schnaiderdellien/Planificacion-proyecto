import pandas as pd
import plotly.express as px

grantt = pd.read_excel('Grantt.xlsx')
grantt = grantt.sort_values(by='Task')

riesgo = pd.read_excel('Tabla_de_riesgos.xlsx')

planificacion = pd.read_excel('Planificacion_de_recursos.xlsx')

costos = pd .read_excel('Estimacion_de_costos.xlsx')

print(riesgo)

print(planificacion)

print(costos)

total_costos = costos['Costo estimado'].sum()

print(f"Precio total estimado: {total_costos}")


fig = px.timeline(
    grantt,
    x_start="start",
    x_end="end",
    y="Task",
    color="progress",
    color_continuous_scale=["red", "yellow", "green"],
    title="Grantt"
)

fig.update_traces(
    text=grantt["Agent"],
    textposition="inside",
    insidetextanchor="middle",
    textfont=dict(color="black", size=12)
)

fig.update_yaxes(categoryorder="total ascending")
fig.update_layout(
    hovermode="y unified",
    coloraxis_colorbar=dict(
        title="Progreso",
        tickformat=".0%",
    ),
)

fig.show()


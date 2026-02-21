
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv("ed_patient_data.csv") 
st.title("🏥 ED Patient Data — Overview")

# ── Sidebar filters ──────────────────────────────────────────────
st.sidebar.header("Filters")
triage_filter = st.sidebar.multiselect(
    "Triage Levels:",
    options=sorted(df['triage_level'].unique()),
    default=sorted(df['triage_level'].unique())
)

filtered_df = df[df['triage_level'].isin(triage_filter)].copy()
filtered_df['hour'] = pd.to_datetime(filtered_df['arrival_datetime']).dt.hour

# ── Plot 1 – Wait Time Distribution by Triage Level ─────────────
fig1 = px.histogram(
    filtered_df, x="wait_time_minutes", color="triage_level",
    facet_col="triage_level", facet_col_wrap=3,
    nbins=20,
    title="Wait Time Distribution by Triage Level",
  labels={"wait_time_minutes": "Wait Time (minutes)", "triage_level": "Triage Level"},
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig1.update_layout(
    showlegend=False,
    height=500,  # más altura para dar espacio entre filas
)

# Corrige las anotaciones del eje X para cada faceta
fig1.for_each_xaxis(lambda axis: axis.update(title_text="wait_time_minutes"))

fig1.update_layout(
    showlegend=False,
    height=550,
    margin=dict(b=80)  # más margen inferior
)

# ── Plot 2 – Arrivals by Hour of Day ────────────────────────────
hourly = filtered_df.groupby('hour').size().reset_index(name='count')
fig2 = px.bar(
    hourly, x="hour", y="count",
    title="Arrivals by Hour of Day",
    labels={"hour": "Hour", "count": "Count"},
    color_discrete_sequence=["steelblue"]
)

# ── Plot 3 – Disposition Breakdown ──────────────────────────────
disposition = filtered_df['disposition'].value_counts().reset_index()
disposition.columns = ['disposition', 'count']
fig3 = px.bar(
    disposition, x="count", y="disposition", orientation='h',
    title="Disposition Breakdown",
    labels={"count": "Count", "disposition": ""},
    color_discrete_sequence=["coral"]
)

# ── Plot 4 – Avg Wait Time vs Staff on Shift ────────────────────
staff_wait = (
    filtered_df.groupby('staff_on_shift')['wait_time_minutes']
    .mean().reset_index()
)
fig4 = px.line(
    staff_wait, x="staff_on_shift", y="wait_time_minutes",
    markers=True,
    title="Avg Wait Time vs Staff on Shift",
    labels={"staff_on_shift": "Staff Count", "wait_time_minutes": "Avg Wait (min)"},
    color_discrete_sequence=["green"]
)

# ── Layout: 2-column grid + full-width row ───────────────────────
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, width='stretch')
with col2:
    st.plotly_chart(fig2, width='stretch')

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(fig3, width='stretch')
with col4:
    st.plotly_chart(fig4, width='stretch')

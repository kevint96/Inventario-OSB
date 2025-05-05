import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import json
from google.oauth2 import service_account
import gspread

# Configurar el título de la app
st.title("📊 Inventario de Servicios OSB")

# Definir el alcance para Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets"]

# Leer credenciales desde Streamlit Secrets
credentials_json = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
creds = service_account.Credentials.from_service_account_info(credentials_json, scopes=scope)

# Autenticarse en Google Sheets
gc = gspread.authorize(creds)

# ID de tu Google Sheet
SHEET_ID = "1okOylzxtJeXW3QqtQ8k0ms7QHVQ4_gqkiFs8zPnhKmo"
SHEET_NAME = "Inventario_QA"

# Cargar los datos desde Google Sheets
@st.cache_data
def load_data():
    sh = gc.open_by_key(SHEET_ID)
    worksheet = sh.worksheet(SHEET_NAME)
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

# Obtener los datos
df = load_data()

# 🔹 Aplicar el filtro de exclusión
df = df[
    (df["Tipo Business"] != "N/A") &
    (~df["Operacion Business"].isin(["manejarError", "registrarAuditoria"]))
]

# Convertir la columna '#' a texto
df["#"] = df["#"].astype(str)

# 🔍 **Sidebar de Filtros**
st.sidebar.header("🔍 Filtros Principales")

# Filtrar por "Servicio" y "Operación"
servicios = ["Todos"] + sorted(df["Nombre Servicio"].dropna().unique().astype(str)) + sorted(df["Servicio EBS 1"].dropna().unique().astype(str)) + sorted(df["Servicio EBS 2"].dropna().unique().astype(str)) + sorted(df["Servicio EBS 3"].dropna().unique().astype(str)) + sorted(df["Proxy ABC"].dropna().unique().astype(str))
operaciones = ["Todos"] + sorted(df["Operacion"].dropna().unique().astype(str)) + sorted(df["Operacion Business"].dropna().unique().astype(str))
business = ["Todos"] + sorted(df["Nombre Business"].dropna().unique().astype(str))

selected_servicio = st.sidebar.selectbox("Nombre Servicio:", servicios)
selected_operacion = st.sidebar.selectbox("Operación:", operaciones)
selected_business = st.sidebar.selectbox("Business:", business)

# Aplicar filtro inicial
df_filtered = df.copy()
if selected_servicio != "Todos":
    df_filtered = df_filtered[df_filtered["Nombre Servicio"] == selected_servicio]
if selected_operacion != "Todos":
    df_filtered = df_filtered[df_filtered["Operacion"] == selected_operacion]
if selected_operacion != "Todos":
    df_filtered = df_filtered[df_filtered["Nombre Business"] == selected_business]

# **Mostrar filtros adicionales solo si ya se filtró algo**
if selected_servicio != "Todos" or selected_operacion != "Todos":
    st.sidebar.header("📌 Filtros Adicionales")

    # Crear listas desplegables dinámicamente según los valores filtrados
    additional_filters = {}
    for column in df_filtered.columns:
        if column not in ["Nombre Servicio", "Operacion"]:  # Excluir filtros principales
            unique_values = ["Todos"] + sorted(df_filtered[column].dropna().unique().astype(str))
            selected_value = st.sidebar.selectbox(f"{column}:", unique_values, key=column)
            additional_filters[column] = selected_value

    # Aplicar filtros adicionales
    for column, value in additional_filters.items():
        if value != "Todos":
            df_filtered = df_filtered[df_filtered[column] == value]

# 📌 Mostrar la tabla filtrada
st.subheader("📌 Inventario de Servicios OSB")
st.dataframe(
    df_filtered,
    hide_index=True,
    use_container_width=True
)

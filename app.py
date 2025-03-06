import streamlit as st
import pandas as pd
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

# ID de tu Google Sheet (extraído de la URL)
SHEET_ID = "BCS_InventarioServicios_Otorgamiento [Kevin]"

# Nombre de la hoja dentro del archivo
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

# Mostrar la tabla en la app
st.dataframe(df)

# Filtros dinámicos
st.sidebar.header("🔍 Filtros")
column = st.sidebar.selectbox("Selecciona columna", df.columns)
search_value = st.sidebar.text_input("Buscar")

# Filtrar los datos
if search_value:
    df_filtered = df[df[column].astype(str).str.contains(search_value, case=False, na=False)]
else:
    df_filtered = df

# Mostrar los resultados filtrados
st.subheader("📌 Resultados filtrados")
st.dataframe(df_filtered)

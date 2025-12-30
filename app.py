import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

# 1. CONFIGURACIÓN Y AUTO-REFRESCO (Cada 30 segundos)
st.set_page_config(page_title="MNQ SINCRO HUB", layout="wide")

# Estilo Neón Pulido
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    [data-testid="stMetricValue"] { 
        color: #39FF14 !important; 
        font-size: 85px !important; 
        font-weight: 900 !important;
        text-shadow: 0 0 20px #39FF14;
    }
    .status-box { padding: 30px; border-radius: 15px; text-align: center; font-size: 30px; font-weight: 900; border: 2px solid white; }
    </style>
    """, unsafe_allow_html=True)

def obtener_mnq_real():
    try:
        ticker = yf.Ticker("NQ=F")
        precio = ticker.fast_info['last_price']
        return round(precio, 2)
    except:
        return 25697.75 # Último valor conocido si falla la red

# --- CUERPO DE LA APP ---
st.title("🎯 Centro de Inteligencia MNQ")
st.subheader("Escenario de Operación Calma | Volumen: 1500")

# Contenedor de precio que se actualiza
precio_actual = obtener_mnq_real()
st.metric(label="COTIZACIÓN MNQ (SINCRO PRO)", value=f"{precio_actual} PTS")

# --- LÓGICA DE ALERTAS PULIDA ---
try:
    df = pd.read_csv("datos_historicos.csv")
    ultima = df.iloc[-1]
    nota = ultima['nota_didactica'].upper()
    
    if "TRAMPA" in nota:
        st.markdown(f'<div class="status-box" style="background-color: #FF0000; color: white;">🔴 RIESGO DE TRAMPA - PROTEJA SU CAPITAL</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-box" style="background-color: #39FF14; color: black;">🎯 OPORTUNIDAD TP DETECTADA</div>', unsafe_allow_html=True)
    
    st.markdown(f"**📝 Análisis de última señal:** {ultima['nota_didactica']}")
except:
    st.error("Error al leer 'datos_historicos.csv'. Revisa el nombre del archivo.")

# --- FOOTER CON RELOJ VIVO ---
hora_actual = datetime.now().strftime('%H:%M:%S')
st.write(f"Sincronizado: **{hora_actual}** | Fuente: NQ Futures")

# 2. EL PULIDO FINAL: SCRIPT DE AUTO-ACTUALIZACIÓN
# Esto hace que la página se refresque sola cada 30 segundos
time.sleep(30)
st.rerun()

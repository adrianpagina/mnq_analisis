import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN PROFESIONAL ---
st.set_page_config(page_title="MNQ SINCRO HUB", layout="wide")

# Estilo Neón para Máxima Visibilidad
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    [data-testid="stMetricValue"] { 
        color: #39FF14 !important; 
        font-size: 75px !important; 
        font-weight: 900 !important;
        text-shadow: 0 0 15px #39FF14;
    }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; font-size: 20px !important; }
    .status-box { padding: 25px; border-radius: 15px; text-align: center; font-weight: 900; font-size: 28px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN DE DATOS SINCRO ---
def obtener_mnq_real():
    try:
        # Sincronizamos con el contrato de Futuros (NQ=F) para igualar a MNQ Pro
        ticker = yf.Ticker("NQ=F")
        # Obtenemos el precio de la última transacción registrada
        precio = ticker.fast_info['last_price']
        return round(precio, 2)
    except:
        try:
            # Respaldo en caso de error de conexión local
            df = yf.download("NQ=F", period="1d", interval="1m", progress=False)
            return round(df['Close'].iloc[-1], 2)
        except:
            return 25714.00 # Nivel Clave de Referencia

# --- ESTRUCTURA DEL HUB ---
st.title("🎯 MNQ Intelligence Hub")
st.markdown("### Escenario de Operación Calma | Volumen: 1500")

precio_sincro = obtener_mnq_real()

# MÉTRICA PRINCIPAL
st.metric(label="COTIZACIÓN MNQ (SINCRO PRO)", value=f"{precio_sincro} PTS")

# --- ANÁLISIS AUTOMÁTICO DE SEÑALES ---
try:
    # Leemos el registro automático de TPs del día
    df_hist = pd.read_csv("datos_historicos.csv")
    ultima = df_hist.iloc[-1]
    
    # Alerta de Bull Breakout / Bull Trap
    tipo_alerta = "🔴 RIESGO DE TRAMPA" if "trampa" in ultima['nota_didactica'].lower() else "🎯 OPORTUNIDAD TP"
    color_box = "#dc3545" if "trampa" in ultima['nota_didactica'].lower() else "#28a745"
    
    st.markdown(f'<div class="status-box" style="background-color: {color_box}; color: white;">{tipo_alerta} - PROTEJA SU CAPITAL</div>', unsafe_allow_html=True)
    
    st.info(f"📝 **Análisis de última señal:** {ultima['nota_didactica']}")

except:
    st.warning("Archivo de historial no detectado. Cargue 'datos_historicos.csv' en GitHub.")

# --- FOOTER ---
st.caption(f"Sincronizado: {datetime.now().strftime('%H:%M:%S')} | Fuente: NQ Futures (Aceptable Delay 10-15m)")

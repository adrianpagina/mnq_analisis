import streamlit as st
import pandas as pd
import time

# --- CONFIGURACIÓN VISUAL PRO ---
st.set_page_config(
    page_title="Nasdaq Live Hub",
    page_icon="🎯",
    layout="wide",
)

# Estilo CSS para mejorar la estética (Corregido)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .status-box {
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-weight: bold;
        font-size: 28px;
        margin-bottom: 25px;
        border: 2px solid rgba(255,255,255,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN DE DATOS ---
def cargar_datos():
    return pd.read_csv("datos_historicos.csv")

# --- CABECERA ---
st.title("🎯 MNQ Intelligence Hub")
st.markdown(f"### **Escenario de Operación Calma** | Volumen: **1500**")
st.caption(f"Sincronizado en tiempo real: {time.strftime('%H:%M:%S')}")

try:
    df = cargar_datos()
    ultima = df.iloc[-1]
    nota = ultima['nota_didactica'].lower()

    # --- SEMÁFORO VISUAL (Corregido con unsafe_allow_html) ---
    if "sólida" in nota or "confirmado" in nota:
        st.markdown('<div class="status-box" style="background-color: #28a745;">🟢 ESTRUCTURA SÓLIDA - OPORTUNIDAD DETECTADA</div>', unsafe_allow_html=True)
    elif "trampa" in nota or "riesgo" in nota:
        st.markdown('<div class="status-box" style="background-color: #dc3545;">🔴 RIESGO DE TRAMPA - PROTEJA SU CAPITAL</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-box" style="background-color: #ffc107; color: black;">🟡 ZONA DE TRANSICIÓN - PACIENCIA</div>', unsafe_allow_html=True)

    # --- MÉTRICAS ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Nivel Clave actual", f"{ultima['nivel']} pts")
    with c2:
        efec = df[df['nivel'] == ultima['nivel']]['resultado'].mean() * 100
        st.metric("Fiabilidad del Nivel", f"{efec:.1f}%")
    with c3:
        st.metric("Estado del Nasdaq", "Estable" if efec > 75 else "Volátil")

    st.divider()

    # --- ZONA DIDÁCTICA ---
    col_izq, col_der = st.columns([2, 1])
    
    with col_izq:
        st.subheader("📝 Análisis de la última señal")
        if st.sidebar.checkbox("🔓 Desbloquear Análisis Didáctico", value=False):
            st.success(f"**Análisis Profesional:** {ultima['nota_didactica']}")
            st.write("---")
            st.write("### 🏆 Ranking de Niveles Proficuos")
            ranking = df.groupby('nivel')['resultado'].mean().sort_values(ascending=False) * 100
            st.dataframe(ranking.rename("Efectividad %").head(3), use_container_width=True)
        else:
            st.warning("La explicación detallada de este movimiento es exclusiva para suscriptores.")
            st.button("Ver Planes de Suscripción")

    with col_der:
        st.info("**Supervisión Profesional:** El volumen de 1500 actúa como filtro de calidad. En este nivel, las trampas son más fáciles de identificar para el trader principiante.")

except Exception as e:
    st.error("Configure el archivo datos_historicos.csv para ver el análisis.")

# --- FOOTER ---
st.markdown("---")
st.caption("⚠️ **Aviso Legal:** El trading de futuros MNQ implica riesgo. Los datos son didácticos y generados algorítmicamente.")
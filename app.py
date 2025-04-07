import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# -------- CONFIGURACIONES --------
broker = "157.230.214.127"
port = 1883
client_id = "lvruiza"
topic_digital = "saludo"
topic_analog = "saludo30"

# -------- STREAMLIT SETUP --------
st.set_page_config(page_title="Control MQTT", layout="centered")
st.title("🔧 Control MQTT desde Streamlit")

# -------- IMAGEN --------
st.image("codigo.jpg", caption="Dashboard IoT", use_container_width=True)

# -------- VERSIÓN DE PYTHON --------
st.caption(f"🧠 Python version: {platform.python_version()}")

# -------- MQTT CLIENT --------
client = paho.Client(client_id)

def on_publish(client, userdata, result):
    print("📤 Mensaje publicado")
    pass

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    st.toast(f"📩 Mensaje recibido: {msg}")
    print("📩 Mensaje recibido:", msg)

client.on_publish = on_publish
client.on_message = on_message

try:
    client.connect(broker, port)
    st.success("✅ Conectado al broker MQTT")
except:
    st.error("❌ No se pudo conectar al broker")

# -------- INTERFAZ DE BOTONES --------
st.subheader("Controles Digitales")
col1, col2 = st.columns(2)

with col1:
    if st.button('🔛 Encender (ON)', key="on_button", use_container_width=True):
        message = json.dumps({"Act1": "ON"})
        client.publish(topic_digital, message)
        st.success("Dispositivo encendido ✅")

with col2:
    if st.button('🔌 Apagar (OFF)', key="off_button", use_container_width=True):
        message = json.dumps({"Act1": "OFF"})
        client.publish(topic_digital, message)
        st.warning("Dispositivo apagado ⚠️")

# -------- SLIDER Y BOTÓN DE ENVÍO ANALÓGICO --------
st.divider()
st.subheader("Control Analógico")

values = st.slider('🎚 Selecciona el valor analógico', 0.0, 100.0, 50.0, key="slider_value")
st.write(f'🔢 Valor seleccionado: {values}')

if st.button('📤 Enviar valor analógico', key="send_analog_button", use_container_width=True):
    message = json.dumps({"Analog": float(values)})
    client.publish(topic_analog, message)
    st.success(f"Valor {values} enviado al topic '{topic_analog}' 🚀")



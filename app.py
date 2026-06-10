import streamlit as st
import pandas as pd
from anonimizador import detectar, anonimizar


st.set_page_config(
    page_title="Anonimizador PII",
    page_icon="🔒",
    layout="wide"
)

st.title("🔒 Anonimizador local de datos personales")
st.write("Detecta y tacha datos personales antes de enviar textos a herramientas externas.")

texto = st.text_area(
    "Pega aquí el texto a anonimizar",
    height=300,
    placeholder="Ejemplo: Hola, soy Juan Pérez, mi email es juan@email.com..."
)

if st.button("Anonimizar"):
    if not texto.strip():
        st.warning("Introduce un texto primero.")
    else:
        with st.spinner("Detectando datos personales con Ollama..."):
            deteccion = detectar(texto)
            texto_anonimo = anonimizar(texto, deteccion)

        st.subheader("Texto anonimizado")
        st.text_area("Resultado", value=texto_anonimo, height=300)

        st.subheader("Entidades detectadas")

        datos = [
            {"tipo": e.tipo, "texto": e.texto}
            for e in deteccion.entidades
        ]

        df = pd.DataFrame(datos)

        if df.empty:
            st.info("No se detectaron datos personales.")
        else:
            st.dataframe(df, use_container_width=True)

        st.download_button(
            label="Descargar texto anonimizado",
            data=texto_anonimo,
            file_name="texto_anonimizado.txt",
            mime="text/plain"
        )
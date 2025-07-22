import streamlit as st
from app.generate_with_rag import generate_text_with_context
from app.image_generator import generate_image_url
import streamlit.components.v1 as components

st.set_page_config(page_title="Generador IA de Contenidos", layout="centered")

st.title("🧠 Generador de Contenidos con LLM + Imagen IA")

with st.form("content_form"):
    topic = st.text_input("📝 Tema del contenido", value="Inteligencia Artificial")
    platform = st.selectbox("📱 Plataforma", ["Twitter", "LinkedIn", "Instagram", "Blog"])
    company = st.text_input("🏢 Nombre de tu marca o empresa (opcional)", value="")
    tone = st.selectbox("🎙️ Tono del mensaje", [
        "Profesional", "Cercano", "Informativo", "Humorístico", "Técnico"
    ])
    language = st.selectbox("🌐 Idioma del contenido", [
        "Español", "Inglés", "Francés", "Italiano"
    ])
    audience = st.text_input("👥 Audiencia objetivo (opcional)", value="")

    model_display = {
        "LLaMA 3 (8B)": "meta-llama/llama-3-8b-instruct",
        "Mistral 7B": "mistralai/mistral-7b-instruct"
    }
    model_name = st.selectbox("🧠 Modelo LLM", list(model_display.keys()))
    model = model_display[model_name]

    generate_image = st.checkbox("🎨 ¿Generar imagen con IA?", value=True)

    submit = st.form_submit_button("Generar contenido")

if submit:
    with st.spinner("🔄 Generando texto..."):
        result, final_prompt = generate_text_with_context(
            topic, platform, tone, company, language, model, audience
        )

    st.subheader("📄 Contenido generado:")
    st.write(result)

    st.subheader("🧪 Prompt enviado al modelo:")
    st.code(final_prompt, language="text")

    if generate_image:
        with st.spinner("🎨 Generando imagen con IA..."):
            image_data = generate_image_url(topic, platform, tone, audience)

        st.subheader("🖼️ Imagen generada por IA:")
        if image_data:
            components.html(f'<img src="{image_data}" width="512"/>', height=550)
        else:
            st.warning("No se pudo generar la imagen.")

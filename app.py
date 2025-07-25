import streamlit as st
import whisper
import tempfile
import os

st.set_page_config(page_title="Bengali Audio Transcriber", layout="centered")
st.title("🎙️ Bengali Audio Transcriber")
st.markdown("Upload an audio file, and this tool will transcribe it to Bengali text.")

@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.audio(uploaded_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.info("Transcribing... Please wait ⏳")

    try:
        result = model.transcribe(tmp_path, language="bn")
        transcription = result["text"]

        st.success("✅ Transcription Complete!")
        st.text_area("📄 Bengali Transcript", transcription, height=250)
        st.download_button("📥 Download Transcript", transcription, file_name="bengali_transcription.txt")
    except Exception as e:
        st.error(f"❌ Error during transcription: {e}")
    finally:
        os.remove(tmp_path)

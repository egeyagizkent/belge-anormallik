import streamlit as st
import pytesseract
from PIL import Image
import io
import re
from pdf2image import convert_from_bytes

st.set_page_config(page_title="Belge Anormallik Dedektörü")

st.title("📄 Belge Anormallik Dedektörü")
st.write("Muhasebe evrakları için **teknik ön kontrol** aracı.")

uploaded_file = st.file_uploader(
    "PDF veya Görsel Yükle",
    type=["pdf", "png", "jpg", "jpeg"]
)

def extract_text(file_bytes, ext):
    if ext == "pdf":
        images = convert_from_bytes(file_bytes)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img)
        return text
    else:
        image = Image.open(io.BytesIO(file_bytes))
        return pytesseract.image_to_string(image)

def analyze(text):
    results = []

    tckn = re.search(r"\b\d{11}\b", text)
    results.append(("TCKN", "Bulundu ✅" if tckn else "Bulunamadı ❌"))

    vergi = re.search(r"\b\d{10}\b", text)
    results.append(("Vergi No", "Bulundu ✅" if vergi else "Bulunamadı ⚠️"))

    tarih = re.search(r"\b\d{2}[./-]\d{2}[./-]\d{4}\b", text)
    results.append(("Tarih", "Bulundu ✅" if tarih else "Geçerli tarih yok ❌"))

    iban = re.search(r"TR\d{24}", text)
    results.append(("IBAN", "Bulundu ✅" if iban else "Bulunamadı ⚠️"))

    return results

if uploaded_file:
    ext = uploaded_file.name.split(".")[-1].lower()

    with st.spinner("Belge taranıyor..."):
        text = extract_text(uploaded_file.read(), ext)
        results = analyze(text)

    st.subheader("📌 Analiz Sonucu")
    for label, result in results:
        st.write(f"**{label}** — {result}")

    st.markdown("---")
    st.caption("⚠️ Bu sistem yalnızca teknik ön kontrol sağlar. Hukuki veya mali danışmanlık değildir.")


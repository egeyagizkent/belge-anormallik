import os
os.environ["PORT"] = os.environ.get("PORT", "8501")

import streamlit as st
import re

st.set_page_config(
    page_title="Belge Anormallik Dedektörü",
    layout="centered"
)

st.title("📄 Belge Anormallik Dedektörü")
st.write("Muhasebe ve hukuki evraklar için **teknik ön kontrol** aracı.")

# Dosya yükleme
uploaded_file = st.file_uploader(
    "PDF veya Görsel Yükle",
    type=["pdf", "png", "jpg", "jpeg"]
)

# OCR geçici olarak kapalı (deploy-safe stub)
def extract_text(file_bytes, ext):
    return ""

# Regex tabanlı analiz
def analyze(text):
    results = []

    tckn = re.search(r"\b\d{11}\b", text)
    results.append(("TCKN", "Bulundu ✅" if tckn else "Bulunamadı ❌"))

    vergi = re.search(r"\b\d{10}\b", text)
    results.append(("Vergi No", "Bulundu ✅" if vergi else "Bulunamadı ⚠️"))

    tarih = re.search(r"\b\d{2}[./-]\d{2}[./-]\d{4}\b", text)
    results.append(("Tarih", "Bulundu ✅" if tarih else "Geçerli tarih yok ❌"))

    iban = re.search(r"\bTR\d{24}\b", text)
    results.append(("IBAN", "Bulundu ✅" if iban else "Bulunamadı ⚠️"))

    return results

# Ana akış
if uploaded_file:
    ext = uploaded_file.name.split(".")[-1].lower()

    with st.spinner("Belge analiz ediliyor..."):
        text = extract_text(uploaded_file.read(), ext)
        results = analyze(text)

    st.subheader("📌 Analiz Sonucu")

    for label, result in results:
        st.write(f"**{label}** — {result}")

    st.markdown("---")
    st.caption(
        "⚠️ Bu sistem yalnızca teknik ön kontrol sağlar. "
        "Hukuki veya mali danışmanlık değildir."
    )


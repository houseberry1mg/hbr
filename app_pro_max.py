
import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
from batch_prompt_generator import generate_batch

st.set_page_config(page_title="Batch-Maker-By-HBR | Pro Studio", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"]  {
        background-color: #091235;
        color: #FFFFFF;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .title {
        font-size: 3em;
        font-weight: 800;
        color: white;
        margin-bottom: 0.2em;
    }
    .subtitle {
        font-size: 1.2em;
        font-weight: 300;
        color: #AAB4D4;
        margin-bottom: 2em;
    }
    .card {
        background-color: #0F1A3C;
        padding: 1.5em;
        border-radius: 12px;
        margin-bottom: 1.5em;
        border: 1px solid #2B3558;
    }
    .card h4 {
        margin-top: 0;
        color: white;
    }
    .ref-img {
        border-radius: 10px;
        margin-top: 0.5em;
    }
    .btn-primary button {
        background-color: #FFFFFF !important;
        color: #091235 !important;
        font-weight: bold;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 5])
with col1:
    st.image("HBR.jpg", width=100)
with col2:
    st.markdown("<div class='title'>Batch-Maker-By-HBR</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Create editorial-grade AI prompts and metadata, ready for commercial campaigns.</div>", unsafe_allow_html=True)

st.markdown("### 🧠 Generate Your Custom Prompt")
concepts_input = st.text_area("Concepts (one per line)", height=150)
category = st.selectbox("Select a category", ["Fashion", "Skincare", "Business", "Lifestyle"])
batch_size = st.slider("Number of prompts", 1, 20, 5)

st.markdown("---")

if st.button("🚀 Generate Now", use_container_width=True):
    concepts = [c.strip() for c in concepts_input.split("\n") if c.strip()]
    if not concepts:
        st.warning("Please enter at least one concept.")
    else:
        df = generate_batch(concepts, category, batch_size)

        for i, row in df.iterrows():
            with st.container():
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"<h4>{row['Title']}</h4>", unsafe_allow_html=True)
                st.write("📄 **Prompt:**", row["Prompt"])
                st.write("📝 **Description:**", row["Image Description"])
                st.write("🏷️ **Keywords:**", row["Keywords"])
                st.write("💡 **Suggestions:**", row["Suggestions"])

                if row["Reference"]:
                    try:
                        img_data = requests.get(row["Reference"], timeout=3).content
                        img = Image.open(BytesIO(img_data))
                        st.image(img, caption="Reference Preview", use_column_width=True, output_format="JPEG")
                    except:
                        st.markdown(f"[🔗 View Reference]({row['Reference']})")
                st.markdown("</div>", unsafe_allow_html=True)

        st.download_button("⬇️ Download CSV", df.to_csv(index=False), file_name="batch_prompts_maxed.csv", use_container_width=True)

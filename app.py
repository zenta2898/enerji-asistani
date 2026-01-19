import streamlit as st
import time
import base64
import pandas as pd
import plotly.express as px

# 1. Sayfa Konfigürasyonu
st.set_page_config(page_title="Enerji Master Pro", page_icon="🔋", layout="centered")

# --- ÖZEL TASARIM AYARLARI (CSS) ---
st.markdown("""
    <style>
    /* Butonları Yeşil Yap */
    div.stButton > button:first-child {
        background-color: #2E7D32;
        color: white;
        border-radius: 12px;
        border: none;
        font-weight: bold;
    }
    div.stButton > button:first-child:hover {
        background-color: #4CAF50;
        color: white;
    }
    /* Kart Görünümü */
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- VİDEO ARKAPLAN SİHRİ ---
def get_base64_bin(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg_video(video_file):
    try:
        bin_str = get_base64_bin(video_file)
        st.markdown(
            f"""
            <style>
            #root > div:nth-child(1) > div > div > div {{ background: none; }}
            .stApp {{ background: transparent; }}
            video {{
                position: fixed;
                top: 50%; left: 50%;
                transform: translate(-50%, -50%);
                min-width: 100%; min-height: 100%;
                z-index: -1;
                object-fit: cover;
                filter: brightness(0.5);
            }}
            .video-content {{
                position: relative;
                z-index: 1;
                text-align: center;
                color: white;
                margin-top: 15vh;
            }}
            </style>
            <video autoplay loop muted playsinline>
                <source src="data:video/mp4;base64,{bin_str}" type="video/mp4">
            </video>
            """,
            unsafe_allow_html=True
        )
    except:
        st.info("💡 Animasyon hazırlanıyor...")

# --- OTURUM YÖNETİMİ ---
if 'giris' not in st.session_state: st.session_state.giris = False
if 'cihazlar' not in st.session_state: st.session_state.cihazlar = []

# --- GİRİŞ EKRANI ---
if not st.session_state.giris:
    set_bg_video("intro.mp4")
    st.markdown('<div class="video-content">', unsafe_allow_html=True)
    st.markdown("<h1 style='text-shadow: 2px 2px 10px #000; font-size: 3rem;'>Enerji Master</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-shadow: 2px 2px 10px #000; font-size: 1.2rem;'>Watt'ını Bil, Cebini Koru.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Analizi Başlat", use_container_width=True):
            st.session_state.giris = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANA PANEL ---
else:
    st.sidebar.image("logo.png", width=100)
    st.sidebar.title("🌱 Menü")
    sayfa = st.sidebar.radio("Sayfa:", ["📊 Fatura Analizi", "📚 Tasarruf Sırları"])

    if sayfa == "📊 Fatura Analizi":
        st.title("⚡ Akıllı Enerji Paneli")
        
        with st.expander("➕ Cihaz Ekle", expanded=True):
            c_ad = st.selectbox("Cihaz:", ["Buzdolabı", "Klima", "TV", "Çamaşır Makinesi", "Ütü", "Fırın", "Aydınlatma"])
            c_watt = st.number_input("Güç (Watt):", value=200)
            c_saat = st.slider("Günlük Saat:", 0.5, 24.0, 3.0)
            if st.button("Listeye Ekle"):
                st.session_state.cihazlar.append({"Cihaz": c_ad, "Watt": c_watt, "Saat": c_saat})
                st.rerun()

        if st.session_state.cihazlar:
            df = pd.DataFrame(st.session_state.cihazlar)
            df['Maliyet'] = (df['Watt'] / 1000) * df['Saat'] * 30 * 3.50
            
            st.metric("📊 Toplam Tahmini Fatura", f"{df['Maliyet'].sum():.2f} TL")
            
            # Pasta Grafiği
            fig = px.pie(df, values='Maliyet', names='Cihaz', hole=0.4,
                         color_discrete_sequence=px.colors.sequential.Greens_r)
            st.plotly_chart(fig, use_container_width=True)
            
            # Liste
            for idx, row in df.iterrows():
                c1, c2, c3 = st.columns([3,2,1])
                c1.write(f"**{row['Cihaz']}**")
                c2.write(f"{row['Maliyet']:.2f} TL")
                if c3.button("Sil", key=f"d_{idx}"):
                    st.session_state.cihazlar.pop(idx)
                    st.rerun()
    
    elif sayfa == "📚 Tasarruf Sırları":
        st.header("📖 Tasarruf Kütüphanesi")
        st.success("Tebrikler! Tasarruf adımlarını takip ederek verimliliği artırabilirsin.")

    if st.sidebar.button("Güvenli Çıkış"):
        st.session_state.giris = False
        st.rerun()
      

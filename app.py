import streamlit as st
import time
import base64

# 1. Sayfa Ayarları ve iPhone İkonu
st.set_page_config(page_title="Enerji Master", page_icon="🔋", layout="centered")

st.markdown(
    """
    <head>
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/zenta2898/enerji-asistani/main/logo.png">
    </head>
    """,
    unsafe_allow_html=True
)

# --- VİDEO ARKAPLAN FONKSİYONU ---
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
            #root > div:nth-child(1) > div > div > div {{
                background: none;
            }}
            .stApp {{
                background: transparent;
            }}
            video {{
                position: fixed;
                right: 0;
                bottom: 0;
                min-width: 100%;
                min-height: 100%;
                z-index: -1;
                object-fit: cover;
                filter: brightness(0.6);
            }}
            .video-content {{
                position: relative;
                z-index: 1;
                text-align: center;
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
        st.info("💡 Giriş animasyonu yükleniyor... (intro.mp4 dosyasını GitHub'a yüklediğinizden emin olun)")

# --- OTURUM YÖNETİMİ ---
if 'giris' not in st.session_state:
    st.session_state.giris = False

# --- GİRİŞ EKRANI (VİDEOLU) ---
if not st.session_state.giris:
    set_bg_video("intro.mp4")
    
    st.markdown('<div class="video-content">', unsafe_allow_html=True)
    st.markdown("<h1 style='color: white; text-shadow: 2px 2px 8px #000;'>Enerji Master</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: white; font-size: 20px; text-shadow: 2px 2px 8px #000;'>Watt'ını Bil, Cebini Koru.</p>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.warning("⚠️ Mevcut Verimlilik Puanın: %35")
        if st.button("🚀 Analizi Başlat ve Tasarruf Et", use_container_width=True):
            with st.spinner('Sistem optimize ediliyor...'):
                time.sleep(1.5)
                st.session_state.giris = True
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANA UYGULAMA SAYFASI (VİDEO BİTİNCE AÇILAN KISIM) ---
else:
    # Sidebar
    st.sidebar.markdown(
        '<div style="text-align: center;"><img src="https://raw.githubusercontent.com/zenta2898/enerji-asistani/main/logo.png" width="100"></div>',
        unsafe_allow_html=True
    )
    st.sidebar.title("🌱 Menü")
    sayfa = st.sidebar.radio("Sayfa Seçin:", ["📊 Hesaplama Paneli", "📚 Tasarruf Sırları"])

    if sayfa == "📊 Hesaplama Paneli":
        st.title("⚡ Akıllı Enerji Paneli")
        
        tab1, tab2 = st.tabs(["🔌 Elektrikli Cihazlar", "🔥 Doğalgaz"])
        
        with tab1:
            cihaz = st.selectbox("Cihaz:", ["Buzdolabı", "Klima", "Ütü", "Çamaşır Makinesi", "TV"])
            watt = st.number_input("Watt Değeri:", value=150)
            saat = st.slider("Günlük Kullanım (Saat):", 0.0, 24.0, 5.0)
            maliyet = (watt/1000) * saat * 30 * 3.50
            st.metric("Aylık Tahmini Fatura Etkisi", f"{maliyet:.2f} TL")

        with tab2:
            st.header("Doğalgaz Tasarrufu")
            derece = st.slider("Kombi Isısı:", 35, 75, 45)
            st.metric("Tahmini Gaz Faturası", f"{(derece * 25):.2f} TL")

    elif sayfa == "📚 Tasarruf Sırları":
        st.header("📖 Tasarruf Kütüphanesi")
        st.info("Buzdolabı arkasını temizlemek verimliliği %15 artırır!")

    if st.sidebar.button("Güvenli Çıkış"):
        st.session_state.giris = False
        st.rerun()


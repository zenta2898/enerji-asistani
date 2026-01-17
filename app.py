import streamlit as st
import time

# 1. Sayfa Ayarları
st.set_page_config(page_title="Enerji Master", page_icon="🔋", layout="centered")

# 2. iPhone Ana Ekran İkonu ve Logo Ortalama Ayarları (HTML)
st.markdown(
    """
    <head>
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/zenta2898/enerji-asistani/main/logo.png">
    </head>
    <style>
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        .logo-container img {
            width: 200px;
            border-radius: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- OTURUM YÖNETİMİ ---
if 'giris' not in st.session_state:
    st.session_state.giris = False

# --- GİRİŞ SAYFASI ---
if not st.session_state.giris:
    # Logo Ortalama
    st.markdown(
        '<div class="logo-container"><img src="https://raw.githubusercontent.com/zenta2898/enerji-asistani/main/logo.png"></div>',
        unsafe_allow_html=True
    )
    
    st.markdown("<h1 style='text-align: center; color: #2E7D32;'>Enerji Master</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-weight: bold;'>Watt'ını Bil, Cebini Koru.</p>", unsafe_allow_html=True)
    
    st.divider()
    
    st.warning("⚠️ Mevcut Verimlilik Puanın: %35")
    st.progress(35)
    st.caption("Telefonunun şarjı gibi düşün; evin enerjisi de sızıyor olabilir!")
    
    if st.button("🚀 Analizi Başlat ve Tasarruf Et", use_container_width=True):
        with st.spinner('Ev verileri optimize ediliyor...'):
            time.sleep(1.2)
            st.session_state.giris = True
            st.rerun()

# --- ANA UYGULAMA SAYFASI ---
else:
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


import streamlit as st
import time

# 1. Sayfa Konfigürasyonu ve Apple İkon Desteği
st.set_page_config(
    page_title="Enerji Master", 
    page_icon="🔋", 
    layout="centered"
)

# iPhone Ana Ekran İkonu İçin HTML (GitHub kullanıcı adını ve repo adını buraya yazmalısın)
# Örn: https://raw.githubusercontent.com/zenta2898/enerji-asistani/main/logo.png
st.markdown(
    """
    <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/zenta2898/enerji-asistani/main/logo.png">
    """,
    unsafe_allow_html=True
)

# --- TASARIM VE STİL ---
st.markdown("""
    <style>
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    .main {
        background-color: #f5f7f9;
    }
    </style>
    """, unsafe_allow_html=True)

# --- OTURUM YÖNETİMİ ---
if 'giris' not in st.session_state:
    st.session_state.giris = False

# --- GİRİŞ SAYFASI ---
if not st.session_state.giris:
    col1, col2, col3 = st.columns([1,2,1])
   # Eski col2 içindeki st.image yerine bunu yapıştır:
with col2:
    st.markdown(
        """
        <div style="display: flex; justify-content: center;">
            <img src="https://raw.githubusercontent.com/zenta2898/enerji-asistani/main/logo.png" width="200">
        </div>
        """,
        unsafe_allow_html=True
    )
        except:
            st.write("🔋") # Logo yüklenene kadar yedek ikon
            
        st.markdown("<h1 style='text-align: center; color: #2E7D32;'>Enerji Master</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>Watt'ını Bil, Cebini Koru.</p>", unsafe_allow_html=True)
        
        st.divider()
        
        # Pil ve Verimlilik Vurgusu
        st.warning("⚠️ Mevcut Verimlilik Puanın: %35")
        st.progress(35)
        st.caption("Telefonunun şarjı gibi düşün; evin enerjisi de sızıyor olabilir!")
        
        if st.button("🚀 Analizi Başlat ve Tasarruf Et", use_container_width=True):
            with st.spinner('Ev verileri optimize ediliyor...'):
                time.sleep(1.5)
                st.session_state.giris = True
                st.rerun()

# --- ANA UYGULAMA SAYFASI ---
else:
    # Sidebar Logo ve Menü
    try:
        st.sidebar.image("logo.png", width=100)
    except:
        pass
        
    st.sidebar.title("🌱 Enerji Master Menü")
    sayfa = st.sidebar.radio("Sayfa Seçin:", ["📊 Hesaplama Paneli", "📚 Tasarruf Sırları", "🛠️ Ayarlar"])

    if sayfa == "📊 Hesaplama Paneli":
        st.title("⚡ Akıllı Enerji Paneli")
        
        tab1, tab2 = st.tabs(["🔌 Elektrikli Cihazlar", "🔥 Doğalgaz"])
        
        with tab1:
            cihaz = st.selectbox("Cihaz:", ["Buzdolabı", "Klima", "Ütü", "Çamaşır Makinesi", "TV"])
            watt = st.number_input("Watt Değeri:", value=150)
            saat = st.slider("Günlük Kullanım (Saat):", 0.0, 24.0, 5.0)
            
            maliyet = (watt/1000) * saat * 30 * 3.50
            st.metric("Aylık Tahmini Fatura Etkisi", f"{maliyet:.2f} TL")
            
            # Seçilen cihaza özel sırları burada gösterelim
            if cihaz == "Buzdolabı":
                st.info("✨ Sır: Buzdolabını duvardan uzaklaştırmak verimlilik pilini %15 artırır!")

        with tab2:
            derece = st.slider("Kombi Isısı:", 35, 75, 45)
            st.metric("Tahmini Gaz Faturası", f"{(derece * 25):.2f} TL")

    elif sayfa == "📚 Tasarruf Sırları":
        st.header("📖 Tasarruf Kütüphanesi")
        st.write("Burada cihazların detaylı tasarruf sırlarını listeleyeceğiz.")

    if st.sidebar.button("Güvenli Çıkış"):
        st.session_state.giris = False
        st.rerun()


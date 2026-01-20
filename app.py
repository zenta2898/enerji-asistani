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
    /* Cihaz Kartları Tasarımı */
    .device-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2E7D32;
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        color: #333;
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
        # Güncel Elektrik Birim Fiyatı (EPDK'ya göre burayı güncelleyebilirsin)
        birim_fiyat = 2.59  # Örneğin 3.80 TL yaptık
        
        with st.expander("➕ Cihaz Ekle (Etikete Göre)", expanded=True):
            c_ad = st.selectbox("Cihaz Türü:", 
                                ["Buzdolabı", "Çamaşır Makinesi", "Bulaşık Makinesi", "Klima", "TV", "Aydınlatma (Ampul)", "Fırın/Ütü/Süpürge"])
            
            # --- CİHAZA ÖZEL AKILLI SORULAR ---
            if c_ad == "Buzdolabı":
                c_yillik_kwh = st.number_input("Etiketteki Yıllık Tüketim (kWh/annum):", value=274, 
                                               help="Siemens veya diğer marka etiketlerinin altındaki yıllık toplam kWh değeridir.")
                # Aylık kWh hesabı: Yıllık / 12
                aylik_kwh = c_yillik_kwh / 12
                c_watt = (aylik_kwh / 30) * 1000 / 24 # Arka plan uyumu için watt'a çevrilir
                c_saat = 24.0

            elif c_ad in ["Çamaşır Makinesi", "Bulaşık Makinesi"]:
                c_100_dongu = st.number_input("100 Döngü Başına Tüketim (kWh):", value=50, 
                                              help="Yeni etiketlerdeki '100' simgesinin yanındaki değerdir.")
                c_haftalik = st.slider("Haftalık Kullanım Sayısı:", 1, 14, 3)
                # Aylık kWh: (Değer/100) * Haftalık * 4.3 hafta
                aylik_kwh = (c_100_dongu / 100) * c_haftalik * 4.3
                c_watt = (aylik_kwh / 30) * 1000 / 1 # Arka plan uyumu
                c_saat = 1.0

            elif c_ad == "Klima":
                c_klima_yillik = st.number_input("Etiketteki Yıllık Isıtma/Soğutma Tüketimi (kWh/annum):", value=150, 
                                                 help="Klima etiketindeki mevsimsel kullanım değeridir.")
                aylik_kwh = c_klima_yillik / 12
                c_watt = (aylik_kwh / 30) * 1000 / 24
                c_saat = 24.0

            elif c_ad == "TV":
                c_tv_1000h = st.number_input("1000 Saatlik Tüketim (kWh):", value=60, 
                                             help="TV etiketindeki '1000h' yazan kutucuktaki değerdir.")
                c_gunluk_saat = st.slider("Günlük TV İzleme Süresi (Saat):", 1.0, 24.0, 4.0)
                # Aylık kWh: (Değer/1000) * Günlük Saat * 30
                aylik_kwh = (c_tv_1000h / 1000) * c_gunluk_saat * 30
                c_watt = (aylik_kwh / 30) * 1000 / c_gunluk_saat
                c_saat = c_gunluk_saat

            elif c_ad == "Aydınlatma (Ampul)":
                c_watt = st.number_input("Ampulün Gücü (Watt):", value=9, help="Ampul üzerindeki 5W, 9W, 12W gibi değerdir.")
                c_adet = st.number_input("Aynı Tip Ampul Adedi:", value=1, step=1)
                c_saat = st.slider("Günlük Yanma Süresi (Saat):", 1.0, 24.0, 5.0)
                c_watt = c_watt * c_adet # Toplam watt

            else: # Fırın, Ütü, Süpürge
                c_watt = st.number_input("Cihazın Gücü (Watt):", value=2000, help="Cihazın arkasındaki metal plaka veya kutudaki W değeridir.")
                c_saat = st.slider("Günlük Ortalama Kullanım (Saat):", 0.1, 10.0, 1.0)

            # --- EKLEME BUTONU ---
            if st.button("🚀 Cihazı Listeye Ekle"):
                st.session_state.cihazlar.append({"Cihaz": c_ad, "Watt": c_watt, "Saat": c_saat})
                st.toast(f"✅ {c_ad} hesaplamaya dahil edildi!")
                st.rerun()

        if st.session_state.cihazlar:
            df = pd.DataFrame(st.session_state.cihazlar)
            df['Maliyet'] = (df['Watt'] / 1000) * df['Saat'] * 30 * birim_fiyat
            
            # Eski st.metric yerine bu şık ve okunabilir kartı koyuyoruz:
            toplam_fatura_degeri = df['Maliyet'].sum()
            st.markdown(f"""
                <div style="
                    background-color: #f0f2f6; 
                    padding: 20px; 
                    border-radius: 15px; 
                    text-align: center;
                    border-left: 8px solid #2E7D32;
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                    margin-bottom: 20px;">
                    <p style="color: #555; margin: 0; font-size: 1.1rem; font-weight: bold;">📊 Toplam Tahmini Fatura</p>
                    <h2 style="color: #1a1a1a; margin: 0; font-size: 2.2rem; font-weight: 900;">{toplam_fatura_degeri:.2f} TL</h2>
                </div>
            """, unsafe_allow_html=True)
            
            # Pasta Grafiği
            fig = px.pie(df, values='Maliyet', names='Cihaz', hole=0.4,
                         color_discrete_sequence=px.colors.sequential.Greens_r)
            st.plotly_chart(fig, use_container_width=True)
            
            # Liste
            for idx, row in df.iterrows():
                with st.container():
                    # HTML ile kart görünümü oluşturuyoruz
                    st.markdown(f"""
                        <div class="device-card">
                            <div style="display: flex; justify-content: space-between;">
                                <strong>{row['Cihaz']}</strong>
                                <span style="color: #2E7D32; font-weight: bold;">{row['Maliyet']:.2f} TL</span>
                            </div>
                            <small style="color: gray;">Tahmini Aylık Tüketim: <b>{(row['Watt'] * row['Saat'] * 30 / 1000):.1f} kWh</b></small>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"🗑️ Sil", key=f"d_{idx}"):
                        st.session_state.cihazlar.pop(idx)
                        st.rerun()
    
    elif sayfa == "📚 Tasarruf Sırları":
        st.header("📖 Tasarruf Kütüphanesi")
        st.success("Tebrikler! Tasarruf adımlarını takip ederek verimliliği artırabilirsin.")

    if st.sidebar.button("Güvenli Çıkış"):
        st.session_state.giris = False
        st.rerun()
      

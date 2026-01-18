import streamlit as st
import time
import base64

# 1. Sayfa Ayarları
st.set_page_config(page_title="Enerji Master Pro", page_icon="🔋", layout="centered")

# --- VİDEO VE STİL AYARLARI ---
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
                width: auto; height: auto;
                z-index: -1;
                object-fit: cover;
                filter: brightness(0.5);
            }}
            .main-content {{
                position: relative;
                z-index: 1;
                text-align: center;
                color: white;
                padding-top: 10vh;
            }}
            </style>
            <video autoplay loop muted playsinline>
                <source src="data:video/mp4;base64,{bin_str}" type="video/mp4">
            </video>
            """,
            unsafe_allow_html=True
        )
    except:
        st.info("💡 Animasyon yükleniyor...")

# iPhone İkon Desteği
st.markdown('<link rel="apple-touch-icon" href="https://raw.githubusercontent.com/zenta2898/enerji-asistani/main/logo.png">', unsafe_allow_html=True)

# --- OTURUM VE VERİ YÖNETİMİ ---
if 'giris' not in st.session_state: st.session_state.giris = False
if 'cihazlar' not in st.session_state: st.session_state.cihazlar = []

# --- GİRİŞ EKRANI ---
if not st.session_state.giris:
    set_bg_video("intro.mp4")
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown("<h1 style='text-shadow: 2px 2px 10px #000;'>Enerji Master</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-shadow: 2px 2px 10px #000;'>En temiz enerji, tüketilmeyendir.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Enerji Yolculuğuna Başla", use_container_width=True):
            st.session_state.giris = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANA UYGULAMA ---
else:
    st.sidebar.image("logo.png", width=100)
    st.sidebar.title("🛠️ Kontrol Merkezi")
    sayfa = st.sidebar.radio("Sayfa:", ["📊 Fatura Analizi", "📚 Tasarruf Sırları"])

    if sayfa == "📊 Fatura Analizi":
        st.title("⚡ Akıllı Enerji Paneli")
        
        # CİHAZ EKLEME BÖLÜMÜ
        with st.expander("➕ Yeni Cihaz Ekle", expanded=True):
            c_ad = st.selectbox("Cihaz Tipi:", ["Buzdolabı", "Çamaşır Makinesi", "Bulaşık Makinesi", "Klima", "TV", "Ütü", "Fırın", "Diğer"])
            c_watt = st.number_input("Güç (Watt):", value=200, step=10)
            c_saat = st.slider("Günlük Kullanım (Saat):", 0.5, 24.0, 2.0)
            
            if st.button("Listeye Ekle"):
                st.session_state.cihazlar.append({"ad": c_ad, "watt": c_watt, "saat": c_saat})
                st.toast(f"{c_ad} başarıyla eklendi!")

        # HESAPLAMALAR VE TABLO
        if st.session_state.cihazlar:
            st.divider()
            toplam_kwh = 0
            birim_fiyat = 3.50 # TL/kWh
            
            data_for_chart = []
            
            for idx, c in enumerate(st.session_state.cihazlar):
                gunluk = (c['watt'] / 1000) * c['saat']
                aylik = gunluk * 30
                maliyet = aylik * birim_fiyat
                toplam_kwh += aylik
                
                col_a, col_b, col_c = st.columns([3,2,1])
                col_a.write(f"**{c['ad']}** ({c['watt']}W)")
                col_b.write(f"{maliyet:.2f} TL/Ay")
                if col_c.button("❌", key=f"del_{idx}"):
                    st.session_state.cihazlar.pop(idx)
                    st.rerun()
                
                data_for_chart.append({"Cihaz": c['ad'], "Maliyet": maliyet})

            # GENEL RAPOR
            st.divider()
            toplam_fatura = toplam_kwh * birim_fiyat
            st.metric("📊 Toplam Aylık Elektrik Faturası", f"{toplam_fatura:.2f} TL")
            
            # Yüzdesel Dağılım Grafiği
            if toplam_fatura > 0:
                st.subheader("💡 Faturanın Yüzde Kaçı Nereye Gidiyor?")
                import pandas as pd
                df = pd.DataFrame(data_for_chart)
                st.bar_chart(df.set_index("Cihaz"))
        else:
            st.info("Henüz cihaz eklemediniz. Yukarıdaki panelden ilk cihazınızı ekleyin!")

    elif sayfa == "📚 Tasarruf Sırları":
        st.header("📖 Tasarruf Kütüphanesi")
        st.success("Tebrikler! Listendeki cihazlarla bilinçli tüketime başladın.")

    if st.sidebar.button("Güvenli Çıkış"):
        st.session_state.giris = False
        st.rerun()

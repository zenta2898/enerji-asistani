import streamlit as st
import time
import base64
import pandas as pd
import plotly.express as px

# 1. Sayfa Ayarları
st.set_page_config(page_title="Enerji Master Pro", page_icon="🔋", layout="centered")

# --- MODERN TASARIM VE YEŞİL TEMA (CSS) ---
st.markdown("""
    <style>
    /* Ana Buton Tasarımı */
    div.stButton > button:first-child {
        background-color: #2E7D32;
        color: white;
        border-radius: 12px;
        border: none;
        height: 3em;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #4CAF50;
        border: none;
        color: white;
    }
    /* Kart Görünümü */
    .stExpander {
        border: 1px solid #e6e9ef;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

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
            .video-overlay {{
                position: relative;
                z-index: 1;
                text-align: center;
                color: white;
                padding-top: 15vh;
            }}
            </style>
            <video autoplay loop muted playsinline>
                <source src="data:video/mp4;base64,{bin_str}" type="video/mp4">
            </video>
            """,
            unsafe_allow_html=True
        )
    except:
        st.info("💡 Giriş animasyonu hazırlanıyor...")

# iPhone İkonu
st.markdown('<link rel="apple-touch-icon" href="https://raw.githubusercontent.com/zenta2898/enerji-asistani/main/logo.png">', unsafe_allow_html=True)

# --- OTURUM YÖNETİMİ ---
if 'giris' not in st.session_state: st.session_state.giris = False
if 'cihazlar' not in st.session_state: st.session_state.cihazlar = []

# --- GİRİŞ EKRANI ---
if not st.session_state.giris:
    set_bg_video("intro.mp4")
    st.markdown('<div class="video-overlay">', unsafe_allow_html=True)
    st.markdown("<h1 style='text-shadow: 2px 2px 10px #000; font-size: 3rem;'>Enerji Master</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-shadow: 2px 2px 10px #000; font-size: 1.2rem;'>Watt'ını Bil, Cebini Koru.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Enerji Yolculuğuna Başla", use_container_width=True):
            st.session_state.giris = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANA UYGULAMA PANELİ ---
else:
    st.sidebar.image("logo.png", width=100)
    st.sidebar.title("🌱 Kontrol Merkezi")
    sayfa = st.sidebar.radio("Gitmek İstediğin Yer:", ["📊 Fatura Analizi", "📚 Tasarruf Sırları"])

    if sayfa == "📊 Fatura Analizi":
        st.title("⚡ Akıllı Enerji Paneli")
        
        # Cihaz Ekleme Formu
        with st.expander("➕ Listeye Cihaz Ekle", expanded=True):
            c_ad = st.selectbox("Cihaz Seçin:", ["Buzdolabı", "Klima", "Çamaşır Makinesi", "Bulaşık Makinesi", "TV", "Fırın", "Ütü", "Süpürge", "Aydınlatma"])
            c_watt = st.number_input("Güç (Watt):", value=200, step=50)
            c_saat = st.slider("Günlük Kullanım (Saat):", 0.5, 24.0, 3.0)
            
            if st.button("Cihazı Listeye Ekle"):
                st.session_state.cihazlar.append({"Cihaz": c_ad, "Watt": c_watt, "Saat": c_saat})
                st.toast(f"✅ {c_ad} eklendi!")

        # Analiz Sonuçları
        if st.session_state.cihazlar:
            st.divider()
            df = pd.DataFrame(st.session_state.cihazlar)
            
            # Hesaplama (Birim Fiyat: 3.50 TL/kWh)
            df['Aylık_Maliyet'] = (df['Watt'] / 1000) * df['Saat'] * 30 * 3.50
            toplam_fatura = df['Aylık_Maliyet'].sum()
            
            st.metric("📊 Toplam Aylık Elektrik Faturası", f"{toplam_fatura:.2f} TL")

            # Pasta Grafiği (Hangi cihaz yüzde kaç?)
            fig = px.pie(df, values='Aylık_Maliyet', names='Cihaz', 
                         title='Faturadaki Yüzdesel Dağılım',
                         color_discrete_sequence=px.colors.sequential.Greens_r)
            st.plotly_chart(fig, use_container_width=True)

            # Cihaz Listesi ve Silme
            st.subheader("📋 Eklenen Cihazlar")
            for idx, row in df.iterrows():
                col_n, col_m, col_d = st.columns([3,2,1])
                col_n.write(f"**{row['Cihaz']}**")
                col_m.write(f"{row['Aylık_Maliyet']:.2f} TL")
                if col_d.button("Sil", key=f"del_{idx}"):
                    st.session_state.cihazlar.pop(idx)
                    st.rerun()
        else:
            st.info("Henüz cihaz eklemediniz. Yukarıdan cihaz ekleyerek analize başlayın!")

    elif sayfa == "📚 Tasarruf Sırları":
        st.header("📖 Tasarruf Kütüphanesi")
        st.success("Buzdolabını %15 daha verimli kullanmak için arkasını ayda bir süpürün!")

    if st.sidebar.button("Çıkış Yap"):
        st.session_state.giris = False
        st.rerun()

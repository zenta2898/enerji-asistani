# Colab üzerinde Streamlit çalıştırmak için gerekli kurulum (Sadece bir kez)
!pip install -q streamlit

# Uygulama dosyasını oluşturuyoruz
with open('app.py', 'w') as f:
    f.write('''
import streamlit as st

st.set_page_config(page_title="Enerji Master Pro", page_icon="🌱")

st.title("🌱 Enerji Master: Tasarruf Asistanı")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["⚡ Elektrik", "🔥 Doğalgaz", "📊 Genel Rapor"])

with tab1:
    st.header("Elektrikli Cihaz Analizi")
    
    col1, col2 = st.columns(2)
    with col1:
        cihaz = st.selectbox("Cihaz Seçin", ["Buzdolabı", "Çamaşır Makinesi", "Bulaşık Makinesi", "Klima", "Ütü", "Televizyon"])
        watt = st.number_input("Cihazın Gücü (Watt)", value=150, step=10)
    
    with col2:
        saat = st.slider("Günlük Kullanım (Saat)", 0.0, 24.0, 5.0)
        birim_fiyat = 3.50 # TL/kWh

    aylik_tuketim = (watt / 1000) * saat * 30
    aylik_maliyet = aylik_tuketim * birim_fiyat

    # Verimlilik Sınıfı Mantığı
    if watt < 100: sinif, renk = "A+++", "green"
    elif watt < 200: sinif, renk = "B", "orange"
    else: sinif, renk = "G (Verimsiz)", "red"

    st.metric("Tahmini Aylık Maliyet", f"{aylik_maliyet:.2f} TL", delta=f"{sinif} Sınıfı", delta_color="normal")

    # Cihaza Özel Zeki İpuçları
    ipucu_kutusu = st.expander("✨ Bu Cihaz İçin Tasarruf Sırları")
    if cihaz == "Buzdolabı":
        ipucu_kutusu.write("- Duvarla arasına en az 10 cm mesafe bırakın (Enerji %15 azalır).")
        ipucu_kutusu.write("- Kapak fitillerinin sızdırmazlığını kontrol edin.")
    elif cihaz == "Ütü":
        ipucu_kutusu.write("- Ütüleme bitmeden 5 dk önce fişi çekin, kalan ısı yeterli olacaktır.")

with tab2:
    st.header("Doğalgaz Tasarrufu")
    derece = st.slider("Kombi Ayarı (°C)", 35, 70, 45)
    yalitim = st.toggle("Evde Isı Yalıtımı (Mantolama) Var mı?")
    
    carpan = 0.7 if yalitim else 1.3
    tahmini_m3 = (derece / 40) * carpan * 10 * 30
    gaz_faturasi = tahmini_m3 * 9.0 # 9 TL/m3 varsayımı
    
    st.metric("Tahmini Gaz Faturası", f"{gaz_faturasi:.2f} TL")
    
    st.info("💡 İpucu: Peteklerin arkasına ısı yalıtım levhası koyarak faturanızı %5 düşürebilirsiniz.")

with tab3:
    st.subheader("Tasarruf Hedefleri")
    hedef = st.progress(70, text="Bu ayki enerji tasarrufu hedefine %70 yaklaştınız!")
    st.write("✅ Buzdolabı ayarı yapıldı (+20 TL kazanç)")
    st.write("❌ Klima gereksiz çalıştırıldı (-45 TL kayıp)")
    ''')

# Uygulamayı geçici olarak internete açmak için (Colab için özel)
!npx localtunnel --port 8501

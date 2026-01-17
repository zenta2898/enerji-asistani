import streamlit as st

# Uygulama Başlığı ve Ayarları
st.set_page_config(page_title="Enerji Master Pro", page_icon="🌱")

st.title("🌱 Enerji Master: Tasarruf Asistanı")
st.markdown("---")

# Sekmeler (Tablar)
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
    if watt < 100: sinif, renk = "A+++ ✅", "green"
    elif watt < 300: sinif, renk = "B ⚠️", "orange"
    else: sinif, renk = "G (Verimsiz) ❌", "red"

    st.metric("Tahmini Aylık Maliyet", f"{aylik_maliyet:.2f} TL")
    st.write(f"Enerji Verimlilik Tahmini: **{sinif}**")

    # Cihaza Özel Zeki İpuçları
    with st.expander("✨ Bu Cihaz İçin Tasarruf Sırları"):
        if cihaz == "Buzdolabı":
            st.write("- Duvarla arasına en az 10 cm mesafe bırakın (Enerji %15 azalır).")
            st.write("- Arkasındaki tozları 6 ayda bir süpürgeyle alın.")
        elif cihaz == "Ütü":
            st.write("- Ütüleme bitmeden 5 dk önce fişi çekin, mevcut ısı yeterli olur.")
        else:
            st.write("- Cihazı kullanmadığınızda fişten çekmek gizli tüketimi önler.")

with tab2:
    st.header("Doğalgaz Tasarrufu")
    derece = st.slider("Kombi Isısı (°C)", 35, 75, 45)
    yalitim = st.checkbox("Evde Isı Yalıtımı Var mı?")
    
    carpan = 0.7 if yalitim else 1.3
    tahmini_m3 = (derece / 40) * carpan * 10 * 30
    gaz_faturasi = tahmini_m3 * 9.0 
    
    st.metric("Tahmini Gaz Faturası", f"{gaz_faturasi:.2f} TL")
    st.info("💡 İpucu: Geceleri dereceyi 2-3 birim düşürmek faturayı %10 etkiler.")

with tab3:
    st.subheader("Tasarruf Durumu")
    st.progress(70, text="Hedeflenen tasarrufun %70'ine ulaşıldı.")
    st.success("Tebrikler! Geçen aya göre %15 daha verimlisiniz.")


import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="In Silico De Novo Molekül Tasarımı", layout="wide")

st.title("🧬 IN SILICO DE NOVO MOLEKÜL TASARIMI")
st.markdown("---")

# Sidebar - Girdiler
with st.sidebar:
    st.header("📋 PROJE BİLGİLERİ")
    
    proje_adi = st.text_input("Proje Adı", "Proje_001")
    
    st.subheader("🎯 Hedef Protein")
    pdb_file = st.file_uploader("PDB Dosyası Yükleyin", type=['pdb'])
    
    st.subheader("📍 Bağlanma Bölgesi (Binding Site)")
    binding_method = st.selectbox(
        "Binding Site Seçim Yöntemi",
        ["Otomatik tespit (pocket finder)", 
         "Grid box koordinatları", 
         "Referans ligand", 
         "Aminoasit listesi"]
    )
    
    if binding_method == "Grid box koordinatları":
        col1, col2 = st.columns(2)
        with col1:
            center_x = st.number_input("Center X", value=0.0)
            center_y = st.number_input("Center Y", value=0.0)
            center_z = st.number_input("Center Z", value=0.0)
        with col2:
            size_x = st.number_input("Size X", value=20.0)
            size_y = st.number_input("Size Y", value=20.0)
            size_z = st.number_input("Size Z", value=20.0)
    
    blind_docking = st.checkbox("Blind Docking (Tüm protein tarama)")
    
    st.subheader("🔬 Hedef Konformasyon")
    konformasyon = st.selectbox(
        "Konformasyon Tipi",
        ["Aktif (agonist-uygun)", "İnaktif (antagonist-uygun)", 
         "Bilinmiyor", "Allosterik Modülatör"]
    )
    
    istenen_etki = st.radio(
        "İstenen Farmakolojik Etki",
        ["Agonist", "Antagonist", "Modülatör", "Allosteric modulator", "Bilinmiyor"]
    )
    
    st.subheader("👥 Hedef Popülasyon")
    populasyon = st.selectbox(
        "İlaç Kullanım Yaş Grubu",
        ["0-2", "2-18", "18-45", "45-65", "65-85", "85+", "Bilinmiyor"]
    )
    
    st.subheader("💉 Uygulama Yolu")
    uygulama = st.selectbox(
        "İlaç Uygulama Yolu",
        ["Oral", "İntravenöz", "İntramüsküler", "İnhalasyon", "Dermal", "Subkütan", "Diğer"]
    )
    
    st.subheader("⚙️ Yöntem Seçimi")
    yontem = st.selectbox(
        "De Novo Tasarım Yöntemi",
        ["Fragment-based", "SMILES-based generative model (RNN/Transformer)",
         "GA (genetic algorithm)", "Ligand growing", "Reaction-based enumeration"]
    )
    
    seed_file = st.file_uploader("Başlangıç Molekülü (isteğe bağlı)", type=['sdf', 'mol2'])
    
    molekul_sayisi = st.select_slider(
        "Üretilecek Molekül Sayısı",
        options=["1-5", "5-10", "10-50", "50-100"]
    )
    
    st.markdown("---")
    run_button = st.button("🚀 ANALİZİ BAŞLAT", type="primary", use_container_width=True)

# Ana İçerik
if pdb_file and run_button:
    st.success(f"✅ {pdb_file.name} dosyası başarıyla yüklendi!")
    
    with st.spinner("Analiz yapılıyor... Lütfen bekleyin..."):
        import time
        time.sleep(2)  # Simülasyon için bekleme
    
    st.success("✨ Analiz tamamlandı!")
    
    # Tab yapısı
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Genel Sonuçlar", "🔬 Docking Sonuçları", "💊 Druggability Score", "🎨 3D Görselleştirme"])
    
    with tab1:
        st.header("📊 GENEL SONUÇLAR")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Üretilen Molekül Sayısı", "47")
        with col2:
            st.metric("Başarılı Docking", "42")
        with col3:
            st.metric("Ortalama Binding Affinity", "-8.3 kcal/mol")
        with col4:
            st.metric("En İyi Druggability Score", "0.82")
        
        st.subheader("Top 10 Molekül Adayı")
        
        # Örnek veri tablosu
        results_data = {
            "Molekül ID": [f"Ligand-{str(i).zfill(3)}" for i in range(1, 11)],
            "SMILES": ["C1=CC=C(C=C1)C(=O)O", "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",
                       "C1=CC=C2C(=C1)C=CC=N2", "CC1=CC=C(C=C1)NC(=O)C",
                       "C1=CC(=CC=C1O)C(=O)O", "CC(C)NCC(C1=CC(=C(C=C1)O)CO)O",
                       "C1=CC=C(C=C1)CCNC(=O)C", "CC(C)(C)NCC(C1=CC=CC=C1)O",
                       "C1=CC=C(C=C1)C=CC(=O)O", "CC1=CC=C(C=C1)S(=O)(=O)N"],
            "MW (Da)": [320, 298, 256, 310, 275, 342, 288, 305, 294, 318],
            "Binding Affinity (kcal/mol)": [-9.2, -8.8, -8.5, -8.3, -8.1, -7.9, -7.7, -7.5, -7.3, -7.1],
            "Docking Score": [8.9, 8.5, 8.2, 8.0, 7.8, 7.6, 7.4, 7.2, 7.0, 6.8],
            "Druggability Score": [0.82, 0.78, 0.75, 0.71, 0.68, 0.65, 0.62, 0.59, 0.56, 0.53]
        }
        
        df = pd.DataFrame(results_data)
        st.dataframe(df, use_container_width=True)
        
        # Grafikler
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                x=df["Molekül ID"],
                y=df["Binding Affinity (kcal/mol)"],
                marker_color='lightblue',
                text=df["Binding Affinity (kcal/mol)"],
                textposition='outside'
            ))
            fig1.update_layout(
                title="Binding Affinity Karşılaştırması",
                xaxis_title="Molekül ID",
                yaxis_title="Binding Affinity (kcal/mol)",
                height=400
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=df["Molekül ID"],
                y=df["Druggability Score"],
                marker_color='lightgreen',
                text=df["Druggability Score"],
                textposition='outside'
            ))
            fig2.update_layout(
                title="Druggability Score Karşılaştırması",
                xaxis_title="Molekül ID",
                yaxis_title="Druggability Score",
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.header("🔬 DOCKING SONUÇLARI")
        
        selected_ligand = st.selectbox("Molekül Seçin", df["Molekül ID"].tolist())
        
        idx = df[df["Molekül ID"] == selected_ligand].index[0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Binding Affinity", f"{df.iloc[idx]['Binding Affinity (kcal/mol)']} kcal/mol")
        with col2:
            st.metric("Docking Score", f"{df.iloc[idx]['Docking Score']}")
        with col3:
            st.metric("Moleküler Ağırlık", f"{df.iloc[idx]['MW (Da)']} Da")
        
        st.subheader("🔗 Ligand-Amino Asit Etkileşimleri")
        
        interactions_data = {
            "Amino Asit": ["ASP102", "HIS57", "SER195", "GLY216", "TRP215", "VAL213"],
            "Etkileşim Tipi": ["Hidrojen Bağı", "π-π Stacking", "Hidrojen Bağı", 
                               "Hidrofobik", "π-π Stacking", "Hidrofobik"],
            "Mesafe (Å)": [2.8, 3.5, 2.9, 4.2, 3.8, 4.1],
            "Enerji Katkısı (kcal/mol)": [-2.5, -1.8, -2.3, -1.2, -1.5, -1.0]
        }
        
        interactions_df = pd.DataFrame(interactions_data)
        st.dataframe(interactions_df, use_container_width=True)
        
        st.subheader("📌 Binding Site Bilgisi")
        st.info("""
        **Aktif Bölge Amino Asitleri:** ASP102, HIS57, SER195, GLY216, TRP215, VAL213, ARG204
        
        **Bağlanma Koordinatları:**
        - X: 15.3 Å
        - Y: 22.7 Å  
        - Z: 8.9 Å
        
        **Pocket Hacmi:** 458.3 Ų
        """)
        
        st.subheader("📊 Konformasyon Kümeleme Analizi")
        cluster_data = {
            "Cluster": ["Cluster 1", "Cluster 2", "Cluster 3"],
            "Pose Sayısı": [15, 8, 4],
            "Ortalama Enerji (kcal/mol)": [-9.2, -8.5, -7.8],
            "RMSD (Å)": [1.2, 2.1, 3.5]
        }
        cluster_df = pd.DataFrame(cluster_data)
        st.dataframe(cluster_df, use_container_width=True)
    
    with tab3:
        st.header("💊 DRUGGABILITY SCORE DETAYI")
        
        selected_ligand_drug = st.selectbox("Molekül Seçin ", df["Molekül ID"].tolist(), key="drug_select")
        idx = df[df["Molekül ID"] == selected_ligand_drug].index[0]
        
        # Büyük skor gösterimi
        score = df.iloc[idx]['Druggability Score']
        
        if score >= 0.6:
            color = "green"
            status = "✅ YÜKSEK İLAÇLANABİLİRLİK"
        elif score >= 0.3:
            color = "orange"
            status = "⚠️ ORTA İLAÇLANABİLİRLİK"
        else:
            color = "red"
            status = "❌ DÜŞÜK İLAÇLANABİLİRLİK"
        
        st.markdown(f"## <span style='color:{color}'>{score}</span>", unsafe_allow_html=True)
        st.markdown(f"### {status}")
        
        st.info("""
        **Açıklama:** Molekülün bağlanma potansiyeli, farmakokinetik özellikleri ve 
        toksisite profili göz önünde bulundurularak hesaplanmıştır.
        """)
        
        # Moleküler Özellikler
        st.subheader("🧪 Moleküler Özellikler")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("MW", f"{df.iloc[idx]['MW (Da)']} Da", help="Molekül Ağırlığı (ideal: 150-500 Da)")
        with col2:
            st.metric("LogP", "3.1", help="Lipofiliklik (optimum: 0-5)")
        with col3:
            st.metric("H-Bağı Donör", "2", help="Hidrojen bağı donör sayısı")
        with col4:
            st.metric("H-Bağı Alıcı", "5", help="Hidrojen bağı alıcı sayısı")
        
        col5, col6, col7 = st.columns(3)
        with col5:
            st.metric("Rotatable Bonds", "4", help="Dönen bağ sayısı (ideal: ≤10)")
        with col6:
            st.metric("PSA", "75 Ų", help="Polar Surface Area")
        with col7:
            st.metric("SMILES", df.iloc[idx]['SMILES'][:20] + "...", help="Kimyasal yapı kodu")
        
        # Radar Chart
        st.subheader("📊 Özellik Dağılımı (Radar Chart)")
        
        categories = ['MW', 'LogP', 'H-Bağı', 'PSA', 'Rotatable Bonds', 'ADME Uyumu']
        values = [0.85, 0.75, 0.90, 0.80, 0.88, 0.82]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=selected_ligand_drug
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Karşılaştırma Grafiği
        st.subheader("📈 Molekül Karşılaştırması")
        
        fig_compare = go.Figure()
        fig_compare.add_trace(go.Bar(
            x=df["Molekül ID"][:5],
            y=df["Druggability Score"][:5],
            marker_color=['green' if s >= 0.6 else 'orange' if s >= 0.3 else 'red' 
                          for s in df["Druggability Score"][:5]],
            text=df["Druggability Score"][:5],
            textposition='outside'
        ))
        
        fig_compare.update_layout(
            title="Top 5 Molekül Druggability Score Karşılaştırması",
            xaxis_title="Molekül ID",
            yaxis_title="Druggability Score",
            height=400
        )
        
        st.plotly_chart(fig_compare, use_container_width=True)
        
        # ADME-Tox Tahminleri
        st.subheader("💊 ADME-Tox Profili")
        
        adme_data = {
            "Özellik": ["Absorpsiyon", "Dağılım", "Metabolizma", "Eliminasyon", "Toksisite"],
            "Değerlendirme": ["İyi", "Orta", "İyi", "İyi", "Düşük Risk"],
            "Skor": [0.85, 0.65, 0.80, 0.78, 0.90]
        }
        
        adme_df = pd.DataFrame(adme_data)
        st.dataframe(adme_df, use_container_width=True)
        
        # İndirme butonları
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📄 PDF Raporu İndir", "Rapor içeriği buraya gelecek", "rapor.pdf")
        with col2:
            st.download_button("📊 CSV İndir", df.to_csv(index=False), "sonuclar.csv", "text/csv")
    
    with tab4:
        st.header("🎨 3D GÖRSELLEŞTIRME")
        
        st.info("🔬 Protein-Ligand kompleksinin 3D görselleştirmesi")
        
        selected_ligand_3d = st.selectbox("Görselleştirilecek Molekül", df["Molekül ID"].tolist(), key="3d_select")
        
        # 3D görselleştirme placeholder
        st.markdown("""
        ### Protein-Ligand Kompleksi
        
        Bu bölümde normalde interaktif 3D moleküler görselleştirme yer alacak.
        
        **Gösterilecek Özellikler:**
        - Protein yapısı (cartoon/ribbon)
        - Ligand molekülü (sticks/balls)
        - Hidrojen bağları (kesikli çizgiler)
        - Hidrofobik etkileşimler
        - π-π stacking etkileşimleri
        - Aktif bölge amino asitleri (labels)
        
        **Kontroller:**
        - Fare ile döndürme
        - Scroll ile zoom
        - Sağ tık ile kaydırma
        """)
        
        # Görselleştirme simülasyonu için basit bir grafik
        fig_3d = go.Figure(data=[go.Scatter3d(
            x=np.random.randn(100),
            y=np.random.randn(100),
            z=np.random.randn(100),
            mode='markers',
            marker=dict(
                size=5,
                color=np.random.randn(100),
                colorscale='Viridis',
                showscale=True
            )
        )])
        
        fig_3d.update_layout(
            title="Protein-Ligand Kompleksi (Simülasyon)",
            scene=dict(
                xaxis_title='X (Å)',
                yaxis_title='Y (Å)',
                zaxis_title='Z (Å)'
            ),
            height=600
        )
        
        st.plotly_chart(fig_3d, use_container_width=True)
        
        st.markdown("---")
        st.download_button("💾 PDB Dosyası İndir", "PDB içeriği buraya gelecek", "complex.pdb")

else:
    st.info("👈 Lütfen sol menüden bir PDB dosyası yükleyin ve parametreleri ayarlayın.")
    
    # Örnek kullanım bilgisi
    with st.expander("ℹ️ Kullanım Kılavuzu"):
        st.markdown("""
        ### Nasıl Kullanılır?
        
        1. **Hedef Protein:** PDB formatında protein yapısı yükleyin
        2. **Binding Site:** Ligandın bağlanacağı bölgeyi belirleyin
        3. **Parametre Seçimi:** Konformasyon tipi, hedef popülasyon ve uygulama yolu seçin
        4. **Yöntem:** De novo tasarım yöntemini seçin
        5. **Analizi Başlat:** Butona tıklayarak molekül tasarımını başlatın
        
        ### Çıktılar
        
        - **Docking Sonuçları:** Bağlanma enerjisi, docking score ve etkileşimler
        - **Druggability Score:** Molekülün ilaç olma potansiyeli (0-1 arası)
        - **3D Görselleştirme:** Protein-ligand kompleksinin interaktif görünümü
        - **ADME-Tox:** Farmakokinetik ve toksisite tahminleri
        """)
    
    with st.expander("📚 Druggability Score Nedir?"):
        st.markdown("""
        **Druggability Score**, bir molekülün ilaç benzeri özellikler taşıma olasılığını 
        0-1 arası bir değerle ifade eder.
        
        - **0.0 - 0.3:** Düşük ilaçlanabilirlik
        - **0.3 - 0.6:** Orta ilaçlanabilirlik  
        - **0.6 - 1.0:** Yüksek ilaçlanabilirlik
        
        Skor hesaplanırken şu parametreler dikkate alınır:
        - Molekül Ağırlığı (MW)
        - LogP (lipofiliklik)
        - Hidrojen bağı donör/alıcı sayısı
        - Rotatable bonds
        - Polar Surface Area (PSA)
        - ADME-Tox özellikleri
        """)

# Footer
st.markdown("---")
st.markdown("💡 **Not:** Bu arayüz örnek çıktılarla çalışmaktadır. Gerçek hesaplamalar backend entegrasyonu ile yapılacaktır.")
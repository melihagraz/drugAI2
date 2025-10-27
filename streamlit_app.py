import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="In Silico De Novo Molekül Tasarımı", layout="wide")

st.title("🧬 IN SILICO DE NOVO MOLEKÜL TASARIMI")
st.markdown("---")

# ------------------------------------------------------------
# Yardımcılar
# ------------------------------------------------------------

def demo_dataframe(n: int = 10) -> pd.DataFrame:
    return pd.DataFrame({
        "Molekül ID": [f"Ligand-{str(i).zfill(3)}" for i in range(1, n + 1)],
        "SMILES": [
            "C1=CC=C(C=C1)C(=O)O",
            "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",
            "C1=CC=C2C(=C1)C=CC=N2",
            "CC1=CC=C(C=C1)NC(=O)C",
            "C1=CC(=CC=C1O)C(=O)O",
            "CC(C)NCC(C1=CC(=C(C=C1)O)CO)O",
            "C1=CC=C(C=C1)CCNC(=O)C",
            "CC(C)(C)NCC(C1=CC=CC=C1)O",
            "C1=CC=C(C=C1)C=CC(=O)O",
            "CC1=CC=C(C=C1)S(=O)(=O)N",
        ],
        "MW (Da)": [320, 298, 256, 310, 275, 342, 288, 305, 294, 318],
        "Binding Affinity (kcal/mol)": [-9.2, -8.8, -8.5, -8.3, -8.1, -7.9, -7.7, -7.5, -7.3, -7.1],
        "Docking Score": [8.9, 8.5, 8.2, 8.0, 7.8, 7.6, 7.4, 7.2, 7.0, 6.8],
        "Druggability Score": [0.82, 0.78, 0.75, 0.71, 0.68, 0.65, 0.62, 0.59, 0.56, 0.53],
    })


def safe_bar_chart(x, y, title, x_title, y_title, height=400, texts=None):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=x,
            y=y,
            text=texts if texts is not None else y,
            textposition="outside",
        )
    )
    fig.update_layout(title=title, xaxis_title=x_title, yaxis_title=y_title, height=height)
    return fig


# ------------------------------------------------------------
# Sidebar - Girdiler
# ------------------------------------------------------------
with st.sidebar:
    st.header("📋 PROJE BİLGİLERİ")

    proje_adi = st.text_input("Proje Adı", "Proje_001")

    st.subheader("🎯 Hedef Protein")
    pdb_file = st.file_uploader("PDB Dosyası Yükleyin", type=["pdb"])  # None olabilir

    st.subheader("📍 Bağlanma Bölgesi (Binding Site)")
    binding_method = st.selectbox(
        "Binding Site Seçim Yöntemi",
        [
            "Otomatik tespit (pocket finder)",
            "Grid box koordinatları",
            "Referans ligand",
            "Aminoasit listesi",
        ],
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
        ["Aktif (agonist-uygun)", "İnaktif (antagonist-uygun)", "Bilinmiyor", "Allosterik Modülatör"],
    )

    istenen_etki = st.radio(
        "İstenen Farmakolojik Etki",
        ["Agonist", "Antagonist", "Modülatör", "Allosteric modulator", "Bilinmiyor"],
    )

    st.subheader("👥 Hedef Popülasyon")
    populasyon = st.selectbox(
        "İlaç Kullanım Yaş Grubu",
        ["0-2", "2-18", "18-45", "45-65", "65-85", "85+", "Bilinmiyor"],
    )

    st.subheader("💉 Uygulama Yolu")
    uygulama = st.selectbox(
        "İlaç Uygulama Yolu",
        ["Oral", "İntravenöz", "İntramüsküler", "İnhalasyon", "Dermal", "Subkütan", "Diğer"],
    )

    st.subheader("⚙️ Yöntem Seçimi")
    yontem = st.selectbox(
        "De Novo Tasarım Yöntemi",
        [
            "Fragment-based",
            "SMILES-based generative model (RNN/Transformer)",
            "GA (genetic algorithm)",
            "Ligand growing",
            "Reaction-based enumeration",
        ],
    )

    seed_file = st.file_uploader("Başlangıç Molekülü (isteğe bağlı)", type=["sdf", "mol2"])

    molekul_sayisi = st.select_slider(
        "Üretilecek Molekül Sayısı",
        options=["1-5", "5-10", "10-50", "50-100"],
    )

    st.markdown("---")
    run_button = st.button("🚀 ANALİZİ BAŞLAT", type="primary", use_container_width=True)

# ------------------------------------------------------------
# Ana İçerik (Hata yakalama ile)
# ------------------------------------------------------------
try:
    # Demo DF her zaman elde olsun (boş/None durumlarında bile)
    np.random.seed(42)
    demo_df = demo_dataframe(10)

    if run_button and not pdb_file:
        st.warning("Önce bir PDB dosyası yükleyin.")

    if pdb_file and run_button:
        st.success(f"✅ {getattr(pdb_file, 'name', 'PDB')} dosyası başarıyla yüklendi!")

        with st.spinner("Analiz yapılıyor... Lütfen bekleyin..."):
            import time
            time.sleep(2)  # Simülasyon

        st.success("✨ Analiz tamamlandı!")

        # Analiz sonuçları (örnek)
        df = demo_dataframe(10)

        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Genel Sonuçlar",
            "🔬 Docking Sonuçları",
            "💊 Druggability Score",
            "🎨 3D Görselleştirme",
        ])

        # ---------------- Tab 1 ----------------
        with tab1:
            st.header("📊 GENEL SONUÇLAR")

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("Üretilen Molekül Sayısı", "47")
            with c2:
                st.metric("Başarılı Docking", "42")
            with c3:
                st.metric("Ortalama Binding Affinity", "-8.3 kcal/mol")
            with c4:
                st.metric("En İyi Druggability Score", "0.82")

            st.subheader("Top 10 Molekül Adayı")
            st.dataframe(df, use_container_width=True)

            c1, c2 = st.columns(2)
            with c1:
                fig1 = safe_bar_chart(
                    x=df["Molekül ID"],
                    y=df["Binding Affinity (kcal/mol)"],
                    title="Binding Affinity Karşılaştırması",
                    x_title="Molekül ID",
                    y_title="Binding Affinity (kcal/mol)",
                    height=400,
                )
                st.plotly_chart(fig1, use_container_width=True)

            with c2:
                fig2 = safe_bar_chart(
                    x=df["Molekül ID"],
                    y=df["Druggability Score"],
                    title="Druggability Score Karşılaştırması",
                    x_title="Molekül ID",
                    y_title="Druggability Score",
                    height=400,
                )
                st.plotly_chart(fig2, use_container_width=True)

        # ---------------- Tab 2 ----------------
        with tab2:
            st.header("🔬 DOCKING SONUÇLARI")

            selected_ligand = st.selectbox("Molekül Seçin", df["Molekül ID"].tolist())
            idx = df.index[df["Molekül ID"] == selected_ligand][0]

            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Binding Affinity", f"{df.iloc[idx]['Binding Affinity (kcal/mol)']} kcal/mol")
            with c2:
                st.metric("Docking Score", f"{df.iloc[idx]['Docking Score']}")
            with c3:
                st.metric("Moleküler Ağırlık", f"{df.iloc[idx]['MW (Da)']} Da")

            st.subheader("🔗 Ligand-Amino Asit Etkileşimleri")
            interactions_df = pd.DataFrame({
                "Amino Asit": ["ASP102", "HIS57", "SER195", "GLY216", "TRP215", "VAL213"],
                "Etkileşim Tipi": [
                    "Hidrojen Bağı",
                    "π-π Stacking",
                    "Hidrojen Bağı",
                    "Hidrofobik",
                    "π-π Stacking",
                    "Hidrofobik",
                ],
                "Mesafe (Å)": [2.8, 3.5, 2.9, 4.2, 3.8, 4.1],
                "Enerji Katkısı (kcal/mol)": [-2.5, -1.8, -2.3, -1.2, -1.5, -1.0],
            })
            st.dataframe(interactions_df, use_container_width=True)

            st.subheader("📌 Binding Site Bilgisi")
            st.info(
                """
                **Aktif Bölge Amino Asitleri:** ASP102, HIS57, SER195, GLY216, TRP215, VAL213, ARG204

                **Bağlanma Koordinatları:**
                - X: 15.3 Å
                - Y: 22.7 Å  
                - Z: 8.9 Å

                **Pocket Hacmi:** 458.3 Å³
                """
            )

            st.subheader("📊 Konformasyon Kümeleme Analizi")
            cluster_df = pd.DataFrame(
                {
                    "Cluster": ["Cluster 1", "Cluster 2", "Cluster 3"],
                    "Pose Sayısı": [15, 8, 4],
                    "Ortalama Enerji (kcal/mol)": [-9.2, -8.5, -7.8],
                    "RMSD (Å)": [1.2, 2.1, 3.5],
                }
            )
            st.dataframe(cluster_df, use_container_width=True)

        # ---------------- Tab 3 ----------------
        with tab3:
            st.header("💊 DRUGGABILITY SCORE DETAYI")

            selected_ligand_drug = st.selectbox(
                "Molekül Seçin ", df["Molekül ID"].tolist(), key="drug_select"
            )
            idx = df.index[df["Molekül ID"] == selected_ligand_drug][0]

            score = float(df.iloc[idx]["Druggability Score"])
            if score >= 0.6:
                color = "green"
                status = "✅ YÜKSEK İLAÇLANABİLİRLİK"
            elif score >= 0.3:
                color = "orange"
                status = "⚠️ ORTA İLAÇLANABİLİRLİK"
            else:
                color = "red"
                status = "❌ DÜŞÜK İLAÇLANABİLİRLİK"

            st.markdown(f"## <span style='color:{color}'>{score:.2f}</span>", unsafe_allow_html=True)
            st.markdown(f"### {status}")

            st.info(
                """
                **Açıklama:** Molekülün bağlanma potansiyeli, farmakokinetik özellikleri ve 
                toksisite profili göz önünde bulundurularak hesaplanmıştır.
                """
            )

            st.subheader("🧪 Moleküler Özellikler")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("MW", f"{df.iloc[idx]['MW (Da)']} Da", help="Molekül Ağırlığı (ideal: 150-500 Da)")
            with c2:
                st.metric("LogP", "3.1", help="Lipofiliklik (optimum: 0-5)")
            with c3:
                st.metric("H-Bağı Donör", "2", help="Hidrojen bağı donör sayısı")
            with c4:
                st.metric("H-Bağı Alıcı", "5", help="Hidrojen bağı alıcı sayısı")

            c5, c6, c7 = st.columns(3)
            with c5:
                st.metric("Rotatable Bonds", "4", help="Dönen bağ sayısı (ideal: ≤10)")
            with c6:
                st.metric("PSA", "75 Å²", help="Polar Surface Area")
            with c7:
                st.metric("SMILES", df.iloc[idx]["SMILES"][:20] + "...", help="Kimyasal yapı kodu")

            st.subheader("📊 Özellik Dağılımı (Radar Chart)")
            categories = ["MW", "LogP", "H-Bağı", "PSA", "Rotatable Bonds", "ADME Uyumu"]
            values = [0.85, 0.75, 0.90, 0.80, 0.88, 0.82]
            fig_radar = go.Figure()
            fig_radar.add_trace(
                go.Scatterpolar(r=values, theta=categories, fill="toself", name=selected_ligand_drug)
            )
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True, height=500
            )
            st.plotly_chart(fig_radar, use_container_width=True)

            st.subheader("📈 Molekül Karşılaştırması")
            fig_compare = go.Figure()
            top5 = df.head(5)
            colors = ["green" if s >= 0.6 else "orange" if s >= 0.3 else "red" for s in top5["Druggability Score"]]
            fig_compare.add_trace(
                go.Bar(x=top5["Molekül ID"], y=top5["Druggability Score"], text=top5["Druggability Score"], textposition="outside")
            )
            fig_compare.update_layout(
                title="Top 5 Molekül Druggability Score Karşılaştırması",
                xaxis_title="Molekül ID",
                yaxis_title="Druggability Score",
                height=400,
            )
            st.plotly_chart(fig_compare, use_container_width=True)

            st.subheader("💊 ADME-Tox Profili")
            adme_df = pd.DataFrame(
                {
                    "Özellik": ["Absorpsiyon", "Dağılım", "Metabolizma", "Eliminasyon", "Toksisite"],
                    "Değerlendirme": ["İyi", "Orta", "İyi", "İyi", "Düşük Risk"],
                    "Skor": [0.85, 0.65, 0.80, 0.78, 0.90],
                }
            )
            st.dataframe(adme_df, use_container_width=True)

            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                # Basit bir metin raporu indirilebilir içerik (PDF yerine TXT; byte/str güvenli)
                rapor = "Rapor: Örnek analiz sonuçları\nProje: " + proje_adi
                st.download_button("📄 Raporu İndir (TXT)", rapor, file_name="rapor.txt")
            with c2:
                st.download_button(
                    "📊 CSV İndir", df.to_csv(index=False), file_name="sonuclar.csv", mime="text/csv"
                )

        # ---------------- Tab 4 ----------------
        with tab4:
            st.header("🎨 3D GÖRSELLEŞTIRME")
            st.info("🔬 Protein-Ligand kompleksinin 3D görselleştirmesi (örnek simülasyon)")
            selected_ligand_3d = st.selectbox(
                "Görselleştirilecek Molekül", df["Molekül ID"].tolist(), key="3d_select"
            )

            # Simülasyon 3D nokta bulutu
            fig_3d = go.Figure(
                data=[
                    go.Scatter3d(
                        x=np.random.randn(100),
                        y=np.random.randn(100),
                        z=np.random.randn(100),
                        mode="markers",
                        marker=dict(size=5, color=np.random.randn(100), showscale=True),
                    )
                ]
            )
            fig_3d.update_layout(
                title="Protein-Ligand Kompleksi (Simülasyon)",
                scene=dict(xaxis_title="X (Å)", yaxis_title="Y (Å)", zaxis_title="Z (Å)"),
                height=600,
            )
            st.plotly_chart(fig_3d, use_container_width=True)

            st.markdown("---")
            st.download_button("💾 PDB Dosyası İndir (Örnek)", "PDB içerik örneği", file_name="complex.pdb")

    else:
        # Boş/demoda kullanıcıya rehber ve örnek çıktı göster
        st.info("👈 Soldan bir PDB dosyası yükleyip **ANALİZİ BAŞLAT** butonuna basın. Aşağıda örnek bir görünüm var.")

        st.subheader("Top 10 Molekül Adayı (Örnek)")
        st.dataframe(demo_df, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(
                safe_bar_chart(
                    x=demo_df["Molekül ID"],
                    y=demo_df["Binding Affinity (kcal/mol)"],
                    title="Binding Affinity Karşılaştırması (Örnek)",
                    x_title="Molekül ID",
                    y_title="Binding Affinity (kcal/mol)",
                ),
                use_container_width=True,
            )
        with c2:
            st.plotly_chart(
                safe_bar_chart(
                    x=demo_df["Molekül ID"],
                    y=demo_df["Druggability Score"],
                    title="Druggability Score Karşılaştırması (Örnek)",
                    x_title="Molekül ID",
                    y_title="Druggability Score",
                ),
                use_container_width=True,
            )

    st.markdown("---")
    st.markdown(
        "💡 **Not:** Bu arayüz örnek çıktılarla çalışır. Gerçek hesaplamalar backend entegrasyonu ile sağlanacaktır."
    )

except Exception as e:
    st.error("Uygulama çalışırken bir hata oluştu. Ayrıntılar aşağıda:")
    st.exception(e)

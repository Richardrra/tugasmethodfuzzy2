import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. INTERFACE STREAMLIT (Konfigurasi & Input)
# ==========================================
st.set_page_config(page_title="Fuzzy Tingkat Kemacetan", page_icon="🚘", layout="wide")

st.title("🚘 Logika Fuzzy: Tingkat Kemacetan (Kasus 3)")
st.markdown("Implementasi Streamlit untuk Tugas Praktikum Logika Fuzzy berdasarkan **Jumlah Kendaraan**.")

# Sidebar khusus untuk Input (Bagian dari Interface)
st.sidebar.header("⚙️ Interface Input")
st.sidebar.write("Silakan atur jumlah kendaraan saat ini:")
x_input = st.sidebar.slider("Jumlah Kendaraan (unit):", min_value=0, max_value=1000, value=300, step=1)

# Fungsi Matematika Fuzzifikasi
def mu_lancar(x):
    if x <= 0: return 1.0
    elif 0 < x < 500: return (500 - x) / 500
    else: return 0.0

def mu_padat(x):
    if x <= 0 or x >= 1000: return 0.0
    elif 0 < x < 500: return x / 500
    else: return (1000 - x) / 500

def mu_macet(x):
    if x <= 500: return 0.0
    elif 500 < x < 1000: return (x - 500) / 500
    else: return 1.0

# Hitung nilai saat ini berdasarkan input
val_lancar = mu_lancar(x_input)
val_padat = mu_padat(x_input)
val_macet = mu_macet(x_input)

# Membuat Tab untuk 4 Luaran Sisanya
tab1, tab2, tab3, tab4 = st.tabs([
    "📐 Fungsi Keanggotaan", 
    "🧮 Perhitungan Derajat Keanggotaan", 
    "📈 Grafik Himpunan Fuzzy", 
    "📝 Interpretasi Hasil"
])

# ==========================================
# 2. FUNGSI KEANGGOTAAN
# ==========================================
with tab1:
    st.header("Fungsi Keanggotaan (\u03bc)")
    st.write("Berdasarkan kurva pada studi kasus, berikut adalah representasi matematis dari masing-masing himpunan fuzzy:")
    
    st.markdown("**1. Himpunan Lancar (Kurva Turun)**")
    st.latex(r"""
    \mu_{\text{Lancar}}(x) = 
    \begin{cases} 
    1, & x \le 0 \\
    \frac{500 - x}{500}, & 0 < x < 500 \\
    0, & x \ge 500 
    \end{cases}
    """)
    
    st.markdown("**2. Himpunan Padat (Kurva Segitiga)**")
    st.latex(r"""
    \mu_{\text{Padat}}(x) = 
    \begin{cases} 
    0, & x \le 0 \text{ atau } x \ge 1000 \\
    \frac{x}{500}, & 0 < x < 500 \\
    \frac{1000 - x}{500}, & 500 \le x < 1000 
    \end{cases}
    """)

    st.markdown("**3. Himpunan Macet (Kurva Naik)**")
    st.latex(r"""
    \mu_{\text{Macet}}(x) = 
    \begin{cases} 
    0, & x \le 500 \\
    \frac{x - 500}{500}, & 500 < x < 1000 \\
    1, & x \ge 1000 
    \end{cases}
    """)

# ==========================================
# 3. PERHITUNGAN DERAJAT KEANGGOTAAN
# ==========================================
with tab2:
    st.header("Perhitungan Derajat Keanggotaan")
    st.write(f"Untuk nilai input (Jumlah Kendaraan) = **{x_input}**, berikut adalah hasil fuzzifikasinya:")
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric(label="\u03bc Lancar", value=f"{val_lancar:.2f}")
    col_b.metric(label="\u03bc Padat", value=f"{val_padat:.2f}")
    col_c.metric(label="\u03bc Macet", value=f"{val_macet:.2f}")
    
    st.info("Nilai di atas menunjukkan seberapa kuat input tersebut masuk ke dalam masing-masing kategori himpunan.")

# ==========================================
# 4. GRAFIK HIMPUNAN FUZZY
# ==========================================
with tab3:
    st.header("Grafik Himpunan Fuzzy")
    
    x_vals = np.linspace(0, 1000, 500)
    y_lancar = [mu_lancar(x) for x in x_vals]
    y_padat = [mu_padat(x) for x in x_vals]
    y_macet = [mu_macet(x) for x in x_vals]
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_vals, y_lancar, label="Lancar", color="blue")
    ax.plot(x_vals, y_padat, label="Padat", color="green")
    ax.plot(x_vals, y_macet, label="Macet", color="red")
    
    # Menambahkan garis input
    ax.axvline(x=x_input, color="orange", linestyle="--", linewidth=2, label=f"Input: {x_input}")
    # Menambahkan titik potong derajat keanggotaan
    ax.plot(x_input, val_lancar, 'bo')
    ax.plot(x_input, val_padat, 'go')
    ax.plot(x_input, val_macet, 'ro')
    
    ax.set_title("Grafik Fungsi Keanggotaan Tingkat Kemacetan")
    ax.set_xlabel("Jumlah Kendaraan")
    ax.set_ylabel("Derajat Keanggotaan (\u03bc)")
    ax.legend()
    ax.grid(True, linestyle=":")
    
    st.pyplot(fig)

# ==========================================
# 5. INTERPRETASI HASIL
# ==========================================
with tab4:
    st.header("Interpretasi Hasil (Defuzzifikasi)")
    st.write("Menggunakan Metode **Centroid** untuk menentukan nilai tegas (Crisp Output).")
    
    # Penentuan Nilai Tengah (Centroid) untuk masing-masing rules (skala 0-100)
    c_lancar = 20
    c_padat = 50
    c_macet = 80
    
    total_bobot = val_lancar + val_padat + val_macet
    
    if total_bobot > 0:
        z = ((val_lancar * c_lancar) + (val_padat * c_padat) + (val_macet * c_macet)) / total_bobot
    else:
        z = 0

    st.latex(rf"Z = \frac{{({val_lancar:.2f} \times {c_lancar}) + ({val_padat:.2f} \times {c_padat}) + ({val_macet:.2f} \times {c_macet})}}{{{total_bobot:.2f}}} = {z:.2f}")

    if z <= 40:
        kesimpulan = "Lancar"
    elif 40 < z <= 70:
        kesimpulan = "Padat"
    else:
        kesimpulan = "Macet"

    st.success(f"**Nilai Output Crisp:** {z:.2f}")
    st.subheader(f"🚦 Kesimpulan Tingkat Kemacetan: {kesimpulan}")

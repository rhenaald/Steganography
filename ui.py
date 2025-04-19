# ui.py
import streamlit as st
from scipy.io import wavfile
from utils import embed_message_in_audio, extract_message_from_audio, get_audio_download_bytes
from visualization import plot_audio_waveform, plot_audio_spectrum

def run_app():

    st.sidebar.title("Navigasi")
    menu = st.sidebar.selectbox("Pilih Menu", ["Home", "Steganography", "About", "Developer"])

    if menu == "Home":
        show_home()
    elif menu == "Steganography":
        run_steganography_menu()
    elif menu == "About":
        show_about()
    elif menu == "Developer":
        show_developer()

def show_home():
    st.title("Selamat Datang di EchoHide 👋")
    st.write("""
        **EchoHide** adalah aplikasi steganografi audio berbasis Fourier Transform. 
        Dengan aplikasi ini, Anda dapat menyisipkan pesan rahasia ke dalam file audio `.wav` 
        dan mengekstraknya kembali secara aman.
        
        Silakan pilih menu **Steganography** di sidebar untuk mulai menyembunyikan atau mengambil pesan dari audio.
    """)

def run_steganography_menu():
    st.title("EchoHide - Steganografi Audio")
    st.write("Sembunyikan dan ekstrak pesan dari file audio menggunakan transformasi Fourier.")

    st.sidebar.subheader("Pengaturan Steganografi")
    alpha = st.sidebar.slider("Kekuatan penyisipan (alpha)", 0.001, 0.1, 0.01, 0.001)

    tab1, tab2 = st.tabs(["Sembunyikan Pesan", "Ekstrak Pesan"])
    with tab1:
        run_hide_tab(alpha)
    with tab2:
        run_extract_tab(alpha)

def show_about():
    st.title("Tentang EchoHide")
    st.markdown("""
    **EchoHide** adalah aplikasi steganografi audio yang dikembangkan dengan Python dan Streamlit.
    
    Fitur utama:
    - Menyisipkan pesan teks ke dalam file audio `.wav`.
    - Mengekstrak pesan dari file audio yang telah dimodifikasi.
    - Visualisasi waveform dan spektrum audio.

    Teknologi yang digunakan:
    - **Streamlit** untuk antarmuka web.
    - **SciPy** untuk pemrosesan audio.
    - **Matplotlib** untuk visualisasi.

    """, unsafe_allow_html=True)

def show_developer():
    st.title("Tim Developer EchoHide")
    st.write("Kenali orang-orang keren di balik proyek ini:")

    devs = [
        {
            "name": "Aida Nurfadilah",
            "role": "237006076",
            "desc": "Pengerjaan Laporan & PPT",
            "img": "Image/237006076.jpg"
        },
        {
            "name": "Rosi Saraswati Alrasid",
            "role": "237006087",
            "desc": "Pengerjaan Laporan & PPT",
            "img": "Image/237006087.jpg"
        },
        {
            "name": "Muhammad Rafli Fajar Batubara",
            "role": "237006094",
            "desc": "membuat poster (promosi aplikasi)",
            "img": "Image/237006094.jpg"
        },
        {
            "name": "Ikhwan Kurniawan Julianto",
            "role": "237006102",
            "desc": "pembuatan aplikasi",
            "img": "Image/237006102.jpg"
        },
        {
            "name": "Luthfi Putra Pratama",
            "role": "237006119",
            "desc": "menjelaskan hasil",
            "img": "Image/237006119.jpg"
        }
    ]

    cols = st.columns(5)
    for col, dev in zip(cols, devs):
        with col:
            st.image(dev["img"], width=200)
            st.subheader(dev["name"])
            st.caption(dev["role"])
            st.write(dev["desc"])


def run_hide_tab(alpha):
    st.header("Sembunyikan Pesan dalam Audio")
    audio_file = st.file_uploader("Unggah file audio (.wav)", type=["wav"])

    if audio_file is not None:
        try:
            sample_rate, audio_data = wavfile.read(audio_file)
            st.write(f"Sample Rate: {sample_rate} Hz")
            st.write(f"Channels: {1 if len(audio_data.shape) == 1 else audio_data.shape[1]}")
            st.write(f"Duration: {len(audio_data)/sample_rate:.2f} detik")

            audio_mono = audio_data[:, 0] if len(audio_data.shape) > 1 else audio_data

            st.pyplot(plot_audio_waveform(audio_mono, sample_rate, "Audio Asli"))
            st.pyplot(plot_audio_spectrum(audio_mono, sample_rate, "Spektrum Asli"))
            st.audio(audio_file, format="audio/wav")

            message = st.text_area("Masukkan pesan untuk disembunyikan:", height=100)

            if st.button("🔐 Sembunyikan Pesan") and message:
                max_chars = len(audio_mono) // 800
                if len(message) > max_chars:
                    st.error(f"Pesan terlalu panjang! Maksimum {max_chars} karakter.")
                else:
                    with st.spinner('Menyembunyikan pesan...'):
                        stego_audio = embed_message_in_audio(audio_data, sample_rate, message, alpha)
                        if stego_audio is not None:
                            st.success("Pesan berhasil disembunyikan!")
                            stego_mono = stego_audio[:, 0] if len(stego_audio.shape) > 1 else stego_audio
                            st.pyplot(plot_audio_waveform(stego_mono, sample_rate, "Audio dengan Pesan"))
                            st.pyplot(plot_audio_spectrum(stego_mono, sample_rate, "Spektrum dengan Pesan"))
                            st.audio(get_audio_download_bytes(stego_audio, sample_rate), format="audio/wav")
                            st.download_button("⬇️ Unduh Audio dengan Pesan", 
                            data=get_audio_download_bytes(stego_audio, sample_rate),
                            file_name="stego_audio.wav", mime="audio/wav")

        except Exception as e:
            st.error(f"Error membaca file audio: {e}")

def run_extract_tab(alpha):
    st.header("Ekstrak Pesan dari Audio")
    stego_file = st.file_uploader("Unggah file audio dengan pesan (.wav)", type=["wav"], key="stego_upload")
    original_file = st.file_uploader("Unggah file audio asli (.wav)", type=["wav"], key="original_upload")

    if stego_file and original_file:
        try:
            stego_sample_rate, stego_audio = wavfile.read(stego_file)
            original_sample_rate, original_audio = wavfile.read(original_file)

            if stego_sample_rate != original_sample_rate:
                st.error("Sample rate dari kedua file harus sama!")
            else:
                st.write("Audio dengan Pesan:")
                st.audio(stego_file, format="audio/wav")

                st.write("Audio Asli:")
                st.audio(original_file, format="audio/wav")

                if st.button("🔍 Ekstrak Pesan"):
                    with st.spinner('Mengekstrak pesan...'):
                        message = extract_message_from_audio(stego_audio, original_audio, alpha)
                        if message:
                            st.success("Pesan berhasil diekstrak!")
                            st.text_area("Pesan yang diekstrak:", message, height=150)
                        else:
                            st.error("Tidak ada pesan yang ditemukan atau pesan tidak dapat dibaca.")
        except Exception as e:
            st.error(f"Error membaca file audio: {e}")
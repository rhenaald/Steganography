
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft

def plot_audio_waveform(audio_data, sample_rate, title="Audio Waveform"):
    duration = len(audio_data) / sample_rate
    time = np.linspace(0., duration, len(audio_data))
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(time, audio_data)
    ax.set_title(title)
    ax.set_xlabel("Waktu (detik)")
    ax.set_ylabel("Amplitudo")
    return fig

def plot_audio_spectrum(audio_data, sample_rate, title="Audio Spectrum"):
    n = len(audio_data)
    T = 1 / sample_rate
    yf = fft(audio_data)
    xf = np.linspace(0.0, 1.0/(2.0*T), n//2)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(xf, 2.0/n * np.abs(yf[:n//2]))
    ax.set_title(title)
    ax.set_xlabel("Frekuensi (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_xscale("log")
    return fig

# utils.py
import numpy as np
import io
from scipy.fft import fft, ifft
from scipy.io import wavfile
import streamlit as st

def embed_message_in_audio(audio_data, sample_rate, message, alpha=0.01):
    if len(audio_data.shape) > 1:
        audio_data = audio_data[:, 0]
    
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '00000000'
    
    if len(binary_message) > len(audio_data) // 100:
        st.error(f"Pesan terlalu panjang untuk audio ini. Maksimum karakter: {len(audio_data) // 800}")
        return None
    
    audio_fft = fft(audio_data)
    
    magnitude = np.abs(audio_fft)
    phase = np.angle(audio_fft)
    
    start_idx = 1000
    for i, bit in enumerate(binary_message):
        idx = start_idx + i * 10
        if idx >= len(magnitude) - 10:
            break
            
        if bit == '1':
            magnitude[idx] = magnitude[idx] * (1 + alpha)
        else:
            magnitude[idx] = magnitude[idx] * (1 - alpha)
        
        mirror_idx = len(magnitude) - idx - 1
        if mirror_idx > idx:
            magnitude[mirror_idx] = magnitude[idx]
    
    modified_fft = magnitude * np.exp(1j * phase)
    
    modified_audio = np.real(ifft(modified_fft))
    
    if audio_data.dtype == np.int16:
        modified_audio = np.clip(modified_audio, -32768, 32767)
        return modified_audio.astype(np.int16)
    elif audio_data.dtype == np.float32:
        modified_audio = np.clip(modified_audio, -1.0, 1.0)
        return modified_audio.astype(np.float32)
    else:
        return modified_audio.astype(audio_data.dtype)

def extract_message_from_audio(stego_audio, original_audio, alpha=0.01, max_length=1000):
    if len(stego_audio.shape) > 1:
        stego_audio = stego_audio[:, 0]
    if len(original_audio.shape) > 1:
        original_audio = original_audio[:, 0]
    
    stego_fft = fft(stego_audio)
    original_fft = fft(original_audio)
    
    stego_magnitude = np.abs(stego_fft)
    original_magnitude = np.abs(original_fft)
    
    extracted_bits = ""
    start_idx = 1000
    
    for i in range(max_length):
        idx = start_idx + i * 10
        if idx >= len(stego_magnitude) - 10:
            break
        
        if stego_magnitude[idx] > original_magnitude[idx]:
            extracted_bits += "1"
        else:
            extracted_bits += "0"
        
        if len(extracted_bits) >= 8 and extracted_bits[-8:] == "00000000":
            extracted_bits = extracted_bits[:-8]
            break
    
    message = ""
    for i in range(0, len(extracted_bits), 8):
        if i + 8 <= len(extracted_bits):
            byte = extracted_bits[i:i+8]
            message += chr(int(byte, 2))
    
    return message

def get_audio_download_bytes(audio_data, sample_rate):
    buffer = io.BytesIO()
    wavfile.write(buffer, sample_rate, audio_data)
    buffer.seek(0)
    return buffer

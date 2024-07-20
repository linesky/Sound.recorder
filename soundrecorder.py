import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import threading
#pip install sounddevice scipy

SAMPLING_RATE = 44100  # Taxa de amostragem do áudio
CHANNELS = 1  # Gravação mono

# Variáveis globais para controle da gravação
global recording, frames
recording = False
framess = []

def audio_callback(indata, frames, time, status):
    """Callback para captura de áudio."""
    global recording, framess
    if recording:
        framess.append(indata.copy())

def start_recording():
    global recording, framess
    framess = []
    recording = True
    with sd.InputStream(samplerate=SAMPLING_RATE, channels=CHANNELS, callback=audio_callback):
        print("Gravando... Pressione Enter para parar a gravação.")
        input()  # Aguarda o usuário pressionar Enter para parar a gravação

        recording = False

def save_wavefile(filename, data, samplerate):
    """Salva os dados de áudio em um arquivo WAV."""
    global recording, framess
    wav.write(filename, samplerate, np.concatenate(data))

def main():
    global recording, framess
    # Nome do arquivo para salvar a gravação
    output_filename = input("Digite o nome do arquivo para salvar a gravação (ex: output.wav): ")
    
    # Iniciar a gravação em um thread separado para permitir a interrupção com Enter
    recording_thread = threading.Thread(target=start_recording)
    recording_thread.start()
    recording_thread.join()  # Aguarda a gravação terminar
    
    # Salvar a gravação no arquivo especificado
    save_wavefile(output_filename, framess, SAMPLING_RATE)
    print(f"Gravação salva no arquivo: {output_filename}")
print("\x1bc\x1b[47;34m")
if __name__ == "__main__":
    main()


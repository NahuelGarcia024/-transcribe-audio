
import speech_recognition as sr
import pyaudio
import wave

class Transcribir:
    def __init__(self, formato:pyaudio, canales: int, tass_muestreo: int, tamanio_bufer: int, duracion_grabacion: int, c: str):
        self.formato = formato
        self.canales = canales
        self.tass_muestreo = tass_muestreo
        self.tamanio_bufer = tamanio_bufer
        self.duracion_grabacion = duracion_grabacion
        self.duracion_grabacion = duracion_grabacion

    def grabar_audio(self):
        try:
            audio = pyaudio.PyAudio()
            stream = audio.open(format=self.formato, 
                                channels=self.canales, 
                                rate=self.tass_muestreo, 
                                input=True, 
                                frames_per_buffer=self.tamanio_bufer
            )
            print("Grabando...")
            
            frames = []
            
            for i in range(0, int(self.tass_muestreo / self.tamanio_bufer * self.duracion_grabacion)):
                data = stream.read(self.tamanio_bufer)
                frames.append(data)
                
            print("Grabación finalizada")
            
            ### detener grabación
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            ### guardar archivo
            
            wf = wave.open(self.ruta_archivo, "wb")
            wf.setnchannels(self.canales)
            wf.setsampwidth(audio.get_sample_size(self.formato))
            wf.self.setframerate(self.tass_muestreo)
            wf.writeframes(b"".join(frames))
            wf.close() 
            
            resultado = self.transcribir_audio(self.ruta_archivo)
            
            if resultado["estado"] == "success":
                return {
                    "estado":"success",
                    "mensaje":"Transcripción realizada con éxito",
                    "texto":resultado["texto"]
                }
            return {
                "estado":"error",
                "mensaje":"No se pudo transcribir el audio"
            }
            
            
        except Exception as exception:
            raise NameError(f"Error al grabar el audio, revisa {exception}")
        
    def transcribir_audio(self, ruta_audio):
        try:
            r = sr.Recognizer()
            audio_file = sr.AudioFile(ruta_audio)
            
            with audio_file as source:
                audio = r.record(source)
                
            texto = r.recognize_google(audio, language="es-ES")
            
            if texto:
                return {
                    "estado":"success",
                    "mensaje":"Transcripción realizada con éxito",
                    "texto":texto
                }
            return {
                "estado":"error",
                "mensaje":"No se pudo transcribir el audio"}
            
            
            
        except Exception as exception:
            raise NameError(f"ha ocurrido un Error al transcribir el audio, revisa {exception}")
        
        
        
formato = pyaudio.paInt16
canales = 2
tass_muestreo = 44100

tamaño_bufer = 1024
duración_grabación = 15
ruta_archivo = "audio.wav"

transcribir = Transcribir(formato, canales, tass_muestreo, tamaño_bufer, duración_grabación, ruta_archivo)

print(transcribir.grabar_audio())
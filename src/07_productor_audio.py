from gtts import gTTS
import os

class ProductorAudio:
    def __init__(self):
        self.idioma = 'ca' # Configurem el motor en Català
        
    def generar_mp3(self, text_podcast, nom_arxiu="Podcast_La_Dada_Clara.mp3"):
        print("🎧 Renderitzant l'arxiu d'àudio (MP3)...")
        
        # Netejem una mica el text (traiem asteriscs i emoticones perquè no els llegeixi)
        text_net = text_podcast.replace("*", "").replace("🎙️", "").replace("**", "")
        
        try:
            # Creem l'àudio
            tts = gTTS(text=text_net, lang=self.idioma, slow=False)
            
            # El guardem a l'arrel del projecte
            ruta_arrel = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ruta_final = os.path.join(ruta_arrel, nom_arxiu)
            tts.save(ruta_final)
            
            return ruta_final
        except Exception as e:
            print(f"⚠️ Error generant l'àudio: {e}")
            return None
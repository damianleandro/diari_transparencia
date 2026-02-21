import edge_tts
import asyncio
import os

class ProductorAudio:
    def __init__(self):
        # Utilitzem la veu neuronal de la 'Joana' (Català, molt natural)
        self.veu = "ca-ES-JoanaNeural" 
        
    def generar_mp3(self, text_podcast, nom_arxiu="Podcast_La_Dada_Clara.mp3"):
        print("🎧 Renderitzant l'àudio amb veu neuronal d'alta qualitat (Edge TTS)...")
        
        # Netejem el text perquè la IA no llegeixi coses rares
        text_net = text_podcast.replace("*", "").replace("🎙️", "")
        
        ruta_arrel = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_final = os.path.join(ruta_arrel, nom_arxiu)
        
        # Edge-TTS funciona de manera asíncrona, per això necessitem aquesta petita funció interna
        async def run_tts():
            communicate = edge_tts.Communicate(text_net, self.veu)
            await communicate.save(ruta_final)
            
        try:
            asyncio.run(run_tts())
            return ruta_final
        except Exception as e:
            print(f"⚠️ Error generant l'àudio: {e}")
            return None
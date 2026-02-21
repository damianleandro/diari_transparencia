import os
from google import genai
from dotenv import load_dotenv

# Carreguem la clau de l'arxiu .env
directori_actual = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(os.path.dirname(directori_actual), '.env')
load_dotenv(dotenv_path=env_path)

class RedactorGemini:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("⚠️ No s'ha trobat GEMINI_API_KEY a l'arxiu .env")
            
        self.client = genai.Client(api_key=api_key)

    def redactar_noticia(self, general, critic, historic, bulo):
        """Genera l'article periodístic rigorós i formal."""
        print("🤖 Connectant amb Gemini per redactar la notícia escrita...")
        
        text_historic = f"Fa un any ({historic['any_passat']}), les reserves estaven al {historic['mitjana_1_any']:.1f}%." if historic['mitjana_1_any'] else "No hi ha dades fiables de fa un any."

        prompt = f"""
        Ets el 'Cronista de Dades', un periodista d'intel·ligència artificial expert en periodisme de dades.
        
        DADES OFICIALS REALS DE LES CONQUES INTERNES (Data: {general['data_lectura']}):
        - Estat General: {general['percentatge_mitja']:.1f}% de capacitat.
        - Històric: {text_historic}
        - Excepció Local Crítica: {critic['pantano']} està només al {critic['percentatge']:.2f}%.
        
        NOTÍCIA/BULO: "{bulo['afirmacio']}" (Font: {bulo['font']})
        
        TASCA:
        Escriu una notícia (màxim 3 paràgrafs) analitzant el titular. Si és alarmisme global, desmenteix-ho amb el {general['percentatge_mitja']:.1f}%. Si parla d'un problema local (com Siurana al {critic['percentatge']:.2f}%), matisa-ho donant la raó en l'àmbit local però donant context global.
        
        Idioma: Català. To: Analític, rigorós.
        """
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash', contents=prompt,
                config=genai.types.GenerateContentConfig(temperature=0.3)
            )
            return response.text
        except Exception as e:
            return f"❌ Error de connexió amb Gemini (Notícia): {e}"

    def generar_guio_podcast(self, general, critic, historic, bulo):
        """Genera un guió de ràdio a dues veus preparat per a Text-To-Speech."""
        print("🎙️ Connectant amb Gemini per crear el guió del podcast...")
        
        prompt_podcast = f"""
        Ets el guionista estrella d'un podcast diari anomenat 'La Dada Clara'.
        Escriu un guió de ràdio breu i molt dinàmic (màxim 1 minut) entre dos presentadors:
        - MARC: Fa les preguntes, porta el ritme i presenta la notícia d'avui.
        - ANNA: L'experta en dades que desmunta els mites amb xifres reals.
        
        TEMÀTICA D'AVUI:
        Han de debatre sobre aquest titular que corre per internet: "{bulo['afirmacio']}" (Font: {bulo['font']}).
        
        DADES QUE L'ANNA HA DE DONAR DURANT EL DIÀLEG (Data: {general['data_lectura']}):
        - Les Conques Internes estan avui al {general['percentatge_mitja']:.1f}%.
        - Fa un any estàvem al {historic['mitjana_1_any']:.1f}%.
        - El matís: A l'embassament de {critic['pantano']} la situació segueix sent crítica ({critic['percentatge']:.2f}%), per tant, no tot és perfecte arreu.
        
        ESTRUCTURA:
        MARC: [Text]
        ANNA: [Text]
        ...
        
        Idioma: Català. To: Col·loquial, fresc, de ràdio moderna i molt natural.
        """
        try:
            # Utilitzem una temperatura més alta (0.5) perquè el diàleg sigui més creatiu i natural
            response = self.client.models.generate_content(
                model='gemini-2.5-flash', contents=prompt_podcast,
                config=genai.types.GenerateContentConfig(temperature=0.5)
            )
            return response.text
        except Exception as e:
            return f"❌ Error de connexió amb Gemini (Podcast): {e}"
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
        print("🤖 Connectant amb Gemini per redactar la notícia de Fact-Checking Intel·ligent...")
        
        text_historic = f"Fa un any ({historic['any_passat']}), les reserves estaven al {historic['mitjana_1_any']:.1f}%." if historic['mitjana_1_any'] else "No hi ha dades fiables de fa un any."

        prompt = f"""
        Ets el 'Cronista de Dades', un periodista d'intel·ligència artificial expert en periodisme de dades.
        
        DADES OFICIALS REALS DE LES CONQUES INTERNES (Data: {general['data_lectura']}):
        - Estat General (Global Catalunya): {general['percentatge_mitja']:.1f}% de capacitat.
        - Històric Global: {text_historic}
        - Excepció Local Crítica: L'embassament de {critic['pantano']} es troba només al {critic['percentatge']:.2f}%.
        
        NOTÍCIA O AFIRMACIÓ A ANALITZAR:
        - Font: {bulo['font']}
        - Titular/Afirmació: "{bulo['afirmacio']}"
        
        LA TEVA TASCA (Màxim 3-4 paràgrafs):
        1. Analitza intel·ligentment l'escala de la notícia. Parla d'una sequera generalitzada a tota Catalunya o d'un conflicte local/comarcal (com el Priorat, Siurana, etc.)?
        2. Si la notícia fa una afirmació alarmista GLOBAL sobre tot el territori, utilitza el {general['percentatge_mitja']:.1f}% i l'històric per DESMENTIR-HO amb contundència.
        3. Si la notícia parla d'un conflicte LOCAL (ex: "Guerra de l'aigua al Priorat", problemes a un pantà concret), MATISA-HO I DONA CONTEXT. Explica que, tot i que Catalunya gaudeix d'una mitjana excel·lent ({general['percentatge_mitja']:.1f}%), la notícia té sentit perquè hi ha excepcions territorials greus com l'embassament de {critic['pantano']} al {critic['percentatge']:.2f}%.
        4. Conclou amb una reflexió sobre la importància de no confondre la mitjana global d'un país amb les realitats i crisis locals.
        
        Idioma: Català. To: Analític, rigorós, objectiu i constructiu. Mai ataquessis un mitjà si està informant d'una realitat local verificable amb les nostres dades.
        """
        
        try:
            # Pugem una mica la temperatura (0.3) perquè el model pugui "raonar" millor els matisos
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=genai.types.GenerateContentConfig(temperature=0.3) 
            )
            return response.text
        except Exception as e:
            return f"❌ Error de connexió amb Gemini: {e}"
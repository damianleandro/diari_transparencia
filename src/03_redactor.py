import os
from google import genai
from dotenv import load_dotenv

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
        print("🤖 Redactant l'article principal...")
        text_historic = f"Fa un any ({historic['any_passat']}), les reserves estaven al {historic['mitjana_1_any']:.1f}%." if historic['mitjana_1_any'] else "No hi ha dades fiables de fa un any."
        
        prompt = f"""
        Ets el 'Cronista de Dades'. DADES (Data: {general['data_lectura']}): General: {general['percentatge_mitja']:.1f}%. Històric: {text_historic}. Pantà crític: {critic['pantano']} ({critic['percentatge']:.2f}%).
        NOTÍCIA A ANALITZAR: "{bulo['afirmacio']}" (Font: {bulo['font']})
        TASCA: Escriu una notícia (màxim 3 paràgrafs) analitzant el titular. Dona context global però matisa amb les excepcions locals si cal.
        Idioma: Català. To: Analític i rigorós.
        """
        
        response = self.client.models.generate_content(model='gemini-2.5-flash', contents=prompt, config=genai.types.GenerateContentConfig(temperature=0.3))
        return response.text

    def redactar_comparativa(self, general, historic):
        print("📊 Redactant la secció de comparativa històrica...")
        text_historic = f"Fa un any ({historic['any_passat']}), les reserves estaven al {historic['mitjana_1_any']:.1f}%." if historic['mitjana_1_any'] else ""
        
        prompt = f"""
        Ets un analista de dades. Escriu una secció curta (1 o 2 paràgrafs) comparant exclusivament l'estat actual de les Conques Internes ({general['percentatge_mitja']:.1f}%) amb la situació de fa un any ({text_historic}).
        Aporta context sobre el ritme de recuperació.
        Idioma: Català. To: Tècnic, precís i directe. No posis títol al text, comença directament a redactar.
        """
        
        response = self.client.models.generate_content(model='gemini-2.5-flash', contents=prompt, config=genai.types.GenerateContentConfig(temperature=0.2))
        return response.text

    def redactar_per_a_tts(self, general, critic, bulo):
        print("🎙️ Adaptant el text per a Edge-TTS (Sense símbols, només veu)...")
        
        prompt = f"""
        Escriu una crònica de ràdio d'un sol locutor (1 minut màxim) analitzant aquest titular: "{bulo['afirmacio']}".
        Utilitza la dada de la mitjana actual ({general['percentatge_mitja']:.1f}%) i el pantà crític de {critic['pantano']} ({critic['percentatge']:.2f}%).
        MOLT IMPORTANT PER A LA SÍNTESI DE VEU:
        - Escriu frases curtes i amb puntuació molt clara (comes i punts) perquè la IA de veu respiri de forma natural.
        - PROHIBIT utilitzar qualsevol símbol com asteriscs (*), guions o emojis. 
        - Els números escriu-los de manera natural per ser llegits.
        - No incloguis títols ni acotacions, només el text net per ser llegit.
        Idioma: Català. To: Periodístic i informatiu.
        """
        
        response = self.client.models.generate_content(model='gemini-2.5-flash', contents=prompt, config=genai.types.GenerateContentConfig(temperature=0.3))
        return response.text.replace('*', '') # Neteja extra de seguretat
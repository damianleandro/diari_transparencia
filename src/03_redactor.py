import os
import sys
from google import genai
from dotenv import load_dotenv

# Truco de arquitectura: Afegim la carpeta actual al path de Python 
# perquè pugui trobar els altres fitxers sense importar des d'on executem.
directori_actual = os.path.dirname(os.path.abspath(__file__))
sys.path.append(directori_actual)

# Carreguem la clau de l'arxiu .env
load_dotenv()

class RedactorGemini:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("⚠️ No s'ha trobat GEMINI_API_KEY a l'arxiu .env")
            
        # Iniciem el NOU client de Gemini
        self.client = genai.Client(api_key=api_key)

    # Actualitza la definició per rebre el paràmetre 'historic'
    # Afegim el paràmetre 'bulo'
    def redactar_noticia(self, general, critic, historic, bulo):
        print("🤖 Connectant amb Gemini per redactar la notícia ANTI-BULOS...")
        
        text_historic = f"Fa un any ({historic['any_passat']}), les reserves estaven al {historic['mitjana_1_any']:.1f}%." if historic['mitjana_1_any'] else "No hi ha dades fiables de fa un any."

        prompt = f"""
        Ets el 'Cronista de Dades', un periodista d'intel·ligència artificial expert en fact-checking.
        
        DADES OFICIALS REALS (Data: {general['data_lectura']}):
        - Conques Internes: {general['percentatge_mitja']:.1f}% de capacitat (Pràcticament plenes).
        - Històric: {text_historic}
        - Excepció: {critic['pantano']} està al {critic['percentatge']:.2f}%.
        
        OBJECTIU DE DESINFORMACIÓ A DESMENTIR:
        - Font que difon el bulo: {bulo['font']}
        - Afirmació falsa literal: "{bulo['afirmacio']}"
        
        LA TEVA TASCA:
        Escriu una notícia (màxim 3-4 paràgrafs) on:
        1. Comencis citant directament la font del bulo i la seva afirmació falsa.
        2. Utilitzis immediatament la dada del {general['percentatge_mitja']:.1f}% i l'evolució històrica per DESMENTIR rotundament aquesta mentida (és matemàticament impossible tenir gairebé un 90% d'aigua si destrueixes preses).
        3. Mantinguis el rigor periodístic esmentant que l'únic punt realment crític és {critic['pantano']}.
        
        Idioma: Català. To: Contundent contra la mentida, però basat estrictament en les dades obertes.
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=genai.types.GenerateContentConfig(temperature=0.2)
            )
            return response.text
        except Exception as e:
            return f"❌ Error de connexió: {e}"
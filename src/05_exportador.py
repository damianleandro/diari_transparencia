import docx
from docx.shared import Inches
import os

class ExportadorWord:
    def __init__(self):
        self.doc = docx.Document()
        
    def generar_document(self, text_noticia, text_comparativa, text_tts, ruta_imatge, nom_arxiu="Reportatge_Estructurat.docx"):
        print("📝 Maquetant el document Word estructurat (Inputs de Dades)...")
        
        # --- SECCIÓ 1: ARTICLE PRINCIPAL ---
        self.doc.add_heading("Agència de Notícies IA - Article Principal", 0)
        if os.path.exists(ruta_imatge):
            self.doc.add_picture(ruta_imatge, width=Inches(6.0))
            self.doc.paragraphs[-1].alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
        
        for paragraf in text_noticia.split('\n'):
            if paragraf.strip(): 
                self.doc.add_paragraph(paragraf.replace('**', '').strip())
                    
        # --- SECCIÓ 2: COMPARATIVA DE DATES ---
        self.doc.add_paragraph() # Espai
        self.doc.add_heading("📊 Anàlisi Històric de Dates", level=1)
        for paragraf in text_comparativa.split('\n'):
            if paragraf.strip():
                self.doc.add_paragraph(paragraf.replace('**', '').strip())

        # --- SECCIÓ 3: INPUT PER A EDGE-TTS ---
        self.doc.add_page_break()
        self.doc.add_heading("🎙️ Input d'Àudio (Optimitzat per a Edge-TTS)", level=1)
        self.doc.add_paragraph("Aquest bloc de text ha estat optimitzat per a síntesi de veu neuronal: sense símbols i amb estructura de respiració natural.\n").italic = True
        
        for linia in text_tts.split('\n'):
            if linia.strip():
                self.doc.add_paragraph(linia.replace('**', '').strip())

        peu = self.doc.add_paragraph("\nDocument estructurat autogenerat a partir de Dades Obertes.")
        peu.style = 'Intense Quote'
        
        ruta_arrel = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_final = os.path.join(ruta_arrel, nom_arxiu)
        self.doc.save(ruta_final)
        
        return ruta_final
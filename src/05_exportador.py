import docx
from docx.shared import Inches
import os

class ExportadorWord:
    def __init__(self):
        self.doc = docx.Document()
        
    def generar_document(self, text_noticia, ruta_imatge, nom_arxiu="Reportatge_Sequera.docx"):
        print("📝 Maquetant el document Word per a la redacció...")
        
        # Afegim un títol principal (Heading 1)
        self.doc.add_heading("Agència de Notícies IA - El Cronista de Dades", 0)
        
        # Afegim el gràfic centrat
        if os.path.exists(ruta_imatge):
            self.doc.add_picture(ruta_imatge, width=Inches(6.0))
            paragraf_imatge = self.doc.paragraphs[-1]
            paragraf_imatge.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
        
        self.doc.add_paragraph() # Espai en blanc
        
        # Inserim el text de la notícia
        for paragraf in text_noticia.split('\n'):
            if paragraf.strip(): # Evitem línies completament buides
                # Si el paràgraf sembla un títol (comença per ** i acaba per **), el fem Heading
                if paragraf.startswith('**') and paragraf.endswith('**'):
                    self.doc.add_heading(paragraf.replace('**', ''), level=1)
                else:
                    self.doc.add_paragraph(paragraf.strip())
                    
        # Afegim un peu de pàgina de transparència
        peu = self.doc.add_paragraph("\nDocument generat automàticament a partir de Dades Obertes de la Generalitat de Catalunya.")
        peu.style = 'Intense Quote'
        
        # Guardem l'arxiu a l'arrel
        ruta_arrel = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_final = os.path.join(ruta_arrel, nom_arxiu)
        self.doc.save(ruta_final)
        
        return ruta_final
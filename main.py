import os
import sys
import importlib.util
import json

# Afegim la carpeta src al path perquè Python trobi els arxius
directori_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.append(directori_src)

def importar_modul(nom_arxiu, nom_modul):
    ruta = os.path.join(directori_src, nom_arxiu)
    spec = importlib.util.spec_from_file_location(nom_modul, ruta)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul

def main():
    print("🚀 INICIANT EL CRONISTA DE DADES (V4.0 - Anti-Bulos Quirúrgic) 🚀\n")

    # --- IMPORTACIONS DELS MÒDULS ---
    dades_extractor = importar_modul("dades_extractor.py", "extractor")
    analitzador = importar_modul("02_analista.py", "analista")
    redactor_ia = importar_modul("03_redactor.py", "redactor")
    graficador = importar_modul("04_graficador.py", "graficador")
    exportador_doc = importar_modul("05_exportador.py", "exportador")

    # 1. Extracció (Ara descarreguem 25.000 registres per viatjar al passat)
    extractor = dades_extractor.ExtractorAigua()
    df = extractor.obtenir_dades_embassaments(limit=25000)
    
    if df is None or df.empty:
        print("❌ Error: No s'han pogut obtenir dades.")
        return

    # 2. Anàlisi
    analista = analitzador.AnalistaAigua(df)
    general = analista.obtenir_estat_general()
    critic = analista.insight_pantano_critic()
    
    print("🕰️ Calculant l'evolució històrica...")
    historic = analista.obtenir_evolucio_historica()

    # 🔥 NOVETAT: Carreguem el Bulo a desmentir 🔥
    ruta_bulos = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bulos.json')
    try:
        with open(ruta_bulos, 'r', encoding='utf-8') as f:
            base_datos_bulos = json.load(f)
            bulo_objectiu = base_datos_bulos['sequera']
    except Exception as e:
        print(f"⚠️ No s'ha pogut carregar bulos.json: {e}")
        # Si falla per algun motiu, creem un bulo de reserva perquè el programa no caigui
        bulo_objectiu = {
            "font": "Xarxes Socials", 
            "afirmacio": "El govern està enderrocant preses i buidant pantans per crear una sequera artificial."
        }

    # 3. Gràfic
    artista = graficador.Graficador()
    ruta_grafic = artista.generar_linia_temps(df, general)

    # 4. Redacció (Li passem l'històric i el bulo_objectiu a la IA)
    redactor = redactor_ia.RedactorGemini()
    noticia = redactor.redactar_noticia(general, critic, historic, bulo_objectiu)

    # 5. EMPAQUETAT FINAL A WORD (.docx)
    word = exportador_doc.ExportadorWord()
    ruta_word = word.generar_document(noticia, ruta_grafic)

    # RESULTAT FINAL
    print("\n" + "="*70)
    print("📰 PUBLICACIÓ UNIFICADA I LLESTA PER A LA PREMSA")
    print("="*70)
    print(f"✅ S'ha generat l'article llest per a imprimir a: {ruta_word}")
    print("="*70)
    print("🎉 Jornada tancada amb èxit! Bona feina, equip!")

if __name__ == "__main__":
    main()
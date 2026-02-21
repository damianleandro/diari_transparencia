import os
import sys
import importlib.util

directori_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.append(directori_src)

def importar_modul(nom_arxiu, nom_modul):
    ruta = os.path.join(directori_src, nom_arxiu)
    spec = importlib.util.spec_from_file_location(nom_modul, ruta)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul

def main():
    print("🚀 INICIANT EL CRONISTA DE DADES (V7.0 - Pipeline de Dades Estructurades) 🚀\n")

    dades_extractor = importar_modul("dades_extractor.py", "extractor")
    analitzador = importar_modul("02_analista.py", "analista")
    redactor_ia = importar_modul("03_redactor.py", "redactor")
    graficador = importar_modul("04_graficador.py", "graficador")
    exportador_doc = importar_modul("05_exportador.py", "exportador")
    sabueso_web = importar_modul("06_sabueso.py", "sabueso")
    productor_audio = importar_modul("07_productor_audio.py", "productor")

    # 1 i 2. Extracció i Anàlisi
    extractor = dades_extractor.ExtractorAigua()
    df = extractor.obtenir_dades_embassaments(limit=25000)
    if df is None or df.empty: return
    
    analista = analitzador.AnalistaAigua(df)
    general, critic, historic = analista.obtenir_estat_general(), analista.insight_pantano_critic(), analista.obtenir_evolucio_historica()

    # 3 i 4. Cerca i Gràfic
    gos_rastrejador = sabueso_web.SabuesoNoticies()
    bulo_objectiu = gos_rastrejador.buscar_noticia_recent("sequera conques internes catalunya OR embassaments ACA")
    artista = graficador.Graficador()
    ruta_grafic = artista.generar_linia_temps(df, general)

    # 5. Generació Estructurada (3 parts)
    redactor = redactor_ia.RedactorGemini()
    noticia = redactor.redactar_noticia(general, critic, historic, bulo_objectiu)
    comparativa = redactor.redactar_comparativa(general, historic)
    text_tts = redactor.redactar_per_a_tts(general, critic, bulo_objectiu)

    # 6. Maquetació a Word
    word = exportador_doc.ExportadorWord()
    ruta_word = word.generar_document(noticia, comparativa, text_tts, ruta_grafic)

    # 7. Producció d'Àudio exclusivament amb el text optimitzat
    productor = productor_audio.ProductorAudio()
    ruta_mp3 = productor.generar_mp3(text_tts, nom_arxiu="Butlleti_Informatiu.mp3")

    print("\n" + "="*70)
    print("✅ PIPELINE COMPLETAT: PRODUCTES GENERATS")
    print("="*70)
    print(f"📄 Document Word Estructurat: {ruta_word}")
    print(f"🎧 Butlletí d'Àudio Net: {ruta_mp3}")
    print("="*70)

if __name__ == "__main__":
    main()
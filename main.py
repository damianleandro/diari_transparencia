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
    print("🚀 INICIANT EL CRONISTA DE DADES (V6.0 - Factoria 360º Multimèdia) 🚀\n")

    # --- IMPORTACIONS ---
    dades_extractor = importar_modul("dades_extractor.py", "extractor")
    analitzador = importar_modul("02_analista.py", "analista")
    redactor_ia = importar_modul("03_redactor.py", "redactor")
    graficador = importar_modul("04_graficador.py", "graficador")
    exportador_doc = importar_modul("05_exportador.py", "exportador")
    sabueso_web = importar_modul("06_sabueso.py", "sabueso")
    productor_audio = importar_modul("07_productor_audio.py", "productor")

    # 1. Extracció (25.000 registres)
    extractor = dades_extractor.ExtractorAigua()
    df = extractor.obtenir_dades_embassaments(limit=25000)
    
    if df is None or df.empty:
        print("❌ Error: No s'han pogut obtenir dades oficials.")
        return

    # 2. Anàlisi
    analista = analitzador.AnalistaAigua(df)
    general = analista.obtenir_estat_general()
    critic = analista.insight_pantano_critic()
    print("🕰️ Calculant l'evolució històrica...")
    historic = analista.obtenir_evolucio_historica()

    # 3. Sabueso (Filtre geogràfic exacte per evitar Fal·làcia Ecològica)
    gos_rastrejador = sabueso_web.SabuesoNoticies()
    bulo_objectiu = gos_rastrejador.buscar_noticia_recent("sequera conques internes catalunya OR embassaments ACA")

    # 4. Gràfic
    artista = graficador.Graficador()
    ruta_grafic = artista.generar_linia_temps(df, general)

    # 5. Redacció (Doble Motor: Text i Audio)
    redactor = redactor_ia.RedactorGemini()
    noticia = redactor.redactar_noticia(general, critic, historic, bulo_objectiu)
    guio_podcast = redactor.generar_guio_podcast(general, critic, historic, bulo_objectiu)

    # 7. Producció d'Àudio (MP3)
    productor = productor_audio.ProductorAudio()
    ruta_mp3 = productor.generar_mp3(guio_podcast)

    # Vistes Prèvies a la Terminal
    print("\n" + "-"*70)
    print("📰 VISTA PRÈVIA: LA NOTÍCIA")
    print("-" * 70)
    print(noticia)
    print("\n" + "-"*70)
    print("🎙️ VISTA PRÈVIA: EL GUIÓ DEL PODCAST")
    print("-" * 70)
    print(guio_podcast)
    print("-" * 70 + "\n")

    # 6. Maquetació a Word (.docx) amb les dues pàgines
    word = exportador_doc.ExportadorWord()
    ruta_word = word.generar_document(noticia, guio_podcast, ruta_grafic)

    # RESULTAT FINAL
    print("\n" + "="*70)
    print("📰 PUBLICACIÓ MULTIMÈDIA LLESTA PER A PRODUCCIÓ")
    print("="*70)
    print(f"✅ S'ha generat l'article a: {ruta_word}\n🎧 S'ha generat el podcast a: {ruta_mp3}")
    print("="*70)

if __name__ == "__main__":
    main()
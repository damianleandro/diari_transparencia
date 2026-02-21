import os
import sys
import importlib.util

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
    print("🚀 INICIANT EL CRONISTA DE DADES (V5.0 - Sabueso d'Internet) 🚀\n")

    # --- IMPORTACIONS DELS MÒDULS ---
    dades_extractor = importar_modul("dades_extractor.py", "extractor")
    analitzador = importar_modul("02_analista.py", "analista")
    redactor_ia = importar_modul("03_redactor.py", "redactor")
    graficador = importar_modul("04_graficador.py", "graficador")
    exportador_doc = importar_modul("05_exportador.py", "exportador")
    
    # 🔥 EL NOU MÒDUL RASTREJADOR 🔥
    sabueso_web = importar_modul("06_sabueso.py", "sabueso")

    # 1. Extracció de Dades Obertes (25.000 registres)
    extractor = dades_extractor.ExtractorAigua()
    df = extractor.obtenir_dades_embassaments(limit=25000)
    
    if df is None or df.empty:
        print("❌ Error: No s'han pogut obtenir dades oficials.")
        return

    # 2. Anàlisi Matemàtica i Històrica
    analista = analitzador.AnalistaAigua(df)
    general = analista.obtenir_estat_general()
    critic = analista.insight_pantano_critic()
    
    print("🕰️ Calculant l'evolució històrica...")
    historic = analista.obtenir_evolucio_historica()

# 3. Cerca Dinàmica (Filtrem estrictamente per Conques Internes o ACA)
    gos_rastrejador = sabueso_web.SabuesoNoticies()
    bulo_objectiu = gos_rastrejador.buscar_noticia_recent("sequera conques internes catalunya OR embassaments ACA")
    # Pots modificar els termes de cerca per adaptar-los a l'actualitat del dia
    bulo_objectiu = gos_rastrejador.buscar_noticia_recent("bulo sequera pantans catalunya")

    # 4. Generació del Gràfic
    artista = graficador.Graficador()
    ruta_grafic = artista.generar_linia_temps(df, general)

    # 5. Redacció amb IA (Creuant dades obertes amb notícies d'internet)
    redactor = redactor_ia.RedactorGemini()
    noticia = redactor.redactar_noticia(general, critic, historic, bulo_objectiu)

    # 🔥 EL QUE TROBAVES A FALTAR: Imprimir la vista prèvia per consola 🔥
    print("\n" + "-"*70)
    print("📰 VISTA PRÈVIA DEL TEXT GENERAT")
    print("-"*70)
    print(noticia)
    print("-"*70 + "\n")

    # 6. Maquetació a Word (.docx)
    word = exportador_doc.ExportadorWord()
    ruta_word = word.generar_document(noticia, ruta_grafic)

    # 6. Maquetació a Word (.docx)
    word = exportador_doc.ExportadorWord()
    ruta_word = word.generar_document(noticia, ruta_grafic)

    # RESULTAT FINAL
    print("\n" + "="*70)
    print("📰 PUBLICACIÓ UNIFICADA I LLESTA PER A LA PREMSA")
    print("="*70)
    print(f"✅ S'ha generat l'article llest per a imprimir a: {ruta_word}")
    print("="*70)
    print("🎉 MVP V5.0 completat! L'agència de notícies és ara 100% autònoma.")

if __name__ == "__main__":
    main()
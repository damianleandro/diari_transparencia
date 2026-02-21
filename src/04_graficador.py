import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import os

class Graficador:
    def __init__(self):
        # Utilitzem un estil més net i professional
        sns.set_theme(style="ticks")
        
    def generar_linia_temps(self, df, general, nom_arxiu="grafic_sequera.png"):
        print("🎨 Generant la línia de temps històrica professional...")
        
        # 1. Preparar dades (Agrupem per dia)
        evolucio = df.groupby('dia')['percentatge_volum_embassat'].mean().reset_index()
        evolucio = evolucio.sort_values('dia')
        
        # 2. Crear la figura i els eixos
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # --- NOVETAT 1: ZONES DE SEMÀFOR (CONTEXT) ---
        # Pintem franges horitzontals per indicar els nivells de gravetat (approx ACA)
        # Vermell (Emergència < 16%)
        ax.axhspan(0, 16, color='#e74c3c', alpha=0.15, label='Emergència (<16%)')
        # Taronja (Excepcionalitat 16-25%)
        ax.axhspan(16, 25, color='#e67e22', alpha=0.15, label='Excepcionalitat')
        # Groc (Alerta 25-40%)
        ax.axhspan(25, 40, color='#f1c40f', alpha=0.15, label='Alerta')
        # (La resta fins al 100% és "Normalitat" en blanc)

        # 3. Dibuixar la línia principal (més gruixuda)
        sns.lineplot(data=evolucio, x='dia', y='percentatge_volum_embassat', 
                     color='#2980b9', linewidth=3, ax=ax)
        
        # Omplim sota la línia
        ax.fill_between(evolucio['dia'], evolucio['percentatge_volum_embassat'], 
                         color='#3498db', alpha=0.2)
        
        # --- NOVETAT 2: DESTACAR EL PUNT ACTUAL ---
        # Agafem l'últim registre
        ultim_dia = evolucio.iloc[-1]
        # Dibuixem un punt gros al final
        ax.scatter(ultim_dia['dia'], ultim_dia['percentatge_volum_embassat'], 
                   color='#2c3e50', s=150, zorder=5, edgecolor='white', linewidth=2)
        
        # Afegim una etiqueta de text al costat del punt
        ax.annotate(f"AVUI: {ultim_dia['percentatge_volum_embassat']:.1f}%",
                    xy=(ultim_dia['dia'], ultim_dia['percentatge_volum_embassat']),
                    xytext=(15, 0), textcoords='offset points',
                    fontweight='bold', fontsize=14, color='#2c3e50', va='center')

        # --- NOVETAT 3: NETEJA I FORMAT ---
        # Títols i etiquetes
        ax.set_title(f"Evolució de les Reserves d'Aigua a Catalunya\n(Fins al {general['data_lectura']})", 
                     fontsize=18, fontweight='bold', pad=20)
        ax.set_ylabel("Capacitat Mitjana (%)", fontsize=12, fontweight='bold')
        ax.set_xlabel("") # Treiem l'etiqueta "dia" que és redundant
        
        # Límits i eixos
        ax.set_ylim(0, 100)
        ax.set_xlim(evolucio['dia'].min(), evolucio['dia'].max())
        
        # Formatar l'eix X per mostrar només els anys de forma neta
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        plt.xticks(fontsize=12, rotation=0)
        plt.yticks(fontsize=12)

        # Afegir una llegenda discreta per les zones
        ax.legend(loc='upper left', frameon=True)
        
        # Treure els bordes de dalt i dreta (estil "Tufte")
        sns.despine(trim=True)
        ax.grid(axis='y', linestyle='--', alpha=0.7) # Només línies horitzontals

        # 6. Guardar
        ruta_arrel = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_final = os.path.join(ruta_arrel, nom_arxiu)
        
        plt.tight_layout()
        plt.savefig(ruta_final, dpi=300, bbox_inches='tight')
        plt.close()
        
        return nom_arxiu
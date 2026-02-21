import requests
import pandas as pd

class ExtractorAigua:
    def __init__(self, dataset_id="gn9e-3qhr"):
        self.api_url = f"https://analisi.transparenciacatalunya.cat/resource/{dataset_id}.json"
    
    def obtenir_dades_embassaments(self, limit=25000):
        print(f"📥 Connectant al sensor de l'Agència Catalana de l'Aigua...")
        
        params = {
            "$limit": limit,
            # Ordenamos por dia descendente para tener la foto de HOY
            "$order": "dia DESC"
        }
        
        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status() 
            
            df = pd.DataFrame(response.json())
            
            # Limpieza y conversión a números
            df['percentatge_volum_embassat'] = pd.to_numeric(df['percentatge_volum_embassat'], errors='coerce')
            df['volum_embassat'] = pd.to_numeric(df['volum_embassat'], errors='coerce')
            df['dia'] = pd.to_datetime(df['dia'])
            
            # Eliminamos filas sin datos numéricos
            df_net = df.dropna(subset=['percentatge_volum_embassat']).copy()
            
            print(f"✅ Extracció completada: {len(df_net)} lectures de pantans preparades.")
            return df_net
            
        except Exception as e:
            print(f"❌ Error HTTP: {e}")
            return None
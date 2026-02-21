import pandas as pd
from dades_extractor import ExtractorAigua

class AnalistaAigua:
    def __init__(self, df):
        self.df = df

    def obtenir_estat_general(self):
        """Calcula la mitjana de tots els embassaments per a la data més recent."""
        # Ens quedem només amb els registres del dia més recent
        dia_recent = self.df['dia'].max()
        dades_avui = self.df[self.df['dia'] == dia_recent]
        
        mitjana_total = dades_avui['percentatge_volum_embassat'].mean()
        
        return {
            "tipus_noticia": "estat_general",
            "titular_base": f"L'estat de les Conques Internes se situa al {mitjana_total:.1f}%",
            "percentatge_mitja": mitjana_total,
            "data_lectura": dia_recent.strftime("%d/%m/%Y")
        }

    def insight_pantano_critic(self):
        """Troba l'embassament amb el percentatge d'aigua més baix."""
        
        # 🛡️ Cerca dinàmica de la columna del nom (estaci, pant, etc.)
        col_nom = None
        for candidat in ['estaci', 'estacio', 'pant', 'embassament', 'nom_estacio']:
            if candidat in self.df.columns:
                col_nom = candidat
                break
                
        if not col_nom:
            print(f"⚠️ Columnes disponibles: {list(self.df.columns)}")
            return {"error": "No s'ha trobat la columna amb el nom del pantà."}

        # Ens quedem amb l'últim dia de dades per a cada pantà
        ultimes_lectures = self.df.loc[self.df.groupby(col_nom)['dia'].idxmax()]
        
        # Busquem el pitjor
        idx_min = ultimes_lectures['percentatge_volum_embassat'].idxmin()
        pantano_critic = ultimes_lectures.loc[idx_min]
        
        return {
            "tipus_noticia": "alerta_sequera",
            "titular_base": f"L'embassament de {pantano_critic[col_nom]} registra el nivell més baix",
            "pantano": pantano_critic[col_nom],
            "percentatge": pantano_critic['percentatge_volum_embassat'],
            "volum_hm3": pantano_critic['volum_embassat'],
            "data_lectura": pantano_critic['dia'].strftime("%d/%m/%Y")
        }

    def obtenir_evolucio_historica(self):
        """Calcula la mitjana actual i la compara amb fa 1 i 5 anys."""
        dia_actual = self.df['dia'].max()
        
        # Calculem les dates exactes al passat
        dia_1_any = dia_actual - pd.DateOffset(years=1)
        dia_5_anys = dia_actual - pd.DateOffset(years=5)

        def mitjana_propera(data_objectiu):
            # Busquem dades en un marge de +- 3 dies per si aquell dia exacte no hi ha registre
            marge = pd.Timedelta(days=3)
            dades_properes = self.df[(self.df['dia'] >= data_objectiu - marge) & 
                                     (self.df['dia'] <= data_objectiu + marge)]
            if dades_properes.empty:
                return None
            return dades_properes['percentatge_volum_embassat'].mean()

        mitjana_actual = self.df[self.df['dia'] == dia_actual]['percentatge_volum_embassat'].mean()
        mitjana_1_any = mitjana_propera(dia_1_any)
        mitjana_5_anys = mitjana_propera(dia_5_anys)

        return {
            "mitjana_actual": mitjana_actual,
            "mitjana_1_any": mitjana_1_any,
            "mitjana_5_anys": mitjana_5_anys,
            "any_actual": dia_actual.year,
            "any_passat": dia_1_any.year,
            "any_historic": dia_5_anys.year
        }

# --- Test de l'Analista ---
if __name__ == "__main__":
    extractor = ExtractorAigua()
    # Pongo 25000 en el test también para que pueda encontrar el histórico
    df_dades = extractor.obtenir_dades_embassaments(limit=25000) 
    
    if df_dades is not None and not df_dades.empty:
        analista = AnalistaAigua(df_dades)
        
        print("\n🕵️‍♂️ CERCANT TITULARS CLIMÀTICS...\n" + "-"*40)
        
        general = analista.obtenir_estat_general()
        critic = analista.insight_pantano_critic()
        historic = analista.obtenir_evolucio_historica()
        
        print(f"🌍 ESTAT ACTUAL: {general['percentatge_mitja']:.1f}%")
        if historic['mitjana_1_any']:
            print(f"🕰️ FA 1 ANY ({historic['any_passat']}): {historic['mitjana_1_any']:.1f}%")
        if historic['mitjana_5_anys']:
            print(f"🕰️ FA 5 ANYS ({historic['any_historic']}): {historic['mitjana_5_anys']:.1f}%")
        print(f"🚨 CRÍTIC: {critic['pantano']} al {critic['percentatge']:.2f}%")
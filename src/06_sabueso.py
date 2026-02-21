from duckduckgo_search import DDGS

class SabuesoNoticies:
    def __init__(self):
        self.ddgs = DDGS()

    def buscar_noticia_recent(self, tema="bulo pantanos sequia catalunya"):
        print(f"🔎 Rastrejant internet per notícies recents sobre: '{tema}'...")
        
        try:
            # Busquem a la secció de notícies de DuckDuckGo (només el 1r resultat)
            resultats = list(self.ddgs.news(tema, max_results=100))
            
            if resultats:
                noticia = resultats[0]
                print(f"🎯 Hem trobat un objectiu: {noticia['title']}")
                return {
                    "font": noticia['source'],
                    "enllac": noticia['url'],
                    "afirmacio": noticia['title'], # Usem el titular com a afirmació a tractar
                    "data_publicacio": noticia.get('date', 'Data desconeguda')
                }
            else:
                raise ValueError("No s'han trobat notícies recents.")
                
        except Exception as e:
            print(f"⚠️ Error en la cerca web: {e}")
            # El nostre paracaigudes de seguretat
            return {
                "font": "Xarxes Socials (Fallback)", 
                "afirmacio": "El govern està enderrocant preses per crear una sequera artificial."
            }
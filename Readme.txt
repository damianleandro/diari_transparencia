# 💧 El Cronista de Dades: Aigua i Transparència

**Projecte presentat per a l'Open Data Day 2026**

Una agència de notícies automatitzada que combat la desinformació climàtica creuant dades obertes històriques amb Intel·ligència Artificial Generativa responsable.

## 🎯 L'Objectiu
En un context d'emergència climàtica, la informació ciutadana sovint es veu enterbolida per la desinformació. *El Cronista de Dades* automatitza l'extracció de milers de registres històrics de l'Agència Catalana de l'Aigua (ACA), els analitza de forma determinista amb Python, i utilitza un LLM per redactar una notícia periodística completament veraç, acompanyada d'una visualització temporal de l'evolució dels embassaments.

**Pilars del concurs assolits:**
* ✅ **Combat la desinformació:** Totes les dades s'extreuen de fonts oficials (`analisi.transparenciacatalunya.cat`).
* ✅ **IA Responsable:** L'IA no analitza els números (per evitar al·lucinacions), només redacta el text basant-se en un *prompt* estrictament controlat per l'analista de dades previ.
* ✅ **Millora de la qualitat de la informació:** Tradueix JSONs incomprensibles i milers de files en un gràfic visual i un llenguatge periodístic assequible.

## ⚙️ Arquitectura del Sistema
El projecte s'estructura en un *pipeline* modular de 4 fases:

1. **`dades_extractor.py`**: Es connecta via API (Socrata) al portal de Dades Obertes de la Generalitat i descarrega l'històric (últims 5 anys) de l'estat de les Conques Internes.
2. **`02_analista.py`**: Processa les dades amb `pandas`. Calcula la situació actual, viatja en el temps per comparar-ho amb fa 1 i 5 anys, i detecta el punt més crític del territori.
3. **`04_graficador.py`**: Utilitza `seaborn` i `matplotlib` per generar una línia de temps renderitzada que visualitza el volum d'aigua històric.
4. **`03_redactor.py`**: Un cop verificats els *insights*, envia les variables rígides al model **Gemini 2.5 Flash** per compondre la narrativa periodística final.

## 🚀 Instal·lació i Ús

### 1. Clonar el repositori i preparar l'entorn
```bash
git clone [https://github.com/teu-usuari/cronista-de-dades.git](https://github.com/teu-usuari/cronista-de-dades.git)
cd cronista-de-dades
pip install -r requirements.txt
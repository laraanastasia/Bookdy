import streamlit as st
import utils.conf as config
from recommend_rag import get_recommendation, get_vectorstore as get_vectorstore_logic
import streamlit.components.v1 as components
from graph_builder import build_knowledge_graph
from recommend_graph import get_author_analysis, visualize_author_subgraph
import utils.prep as prep

cfg = config.load_config("configs/config.yaml")
chat_model = cfg.get("chat_model")
embed_model = cfg.get("embed_model")
persist_dir = cfg.get("persist_dir")
goodreads_csv_path = cfg.get("goodreads_csv_path") 
graph_viz_path = cfg.get("graph_viz_path")

@st.cache_resource
def load_cached_vectorstore(persist_dir: str, embed_model: str):
    try:
        vectorstore = get_vectorstore_logic(persist_dir, embed_model)
        st.success("Vektorindex erfolgreich geladen.")
        return vectorstore
    except FileNotFoundError as e:
        st.error(f"Fehler: {e}. Bitte zuerst 'ingest.py' ausführen.")
        return None
    except Exception as e:
        st.error(f"Fehler beim Laden des Vektorindex oder Embedding-Modells: {e}")
        return None

@st.cache_resource
def load_cached_graph(csv_path: str):
    try:
        df = prep.load_and_prep_data(csv_path)
        graph = build_knowledge_graph(df)
        st.success("Knowledge Graph erfolgreich erstellt.")
        return graph, df
    except FileNotFoundError:
        st.error(f"Fehler: Die Datei '{csv_path}' wurde nicht gefunden.")
        return None, None
    except Exception as e:
        st.error(f"Ein Fehler ist beim Erstellen des Graphen aufgetreten: {e}")
        return None, None

st.set_page_config(page_title="Book Preference LLM", page_icon="📚", layout="wide")
st.title("Buch-Empfehlungs-App")

vectorstore = load_cached_vectorstore(persist_dir, embed_model)
knowledge_graph, df_authors = load_cached_graph(goodreads_csv_path)

rag_tab, kg_tab = st.tabs(["**📚 RAG Empfehlung**", "**🕸️ Knowledge Graph Analyse**"])
with rag_tab:
    with st.sidebar:
        st.header("Konfiguration")
        k = st.slider("Top-K ähnliche Bücher (für LLM-Kontext)", min_value=3, max_value=15, value=int(cfg.get("k", 5)), key="k_slider")
    
        st.markdown("---")
        st.subheader("Reranking-Gewichtung")
        rating_boost = st.slider("Boost (4+/5 Sterne)", min_value=0.0, max_value=1.0, value=0.3, step=0.05)
        dnf_penalty = st.slider("Penalty (DNF/Abbruch)", min_value=0.0, max_value=1.0, value=0.4, step=0.05)
    

    st.subheader("Klappentext-Analyse")
    blurb = st.text_area("Klappentext (Blurb) des neuen Buches eingeben", height=200)

    if st.button("Vorhersagen") and blurb.strip():
        if not load_cached_vectorstore(persist_dir, embed_model):
            st.stop()

        with st.spinner("LLM wird mit deiner Lesehistorie befragt und Reranking angewendet..."):
            try:
                rag_out = get_recommendation(
                    blurb=blurb, 
                    persist_dir=persist_dir, 
                    chat_model=chat_model, 
                    embed_model=embed_model, 
                    k=k,
                    rating_boost=rating_boost,
                    dnf_penalty=dnf_penalty
                )
            except Exception as e:
                st.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
                st.stop()


        st.markdown("### 📚 Personalisierte Analyse")
        st.write(rag_out["explanation"])

        if rag_out['contexts']:
            with st.expander(f"🔎 Top {len(rag_out['contexts'])} reranked Bücher aus deiner Historie (Context)"):
                st.markdown(
                    "Die Liste zeigt die **gewichtetsten** Bücher, die der LLM für die Analyse verwendet hat. "
                    "Die Spalte **Adj.** zeigt die Anpassung des Ähnlichkeits-Scores aufgrund deiner **My Rating** und **Shelf**-Präferenzen."
                )
                
                for d in rag_out["contexts"]:
                    meta = d.metadata
                    col1, col2 = st.columns([0.7, 0.3])
                    
                    with col1:
                        st.markdown(f"**{meta.get('title','N/A')}** – {meta.get('author','N/A')}")
                        st.caption(f"**Shelf:** {meta.get('shelf','N/A')} · **Pages:** {meta.get('pages','N/A')}")
                    
                    with col2:
                        score_color = "green" if meta.get('adjustment', 0.0) >= 0 else "red"
                        st.markdown(
                            f"**Bewertung:** {meta.get('rating',0)}★ "
                            f"| <span style='color:{score_color}'>**Adj:** {meta.get('adjustment', 0.0):+.2f}</span>",
                            unsafe_allow_html=True
                        )
                    
                    st.markdown(f"> {d.page_content.replace(chr(10), '  \n> ')}")
                    st.divider()
with kg_tab:
    st.header("Analyse basierend auf deinem Graphen")
    st.markdown(
        "Wähle einen Autor aus deiner Lesehistorie aus, um deine Beziehung zu seinen Werken "
        "visuell und textuell zu analysieren. Dies hilft dir zu entscheiden, ob du ein "
        "weiteres Buch von diesem Autor lesen solltest."
    )

    if knowledge_graph is None or df_authors is None:
        st.error("Graph-Analyse nicht möglich, da die Goodreads-Daten nicht geladen werden konnten.")
    else:
        author_list = sorted(df_authors['author'].unique().tolist())
        
        selected_author = st.selectbox(
            "Wähle einen Autor zur Analyse:",
            options=author_list,
            index=None,
            placeholder="Autor auswählen..."
        )

        if selected_author:
            analysis_result = get_author_analysis(knowledge_graph, selected_author)
            st.markdown(analysis_result["explanation"])
            
            st.subheader("Interaktive Visualisierung")
            with st.spinner("Erstelle Graphen-Visualisierung..."):
                html_content = visualize_author_subgraph(knowledge_graph, selected_author, file_path=graph_viz_path)
                if html_content:
                    components.html(html_content, height=610, scrolling=False)
                else:
                    st.warning("Für diesen Autor konnte keine Visualisierung erstellt werden.")
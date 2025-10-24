import streamlit as st
import utils.conf as config
from recommend_rag import get_recommendation, get_vectorstore as get_vectorstore_logic
import streamlit.components.v1 as components
import utils.prep as prep


cfg = config.load_config("configs/config.yaml")
chat_model = cfg.get("chat_model")
embed_model = cfg.get("embed_model")
persist_dir = cfg.get("persist_dir")
goodreads_csv_path = cfg.get("goodreads_csv_path") 

@st.cache_resource
def load_cached_vectorstore(persist_dir: str, embed_model: str):
    try:
        vectorstore = get_vectorstore_logic(persist_dir, embed_model)
        return vectorstore
    except FileNotFoundError as e:
        st.error(f"Error: {e}. Please run 'ingest.py' first.")
        return None
    except Exception as e:
        st.error(f"Error loading vector index or embedding model: {e}")
        return None

st.set_page_config(page_title="Book Preference LLM", page_icon="📚", layout="wide")
st.title("Book Recommendation App")

vectorstore = load_cached_vectorstore(persist_dir, embed_model)

rag_tab, = st.tabs(["**📚 RAG Recommendation**"])

with rag_tab:
    with st.sidebar:
        st.header("Configuration")
        k = st.slider(
            "Top-K similar books (for LLM context)", 
            min_value=3, 
            max_value=15, 
            value=int(cfg.get("k", 5)), 
            key="k_slider"
        )
    
        st.markdown("---")
        st.subheader("Reranking Weights")
        rating_boost = st.slider(
            "Boost (4+/5 stars)", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.3, 
            step=0.05
        )
        dnf_penalty = st.slider(
            "Penalty (DNF/Did Not Finish)", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.4, 
            step=0.05
        )
    
    st.subheader("Blurb Analysis")
    blurb = st.text_area("Enter the blurb of the new book", height=200)

    if st.button("Predict") and blurb.strip():
        if not vectorstore: 
            st.error("Vector store is not loaded. Cannot proceed.")
            st.stop()

        with st.spinner("Querying your reading history and applying reranking..."):
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
                st.error(f"An unexpected error occurred: {e}")
                st.stop()

        st.markdown("### 📚 Personalized Analysis")
        st.write(rag_out["explanation"])

        if rag_out['contexts']:
            with st.expander(f"🔎 Top {len(rag_out['contexts'])} reranked books from your history (Context)"):
                st.markdown(
                    "This list shows the **highest-weighted** books that the LLM used for its analysis. "
                    "The **Adj.** column shows the score adjustment based on your **My Rating** and **Shelf** preferences."
                )
                
                for d in rag_out["contexts"]:
                    meta = d.metadata
                    col1, col2 = st.columns([0.7, 0.3])
                    
                    with col1:
                        st.markdown(f"**{meta.get('title','N/A')}** – {meta.get('author','N/A')}")
                        st.caption(f"**Shelf:** {meta.get('shelf','N/A')} · **Rating:** {meta.get('rating',0)}★")
                    
                    with col2:
                        adjustment = meta.get('adjustment', 0.0)
                        if adjustment < 0:
                            score_color = "green"
                        elif adjustment > 0:
                            score_color = "red"
                        else:
                            score_color = "grey"
                            
                        st.markdown(
                            f"**Orig. Score:** {meta.get('original_score', 0.0):.3f} "
                            f"| <span style='color:{score_color}'>**Adj:** {adjustment:+.2f}</span>",
                            unsafe_allow_html=True
                        )
                    
                    if meta.get('clean_blurb'):
                        st.markdown(f"**Blurb:** *{meta.get('clean_blurb').replace(chr(10), '  \n ')}*")
                    
                    if meta.get('my_review'):
                        st.markdown(f"**My Review:** {meta.get('my_review').replace(chr(10), '  \n> ')}")
                    


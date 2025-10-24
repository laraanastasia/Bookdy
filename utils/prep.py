import pandas as pd
from langchain.docstore.document import Document
from tqdm import tqdm

def load_and_prep_data(file_path):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        print("Have you run the 'get_blurbs_env.py' script first?")
        return pd.DataFrame()
    
    original_columns = df.columns
    new_columns = [col.lower().replace(' ', '_').replace('-', '_') for col in original_columns]
    df.columns = new_columns
    relevant_shelves = ['read', 'dnf', 'did-not-finish', 'to-read']
    if 'exclusive_shelf' not in df.columns:
        raise ValueError("The required column 'exclusive_shelf' is missing from the dataset.")
        
    df_filtered = df[df['exclusive_shelf'].isin(relevant_shelves)].copy()
    df_filtered['my_review'] = df_filtered['my_review'].fillna('')
    if 'blurb' in df_filtered.columns:
        df_filtered['blurb'] = df_filtered['blurb'].fillna('')
    else:
        print("Warning: 'blurb' column not found in the CSV.")
        print("Blurbs will be missing. Please run 'get_blurbs_env.py' first.")
        df_filtered['blurb'] = ''
    return df_filtered


def create_book_documents(df):
    docs = []
    print("Creating documents (blurb-only) for vector store...")
    
    for _, row in tqdm(df.iterrows(), total=len(df)):
        
        blurb_text = str(row.get('blurb', '')).strip()
        review_text = str(row.get('my_review', '')).strip()
        rating = row.get('my_rating', 0)
        shelf = row.get('exclusive_shelf', 'unknown')
        pages = row.get('number_of_pages', 'unknown')
        title = row.get('title', 'N/A')
        author = row.get('author', 'N/A')

        page_content = blurb_text
        
        if (not page_content or 
            'no blurb found' in page_content.lower() or 
            'book not found' in page_content.lower() or
            'api request error' in page_content.lower()):
            page_content = f"Title: {title}\nAuthor: {author}"
            blurb_text = "" 

        meta = {
            "title": title,
            "author": author,
            "rating": int(rating),
            "pages": int(pages) if str(pages).isdigit() else 0,
            "shelf": shelf,
            "book_id": str(row.get('book_id', '')),
            "clean_blurb": blurb_text, 
            "my_review": review_text.replace('<br/>', '\n') if review_text and review_text != 'nan' else "",
            "user_verdict": "" 
        }

        user_verdict = ""
        if shelf in ['dnf', 'did-not-finish']:
            user_verdict = "[USER OPINION: STRONGLY NEGATIVE (Did Not Finish)]"
        elif rating >= 4:
            user_verdict = f"[USER OPINION: EXTRAORDINARY ({rating}/5 stars)]"
        elif rating == 3:
            user_verdict = f"[USER OPINION: GOOD ({rating}/5 stars)]"
        elif rating > 0:
            user_verdict = f"[USER OPINION: NEGATIVE ({rating}/5 stars)]"
        
        meta['user_verdict'] = user_verdict

        docs.append(Document(page_content=page_content, metadata=meta))
    
    return docs
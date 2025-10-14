import pandas as pd
from langchain.docstore.document import Document
from tqdm import tqdm

def load_and_prep_data(file_path):
    df = pd.read_csv(file_path)
    original_columns = df.columns
    new_columns = [col.lower().replace(' ', '_').replace('-', '_') for col in original_columns]
    df.columns = new_columns
    relevant_shelves = ['read', 'dnf', 'did-not-finish']
    if 'exclusive_shelf' not in df.columns:
        raise ValueError("The required column 'exclusive_shelf' is missing from the dataset.")
    df_filtered = df[df['exclusive_shelf'].isin(relevant_shelves)].copy()
    df_filtered['my_review'] = df_filtered['my_review'].fillna('')
    return df_filtered

# In utils/prep.py

def create_book_documents(df):
    docs = []
    print("Creating rich documents for each book...")
    
    for _, row in tqdm(df.iterrows(), total=len(df)):
  
        rating = row.get('my_rating', 0)
        shelf = row.get('exclusive_shelf', 'unknown')
        pages = row.get('number_of_pages', 'unknown')
        review_text = str(row.get('my_review', '')).strip()

        # --- NEUE LOGIK ZUR ERZEUGUNG DES VERDIKTS ---
        user_verdict = ""
        if shelf in ['dnf', 'did-not-finish']:
            user_verdict = "[USER OPINION: STRONGLY NEGATIVE (Did Not Finish)]"
        elif rating >= 4:
            user_verdict = f"[USER OPINION: POSITIVE ({rating}/5 stars)]"
        elif rating == 3:
            user_verdict = f"[USER OPINION: MIXED ({rating}/5 stars)]"
        elif rating > 0:
            user_verdict = f"[USER OPINION: NEGATIVE ({rating}/5 stars)]"
        
        content_parts = [user_verdict] if user_verdict else []
        # --- ENDE NEUE LOGIK ---

        content_parts.extend([
            f"Title: {row.get('title', 'N/A')}",
            f"Author: {row.get('author', 'N/A')}"
        ])

        if rating > 0:
            content_parts.append(f"My Rating: I rated this book {rating} out of 5 stars.")
        else:
            content_parts.append("My Rating: I have not rated this book.")

        if shelf in ['dnf', 'did-not-finish']:
             content_parts.append(f"Shelf Status: I did not finish this book (DNF).")
        else:
             content_parts.append(f"Shelf Status: I have read this book.")

        content_parts.append(f"Book Details: It has {pages} pages.")

        if review_text and review_text != 'nan':
            cleaned_review = review_text.replace('<br/>', '\n')
            content_parts.append(f"My Personal Review: {cleaned_review}")
        else:
            content_parts.append("My Personal Review: I did not write a review.")
            
        page_content = "\n".join(content_parts)

        meta = {
            "title": row.get('title', ''),
            "author": row.get('author', ''),
            "rating": int(rating),
            "pages": int(pages) if str(pages).isdigit() else 0,
            "shelf": shelf,
            "book_id": str(row.get('book_id', ''))
        }

        docs.append(Document(page_content=page_content, metadata=meta))
    
    return docs
import pandas as pd
import requests
import time
import re
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
INPUT_FILE = 'goodreads_library_export.csv'
OUTPUT_FILE = 'goodreads_with_blurbs.csv'


def clean_isbn(isbn_str):
    if pd.isna(isbn_str):
        return None
    match = re.search(r'\d{10,13}', str(isbn_str))
    if match:
        return match.group(0)
    return None

def get_book_blurb(isbn13, isbn, title, author):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    query = ""
    if isbn13:
        query = f"isbn:{isbn13}"
    elif isbn:
        query = f"isbn:{isbn}"
    elif pd.notna(title) and pd.notna(author):
        query = f"intitle:{title}+inauthor:{author}"
    else:
        return "No valid search terms (ISBN, Title, or Author)"

    url = f"{base_url}?q={query}&key={API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()

        if data.get('totalItems', 0) > 0:
            volume_info = data.get('items', [{}])[0].get('volumeInfo', {})
            description = volume_info.get('description', 'No blurb found.')
            return description
        else:
            return "Book not found via API."

    except requests.exceptions.RequestException as e:
        return f"API Request Error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    print(f"Loading data from {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"ERROR: Input file '{INPUT_FILE}' not found.")
        print("Please make sure your Goodreads file is in the same directory as this script.")
        return

    df['Blurb'] = ''

    print("Cleaning ISBNs...")
    df['clean_isbn13'] = df['ISBN13'].apply(clean_isbn)
    df['clean_isbn'] = df['ISBN'].apply(clean_isbn)

    total_books = len(df)
    print(f"Found {total_books} books. Starting to fetch blurbs...")

  
    for index, row in df.iterrows():
        title = row['Title']
        print(f"Processing {index + 1}/{total_books}: {title}...")

        blurb = get_book_blurb(
            isbn13=row['clean_isbn13'],
            isbn=row['clean_isbn'],
            title=title,
            author=row['Author']
        )
  
        df.at[index, 'Blurb'] = blurb  

        time.sleep(1) # 1-second delay between requests

    df = df.drop(columns=['clean_isbn13', 'clean_isbn'])

    print("\nProcessing complete.")
    
    try:
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
        print(f"Successfully saved updated library to: {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    main()
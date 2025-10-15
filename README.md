# 🔮✨ My Bookish Oracle ✨🔮

Hello, dear bookworm\! 🌸 Do you sometimes feel overwhelmed by your endless TBR pile? You stand before a new, shiny book, read the blurb, and ask yourself: "Will we be soulmates, or will I DNF it after 50 pages?"

Worry no more\! This little app is your personal book fortune-teller, your literary oracle, and your new best friend in deciding which book gets to conquer your heart next. It knows your soul (or at least your Goodreads library 😉) and gives you a magical prediction\!

## What this little magic app can do for you

This app has two magical sides, just like your favorite book:

### 📚 The Crystal Ball (RAG Recommendation)

Enter the blurb of a book that's calling to you. Our app looks deep into the pages of your past reading adventures, finds the books most similar to it, and then consults a wise AI (your personal book spirit\!) to predict whether you will like this new book.

- **Personalized Analysis:** Receive a lovingly crafted prediction based on YOUR preferences.
- **Intelligent Ranking:** Books you've rated with 5 stars carry more weight. Books you've abandoned (DNF) are seen as a warning. This makes the prediction even more accurate\!
- **Complete Transparency:** See exactly which books from your past were used to make the prediction.

### 🕸️ The Author Constellation (Knowledge Graph Analysis)

Have you ever wondered if you and a certain author just "click"? This part of the app draws a beautiful star map of your relationship with an author.

- **Choose an Author:** Pick someone from your reading list.
- **Visual Magic:** See an interactive web that connects you, the author, and all of their books that you've read. Each node tells a story about your ratings and feelings.
- **Clear Decision Support:** A text analysis tells you whether it's a good idea to add another book by this author to your wishlist.

## How to bring your own Reading Oracle to life

Follow these steps to unleash your personal reading magic. It's a bit like a ritual with candlelight and tea\! ☕️

### Step 1: Your Personal Reading Journal (Goodreads Data)

First things first\! The oracle needs to get to know you.

1.  Go to [Goodreads](https://www.goodreads.com/review/import).
2.  Click on **"Export Library"** and wait for the download link to appear.
3.  Download the `csv` file.
4.  **IMPORTANT:** Rename the file to `goodreads_library_export.csv` and place it in the `data` folder of this project.

### Step 2: Your Cozy Reading Nook (Installation)

Let's prepare everything for a cozy programming afternoon.

1.  **Python Magic:** Make sure you have Python 3.9 or higher installed.
2.  **Virtual Bubble:** It's always a good idea to work in a clean environment. Create a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3.  **The Magic Spells (Install Dependencies):** Install all the necessary packages with this one magic command:
    ```bash
    pip install -r requirements.txt
    ```

### Step 3: Summon the Book Spirit (Local LLM with Ollama)

Our app needs a clever mind in the background. We use Ollama for this – it's super easy\!

1.  **Install Ollama:** Download it from [ollama.com](https://ollama.com/) and install it.
2.  **Summon the Spirits:** Open your terminal and run these two commands to download the AI models we need. (This will take a moment, so feel free to make a cup of tea\!)
    ```bash
    ollama pull llama3
    ollama pull nomic-embed-text
    ```

### Step 4: The Grand Inauguration Ritual (Process Data)

Before we can start the app, we need to teach the oracle about all your books. This step reads your Goodreads file and transforms it into magical knowledge.
**Run this command only once (or whenever you have updated your Goodreads list):**

```bash
python ingest.py
```

Be patient, this is where the real alchemy happens\! ✨

### Step 5: Open the Portal\! (Start the App)

Everything is ready\! Time to unleash the magic.

```bash
streamlit run app.py
```

Your browser should now open with your beautiful, personal book recommendation app\!

---

Have fun discovering your next favorite book\! May your pages never stick together and your reading time never end. 💖📖

**Happy Reading\!**

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

## How to bring your own Reading Oracle to life

Follow these steps to unleash your personal reading magic. It's a bit like a ritual with candlelight and tea\! ☕️

### Step 1: Your Personal Reading Journal (Goodreads Data)

First things first\! The oracle needs to get to know you.

1.  Go to [Goodreads](https://www.goodreads.com/review/import).
2.  Click on **"Export Library"** and wait for the download link to appear.
3.  Download the `csv` file.
4.  **IMPORTANT:** Rename the file to `goodreads_library_export.csv`. Put this file into the `utils` folder.

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

### Step 3: Investigation Mode !ON! (API KEY)

To include book blurbs, the script needs to connect to the Google Books database. You'll need a free API key for this. You need to run this script once in the beginning(or when you want to add an updated goodreads export)

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/apis/dashboard).
2.  If you don't have one, create a new project (e.g., "My Book Project").
3.  In the main dashboard, click **"+ ENABLE APIS AND SERVICES"**.
4.  Search for **"Google Books API"** and click on it.
5.  Click the **"Enable"** button.
6.  Go to the "Credentials" tab on the left-hand side.
7.  Click **"+ CREATE CREDENTIALS"** at the top and select **"API key"**.
8.  A window will pop up with your new key. **Copy this key**—you'll need it in the next step.
9.  Inside the `utils` folder, create a new file named exactly `.env`
    Open this new `.env` file and add the following line, pasting the API key you copied from step 8:

        ```ini
        GOOGLE_BOOKS_API_KEY="YOUR_API_KEY_GOES_HERE"
        ```
        * **Security Tip:** If you are using Git, add `.env` to your `.gitignore` file to keep your API key private.

10. Open your terminal and make sure you are in the utils project folder.
11. Run the script:
    ```bash
    python get_blurbs_env.py
    ```

The script will start! It will find your CSV and `.env` files inside the `utils` folder. You will see it process each book one by one in the terminal.

When it's finished, a new file named `goodreads_with_blurbs.csv` will be saved in your utils project folder. This file will have all your original data plus a new "Blurb" column.

### Step 4: Summon the Book Spirit (Local LLM with Ollama)

Our app needs a clever mind in the background. We use Ollama for this – it's super easy\!

1.  **Install Ollama:** Download it from [ollama.com](https://ollama.com/) and install it.
2.  **Summon the Spirits:** Open your terminal and run these two commands to download the AI models we need. (This will take a moment, so feel free to make a cup of tea\!)
    ```bash
    ollama pull llama3
    ollama pull nomic-embed-text
    ```

### Step 5: The Grand Inauguration Ritual (Process Data)

Before we can start the app, we need to teach the oracle about all your books. This step reads your Goodreads file and transforms it into magical knowledge.
**Run this command only once (or whenever you have updated your Goodreads list):**

```bash
python ingest.py
```

Be patient, this is where the real alchemy happens\! ✨

### Step 6: Open the Portal\! (Start the App)

Everything is ready\! Time to unleash the magic.

```bash
streamlit run app.py
```

Your browser should now open with your beautiful, personal book recommendation app\!

---

Have fun discovering your next favorite book\! May your pages never stick together and your reading time never end. 💖📖

**Happy Reading\!**

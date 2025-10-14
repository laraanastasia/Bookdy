# 🔮✨ My Bookish Oracle ✨🔮

Hallo, liebe Leseratte\! 🌸 Fühlst du dich auch manchmal von deinem endlosen SuB überfordert? Du stehst vor einem neuen, glänzenden Buch, liest den Klappentext und fragst dich: "Werden wir Seelenverwandte sein oder werde ich es nach 50 Seiten abbrechen?"

Keine Sorge mehr\! Diese kleine App ist deine persönliche Buch-Wahrsagerin, dein literarisches Orakel und deine neue beste Freundin bei der Entscheidung, welches Buch als Nächstes dein Herz erobern darf. Sie kennt deine Seele (oder zumindest deine Goodreads-Bibliothek 😉) und gibt dir eine magische Vorhersage\!

## Was diese kleine Zauber-App für dich tun kann

Diese App hat zwei magische Seiten, genau wie dein Lieblingsbuch:

### 📚 Die Kristallkugel (RAG-Empfehlung)

Gib den Klappentext eines Buches ein, das dich anlacht. Unsere App schaut tief in die Seiten deiner bisherigen Leseabenteuer, findet die Bücher, die ihm am ähnlichsten sind, und befragt dann eine weise KI (deinen persönlichen Buch-Geist\!), ob dieses neue Buch dir gefallen wird.

- **Personalisierte Analyse:** Erhalte eine liebevoll formulierte Vorhersage, die auf DEINEN Vorlieben basiert.
- **Intelligentes Ranking:** Bücher, die du mit 5 Sternen bewertet hast, haben mehr Gewicht. Bücher, die du abgebrochen hast (DNF), werden als Warnung gesehen. So wird die Vorhersage noch genauer\!
- **Vollkommene Transparenz:** Sieh genau, welche Bücher aus deiner Vergangenheit für die Vorhersage herangezogen wurden.

### 🕸️ Die Autoren-Konstellation (Knowledge Graph Analyse)

Hast du dich je gefragt, ob du und ein bestimmter Autor einfach "klicken"? Dieser Teil der App zeichnet eine wunderschöne Sternenkarte deiner Beziehung zu einem Autor.

- **Wähle einen Autor:** Such dir jemanden aus deiner Leseliste aus.
- **Visuelle Magie:** Sieh ein interaktives Netz, das dich, den Autor und all seine Bücher, die du gelesen hast, miteinander verbindet. Jeder Knotenpunkt erzählt eine Geschichte über deine Bewertungen und Gefühle.
- **Klare Entscheidungshilfe:** Eine textliche Analyse verrät dir, ob es eine gute Idee ist, ein weiteres Buch dieses Autors auf deine Wunschliste zu setzen.

## Wie du dein eigenes Lese-Orakel zum Leben erweckst

Folge diesen Schritten, um deine persönliche Lese-Magie zu entfesseln. Es ist ein bisschen wie ein Ritual bei Kerzenschein und Tee\! ☕️

### Schritt 1: Dein persönliches Lese-Tagebuch (Goodreads-Daten)

Das Wichtigste zuerst\! Das Orakel muss dich kennenlernen.

1.  Gehe zu [Goodreads](https://www.goodreads.com/review/import).
2.  Klicke auf **"Export Library"** und warte, bis der Link zum Herunterladen erscheint.
3.  Lade die `csv`-Datei herunter.
4.  **WICHTIG:** Benenne die Datei in `goodreads_library_export.csv` um und lege sie in den `data` Ordner dieses Projekts.

### Schritt 2: Dein gemütlicher Lese-Winkel (Installation)

Bereiten wir alles für einen gemütlichen Programmier-Nachmittag vor.

1.  **Python-Magie:** Stelle sicher, dass du Python 3.9 oder höher installiert hast.
2.  **Virtuelle Blase:** Es ist immer eine gute Idee, in einer sauberen Umgebung zu arbeiten. Erstelle ein virtuelles Environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Auf Windows: .venv\Scripts\activate
    ```
3.  **Die Zaubersprüche (Abhängigkeiten installieren):** Installiere alle benötigten Pakete mit diesem einen, magischen Befehl:
    ```bash
    pip install -r requirements.txt
    ```
    _(Falls keine `requirements.txt` da ist, musst du sie mit den importierten Modulen wie `streamlit`, `pandas`, `langchain`, `ollama` usw. erstellen.)_

### Schritt 3: Den Buch-Geist herbeirufen (Lokales LLM mit Ollama)

Unsere App braucht ein kluges Köpfchen im Hintergrund. Wir nutzen dafür Ollama – das ist super einfach\!

1.  **Installiere Ollama:** Lade es von [ollama.com](https://ollama.com/) herunter und installiere es.
2.  **Rufe die Geister herbei:** Öffne dein Terminal und führe diese beiden Befehle aus, um die KI-Modelle herunterzuladen, die wir brauchen. (Das dauert einen Moment, also mach dir ruhig einen Tee\!)
    ```bash
    ollama pull llama3
    ollama pull nomic-embed-text
    ```

### Schritt 4: Das große Einweihungs-Ritual (Daten verarbeiten)

Bevor wir die App starten können, müssen wir dem Orakel all deine Bücher beibringen. Dieser Schritt liest deine Goodreads-Datei und verwandelt sie in magisches Wissen.
**Führe diesen Befehl nur einmal aus (oder immer dann, wenn du deine Goodreads-Liste aktualisiert hast):**

```bash
python ingest.py
```

Hab etwas Geduld, hier passiert die wahre Alchemie\! ✨

### Schritt 5: Öffne das Portal\! (App starten)

Alles ist bereit\! Zeit, die Magie zu entfesseln.

```bash
streamlit run app.py
```

Dein Browser sollte sich nun mit deiner wunderschönen, persönlichen Buch-Empfehlungs-App öffnen\!

---

Viel Spaß beim Entdecken deines nächsten Lieblingsbuchs\! Mögen deine Seiten niemals kleben und deine Lesezeit niemals enden. 💖📖

**Happy Reading\!**

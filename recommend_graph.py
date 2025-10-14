import networkx as nx
from pyvis.network import Network
import os

def get_author_analysis(graph: nx.Graph, author_name: str):
    """
    Analysiert die Beziehung des Nutzers zu einem bestimmten Autor im Graphen.
    """
    if not graph.has_node(author_name):
        return {
            "explanation": f"Der Autor '{author_name}' wurde in deiner Lesehistorie nicht gefunden.",
            "read_books": []
        }

    read_books = []
    total_rating = 0
    high_rated_books = 0
    dnf_books = 0

    for book_node in graph.neighbors(author_name):
        # Überprüfe, ob der Nutzer dieses Buch gelesen hat
        if graph.has_edge("You", book_node):
            edge_data = graph.get_edge_data("You", book_node)
            book_info = {
                "title": book_node,
                "rating": edge_data.get('rating', 0),
                "shelf": edge_data.get('shelf', 'unknown')
            }
            read_books.append(book_info)

            if edge_data.get('shelf') in ['dnf', 'did-not-finish']:
                dnf_books += 1
            if edge_data.get('rating', 0) >= 4:
                high_rated_books += 1
            total_rating += edge_data.get('rating', 0)
    
    if not read_books:
        return {
            "explanation": f"Obwohl '{author_name}' in deiner Bibliothek ist, scheint es keine gelesenen Bücher zu geben, die analysiert werden könnten.",
            "read_books": []
        }

    num_books = len(read_books)
    avg_rating = total_rating / num_books if num_books > 0 else 0
    
    explanation = f"**Analyse für {author_name}:**\n\n"
    explanation += f"Du hast **{num_books} Buch/Bücher** von diesem Autor gelesen.\n"
    explanation += f"- Deine durchschnittliche Bewertung ist **{avg_rating:.2f} Sterne**.\n"
    explanation += f"- Davon hast du **{high_rated_books} als sehr gut** (4+ Sterne) bewertet.\n"
    
    if dnf_books > 0:
        explanation += f"- ⚠️ Du hast **{dnf_books} Buch/Bücher nicht beendet** (DNF).\n\n"
   
    if dnf_books > 0 and dnf_books >= high_rated_books:
        conclusion = f"**Fazit:** Vorsicht ist geboten. Da du mindestens so viele Bücher von {author_name} abgebrochen wie geliebt hast, besteht ein **erhöhtes Risiko**, dass dir ein neues Buch nicht gefallen wird."
    elif high_rated_books > 0 and high_rated_books > dnf_books:
        conclusion = f"**Fazit:** Die Chancen stehen gut! Da du überwiegend positive Erfahrungen mit den Werken von {author_name} gemacht hast, ist es **sehr wahrscheinlich**, dass dir ein neues Buch gefallen wird."
    else:
        conclusion = f"**Fazit:** Deine Erfahrungen mit {author_name} sind gemischt. Ein neues Buch könnte in beide Richtungen ausschlagen. Schau dir die Themen genau an."

    explanation += conclusion

    return {
        "explanation": explanation,
        "read_books": read_books
    }


def visualize_author_subgraph(graph: nx.Graph, author_name: str, file_path="graph.html"):
    """
    Erstellt eine interaktive Visualisierung des Subgraphen für einen Autor.
    """
    if not graph.has_node(author_name):
        return None

    subG = nx.Graph()
    
    subG.add_node("You", **graph.nodes["You"])
    subG.add_node(author_name, **graph.nodes[author_name])

    for book in graph.neighbors(author_name):
        if graph.has_edge("You", book):
            subG.add_node(book, **graph.nodes[book])
            subG.add_edge("You", book, **graph.get_edge_data("You", book))
            subG.add_edge(author_name, book, **graph.get_edge_data(author_name, book))
    
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white", notebook=True, cdn_resources='in_line')
    net.from_nx(subG)

    net.set_options("""
    var options = {
      "nodes": {
        "borderWidth": 2,
        "borderWidthSelected": 4,
        "font": {
          "size": 16,
          "face": "tahoma"
        }
      },
      "edges": {
        "width": 2,
        "font": {
            "size": 14,
            "strokeWidth": 4,
            "strokeColor": "#222222"
        },
        "smooth": {
            "type": "continuous"
        }
      },
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 200,
          "springConstant": 0.08,
          "avoidOverlap": 0.5
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      }
    }
    """)
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    net.save_graph(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    return html_content
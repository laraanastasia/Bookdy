import pandas as pd
import networkx as nx

def build_knowledge_graph(df: pd.DataFrame):
    G = nx.Graph()
    user_node = "You"
    G.add_node(user_node, type="user", color="#FFD700") 

    for _, row in df.iterrows():
        book_title = row.get('title', 'N/A')
        author_name = row.get('author', 'N/A')
        rating = row.get('my_rating', 0)
        shelf = row.get('exclusive_shelf', 'unknown')

        book_color = "#1f78b4" 
        if shelf in ['dnf', 'did-not-finish']:
            book_color = "#e31a1c" 
        elif rating >= 4:
            book_color = "#33a02c" 

    
        G.add_node(book_title, type="book", color=book_color, title=f"Rating: {rating}★\nShelf: {shelf}")
        G.add_node(author_name, type="author", color="#6a3d9a")

       
        G.add_edge(author_name, book_title, relation="WROTE")
        
        edge_label = f"{rating}★"
        if shelf in ['dnf', 'did-not-finish']:
            edge_label = "DNF"
            
        G.add_edge(user_node, book_title, relation="READ", rating=rating, shelf=shelf, label=edge_label)
        
    return G
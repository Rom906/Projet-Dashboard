from dash import Dash, dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(current_dir, "Donnees_M&Ms_S3.xlsx")

try:
    # Charger le fichier en ignorant la dernière ligne (totaux)
    df = pd.read_excel(excel_path, skipfooter=1)
    print("Fichier chargé avec succès !")
    print("Colonnes disponibles :", df.columns.tolist())
    print("Nombre de lignes :", len(df))
    
    # Nettoyer les noms de colonnes (supprimer les espaces en fin)
    df.columns = df.columns.str.strip()
    print("Colonnes après nettoyage :", df.columns.tolist())
    
    # Ajouter un index chronologique (l'ordre d'entrée dans le fichier)
    df = df.reset_index().rename(columns={'index': 'ordre_chrono'})
    df['ordre_chrono'] = df.index + 1
    
except Exception as e:
    print(f"Erreur lors du chargement : {e}")
    df = pd.DataFrame()

# Colonnes de couleurs (avec les noms exacts après nettoyage)
color_cols = ["jaune", "rouge", "bleu", "vert", "marron", "orange"]

# Couleurs spécifiques pour chaque type de M&M
color_palette = {
    "jaune": "#FFD700",  # Jaune
    "rouge": "#DC143C",  # Rouge
    "bleu": "#1E90FF",   # Bleu
    "vert": "#32CD32",   # Vert
    "marron": "#8B4513", # Marron
    "orange": "#FFA500"  # Orange
}

color_names_fr = {
    "jaune": "Jaune", 
    "rouge": "Rouge", 
    "bleu": "Bleu", 
    "vert": "Vert", 
    "marron": "Marron", 
    "orange": "Orange"
}

app = Dash(__name__)

# Vérifier si le DataFrame n'est pas vide avant de créer les options
if not df.empty and "nom de l'image" in df.columns:
    total_images = len(df)
    slider_min = 1
    slider_max = total_images
    slider_value = [1, min(20, total_images)]  # Afficher les 20 premières par défaut
else:
    total_images = 0
    slider_min = 0
    slider_max = 1
    slider_value = [0, 1]

app.layout = html.Div([
    html.H1("🍬 Analyse des M&M's par image", style={"textAlign": "center", "color": "#2c3e50"}),
    
    # Sélection du type de graphique
    html.Div([
        html.Label("Type de graphique :", style={"fontWeight": "bold", "marginRight": "10px"}),
        dcc.RadioItems(
            id="chart_type",
            options=[
                {"label": "📊 Histogramme empilé", "value": "stacked_bar"},
                {"label": "📈 Courbes par couleur", "value": "line_chart"}
            ],
            value="stacked_bar",
            inline=True,
            style={"marginBottom": "20px"}
        )
    ], style={"textAlign": "center", "margin": "20px"}),
    
    # Graphique principal
    dcc.Graph(id="main_chart", style={"height": "600px"}),
    
    # Contrôles
    html.Div([
        # Sélection des couleurs
        html.Div([
            html.Label("Couleurs à afficher :", style={"fontWeight": "bold"}),
            dcc.Checklist(
                id="color_selector",
                options=[{"label": color_names_fr[col], "value": col} for col in color_cols],
                value=color_cols,
                inline=True,
                style={"marginTop": "10px"}
            )
        ], style={"marginBottom": "20px"}),
        
        # Sélection de la plage d'images (ordre chronologique)
        html.Div([
            html.Label("Plage d'images (ordre chronologique) :", style={"fontWeight": "bold", "marginRight": "10px"}),
            dcc.RangeSlider(
                id="image_range",
                min=slider_min,
                max=slider_max,
                value=slider_value,
                marks={i: f"{i}" for i in range(slider_min, slider_max + 1, max(1, slider_max // 10))},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.Div([
                html.Button("Toutes les images", id="select_all_btn", n_clicks=0,
                           style={"marginRight": "10px", "padding": "5px 10px", "fontSize": "12px"}),
                html.Button("20 premières images", id="select_first_20_btn", n_clicks=0,
                           style={"marginRight": "10px", "padding": "5px 10px", "fontSize": "12px"}),
                html.Button("20 dernières images", id="select_last_20_btn", n_clicks=0,
                           style={"padding": "5px 10px", "fontSize": "12px"})
            ], style={"marginTop": "10px", "textAlign": "center"})
        ], style={"marginBottom": "20px", "width": "90%", "margin": "0 auto"}),
        
        # Affichage des images sélectionnées
        html.Div(id="selected_images_info", style={"marginTop": "10px", "fontStyle": "italic"}),
        
    ], style={"textAlign": "center", "margin": "20px"}),
    
    # Stocke les données pour la session
    dcc.Store(id="data_store", data=df.to_dict("records")),
    
    # Formulaire pour ajouter une nouvelle image
    html.Div([
        html.H3("➕ Ajouter une nouvelle image", style={"textAlign": "center", "color": "#2c3e50"}),
        html.Div([
            dcc.Input(id="new_image", type="number", placeholder="Numéro de l'image", 
                     style={"marginRight": "10px", "padding": "8px"}),
            *[dcc.Input(id=col, type="number", placeholder=color_names_fr[col], 
                       style={"marginRight": "5px", "padding": "8px", "width": "80px"}) for col in color_cols],
            html.Button("Ajouter l'image", id="add_button", n_clicks=0,
                       style={"backgroundColor": "#3498db", "color": "white", "border": "none", 
                              "padding": "8px 16px", "borderRadius": "4px", "cursor": "pointer"})
        ], style={"textAlign": "center", "marginTop": "10px"})
    ], style={"backgroundColor": "#f8f9fa", "padding": "20px", "marginTop": "30px", "borderRadius": "8px"})
])

# Callback pour mettre à jour le graphique principal
@app.callback(
    Output("main_chart", "figure"),
    Input("chart_type", "value"),
    Input("color_selector", "value"),
    Input("image_range", "value"),
    State("data_store", "data")
)
def update_main_chart(chart_type, selected_colors, image_range, data):
    if not data:
        return go.Figure().update_layout(
            title="Aucune donnée disponible",
            xaxis_title="Ordre chronologique des images",
            yaxis_title="Nombre de M&M's"
        )
    
    df_local = pd.DataFrame(data)
    
    # Filtrer par plage d'ordre chronologique
    mask = (df_local["ordre_chrono"] >= image_range[0]) & (df_local["ordre_chrono"] <= image_range[1])
    df_filtered = df_local[mask].sort_values("ordre_chrono")
    
    if df_filtered.empty:
        return go.Figure().update_layout(
            title="Aucune donnée dans la plage sélectionnée",
            xaxis_title="Ordre chronologique des images",
            yaxis_title="Nombre de M&M's"
        )
    
    # Préparer les données pour Plotly
    if chart_type == "stacked_bar":
        # Histogramme empilé
        fig = go.Figure()
        
        for color in selected_colors:
            fig.add_trace(go.Bar(
                x=df_filtered["ordre_chrono"].astype(str),  # Ordre chronologique comme catégorie
                y=df_filtered[color],
                name=color_names_fr[color],
                marker_color=color_palette[color],
                hovertemplate=f"<b>{color_names_fr[color]}</b><br>" +
                             f"Image: %{{customdata}}<br>" +
                             "Ordre: %{x}<br>" +
                             "Nombre: %{y}<br>" +
                             "<extra></extra>",
                customdata=df_filtered["nom de l'image"]
            ))
        
        fig.update_layout(
            barmode='stack',
            title="📊 Distribution des M&M's (ordre chronologique)",
            xaxis_title="Ordre chronologique des images",
            yaxis_title="Nombre de M&M's",
            hovermode="x unified",
            showlegend=True
        )
        
    else:  # line_chart
        # Courbes par couleur
        fig = go.Figure()
        
        for color in selected_colors:
            fig.add_trace(go.Scatter(
                x=df_filtered["ordre_chrono"].astype(str),  # Ordre chronologique comme catégorie
                y=df_filtered[color],
                name=color_names_fr[color],
                mode='lines+markers',
                line=dict(color=color_palette[color], width=3),
                marker=dict(color=color_palette[color], size=8),
                hovertemplate=f"<b>{color_names_fr[color]}</b><br>" +
                             f"Image: %{{customdata}}<br>" +
                             "Ordre: %{x}<br>" +
                             "Nombre: %{y}<br>" +
                             "<extra></extra>",
                customdata=df_filtered["nom de l'image"]
            ))
        
        fig.update_layout(
            title="📈 Évolution du nombre de M&M's (ordre chronologique)",
            xaxis_title="Ordre chronologique des images",
            yaxis_title="Nombre de M&M's",
            hovermode="x unified",
            showlegend=True
        )
    
    # Améliorations esthétiques communes
    fig.update_layout(
        template="plotly_white",
        font=dict(size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            type='category',  # Forcer le traitement en catégorie
            tickangle=0
        )
    )
    
    return fig

# Callback pour les boutons de sélection
@app.callback(
    Output("image_range", "value"),
    Output("selected_images_info", "children"),
    Input("select_all_btn", "n_clicks"),
    Input("select_first_20_btn", "n_clicks"),
    Input("select_last_20_btn", "n_clicks"),
    State("data_store", "data")
)
def update_slider_selection(all_clicks, first_20_clicks, last_20_clicks, data):
    ctx = dash.callback_context
    if not ctx.triggered or not data:
        return [1, 1], "Sélectionnez une plage d'images"
    
    df_local = pd.DataFrame(data)
    total_images = len(df_local)
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "select_all_btn":
        new_range = [1, total_images]
        message = f"Toutes les images sélectionnées ({total_images} images)"
    elif button_id == "select_first_20_btn":
        new_range = [1, min(20, total_images)]
        message = f"20 premières images sélectionnées"
    elif button_id == "select_last_20_btn":
        new_range = [max(1, total_images - 19), total_images]
        message = f"20 dernières images sélectionnées"
    else:
        new_range = [1, 1]
        message = "Sélectionnez une plage d'images"
    
    return new_range, message

# Callback pour mettre à jour la plage du slider
@app.callback(
    Output("image_range", "min"),
    Output("image_range", "max"),
    Input("data_store", "data")
)
def update_slider_range(data):
    if not data:
        return 0, 1
    
    df_local = pd.DataFrame(data)
    total_images = len(df_local)
    return 1, total_images

# Callback pour ajouter une nouvelle image
@app.callback(
    Output("data_store", "data"),
    Output("new_image", "value"),
    Output("jaune", "value"),
    Output("rouge", "value"),
    Output("bleu", "value"),
    Output("vert", "value"),
    Output("marron", "value"),
    Output("orange", "value"),
    Input("add_button", "n_clicks"),
    State("new_image", "value"),
    State("jaune", "value"),
    State("rouge", "value"),
    State("bleu", "value"),
    State("vert", "value"),
    State("marron", "value"),
    State("orange", "value"),
    State("data_store", "data")
)
def add_image(n_clicks, new_image, jaune, rouge, bleu, vert, marron, orange, data):
    if n_clicks > 0 and new_image is not None:
        # Vérifier si l'image existe déjà
        existing_images = [item["nom de l'image"] for item in data]
        if new_image in existing_images:
            print(f"L'image {new_image} existe déjà !")
            return data, None, None, None, None, None, None, None
        
        total = sum([jaune or 0, rouge or 0, bleu or 0, vert or 0, marron or 0, orange or 0])
        new_row = {
            "ordre_chrono": len(data) + 1,  # Nouvel ordre chronologique
            "nom de l'image": new_image,
            "jaune": jaune or 0,
            "rouge": rouge or 0,
            "bleu": bleu or 0,
            "vert": vert or 0,
            "marron": marron or 0,
            "orange": orange or 0,
            "total lignes": total
        }
        data.append(new_row)
        print(f"Image {new_image} ajoutée avec succès !")
        
        # Réinitialiser les champs du formulaire
        return data, None, None, None, None, None, None, None
    
    return data, None, None, None, None, None, None, None

if __name__ == "__main__":
    app.run(debug=True)
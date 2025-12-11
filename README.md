# Projet-Dashboard

## 🎯 Vue d'ensemble

Dashboard Streamlit interactive permettant de visualiser, créer, modifier et supprimer des données directement dans l'interface, avec persistance complète et système de sauvegarde JSON.

> ⭐ **IMPORTANTE**: Utilisez **`main.py`** comme point d'entrée (version finale et stable). Les fichiers `main_V3.py`, `main_V3 copy.py` et `main_v4.py` sont obsolètes et conservés uniquement pour compatibilité.

---

# Manuel d'utilisation de la dashboard

## 📋 Prérequis

Les fichiers Python requis :
- `page_donnees_V3.py` - Gestion des données
- `page_graphique_V3.py` - Gestion des graphiques  
- `main.py` - Point d'entrée principal (dernière version stable)
- `systeme_sauvegarde.py` - Sauvegarde/chargement JSON

Installation de Streamlit :
```bash
pip install streamlit pandas openpyxl
```

## 🚀 Lancement du dashboard

```bash
streamlit run main.py
```

Le dashboard s'ouvre alors en local : `http://localhost:8501`

Vous arrivez sur la **page "Données"** par défaut.

---

## 📖 Guide d'utilisation

### Navigation

Le menu de gauche permet de naviguer entre les pages :
- **Page "Données"** : Importation, création et gestion des données
- **Page "Graphiques"** : Création et visualisation de graphiques

Utilisez le sélecteur dans la section "Navigation" du sidebar pour changer de page.

---

## 🔑 Fonctionnalités principales

### 1️⃣ Importer un fichier CSV

**Localisation** : Section "Importer un fichier CSV" en haut de la page Données

**Comment l'utiliser** :
1. Glissez-déposez votre fichier CSV ou cliquez pour parcourir
2. Le fichier doit avoir ses données en colonnes
3. Un message de confirmation s'affiche : `✅ CSV importé: XXX lignes, YYY colonnes`
4. Le tableau s'affiche automatiquement

**Important** : Les données sont automatiquement sauvegardées en JSON pour persistance

---

### 2️⃣ Ajouter une nouvelle ligne

**Localisation** : Section "Ajouter une nouvelle ligne" sur la page Données

**Comment l'utiliser** :
1. Remplissez les champs correspondant à chaque colonne
2. Les champs acceptent **tous les types de données** : nombres, dates, texte
3. Cliquez sur le bouton **"➕ Ajouter la ligne"**
4. La ligne s'ajoute immédiatement au tableau
5. Les champs se réinitialisent pour une nouvelle saisie

**Exemple** :
```
Colonnes : Date | Ventes | Région
Saisie   : 7/10/21 | 150 | France
→ La ligne est ajoutée et persiste après fermeture du navigateur
```

**🔒 Persistance** :
- ✅ Persiste après rerun
- ✅ Persiste après changement de page
- ✅ Persiste après fermeture du navigateur

---

### 3️⃣ Gérer les lignes

**Localisation** : Section "Gérer les lignes" en bas de la page Données

La section propose 3 actions accessibles via les boutons :

#### **Action 1 : Afficher (📊)**

Sélectionner et afficher des lignes spécifiques.

**Option 1 - Plage d'indices** :
- Entrez l'indice de début (ex: 0)
- Entrez l'indice de fin inclus (ex: 9)
- Cliquez "📊 Afficher la plage"
- Résultat : affiche les lignes 0 à 9

**Option 2 - Sélection individuelle** :
- Sélectionnez les indices que vous voulez (ex: 0, 2, 5)
- Les lignes s'affichent immédiatement
- Utile pour visualiser certaines données non consécutives

#### **Action 2 : Modifier un élément (✏️)**

Modifier une seule cellule à la fois.

**Comment l'utiliser** :
1. Sélectionnez le **numéro de la ligne** à modifier
2. Sélectionnez la **colonne** à modifier
3. Vous voyez la valeur actuelle affichée
4. Entrez la nouvelle valeur dans le champ
5. Cliquez sur **"✏️ Modifier cet élément"**
6. La modification s'applique immédiatement

**Exemple** :
```
Ligne : 5
Colonne : "Date"
Valeur actuelle : 7/10/21
Nouvelle valeur : 8/10/21
→ Cliquer "✏️ Modifier cet élément"
→ La date change immédiatement dans le tableau
```

**🔒 Persistance** :
- ✅ Persiste après rerun
- ✅ Tous types de données supportés (texte, nombres, dates)
- ✅ Les champs se réinitialisent après modification

#### **Action 3 : Supprimer une ligne (🗑️)**

Supprimer une ligne entière de vos données.

**Comment l'utiliser** :
1. Sélectionnez le **numéro de la ligne** à supprimer
2. Un aperçu de la ligne s'affiche
3. Cliquez sur **"🗑️ Supprimer cette ligne"**
4. La ligne disparaît immédiatement du tableau

**🔒 Persistance** :
- ✅ Persiste après rerun
- ✅ Le nombre de lignes se met à jour automatiquement

---

### 4️⃣ Importer une sauvegarde JSON

**Localisation** : Section "Importer une sauvegarde JSON" sur la page Données

**Comment l'utiliser** :
1. Glissez-déposez un fichier de sauvegarde JSON ou cliquez pour parcourir
2. La structure complète (graphiques + données) est restaurée
3. Message de confirmation : `✅ Sauvegarde importée: N colonnes`

**Format** : Utilisez les fichiers générés par le bouton "Télécharger une sauvegarde"

---

### 5️⃣ Statistiques et métriques

**Localisation** : Section "Statistiques descriptives" sur la page Données

Des méthodes Python disponibles pour les calculs :

```python
données = st.session_state.données

# Somme
somme_ventes = données.get_sum("Ventes")

# Moyenne
moyenne_ventes = données.get_mean("Ventes")

# Médiane
med_ventes = données.get_median("Ventes")

# Écart type
std_ventes = données.get_std("Ventes")

# Variance
var_ventes = données.get_variance("Ventes")
```

---

### 6️⃣ Créer des graphiques

**Localisation** : Sidebar - Section "Ajouter des zones"

**Étape 1 - Créer une ligne** :
1. Entrez un titre de ligne (obligatoire)
2. Cochez "Afficher le titre de la ligne" si désiré
3. Cliquez "Ajouter une ligne"

**Étape 2 - Ajouter une zone graphique** :
1. Sélectionnez la ligne où ajouter la zone
2. Entrez le titre de la zone
3. Cochez "Afficher le titre de la zone" si désiré
4. Choisissez le type de graphique :
   - 📊 Histogramme
   - 📈 Graphique normal
   - 🔵 Nuage de points
   - 📝 Markdown
5. Cliquez "Ajouter une zone"

**Étape 3 - Configurer les données** :

Sidebar - Section "Gestion des données graphiques" :
1. Sélectionnez la ligne à modifier
2. Sélectionnez la zone graphique à modifier
3. Choisissez les colonnes à afficher (multiselect)
4. Sélectionnez l'axe des abscisses

---

## 💾 Sauvegarde et téléchargement

**Localisation** : Sidebar - Bouton "Télécharger une sauvegarde"

**Contient** :
- ✅ Structure complète des graphiques (lignes + zones)
- ✅ Paramètres d'affichage (titres visibles/masqués)
- ✅ Données actuelles du tableau
- ✅ Types de graphiques et leurs configurations

**Format** : Fichier JSON réimportable

---

## ✨ Résumé des améliorations

### ✅ Fonctionnalités principales

| Fonctionnalité | Statut | Support |
|---|---|---|
| Ajouter une ligne | ✅ | Tous types de données |
| Modifier un élément | ✅ | Tous types de données |
| Supprimer une ligne | ✅ | Tous types de données |
| Afficher des lignes | ✅ | Plage ou sélection |
| Import CSV | ✅ | Avec persistance JSON |
| Import/Export JSON | ✅ | Structure complète |
| Graphiques | ✅ | 4 types disponibles |
| Statistiques | ✅ | 5 fonctions disponibles |

### 🔒 Persistance des données

**Le système de persistance est maintenant ROBUSTE et FIABLE** :

✅ **Tous les types de données supportés** : Texte, nombres, dates, etc.  
✅ **Modifications persisten** après rerun, changement de page, et fermeture du navigateur  
✅ **Sauvegarde automatique** en JSON à chaque opération  
✅ **Chargement automatique** depuis le JSON au démarrage  
✅ **Aucune perte de données** lors d'interactions avec les widgets  
✅ **Importation CSV sécurisée** - empêche la re-exécution et perte de données  

### 🏗️ Architecture interne

```
Import CSV → JSON Backup → Session State → Affichage UI
    ↓          ↓              ↓
load_data  _save_to_      Bidirectional
           session_state    Sync
```

**Mécanismes de sécurité** :
- Compteurs dynamiques pour réinitialiser les widgets
- File_uploader tracking pour empêcher la re-exécution
- Bidirectional sync `self` ↔ `st.session_state`
- `.copy()` pour forcer Streamlit à reconnaître les changements

---

## 🐛 Résolution des problèmes

### Les données disparaissent après interaction

✅ **Résolu** - Le système charge automatiquement les données depuis le backup JSON avant chaque rendu

### Les modifications ne s'affichent pas

✅ **Résolu** - Chaque modification force un `.copy()` du DataFrame et sauvegarde en JSON

### Les widgets conservent les anciennes valeurs

✅ **Résolu** - Les compteurs dynamiques (`add_row_counter`, `edit_row_counter`, `delete_row_counter`) réinitialisent les widgets

### Le fichier CSV est rechargé à chaque rerun

✅ **Résolu** - File_uploader tracking (`file_key`) empêche la re-exécution du chargement

---

## 📚 Exemple complet de workflow

```
1. Lancer le dashboard
   → streamlit run main.py

2. Importer un CSV (525 lignes)
   → ✅ Affiche "CSV importé: 525 lignes, 3 colonnes"

3. Ajouter une ligne
   → Saisir les valeurs → Cliquer "➕ Ajouter la ligne"
   → ✅ Affiche 526 lignes dans le tableau

4. Modifier la nouvelle ligne
   → Sélectionner ligne 525, colonne "Ventes"
   → Entrer nouvelle valeur → Cliquer "✏️ Modifier cet élément"
   → ✅ Valeur modifiée immédiatement

5. Supprimer une ligne ancienne
   → Sélectionner ligne 100 → Cliquer "🗑️ Supprimer cette ligne"
   → ✅ Affiche 525 lignes (une supprimée)

6. Changer de page "Graphiques"
   → ✅ Les 525 lignes restent dans le tableau

7. Revenir à "Données"
   → ✅ Les 525 lignes sont toujours là, modifications conservées

8. Télécharger la sauvegarde
   → Cliquer "Télécharger une sauvegarde"
   → Fichier JSON contient tout : données + graphiques

9. Fermer et réouvrir le navigateur
   → Les données ne disparaissent pas (sauvegarde JSON persistante)
```

---

## 🎨 Personnalisation

### Modifier les couleurs/styles

Les styles sont gérés par Streamlit. Consultez la documentation officielle : https://docs.streamlit.io/library/get-started/create-an-app

### Ajouter de nouveaux types de graphiques

Modifiez la classe `Area` dans `page_graphique_V3.py` et ajoutez les types dans `get_types()`

### Ajouter de nouvelles statistiques

Ajoutez des méthodes dans la classe `Page_donnees_v3` suivant le modèle existant (ex: `get_sum()`, `get_mean()`)

---

## 🔧 Dépendances complètes

### Installation complète recommandée

```bash
pip install -r requirements.txt
```

### Dépendances essentielles minimales

```bash
pip install streamlit==1.50.0
pip install pandas==2.3.3
pip install openpyxl==3.1.5
pip install seaborn==0.13.2
pip install matplotlib==3.10.7
```

### Vérifier que tout fonctionne

```bash
# Tester l'import des modules
python -c "import streamlit; import pandas; import seaborn; print('✅ Tous les modules importent correctement')"

# Lancer le dashboard
streamlit run main.py
```

---

## 🛠️ Structure des fichiers

### Fichiers principaux

| Fichier | Rôle | Responsabilité |
|---------|------|---|
| `main.py` | Point d'entrée | Navigation, sidebar, orchestration (version finale) |
| `page_donnees_V3.py` | Gestion données | CRUD, persistance JSON, statistiques |
| `page_graphique_V3.py` | Gestion graphiques | Classe Graphiques, Ligne, Area - Rendu |
| `systeme_sauvegarde.py` | Sauvegarde/Import | Sérialisation JSON complète |

### Fichiers de données

| Fichier | Description |
|---------|---|
| `donnees.csv` | Exemple de données (optionnel) |
| `Données_M&Ms_S3.xlsx - Feuille 1.csv` | Données M&M's de l'exemple |

---

## 📚 Documentation des classes

### `Page_donnees_v3` - Gestion des données

**Responsabilités** :
- Charger et traiter les fichiers CSV
- Modifier les données (CRUD)
- Persister en JSON pour fiabilité
- Fournir statistiques descriptives

**Méthodes principales** :

#### Chargement
```python
page_donnees = Page_donnees_v3()
page_donnees.load_data("mon_fichier.csv")  # Charge depuis chemin
page_donnees.load_data(uploaded_file)      # Charge depuis Streamlit
page_donnees.load_data_from_dict({"col1": [1,2,3]})  # Charge depuis dict
```

#### Modification
```python
# Ajouter une ligne
page_donnees.add_row({"Nom": "Alice", "Age": 25, "Ville": "Paris"})

# Modifier une cellule
page_donnees.edit_row(row_index=5, row_data={"Nom": "Bob"})

# Supprimer une ligne
page_donnees.delete_row(row_index=5)
```

#### Requêtage
```python
# Récupérer une portion du tableau
df_slice = page_donnees.get_data_slice(l1=0, l2=10, c1=0, c2=3)

# Récupérer certaines lignes
df_selected = page_donnees.get_lines([0, 2, 5, 10])

# Récupérer certaines colonnes
df_cols = page_donnees.get_columns(["Nom", "Age"])
```

#### Statistiques
```python
somme = page_donnees.get_sum("Age")           # Somme d'une colonne
moyenne = page_donnees.get_mean("Age")        # Moyenne
mediane = page_donnees.get_median("Age")      # Médiane
ecart_type = page_donnees.get_std("Age")      # Écart type
variance = page_donnees.get_variance("Age")   # Variance
```

#### Opérations personnalisées
```python
# Ajouter une colonne calculée
page_donnees.add_column_from_operation(
    column_name="Âge2024",
    operation="somme",
    column_operand="Age"
)
```

### `Graphiques` - Gestion des graphiques

**Responsabilités** :
- Organiser les graphiques en lignes
- Gérer les zones (Area) avec leurs données
- Rendu de tous les graphiques

**Méthodes principales** :

#### Gestion des lignes
```python
graphiques = st.session_state.graphiques

# Ajouter une ligne
graphiques.add_line("Ligne 1", show_name=True)

# Supprimer une ligne
graphiques.delete_line("Ligne 1")

# Récupérer les titres
titres = graphiques.get_lines_titles()  # ["Ligne 1", "Ligne 2"]
```

#### Gestion des zones
```python
# Ajouter une zone graphique
graphiques.add_area(
    line=0,                              # Index de la ligne
    area_name="Zone 1",
    type=graphiques.Area.BARCHART,      # Type : BARCHART, LINECHART, SCATTER, MARKDOWN
    data=df_données,                    # DataFrame (optionnel)
    show_name=True
)

# Supprimer une zone
graphiques.delete_area("Ligne 1", "Zone 1")

# Récupérer les zones d'une ligne
zones = graphiques.get_line_areas_names("Ligne 1")
```

#### Données et abscisse
```python
# Affecter des données à une zone
graphiques.set_datas(
    line_title="Ligne 1",
    area_name="Zone 1",
    data=df_données
)

# Définir l'axe X (abscisse)
graphiques.set_area_abscisse_column(
    line_title="Ligne 1",
    area_name="Zone 1",
    abcsisse_column_name="Date"  # Colonne à utiliser comme X
)
```

#### Rendu
```python
# Afficher tous les graphiques
graphiques.render()
```

### `Area` - Types de graphiques disponibles

**4 types de zones** :

| Type | Code | Description | Usage |
|------|------|---|---|
| Histogramme | `Area.BARCHART` | Diagramme en barres avec comptage | Comparer des valeurs discrètes |
| Graphique normal | `Area.LINECHART` | Courbe avec Streamlit | Voir des tendances |
| Nuage de points | `Area.SCATTER` | Scatter plot | Voir les corrélations |
| Markdown | `Area.MARKDOWN` | Texte formaté | Ajouter du contenu texte |

**Configuration par type** :

```python
# Histogramme : nécessite données + abscisse
area = Area("Ma zone", Area.BARCHART, data=df_data)
area.set_abscisse_column("Catégorie")

# Graphique normal : nécessite données
area = Area("Ma courbe", Area.LINECHART, data=df_data)

# Scatter : nécessite données
area = Area("Ma corrélation", Area.SCATTER, data=df_data)

# Markdown : pas de données, juste du texte
area = Area("Ma description", Area.MARKDOWN)
# Note: le contenu texte n'est pas actuellement éditable via l'UI
```

### `systeme_sauvegarde` - Import/Export

**Responsabilités** :
- Sérialiser structure complète en JSON
- Désérialiser JSON pour restauration
- Gérer les indices pour position exacte des graphiques

**Fonctions** :

```python
from systeme_sauvegarde import save, load

# Sauvegarder
json_complet = save(st.session_state.graphiques, st.session_state.donnees)
# Retourne une chaîne JSON sérialisée

# Charger
graphiques, donnees = load(
    json_complet,
    st.session_state.graphiques,  # Instance destination
    st.session_state.donnees       # Instance destination
)
```

**Format JSON sauvegardé** :

```json
{
    "Ligne 1": {
        "index": 0,
        "show_title": true,
        "Zone 1": {
            "index": 0,
            "type": 1,
            "data": [...]
        }
    },
    "data": {
        "Colonne1": [val1, val2, ...],
        "Colonne2": [val1, val2, ...]
    }
}
```

---

## ⚠️ Résolution avancée des problèmes

### Problème : "ModuleNotFoundError: No module named 'streamlit'"

**Solution** :
```bash
pip install streamlit
# Ou si en environnement virtuel
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate       # Windows
pip install streamlit
```

### Problème : CSV ne charge pas correctement

**Causes possibles** :
- ❌ Séparateur non reconnu (`,`, `;`, `\t`, `|`)
- ❌ Encodage non UTF-8
- ❌ Colonnes vides

**Solutions** :
1. **Vérifier l'encodage** :
   ```bash
   file -i mon_fichier.csv  # Linux/Mac
   ```
   Doit être UTF-8

2. **Vérifier les séparateurs** :
   ```bash
   head -1 mon_fichier.csv  # Regarder la première ligne
   ```

3. **Reconvertir le CSV** :
   ```python
   import pandas as pd
   df = pd.read_csv("mon_fichier.csv", encoding='utf-8')
   df.to_csv("mon_fichier_utf8.csv", encoding='utf-8', index=False)
   ```

### Problème : Les données disparaissent au changement de page

**Cause** : Bug résolu dans cette version ✅

**Si encore présent** :
```python
# Vérifier que la synchronisation est présente
# Dans afficher_page() : DOIT avoir
self._load_from_session_state()  # Au début
st.session_state["données"] = self  # Après load
```

### Problème : Erreur "st.rerun() not available"

**Cause** : Version ancienne de Streamlit

**Solution** :
```bash
pip install --upgrade streamlit>=1.50.0
```

### Problème : Les graphiques ne s'affichent pas

**Vérifications** :
1. Avez-vous ajouté au moins une ligne ? (Sidebar "Ajouter des zones")
2. Avez-vous ajouté au moins une zone à la ligne ? (Sidebar "Ajouter des zones")
3. Avez-vous assigné des données à la zone ? (Sidebar "Gestion des données graphiques")

**Debug** :
```python
# Afficher l'état dans la console Python
print(st.session_state.graphiques.get_lines_titles())
print(st.session_state.graphiques.get_line_areas_names("Ligne 1"))
```

### Problème : "TypeError: 'NoneType' object is not iterable"

**Cause** : Tentative d'opération sur des données None

**Solution** :
```python
if st.session_state.donnees.data is None:
    st.error("❌ Aucune donnée. Veuillez importer un CSV.")
else:
    # Faire l'opération
    pass
```

### Problème : Performances lentes avec beaucoup de données

**Optimisations** :
1. **Limiter l'affichage** : Utiliser la plage d'affichage (ex: 0-100 au lieu de 0-10000)
2. **Filtrer les colonnes** : Utiliser `get_columns()` au lieu de tout charger
3. **Réduire le CSV** : Pré-filtrer les données avant import

---

## 📞 Support et documentation

### Ressources officielles

- **Streamlit** : https://docs.streamlit.io
- **Pandas** : https://pandas.pydata.org/docs
- **Seaborn** : https://seaborn.pydata.org
- **Matplotlib** : https://matplotlib.org/stable/contents.html

### Fichiers de documentation du projet

- `LANCEMENT.md` - Instructions de démarrage
- `MODIFICATIONS_V4.md` - Historique des modifications
- `CHECKLIST_V4.md` - Vérifications complètes
- `RAPPORT_GESTION_DONNEES.md` / `.tex` - Architecture détaillée

### Commandes utiles

```bash
# Voir la version de Streamlit
pip show streamlit

# Relancer le dashboard avec cache désactivé
streamlit run main.py --logger.level=debug

# Enregistrer les logs
streamlit run main.py > dashboard.log 2>&1

# Vérifier les versions de dépendances
pip list | grep -E "streamlit|pandas|seaborn"
```

---

## ✨ Fonctionnalités avancées

### Exporter les données modifiées

```python
# Récupérer le DataFrame actuel
df_export = st.session_state.donnees.data

# Exporter en CSV
df_export.to_csv("donnees_modifiees.csv", index=False, encoding='utf-8')

# Exporter en Excel
df_export.to_excel("donnees_modifiees.xlsx", index=False)
```

### Opérations batch sur les données

```python
donnees = st.session_state.donnees

# Ajouter plusieurs lignes
for row in [{"Nom": "A", "Age": 20}, {"Nom": "B", "Age": 25}]:
    donnees.add_row(row)

# Récupérer une copie filtrée
df_filtered = donnees.data[donnees.data["Age"] > 30]
```

### Configuration de graphiques personnalisés

```python
graphiques = st.session_state.graphiques

# Créer une structure avec graphiques
graphiques.add_line("Analyse Complète", show_name=True)
graphiques.add_area(0, "Histogramme des âges", Area.BARCHART)
graphiques.add_area(0, "Évolution", Area.LINECHART)
graphiques.add_area(0, "Description", Area.MARKDOWN)

# Assigner les données
graphiques.set_datas("Analyse Complète", "Histogramme des âges", df_ages)
```

---

## 📞 Support

Le code est bien documenté avec des docstrings. Pour toute question :
- Consultez les commentaires dans les fichiers Python
- Vérifiez le fichier `probleme.md` pour la résolution des bugs connus

---

## 📄 Résumé des améliorations


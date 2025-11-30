# Projet-Dashboard

## 🎯 Vue d'ensemble

Dashboard Streamlit interactive permettant de visualiser, créer, modifier et supprimer des données directement dans l'interface, avec persistance complète et système de sauvegarde JSON.

---

# Manuel d'utilisation de la dashboard

## 📋 Prérequis

Les fichiers Python requis :
- `page_donnees_V3.py` - Gestion des données
- `page_graphique_V3.py` - Gestion des graphiques  
- `main_V3.py` - Point d'entrée principal
- `systeme_sauvegarde.py` - Sauvegarde/chargement JSON

Installation de Streamlit :
```bash
pip install streamlit pandas openpyxl
```

## 🚀 Lancement du dashboard

```bash
streamlit run main_V3.py
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
   → streamlit run main_V3.py

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

## 📞 Support

Le code est bien documenté avec des docstrings. Pour toute question :
- Consultez les commentaires dans les fichiers Python
- Vérifiez le fichier `probleme.md` pour la résolution des bugs connus

---

## 📄 Résumé des améliorations


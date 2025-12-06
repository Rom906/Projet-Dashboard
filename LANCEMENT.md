# 📊 Projet Dashboard - Version V4

## 🚀 Lancement du projet

### Commande principale (recommandée):
```bash
streamlit run main.py
```

### Accès:
```
http://localhost:8501
```

---

## 📋 Architecture V4

### Fichiers principaux:
- **`main.py`** - Point d'entrée unique (remplace main_V3.py, main_v4.py)
- **`page_donnees_V3.py`** - Gestion complète des données avec persistance JSON
- **`page_graphique_V3.py`** - Gestion des graphiques et zones
- **`systeme_sauvegarde.py`** - Import/export JSON (corrigé V3)

### Fonctionnalités:

✅ **Import CSV** - Charge les données avec détection automatique du format  
✅ **Ajouter ligne** - Avec persistance immédiate  
✅ **Modifier élément** - Changement immédiat avec rerun  
✅ **Supprimer ligne** - Suppression immédiate avec rerun  
✅ **Persistance JSON** - Recharge automatique à chaque rerun  
✅ **Graphiques dynamiques** - Création et configuration en temps réel  
✅ **Sauvegarde complète** - Export/import de la structure entière  

---

## 🔧 Corrections V4 appliquées

### 1. **Reruns corrigés**
- ✅ Ajouter ligne: rerun présent
- ✅ Modifier élément: rerun ajouté
- ✅ Supprimer ligne: rerun ajouté
- ✅ Chaque rerun recharge le JSON depuis `_load_from_session_state()`

### 2. **Imports unifiés**
- ✅ Tous les fichiers utilisent `page_graphique_V3` (pas de mélange v4/V3)
- ✅ `systeme_sauvegarde.py` corrigé: `from page_graphique_V3 import...`

### 3. **Persistance garantie**
- ✅ JSON recharge au début de `afficher_page()`
- ✅ `.copy()` après chaque modification
- ✅ `_save_to_session_state()` appelé systématiquement

---

## 📝 Workflow complet

1. **Import CSV**
   - Fichier chargé → sauvegardé en JSON session state
   - Données visibles immédiatement

2. **Ajouter ligne**
   - Saisie → Click "Ajouter" → JSON save → rerun → Champs reset

3. **Modifier élément**
   - Sélection ligne/colonne → Nouvelle valeur → Click "Modifier" → JSON save → **rerun** → Affichage immédiat

4. **Supprimer ligne**
   - Sélection ligne → Click "Supprimer" → JSON save → **rerun** → Affichage immédiat

5. **Navigation pages**
   - Changement page → JSON recharge → Données persistées

---

## 🐛 Problèmes résolus

| Problème | Solution |
|----------|----------|
| Modifications non visibles | Ajout rerun après edit/delete |
| JSON non rechargé | Recharge au début de afficher_page() |
| Imports incohérents | Tous en V3, pas de v4 |
| Widgets pas reset | Compteurs dynamiques + rerun |

---

## 📦 Dépendances

```bash
pip install streamlit pandas openpyxl seaborn matplotlib
```

Voir `requirements.txt` pour la liste complète.

---

## 🎯 Points clés à retenir

- **Toujours** utiliser `st.session_state` directement, pas de références locales
- **Toujours** appeler `.copy()` après modification de DataFrame
- **Toujours** recharger JSON au début de `afficher_page()`
- **Toujours** ajouter `st.rerun()` après modifications utilisateur

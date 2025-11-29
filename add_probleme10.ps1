$path = "c:\Users\jujup\Documents\Travaux\Projet_S3\Premier_jet\Projet Dashboard\Projet-Dashboard\probleme.md"

$addition = @"
---

## Probleme 10 : Ligne ajoutee disparait apres rerun (file_uploader re-execution)

### Description
Apres avoir ajoute une ligne et sauvegarde dans le JSON (526 lignes), les modifications disparaissaient au clic sur le widget suivant. Les seules 525 lignes du CSV d'origine restaient affichees. Les messages de succes etaient bien affiches mais les donnees perdaient la modification.

### Cause identifiee
BUG STREAMLIT : Le widget file_uploader CONSERVE SA VALEUR lors d'un rerun et re-execute son callback, ce qui recharge le CSV original (525 lignes) et ECRASE le JSON backup contenant les modifications (526 lignes).

### Solution appliquee
Generer une clé unique pour chaque fichier basée sur son nom et sa taille :
- f"loaded_file_{uploaded_file.name}_{uploaded_file.size}"
- Stocker dans st.session_state si le fichier a été chargé
- A chaque rerun, verifier AVANT de recharger
- Si deja charge : IGNORER le file_uploader
- Si nouveau fichier : CHARGER uniquement la premiere fois

### Resultat
✅ PROBLEME CRITIQUE RESOLU : Les donnees ne disparaissent plus lors d'un rerun
✅ Persistance complete a travers les interactions utilisateur
✅ Support de multiples imports sequentiels
"@

$content = Get-Content $path -Raw
$content += $addition
$content | Set-Content $path

Write-Host "Probleme 10 ajoute avec succes au fichier probleme.md"

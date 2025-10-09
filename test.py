import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(current_dir, "Donnees_M&Ms_S3.xlsx")

df = pd.read_excel(excel_path)

# Vérifier les colonnes exactes
print(df.columns.tolist())

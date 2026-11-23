import csv
with open("usuarios.csv", encoding="utf-8") as f:
    ids = [int(r["id"]) for r in csv.DictReader(f)]
faltantes = sorted(list(set(range(1, max(ids) + 1)) - set(ids)))
print("IDs faltantes:", faltantes)

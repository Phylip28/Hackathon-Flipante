import urllib.request, json, csv

url = "http://hpecds.comnetconsultores.cloud:7373/la-chocita/acceso-7k105l7a2axr5uzh/follows"
headers = {"Authorization": "Bearer mofongo"}

req = urllib.request.Request(url, headers=headers)
texto = urllib.request.urlopen(req).read().decode("utf-8")

with open("follows.csv", "w", newline="", encoding="utf-8") as f:
    if texto.strip().startswith(("{", "[")):
        data = json.loads(texto)
        data = data["data"] if isinstance(data, dict) else data
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    else:
        f.write(texto)

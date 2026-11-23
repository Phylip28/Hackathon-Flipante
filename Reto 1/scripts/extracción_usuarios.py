import urllib.request, json, csv

host = "http://hpecds.comnetconsultores.cloud:7373"
with open("usuarios.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "username"])
    for page in range(1, 82):
        url = f"{host}/api/users?page={page}&size=1000"
        data = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))["data"]
        for u in data:
            writer.writerow([u["id"], u["username"]])




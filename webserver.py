from flask import Flask

from threading import Thread

# Inicializace Flask aplikace
app = Flask('')

requests_served = 0  # Pocet vyresenych pozadavku, zacina na 0


@app.route('/')
def home():
  # Inkrementace počtu vyřešených požadavků při každém zobrazení stránky
  global requests_served
  requests_served += 1

  # Změna barvy nebo jiné vizuální zprávy, která indikuje stav bota
  status_message = "<span style='color: green;'>Bot is online</span>"

  # Zobrazení počtu vyřešených požadavků
  count_message = f"Requests served: {requests_served}"

  # Spojení statusové zprávy a počtu vyřešených požadavků
  return f"{status_message}<br>{count_message}"


# Funkce pro spuštění Flask aplikace na daném hostu a portu
def run():
  app.run(host='0.0.0.0', port=8081)


# Funkce pro spuštění Flask aplikace v novém vlákně
def keep_alive():
  t = Thread(target=run)
  t.start()  # Spuštění nového vlákna pro udržení aplikace online

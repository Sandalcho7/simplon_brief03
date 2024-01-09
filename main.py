from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# User story 1
@app.get("/revenu_fiscal_moyen/{city}")
async def revenu_fiscal_moyen(city: str):
    return f"SELECT revenu_fiscal_moyen FROM foyers_fiscaux ff WHERE ville = '{city.capitalize()}' ORDER BY date DESC LIMIT 1"


# User story 2
@app.get("/dernieres_transactions/{city}_last_{number}")
async def last_transactions(city: str, number: int):
    return f"SELECT * FROM transactions_sample ts WHERE ville = '{city.upper()}' ORDER BY date_transaction DESC LIMIT {number}"


# User story 3
@app.get("/nombre_transactions/{city}_{year}")
async def transactions_count(city: str, year: int):
    return f"SELECT COUNT(*) FROM transactions_sample ts WHERE ville LIKE '{city.upper()}%' AND date_transaction LIKE '{year}%'"


# User story 4
@app.get("/prix_moyen_m2/{year}_{type}")
async def average_price(type: str, year: int):
    return f"SELECT AVG(prix/surface_habitable) as prix_m2_moyen FROM transactions_sample ts WHERE type_batiment = '{type.capitalize()}' AND date_transaction LIKE '{year}%'"


# User story 5
@app.get("/nombre_transactions_2/{city}_{year}_{type}_{rooms}")
async def transactions_count2(city: str, type: str, year: int, rooms: int):
    return f"SELECT COUNT(*) FROM transactions_sample ts WHERE type_batiment = '{type.capitalize()}' AND n_pieces = {rooms} AND ville = '{city.upper()}' AND date_transaction LIKE '{year}%'"


# User story 6
@app.get("/repartition_pieces/{city}_{year}_{type}")
async def room_repart(city: str, year: int, type: str):
    return f"SELECT n_pieces, COUNT(*) as nb_transactions FROM transactions_sample ts WHERE type_batiment = '{type.capitalize()}' AND ville LIKE '{city.upper()}%' AND date_transaction LIKE '{year}%' GROUP BY n_pieces"


# User story 7
@app.get("/prix_moyen_m2_2/{city}_{year}_{type}")
async def average_price_2(city: str, year: int, type: str):
    return f"SELECT AVG(prix/surface_habitable) as prix_m2_moyen FROM transactions_sample ts WHERE type_batiment = '{type.capitalize()}' AND ville LIKE '{city.upper()}' AND date_transaction LIKE '{year}%'"
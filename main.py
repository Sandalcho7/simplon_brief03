# Imports
from fastapi import FastAPI, HTTPException
import sqlite3



# Déclaration des variables
con = sqlite3.connect("Chinook.db")

app = FastAPI()



# Déclaration des fonctions
def validate_year(year: str):
    if not year.isdigit() or not (len(year) == 4) :
        raise HTTPException(status_code=400, detail="Year input invalid, must be a 4 figures long number.")
    return year

def execute_sql(con, query):
    cur = con.cursor()
    res = cur.execute(query)
    result = res.fetchall()
    if not result:
        raise HTTPException(status_code=400, detail="Can't find any result")
    return result



# Root
@app.get("/")
async def root():
    return {"message": "Hello World"}


# User story 1
@app.get("/revenu_fiscal_moyen/{city}")
async def revenu_fiscal_moyen(city: str):
    query = f"SELECT revenu_fiscal_moyen FROM foyers_fiscaux ff WHERE ville = '{city.capitalize()}' ORDER BY date DESC LIMIT 1"
    return execute_sql(con, query)


# User story 2
@app.get("/dernieres_transactions/{city}_last_{number}")
async def last_transactions(city: str, number: int):
    query = f"SELECT * FROM transactions_sample ts WHERE ville = '{city.upper()}' ORDER BY date_transaction DESC LIMIT {number}"
    return execute_sql(con, query)


# User story 3
@app.get("/nombre_transactions/{city}_{year}")
async def transactions_count(city: str, year: str):
    year = validate_year(year)
    query = f"SELECT COUNT(*) FROM transactions_sample ts WHERE ville LIKE '{city.upper()}%' AND date_transaction LIKE '{year}%'"
    return execute_sql(con, query)
        

# User story 4
@app.get("/prix_moyen_m2/{year}_{type}")
async def average_price(type: str, year: str):
    year = validate_year(year)
    query = f"SELECT AVG(prix/surface_habitable) as prix_m2_moyen FROM transactions_sample ts WHERE type_batiment = '{type.capitalize()}' AND date_transaction LIKE '{year}%'"
    return execute_sql(con, query)


# User story 5
@app.get("/nombre_transactions_2/{city}_{year}_{type}_{rooms}")
async def transactions_count2(city: str, type: str, year: str, rooms: int):
    year = validate_year(year)
    query = f"SELECT COUNT(*) FROM transactions_sample ts WHERE type_batiment = '{type.capitalize()}' AND n_pieces = {rooms} AND ville = '{city.upper()}' AND date_transaction LIKE '{year}%'"
    return execute_sql(con, query)


# User story 6
@app.get("/repartition_pieces/{city}_{year}_{type}")
async def room_repart(city: str, year: str, type: str):
    year = validate_year(year)
    query = f"SELECT n_pieces, COUNT(*) as nb_transactions FROM transactions_sample ts WHERE type_batiment = '{type.capitalize()}' AND ville LIKE '{city.upper()}%' AND date_transaction LIKE '{year}%' GROUP BY n_pieces"
    return execute_sql(con, query)


# User story 7
@app.get("/prix_moyen_m2_2/{city}_{year}_{type}")
async def average_price_2(city: str, year: str, type: str):
    year = validate_year(year)
    query = f"SELECT AVG(prix/surface_habitable) as prix_m2_moyen FROM transactions_sample ts WHERE type_batiment = '{type.capitalize()}' AND ville LIKE '{city.upper()}' AND date_transaction LIKE '{year}%'"
    return execute_sql(con, query)


# User story 8
@app.get("/departement_transactions/")
async def dep_transactions():
    query = f"SELECT departement, COUNT(*) as nb_transactions FROM transactions_sample ts GROUP BY departement ORDER BY nb_transactions DESC"
    return execute_sql(con, query)


# User story 9
@app.get("/nombre_transactions_3/{year1}_{revenu}_{year2}_{type}")
async def transactions_count3(year1: str, year2: str, revenu: int, type: str):
    query = f"SELECT COUNT(*) as nb_transactions FROM transactions_sample ts JOIN foyers_fiscaux ff ON ts.ville = UPPER(ff.ville) WHERE ff.date LIKE '{year1}%' AND ff.revenu_fiscal_moyen > {revenu} AND ts.date_transaction LIKE '{year2}%' AND type_batiment = '{type}'"
    return execute_sql(con, query)
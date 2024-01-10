# Imports
from fastapi import FastAPI, HTTPException, Path
import sqlite3



# Déclaration des variables
con = sqlite3.connect("immo_fr.db")

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
    columns = [column[0] for column in cur.description]
    result_with_columns = [dict(zip(columns, row)) for row in result]
    if not result:
        raise HTTPException(status_code=400, detail="Can't find any result")
    return result_with_columns



# Root
@app.get("/")
async def root():
    return {"message": "Hello World"}


# User story 1
@app.get("/revenu_fiscal_moyen/{city}", description="Renvoie le revenu fiscal moyen de l'année la plus récente pour une ville donnée")
async def revenu_fiscal_moyen(city: str = Path(description="Ville")):
    query = f"SELECT revenu_fiscal_moyen FROM foyers_fiscaux ff WHERE ville = '{city.capitalize()}' ORDER BY date DESC LIMIT 1"
    return execute_sql(con, query)


# User story 2
@app.get("/dernieres_transactions/{city}_last_{number}", description="Renvoie le nombre choisi de dernières transactions pour une ville donnée")
async def last_transactions(city: str = Path(description="Ville"),
                            number: int = Path(description="Nombre de transactions à afficher")):
    query = f"SELECT * FROM transactions_sample ts WHERE ville LIKE '{city.upper()}%' ORDER BY date_transaction DESC LIMIT {number}"
    return execute_sql(con, query)


# User story 3
@app.get("/nombre_transactions/{city}_{year}", description="Renvoie le nombre de transactions pour une ville et une année donnés")
async def transactions_count(city: str = Path(description="Ville"),
                             year: str = Path(description="Année")):
    year = validate_year(year)
    query = f"SELECT COUNT(*) as nb_transactions FROM transactions_sample ts WHERE ville LIKE '{city.upper()}%' AND date_transaction LIKE '{year}%'"
    return execute_sql(con, query)
        

# User story 4
@app.get("/prix_moyen_m2/{year}_{type}", description="Renvoie le prix moyen par m2 pour une année et un type de biens donnés")
async def average_price(type: str = Path(description="Type de biens"),
                        year: str = Path(description="Année")):
    year = validate_year(year)
    query = f"SELECT AVG(prix/surface_habitable) as prix_m2_moyen FROM transactions_sample ts WHERE type_batiment = '{type.capitalize()}' AND date_transaction LIKE '{year}%'"
    return execute_sql(con, query)


# User story 5
@app.get("/nombre_transactions_2/{city}_{year}_{type}_{rooms}", description="Renvoie le nombre de transactions pour une ville, une année, un type de biens et un nombre de pièces donnés")
async def transactions_count2(city: str = Path(description="Ville"),
                              type: str = Path(description="Type de biens"),
                              year: str = Path(description="Année"),
                              rooms: int = Path(description="Nombre de pièces")):
    year = validate_year(year)
    query = f"SELECT COUNT(*) as nb_transactions FROM transactions_sample ts WHERE type_batiment = '{type.capitalize()}' AND n_pieces = {rooms} AND ville LIKE '{city.upper()}%' AND date_transaction LIKE '{year}%'"
    return execute_sql(con, query)


# User story 6
@app.get("/repartition_pieces/{city}_{year}_{type}", description="Renvoie la répartition des transactions en fonction du nombre de pièces, pour une ville, une année et un type de biens donnés")
async def room_repart(city: str = Path(description="Ville"),
                      year: str = Path(description="Année"),
                      type: str = Path(description="Type de biens")):
    year = validate_year(year)
    query = f"SELECT n_pieces, COUNT(*) as nb_transactions FROM transactions_sample ts WHERE type_batiment = '{type.capitalize()}' AND ville LIKE '{city.upper()}%' AND date_transaction LIKE '{year}%' GROUP BY n_pieces"
    return execute_sql(con, query)


# User story 7                                                                                                                                                                                                   
@app.get("/prix_moyen_m2_2/{city}_{year}_{type}", description="Renvoie le prix moyen par m2 pour une ville, une année et un type de biens donnés")
async def average_price_2(city: str = Path(description="Ville"),
                          year: str = Path(description="Année"),
                          type: str = Path(description="Type de biens")):
    year = validate_year(year)
    query = f"SELECT AVG(prix/surface_habitable) as prix_m2_moyen FROM transactions_sample ts WHERE type_batiment = '{type.capitalize()}' AND ville LIKE '{city.upper()}%' AND date_transaction LIKE '{year}%'"
    return execute_sql(con, query)


# User story 8
@app.get("/departement_transactions/", description="Renvoie le classement des départements en fonction du nombre de transactions réalisées")
async def dep_transactions():
    query = f"SELECT departement, COUNT(*) as nb_transactions FROM transactions_sample ts GROUP BY departement ORDER BY nb_transactions DESC"
    return execute_sql(con, query)


# User story 9
@app.get("/nombre_transactions_3/{year1}_{revenu}_{year2}_{type}", description="Renvoie le nombre total de ventes d'un type de biens à une année donnée, pour les villes ayant un revenu fiscal moyen supérieur à la valeur renseignée au cours de l'année choisie")
async def transactions_count3(year1: str = Path(description="Année concernant le revenu fiscal moyen"),
                              revenu: int = Path(description="Revenu fiscal moyen minimum"),
                              year2: str = Path(description="Année concernant le nombre de ventes"),
                              type: str = Path(description="Type de biens")):
    query = f"SELECT COUNT(*) as nb_transactions FROM transactions_sample ts JOIN foyers_fiscaux ff ON ts.ville = UPPER(ff.ville) WHERE ff.date LIKE '{year1}%' AND ff.revenu_fiscal_moyen > {revenu} AND ts.date_transaction LIKE '{year2}%' AND type_batiment = '{type}'"
    return execute_sql(con, query)


# User story 10
@app.get("/cities_top10_transactions/", description="Renvoie les 10 villes avec le plus de transactions immobilières recensées")
async def cities_top10():
    query = f"SELECT ville, COUNT(*) as nb_transactions FROM transactions_sample ts GROUP BY ville ORDER BY COUNT(*) DESC LIMIT 10"
    return execute_sql(con, query)


# User story 11 & 12
@app.get("/cities_top10_price/{type}", description="Renvoie les 10 villes avec le prix moyen au m2 le plus attractif pour un type de biens donné")
async def cities_top10_price(type: str = Path(description="Type de biens")):
    query = f"SELECT ville, AVG(prix/surface_habitable) as prix_m2_moyen FROM transactions_sample ts WHERE type_batiment = '{type.capitalize()}' GROUP BY ville ORDER BY prix_m2_moyen ASC LIMIT 10"
    return execute_sql(con, query)
# Stap 2: Opslaan in MySQL

#Testen van verbinding met SQL

from sqlalchemy import create_engine, text
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

# Verbinding maken met MySQL
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Verbinding testen
with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print("Verbinding succesvol!")

########################################################################################################################

# Normalisatie 1: DIM_countries tabel aanmaken

from data_loader import Dataloader
# Laad de merged df
df = Dataloader().load_merged()

# Extraheer unieke landen
dim_countries = df[["entity","code","region"]].drop_duplicates().reset_index(drop=True) # Reset_index --> na verwijderen duplicates hebben de rijen nog steeds de originele index --> reset = nieuwe nummering / drop=True geen extra kolom met de oude waarden

# Voeg record_id toe als PK
dim_countries.insert(0,"cid", dim_countries.index + 1) # positie, benaming, waarden (index+1)

print(dim_countries.shape) # 186 landen ipv de geschatte 200 volgens dataexploratie --> er zijn meer aggregate rijen weggevallen
print(dim_countries.head(10))

########################################################################################################################

# Normalisatie 2: FACT_yearly tabel aanmaken

# Eerst de DIM-tabel samenvoegen aan de merged df
fact_yearly = df.merge(dim_countries[["entity", "cid"]], on="entity")

# Nu zijn er dubbelen kolommen, verwijderen van kolommen die al in de DIM-tabel zitten - enkel FK overhouden
fact_yearly = fact_yearly.drop(columns=["entity","code","region"])

# Voeg record_id toe als PK
fact_yearly.insert(0,"rid", fact_yearly.index + 1) # positie, benaming, waarden (index+1)

# Herordenen van de tabel om cid naast rid te plaatsen
fact_yearly = fact_yearly[[
    'rid', 'cid', 'year', 'lfpr_female', 'female_male_ratio',
    'male_unemploy_rate', 'female_unemploy_rate', 'gdp', 'conflict_flag']]

print(fact_yearly.columns.tolist())

print(fact_yearly.shape)
print(fact_yearly.columns.tolist())
print(fact_yearly.head(10))

########################################################################################################################

# Tabellen opslaan in MySQL

dim_countries.to_sql("dim_countries", engine, if_exists="replace", index = False)
print(f"DIM_countries opgeslagen: {len(dim_countries)} rijen")

fact_yearly.to_sql("fact_yearly", engine, if_exists="replace", index = False)
print(f"FACT_yearly opgeslagen: {len(fact_yearly)} rijen")
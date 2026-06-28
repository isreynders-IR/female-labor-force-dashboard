import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text

class Dataloader:

    # Stap 1: Binnenhalen en klaarmaken csv's
    def __init__(self, csv_map="csv"): # csv_map="csv" --> aanpasbaar voor wanneer de info in de toekomst verplaatst wordt
        self.csv_map = csv_map #v ariabele - self = eigenschap object. Elke methode kan er daarna aan via self.csv_map
        self._df = None  # interne cache: wordt gevuld na load_merged()

    def __repr__(self):
        status = "geladen" if self._df is not None else "nog niet geladen"
        return f"Dataloader(csv_map='{self.csv_map}', data={status})"

    def load_ds2(self):
        df2 = pd.read_csv(f"{self.csv_map}/ratio-of-female-to-male-labor-force-participation-rates-ilo-wdi.csv")
        df2 = df2.rename(columns={
            "Entity": "entity",
            "Code": "code",
            "Year": "year",
            "Ratio of female to male labor force participation rate": "female_male_ratio",
            "World region according to OWID": "region"
        })
        return df2

    def load_ds3(self):
        df3 = pd.read_csv(f"{self.csv_map}/unemployment-rate-of-males-vs-females.csv")
        df3 = df3.rename(columns={
            "Entity": "entity",
            "Code": "code",
            "Year": "year",
            "Male unemployment rate": "male_unemploy_rate",
            "Female unemployment rate": "female_unemploy_rate",
            "World region according to OWID": "region"
        })
        return df3

    def load_ds4(self):
        df4 = pd.read_csv(f"{self.csv_map}/female-labor-force-participation-rates-by-national-per-capita-income.csv")
        df4 = df4.rename(columns={
            "Entity": "entity",
            "Code": "code",
            "Year": "year",
            "Female labor force participation rate": "lfpr_female",
            "GDP per capita": "gdp",
            "World region according to OWID": "region"
        })
        return df4

    def load_merged(self): # Dit is de enige die app.py aanroept via Dataloader().load_merged()

        # Laden van de datasets + kolommen verwijderen
        df2 = self.load_ds2().drop(columns=["region"]) # ds4 heeft al region
        df3 = self.load_ds3().drop(columns=["region"]) # idem
        df4 = self.load_ds4()

        # Samenvoegen: dataset 4 (lfpr_female + gdp + region) als basis
        df = df4.merge(df2, on=["entity", "code", "year"], how="left") # left join
        df = df.merge(df3, on=["entity", "code", "year"], how="left") # left join

        # Aggregate rijen verwijderen (geen regio = geen echt land)
        df = df[df["region"].notna()] # df["region"].notna() geeft true of false terug en is eigenlijk een filter, dit pas je toe op de df en behoudt enkel de rijen met true

        # Territory rijen verwijderen (geen lfpr = geen data)
        df = df[df["lfpr_female"].notna()]

        # Conflictlanden markeren - zelf gekozen omdat verschillende jaartallen ontbreken
        conflict_landen = ["Ukraine", "Sudan", "South Sudan", "Palestine", "Lebanon"]
        df["conflict_flag"] = df["entity"].isin(conflict_landen) # voeg een kolom toe = wanneer kolom "entity" voorkomt in de conflictlanden

        return df

    def summary(self): # Snelle samenvatting wat in de dataset staat)

        # Controleren of de data nog niet geladen is = laden via self.load_merged()
        if self._df is None:
            self._df = self.load_merged()

        df = self._df
        print("=== Dataloader samenvatting ===")
        print(f"Landen:       {df['entity'].nunique()}")
        print(f"Regio's:      {df['region'].nunique()}")
        print(f"Periode:      {df['year'].min()} – {df['year'].max()}")
        print(f"Rijen:        {len(df):,}")
        print(f"Kolommen:     {list(df.columns)}")
        print(f"Conflictland: {df[df['conflict_flag']]['entity'].unique().tolist()}")

########################################################################################################################

    # Stap 2: database.py (merged df inladen naar MySQL)

########################################################################################################################


    # Stap 3: Terug naar Python voor analyse
    def load_from_db(self):

        # Data terug inladen vanuit de database
        from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

        engine = create_engine(
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

        query = text("""
            SELECT
                c.entity,
                c.code,
                c.region,
                f.year,
                f.lfpr_female,
                f.gdp,
                f.female_male_ratio,
                f.male_unemploy_rate,
                f.female_unemploy_rate,
                f.conflict_flag
            FROM fact_yearly f
            JOIN dim_countries c ON f.cid = c.cid
        """)

        with engine.connect() as connection:
            df = pd.read_sql(query, connection)

        # issue: conflict_flag komt als een ander format terug uit MySQL, dit moet terug gezet worden naar een boolean
        df["conflict_flag"] = df["conflict_flag"].astype(bool)

        return df
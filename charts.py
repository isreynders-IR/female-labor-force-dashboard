import pandas as pd

########################################################################################################################
# SUBTAB B: TIJD & REGIO
########################################################################################################################

# Analyse 1: Wereldwijd gemiddelde LFPR per jaar
# Gebruik: globale lijngrafiek (ook homepage)
def analyse_trend_wereldwijd(df):
    trend = (
        df.groupby("year")["lfpr_female"] # waardes lfpr_femals, groeperen op jaar
        .mean() # gemiddelde van waardes
        .reset_index()
        .rename(columns={"lfpr_female": "lfpr_female_avg"})
    )
    return trend



# Analyse 2: Gemiddelde LFPR per regio, per jaar
# Gebruik: heatmap + tabel eronder
def analyse_regio_jaar(df):
    pivot = df.pivot_table(
        index="region",
        columns="year",
        values="lfpr_female",
        aggfunc="mean"
    )
    return pivot


# MODUS 1
#*********

# Analyse 3: Top 10 hoogste + laagste LFPR gekozen jaar
def analyse_top_bottom_landen(df, year, n=10): # vb. ook mogelijk om vast te bepalen: (df, 2005, n=5)
    subset = df[df["year"] == year][["entity", "region", "lfpr_female"]].dropna() # filtering gekozen jaar, behoud enkel 3 kolommen
    top = subset.sort_values("lfpr_female", ascending=False).head(n).reset_index(drop=True) # sorteert van hoog naar laag, head(n) --> 10 zoals aangegeven hierboven
    bottom = subset.sort_values("lfpr_female", ascending=True).head(n).reset_index(drop=True) # sorteert van laag naar hoog, head(n) --> 10 zoals aangegeven hierboven
    return {"top": top, "bottom": bottom} # een dictionary met 2 aparte dataframes in return


# Analyse 4: LFPR per land, gekozen jaar.
# BASIS CHOROPLETH MAP
def analyse_geografisch_overzicht(df, year):
    subset = df[df["year"] == year][["entity", "code", "region", "lfpr_female"]].dropna() # filtering op gekozen jaar, behoudt enkel 3 kolommen // code nodig omdat dit ISO is en Plotly deze gebruikt
    return subset.reset_index(drop=True) #reset van de index en drop=True om de originele waardes niet in een extra kolom te verkrijgen



# MODUS 2
#*********

# Analyse 5: LFPR gekozen land, alle jaren, incl wereldgemiddelde
def analyse_trend_land(df, country):
    land_df = (df[df["entity"] == country][["year", "lfpr_female"]]
        .sort_values("year")
        .reset_index(drop=True)
    )

    wereld_df = analyse_trend_wereldwijd(df)

    resultaat = land_df.merge(wereld_df, on="year", how="left")
    return resultaat



########################################################################################################################
# SUBTAB A: WELVAART & GELIJKHEID
########################################################################################################################

# MODUS 1
#*********


# Analyse 6: LFPR tov GDP per capita, gekozen jaar
def analyse_gdp_vs_participation(df, year):
    subset = df[df["year"] == year][["entity", "region", "gdp", "lfpr_female"]] # Behouden van 4 kolommen
    subset = subset.dropna(subset=["gdp", "lfpr_female"]) # MAAR de rijen waar gdp OF lfpr_female ontbreken worden gewist // !! wanneer enkel dropna gebruikt wordt zou elke rij met ook maar één ontbrekende waarde in welke kolom dan ook verwijderd worden = te streng
    return subset.reset_index(drop=True)


# Analyse 7: F/M ratio tov GDP per capita, gekozen jaar
# Meet gendergelijkheid
def analyse_gdp_vs_ratio(df, year):
    subset = df[df["year"] == year][["entity", "region", "gdp", "female_male_ratio"]]
    subset = subset.dropna(subset=["gdp", "female_male_ratio"]) # rijen zonder waarde gdp of female ratio worden gewist - deze 2 waarden zijn nodig voor de scatter
    return subset.reset_index(drop=True)



# MODUS 2
#*********


# # Analyse 8: Evolutie GDP per capita en LFPR gekozen land, alle jaren
def analyse_trend_land_gdp(df, country):
    resultaat = (
        df[df["entity"] == country][["year", "lfpr_female", "gdp"]]
        .dropna(subset=["gdp"]) # rijen zonder waarde gdp worden gewist
        .sort_values("year") # sorteren op jaar
        .reset_index(drop=True)
    )
    return resultaat



########################################################################################################################
# SUBTAB C: WERKLOOSHEIDSKLOOF
########################################################################################################################

# MODUS 1
#*********

# Analyse 9: Verschil M/F werkloosheidsgraad, gemiddeld per regio, gekozen jaar
# gap > 0 = F hogere werkloosheidsgraad dan M
def analyse_werkloosheid_regio(df, year):
    subset = df[df["year"] == year] # filteren op gekozen jaar
    groep = (
        subset.groupby("region")[["male_unemploy_rate", "female_unemploy_rate"]] # subset waardes Mrate en Frate groeperen per regio
        .mean()
        .reset_index()
    )
    groep["gap"] = groep["female_unemploy_rate"] - groep["male_unemploy_rate"] # extra kolom toegevoegd "gap"
    return groep


# MODUS 2
#*********

# Analyse 10: Evolutie werkloosheids graad M/F gekozen land, alle jaren
def analyse_trend_land_werkloosheid(df, country):
    resultaat = (
        df[df["entity"] == country][["year", "male_unemploy_rate", "female_unemploy_rate"]]
        .dropna(subset=["male_unemploy_rate", "female_unemploy_rate"]) # alle rijen zonder waarden in deze 2 kolommen worden gewist
        .sort_values("year") # sorteren op jaar
        .reset_index(drop=True)
    )
    return resultaat


# Analyse 11: Evolutie M/F werkloosheidsgraad, per regio, doorheen jaren
def analyse_werkloosheid_jaren(df):
    temp = df.copy()
    temp["gap"] = temp["female_unemploy_rate"] - temp["male_unemploy_rate"]

    pivot = temp.pivot_table(
        index="region",
        columns="year",
        values="gap",
        aggfunc="mean"
    )
    return pivot







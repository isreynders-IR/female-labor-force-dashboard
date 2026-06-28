import pandas as pd
import plotly.express as px # snelle versie van Plotly - 1 functie aanroep volledige grafiek maken

BG = "#1A1D24"
CARD_BG = "#252932"
TEXT_LIGHT = "#E2E8F0"
GRID_COLOR = "#2D333F"

BLUE = "#3A86FF"      # vrouwen / hoofdaccent
SAND = "#94A3B8"      # mannen
EMERALD = "#70E000"   # top 10 hoogste
ROSE = "#FF006E"      # top 10 laagste

# Gebruik dictionaries zodat Plotly weet welke kleur bij welke categorie hoort
GENDER_COLORS = {
    "female": BLUE,
    "male": SAND,
}

REGION_COLORS = {
    "Africa":        "#70E000",
    "Asia":          "#FFBE0B",
    "Europe":        "#9B5DE5",
    "North America": "#00F5D4",
    "Oceania":       "#FF7A00",
    "South America": "#FF006E",
}

BLUE_SCALE = ["#D2E4FF", "#85B6FF", "#3A86FF", "#0056D2", "#002A7F"]


# Opgezet om binnen charts.py te gebruiken, niet rechtstreeks op te roepen in app.py
def _apply_dark_layout(fig):
    fig.update_layout(
        paper_bgcolor=BG, # achtgrond buiten grafiek
        plot_bgcolor=CARD_BG, # achtergrond binnen grafiek zelf (assen)
        font_color=TEXT_LIGHT,
        title_font_color=BLUE,
        legend_font_color=TEXT_LIGHT,
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR) # rasterkleuren x-as
    fig.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR) # rasterkleuren y-as
    fig.update_layout(showlegend=True, legend=dict(orientation="v",yanchor="top",y=1,xanchor="left",x=1.02))  # verticaal georineteerd, x=1.02 net buiten de rechterrand
    return fig


########################################################################################################################
# SUBTAB B: TIJD & REGIO
########################################################################################################################

# Grafiek 1: Globale trendlijn - lijngrafiek
def grafiek_trend_wereldwijd_lijn(trend_df):
    fig = px.line(
        trend_df, x="year", y="lfpr_female_avg", markers=True, # toont een punt op elke datapositie
        labels={"year": "Jaar", "lfpr_female_avg": "Gemiddelde LFPR (%)"}, #hernoemen naar leesbare aslabels
        title="Wereldwijde evolutie van de female labor force participation rate (1990–2025)",
        color_discrete_sequence=[BLUE] # BLUE staat als list [] want Plotly verwacht een reeks
    )
    fig.update_layout(yaxis_range=[0, 100]) # standaard instellen van 0 tem 100 - anders zoomt deze in op de data
    return _apply_dark_layout(fig)


# Grafiek 2: Evolutie regio per jaar - heatmap
def grafiek_regio_jaar_heatmap(pivot_df):
    fig = px.imshow( # heatmap verwacht pivot table als invoer
        pivot_df, labels=dict(x="Jaar", y="Regio", color="LFPR (%)"),
        aspect="auto", color_continuous_scale=BLUE_SCALE, #aspect=auto --> Plotly bepaalt zelf de verhoudingen
        title="Female labor force participation rate per regio en jaar"
    )
    return _apply_dark_layout(fig)


# MODUS 1
#*********

# Grafiek 3: Top 10 hoogste + laagste LFPR gekozen jaar - barchart
def grafiek_top_bottom_landen_bar(top_bottom_dict, year):
    top = top_bottom_dict["top"].copy() #.copy maken om originele data niet aan te passen
    bottom = top_bottom_dict["bottom"].copy()
    top["categorie"] = "Top 10 hoogste" # nieuwe kolom toevoegen --> Plotly moet weten welke kleur aan welke categorie
    bottom["categorie"] = "Top 10 laagste"
    gecombineerd = pd.concat([top, bottom]) # één dataframe van gemaakt

    fig = px.bar(
        gecombineerd.sort_values("lfpr_female"), x="lfpr_female", y="entity", #sorteren op F, x waarde, y land
        color="categorie", orientation="h", # kleuren gebaseerd op categorie, horizontale staafdiagram
        labels={"lfpr_female": "LFPR (%)", "entity": "Land", "categorie": ""}, # herbenaming naar leesbare labels
        title=f"Top 10 hoogste en laagste landen ({year})",
        color_discrete_map={"Top 10 hoogste": EMERALD, "Top 10 laagste": ROSE}
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"}) # landen worden ook visueel van laag naar hoog gesorteerd.
    return _apply_dark_layout(fig)


# Grafiek 4: LFPR per land, gekozen jaar. - Choropleth
def grafiek_geografisch_overzicht_choropleth(geo_df, year):
    fig = px.choropleth(
        geo_df, locations="code", color="lfpr_female", hover_name="entity", # location = code --> ISO
        color_continuous_scale=BLUE_SCALE, range_color=[0, 100],
        labels={"lfpr_female": "LFPR (%)"},
        title=f"Wereldkaart: female labor force participation rate per land ({year})"
    )
    fig.update_geos(bgcolor=BG, landcolor="#E2E8F0", showframe=False) # bgcolor = achtergrondkleur, kader wordt niet weergegeven
    return _apply_dark_layout(fig)

# MODUS 2
#*********

# Grafiek 5: LFPR gekozen land, alle jaren, incl wereldgemiddelde - lijngrafiek
def grafiek_trend_land_lijn(country_df, country):
    fig = px.line(
        country_df,
        x="year",
        y=["lfpr_female", "lfpr_female_avg"], # lijst van 2 kolommen y-as - automatisch 2 lijnen
        markers=True, # op elke datawaarde een bolletje
        labels={
            "year": "Jaar",
            "value": "LFPR (%)",
            "variable": ""
        },
        title=f"Evolutie van de female labor force participation rate: {country}",
        color_discrete_map={
            "lfpr_female": BLUE,
            "lfpr_female_avg": "#64748B"
        }
    )

    # Leesbare legendanamen in plaats van de kolomnamen
    fig.for_each_trace(lambda t: t.update(
        name=country if t.name == "lfpr_female" else "Wereldgemiddelde"
    )) # naam van trace "lfpr_femal" is, hernoem deze label naar de landnaam, anders hernoem naar "wereldgemiddelde"

    fig.update_layout(yaxis_range=[0, 100])
    return _apply_dark_layout(fig)


########################################################################################################################
# SUBTAB A: WELVAART & GELIJKHEID
########################################################################################################################

# MODUS 1
#*********


# Grafiek 6: LFPR tov GDP per capita, gekozen jaar - scatter
def grafiek_gdp_vs_participation_scatter(gdp_df, year):
    fig = px.scatter(
        gdp_df, x="gdp", y="lfpr_female", color="region", hover_name="entity", # region krijgt een kleur
        labels={"gdp": "GDP per capita ($)", "lfpr_female": "LFPR (%)", "region": "Regio"}, # hernoeming van de labels
        title=f"GDP per capita vs. female labor force participation rate ({year})",
        color_discrete_map=REGION_COLORS
    )
    fig.update_traces(marker=dict(size=8, opacity=0.8))
    fig.update_xaxes(type="log") # x-as op logaritmische schaal - nodig omdat de GDP waarden uiteenlopend zijn vs lineaire schaal = alle arme landen op 1 hoop
    return _apply_dark_layout(fig)


# Grafiek 7: F/M ratio tov GDP per capita, gekozen jaar - scatter
def grafiek_gdp_vs_ratio_scatter(gdp_df, year):
    fig = px.scatter(
        gdp_df, x="gdp", y="female_male_ratio", color="region", hover_name="entity", # region krijgt een kleur
        labels={"gdp": "GDP per capita ($)", "female_male_ratio": "F/M ratio", "region": "Regio"}, # hernoeming van de labels
        title=f"GDP per capita vs. female-to-male participation ratio ({year})",
        color_discrete_map=REGION_COLORS
    )
    fig.update_traces(marker=dict(size=8, opacity=0.8))
    fig.update_xaxes(type="log")
    fig.add_hline(y=100, line_dash="dash", line_color=TEXT_LIGHT, # horizontale referentielijn toe van 100 // dash = gestippeld
                   annotation_text="Volledige gelijkheid (ratio = 100)",
                   annotation_font_color=TEXT_LIGHT)
    return _apply_dark_layout(fig)


# MODUS 2
#*********

# Grafiek 8: Evolutie GDP per capita en LFPR gekozen land, alle jaren - scatter (lijn-punten grafiek)
def grafiek_trend_land_gdp_scatter(country_df, country):
    import plotly.graph_objects as go # binnen de functie geplaatst --> deze wordt enkel op deze functie uitgevoerd

    fig = go.Figure() # aanmaak lege figuur

    fig.add_trace(go.Scatter( # een lijn+punten-grafiek toevoegen
        x=country_df["gdp"],
        y=country_df["lfpr_female"],
        mode="lines+markers+text", # toont lijn, punten en tekst
        line=dict(color=BLUE, width=2),
        marker=dict(color=BLUE, size=6),
        text=country_df["year"].astype(str), #tekst die bij elk punt verschijnt is het jaartal // astype zet het getal om naar string
        textposition="top center",
        textfont=dict(size=9, color="#94A3B8"),
        name=country,
        hovertemplate=(
            "<b>%{text}</b><br>" # %{text} = jaar
            "GDP per capita: $%{x:,.0f}<br>" # %{x:,.0f} = GDP geformatteerd naar scheidingsteken
            "LFPR: %{y:.1f}%<extra></extra>" # %{y:.1f} = LFPR op 1 decimaal // extra-exra verbergt de standaar trace-naam
        )
    ))

    fig.update_layout(
        title=f"GDP per capita vs. LFPR evolutie: {country}",
        xaxis_title="GDP per capita ($)",
        yaxis_title="Female labor force participation rate (%)",
        xaxis_type="log"
    )

    return _apply_dark_layout(fig)



########################################################################################################################
# SUBTAB C: WERKLOOSHEIDSKLOOF
########################################################################################################################

# MODUS 1
#*********

# Grafiek 9: Verschil M/F werkloosheidsgraad, gemiddeld per regio, gekozen jaar - barchart
def grafiek_werkloosheid_regio_bar(gap_df, year):
    long_df = gap_df.melt( # reshape van breed naar lang // oorspronkelijk dataframe 2 aparte kolommen M & F - na MELT 1 kolom met extra kolom geslacht
        id_vars=["region", "gap"],
        value_vars=["female_unemploy_rate", "male_unemploy_rate"],
        var_name="geslacht", value_name="unemploy_rate"
    )

    long_df["geslacht"] = long_df["geslacht"].map({ # herbenoemen van de benamingen
        "male_unemploy_rate": "Mannen", "female_unemploy_rate": "Vrouwen"
    })

    fig = px.bar(
        long_df, x="unemploy_rate", y="region", color="geslacht",
        orientation="h", barmode="group", # horizontaal en gegroepeerd
        labels={"unemploy_rate": "Werkloosheidsgraad (%)", "region": "Regio", "geslacht": ""},
        title=f"Werkloosheidsgraad: vrouwen vs. mannen, per regio ({year})",
        color_discrete_map={"Vrouwen": BLUE, "Mannen": SAND},
        category_orders={"geslacht": ["Vrouwen","Mannen"]} #volgorde van de legenda
    )
    return _apply_dark_layout(fig)


# MODUS 2
#*********

# Grafiek 10: Evolutie werkloosheids graad M/F gekozen land, alle jaren - lijngrafiek
def grafiek_trend_land_werkloosheid_lijn(country_df, country):
    fig = px.line(
        country_df,
        x="year",
        y=["female_unemploy_rate", "male_unemploy_rate"],
        markers=True,
        labels={
            "year": "Jaar",
            "value": "Werkloosheidsgraad (%)",
            "variable": ""
        },
        title=f"Werkloosheidsgraad mannen vs. vrouwen: {country}",
        color_discrete_map={
            "female_unemploy_rate": BLUE,
            "male_unemploy_rate": SAND
        }
    )

    #leesbare legenda namen
    fig.for_each_trace(lambda t: t.update(
        name="Vrouwen" if t.name == "female_unemploy_rate" else "Mannen"
    )) # naam van trace "lfpr_femal" is, hernoem deze label naar de landnaam, anders hernoem naar "wereldgemiddelde"

    return _apply_dark_layout(fig)


# Grafiek 11: Evolutie M/F werkloosheidsgraad, per regio, doorheen jaren - lijngrafiek
def grafiek_werkloosheid_jaren_lijn(gap_pivot_df):
    long_df = (gap_pivot_df.reset_index() #pivot table heeft region als index, geen gewone kolom // reset_index maakt er een gewone kolom an zodat melt ermee kan werken
               .melt(id_vars="region", var_name="year", value_name="gap")) # van regio's als rijen, en jaren als kolommen NAAR één rij per regio-jaar --> px.lin vewacht 1 rij per datapunt
    fig = px.line(
        long_df, x="year", y="gap", color="region", markers=True,
        labels={"year": "Jaar", "gap": "Verschil F-M werkloosheidsgraad (pt)", "region": "Regio"},
        title="Evolutie van de werkloosheidskloof tussen vrouwen en mannen, per regio",
        color_discrete_map=REGION_COLORS
    )
    fig.add_hline(y=0, line_color=TEXT_LIGHT) # een referentielijn toegevoegd
    return _apply_dark_layout(fig)




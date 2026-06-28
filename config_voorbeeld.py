import streamlit as st
from data_loader import Dataloader
from analysis import *
from charts import *

# Allereerste streamlit aanroep
st.set_page_config(page_title="Vrouwen op de Arbeidsmarkt", layout="wide")


@st.cache_data
def get_data():
    return Dataloader().load_merged()
# load_merged() wordt bij vernieuwing (aanroeping van get_data) niet telkens meer aangeroepen omdat het al gecachet is bij de eerste uitvoering


# Variabelen die meerdere keren in de code zullen voorkomen = 1 keer berekenen = 1 keer aanroepen
df = get_data()
laatste_jaar = int(df["year"].max())
trend_df = analyse_trend_wereldwijd(df)


#Instellingen voor:
# - Metric: Metrickaartjes
# - "=tab": tablabels
# - details summary: expander titels
# - .stMarkdown p: algemene bodytekst
st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        background-color: #252932;
        border: 1px solid #2D333F;
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 1px 2px 0 rgba(0,0,0,0.2);
    }
    div[data-testid="stMetric"] label {
        color: #94A3B8 !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 0.7rem !important;
    }
    .stMarkdown p, .stMarkdown li {
    font-size: 1.15rem !important;
    line-height: 1.8 !important;
    }
    button[data-baseweb="tab"] p {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    }
    details summary p {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True # expliciet html toe laten (inclusief <style> blokken)
)


#######################################################################################################################
# TITEL
#######################################################################################################################

st.title("Vrouwen op de wereldwijde arbeidsmarkt")
st.caption("In welke mate is er sprake van gendergelijkheid op de wereldwijde arbeidsmarkt, "
           "hoe heeft deze zich ontwikkeld sinds 1990, en welke rol speelt de economische "
           "welvaart van een land hierin?")

# Tabs aanmaken
tab_home, tab_data, tab_analysis, tab_about = st.tabs(["Homepage", "Dataset", "Analyse", "About the project"])


#######################################################################################################################
# TAB 1: HOMEPAGE
#######################################################################################################################

# df = ['entity', 'code', 'year', 'lfpr_female', 'gdp', 'region', 'female_male_ratio', 'male_unemploy_rate', 'female_unemploy_rate', 'conflict_flag']

with tab_home:
    st.header("Gendergelijkheid op de arbeidsmarkt: een wereldwijd overzicht")

    col1, col2, col3 = st.columns(3) #Streamlit-functie om de pagina op te delen in 3 kolommen --> om de kaartjes te kunnen plaatsen
    waarde_laatste_jaar = trend_df[trend_df["year"] == laatste_jaar]["lfpr_female_avg"].values[0] #wanneer "year" = laatste jaar --> eerste [0] (en enige) getal uit gemiddelde
    waarde_1990 = trend_df[trend_df["year"] == 1990]["lfpr_female_avg"].values[0] #idem voor 1ste jaar

    col1.metric("Landen in dataset", df["entity"].nunique()) #nunique = telt unieke landen
    col2.metric(f"Wereldgem. LFPR ({laatste_jaar})", f"{waarde_laatste_jaar:.1f}%", #.1f = op 1 decimaal
                f"{waarde_laatste_jaar - waarde_1990:+.1f} pt vs. 1990") #+.1f = de + zorgt er voor dat er een min of plusteken staat / wordt aut. rood of groen gekleurd door Streamlit
    col3.metric("Periode", f"1990–{laatste_jaar}")

    st.write("") #lege ruimte

    st.markdown(
        """
        - **Wereldwijde stijging:** de participatie van vrouwen op de arbeidsmarkt is sinds 1990 licht gestegen, van 48.1% naar 51.4% — maar grote regionale verschillen schuilen achter dit globale gemiddelde.
        - **Grote regionale verschillen:** Europa en Afrika scoren het hoogst, Azië blijft structureel achter.
        - **Werkloosheidskloof:** in *elke* regio wereldwijd is de werkloosheidsgraad bij vrouwen hoger dan bij mannen.
        - **Welvaart is geen garantie:** een hoger GDP per capita hangt maar zwak samen met meer gendergelijkheid.
        """
    )

    st.divider() # streep


    # KERNINZICHTEN
    # ****************
    st.subheader("Drie kerninzichten")
    c1, c2 = st.columns(2)

    # Grafiek 1: Globale trendlijn
    with c1:
        st.plotly_chart(grafiek_trend_wereldwijd_lijn(trend_df),  # trend_df = variabele bovenaan de pagina
                        use_container_width=True, key="home_trend") #st.plotly_chart = gebruiken in streamlit, use_container_width = volledige lengte van kolom gebruiken, key om ervoor te zorgen dat veel gebruikte grafieken niet fout gaan

    # Grafiek 2: LFPR per land, gekozen jaar
    with c2:
        st.plotly_chart(grafiek_geografisch_overzicht_choropleth(analyse_geografisch_overzicht(df, laatste_jaar), laatste_jaar),  # analyse haalt data uit df (var boven pagina (get_data)) van het laatste jaar, grafiek maakt grafiek van deze gegevens van het laatste jaar
                        use_container_width=True, key="home_map"
                        )

    # Grafiek 3: Verschil M/F werkloosheidsgraad, gemiddeld per regio, gekozen jaar
    st.plotly_chart(
        grafiek_werkloosheid_regio_bar(analyse_werkloosheid_regio(df, laatste_jaar), laatste_jaar),
        use_container_width=True, key="home_gap"
    )


########################################################################################################################
#TAB 2: DATA
#######################################################################################################################

# df = ['entity', 'code', 'year', 'lfpr_female', 'gdp', 'region', 'female_male_ratio', 'male_unemploy_rate', 'female_unemploy_rate', 'conflict_flag']

with tab_data:

    st.header("Dataset")

    st.markdown(
        """
        Deze analyse is gebaseerd op data van de **International Labour Organization (ILO)**,
        gepubliceerd via *Our World in Data*. 
        
        De dataset combineert verschillende thema's:
        - arbeidsparticipatie van vrouwen
        - de verhouding tussen mannen en vrouwen op de arbeidsmarkt
        - werkloosheidscijfers per geslacht
        - het bruto binnenlands product per land.
        """
    )

    st.divider() # Streep


    # KOLOMBESCHRIJVING
    # *****************
    st.subheader("Kolombeschrijving")

    kolom_beschrijving = {
        "Land": "Naam van het land (bijv. Belgium, Rwanda, Japan).",
        "Code": "ISO3-landcode van drie letters (bijv. BEL, RWA, JPN). Wordt gebruikt om landen op de wereldkaart te plaatsen.",
        "Jaar": "Het jaar van de meting. De dataset loopt van 1990 tot en met 2025.",
        "LFPR Vrouwen (%)": "Female Labor Force Participation Rate (%) — het percentage vrouwen dat actief werkt of actief werk zoekt. Dit is de kernvariabele van dit onderzoek.",
        "GDP per capita ($)": "GDP per capita ($) — het bruto binnenlands product gedeeld door het aantal inwoners, in Amerikaanse dollar. Dit is een maatstaf voor de welvaart van een land. Ontbreekt voor 2025 (World Bank publiceert dit met vertraging).",
        "Regio": "Wereldregio volgens de OWID-indeling: Africa, Asia, Europe, North America, Oceania of South America.",
        "F/M Ratio": "De verhouding van de vrouwelijke participatiegraad ten opzichte van de mannelijke (%). Een waarde van 100 betekent volledige gelijkheid. Waarden onder 100 betekenen dat vrouwen minder participeren dan mannen.",
        "Werkloosheid Mannen (%)": "Werkloosheidsgraad mannen (%) — het percentage mannen dat actief werk zoekt maar geen werk heeft.",
        "Werkloosheid Vrouwen (%)": "Werkloosheidsgraad vrouwen (%) — het percentage vrouwen dat actief werk zoekt maar geen werk heeft.",
        "Conflictland": "Geeft aan of een land als conflictland is aangemerkt (True/False). De vijf conflictlanden zijn: Ukraine, Sudan, South Sudan, Palestine en Lebanon. Hun tijdreeksen breken na verloop van tijd af door ontbrekende data.",
    } #dictionary om deze in de volgende for-loop op te maken

    for kolom, beschrijving in kolom_beschrijving.items():
        st.markdown(f"- **`{kolom}`**: {beschrijving}") #**'{kolom}'** --> ' = 'codelettertype' weergegeven - ** = vetgedrukt

    st.divider()


    # CONCEPTEN & DEFINITIES
    # **********************
    st.subheader("Concepten & definities")
    st.caption("Klik op een term om de definitie te lezen.")

    with st.expander("Female Labor Force Participation Rate (LFPR)"): #st.expander(tekst) - uitklapbare blok
        st.markdown(
            """
            Het percentage vrouwen dat **actief werkt of actief werk zoekt**,
            ten opzichte van alle vrouwen van **15 jaar of ouder**.

            Dit cijfer geeft aan hoeveel vrouwen überhaupt **deelnemen aan de arbeidsmarkt**
            — van iedereen die dat theoretisch zou kunnen. De volgende groepen zijn
            **niet** inbegrepen:
            - **Studenten** die geen betaald werk hebben
            - **Gepensioneerden**
            - **Onbetaalde zorgverleners** (zoals thuisblijvende ouders)
            - **Niet-actieven** die niet actief werk zoeken

            De LFPR volgt de standaarden van de **13th International Conference of Labour
            Statisticians (ICLS)**. Onder dit framework omvat tewerkstelling het werk
            tegen betaling of winst, inclusief **zelfstandigen**, én de productie van
            goederen voor eigen gebruik — zoals **zelfvoorzienende landbouw**.
            """
        )

    with st.expander("Female-to-Male Labor Force Participation Ratio (F/M Ratio)"):
        st.markdown(
            """
            De **verhouding** tussen de participatiegraad van vrouwen en die van mannen,
            uitgedrukt als een **ratio** (geen percentage).

            - Een waarde van **100** betekent **volledige gelijkheid**: vrouwen en mannen
              participeren in gelijke mate.
            - Een waarde **onder 100** betekent dat vrouwen minder participeren dan mannen.
            - Een waarde **boven 100** betekent dat vrouwen meer participeren dan mannen
              — wat in sommige landen voorkomt.

            Het verschil met de LFPR: de LFPR zegt hoeveel vrouwen participeren in
            absolute zin, terwijl de ratio zegt hoe dat zich verhoudt tot mannen.
            Een land kan een hoge LFPR hebben terwijl mannen nóg hoger scoren —
            dan is er nog steeds ongelijkheid.
            """
        )

    with st.expander("Werkloosheidsgraad (Unemployment Rate)"):
        st.markdown(
            """
            Het percentage van de **beroepsbevolking** dat **werkloos** is —
            dus actief werk zoekt maar geen werk heeft.

            Belangrijk: dit is **niet** het percentage van de totale bevolking.
            De volgende groepen zijn **niet** inbegrepen in de noemer:
            - **Studenten** zonder betaald werk
            - **Huismannen/huisvrouwen**
            - **Niet-actieven** die niet actief werk zoeken

            Dit betekent dat de werkloosheidsgraad enkel personen meet die
            **wél willen werken maar het niet kunnen vinden** — niet iedereen
            die geen betaald werk heeft.
            """
        )

    with st.expander("GDP per capita"):
        st.markdown(
            """
            Het **bruto binnenlands product** (de totale economische output van een land)
            **gedeeld door het aantal inwoners**, uitgedrukt in Amerikaanse dollar.

            GDP per capita is een maatstaf voor de **gemiddelde welvaart** van een land:
            hoe hoger het GDP per capita, hoe welvarender het land gemiddeld is.

            **Belangrijke bemerking:** GDP per capita is een gemiddelde en zegt niets
            over de **verdeling** van welvaart binnen een land. Een hoog GDP per capita
            kan samengaan met grote ongelijkheid tussen arm en rijk.

            In dit onderzoek wordt GDP per capita gebruikt als indicator voor de
            economische ontwikkeling van een land, om te onderzoeken of rijkere landen
            meer gendergelijkheid kennen op de arbeidsmarkt.
            """
        )

    st.divider()


    # DATASAMPLE
    # ****************
    st.subheader("Datasample")
    st.caption(
        "Gebruik de filters hieronder om de dataset te verkennen. "
        "De tabel toont maximaal 30 rijen."
    ) # st.caption = kleinere, grijs gekleurde tekst

    filter_col1, filter_col2, filter_col3 = st.columns(3) # scherm opgedeel din 3 kolommen

    with filter_col1:
        regio_opties = ["Alle regio's"] + sorted(df["region"].unique().tolist()) # Extra keuze 'alle regio's" + alle unieke namen uit de kolom regio, gesorteerd en naar een lijst
        gekozen_regio = st.selectbox("Filter op regio", regio_opties) #st.selectbox = dropdownmenu, met label 'filter op regio', alle opties

    with filter_col2:
        jaren = ["Alle jaren"] + sorted(df["year"].unique().tolist()) # Extra keuze "Alle jaren" + alle unieke jaren, gesorteerd en naar lijst
        gekozen_jaar = st.selectbox("Filter op jaar", jaren)

    with filter_col3:
        conflict_filter = st.selectbox(
            "Conflictlanden",
            ["Alle landen", "Enkel conflictlanden", "Zonder conflictlanden"] # 3 vaste opties
        )

    gefilterd = df.copy() # !!! copy gemaakt om te vermijden dat de betaande dataset aangepast wordt. 6682 rijen
    if gekozen_regio != "Alle regio's":
        gefilterd = gefilterd[gefilterd["region"] == gekozen_regio] # vb. Europa = 1436 rijen --> 'gefilterd' wordt overschreven // gekozen regio var hierboven
    if gekozen_jaar != "Alle jaren":
        gefilterd = gefilterd[gefilterd["year"] == gekozen_jaar] # vb. 2025 --> op vorige gefilterd 1436 rijen --> uitkomst 39 rijen // gekozen jaar var hierboven
    if conflict_filter == "Enkel conflictlanden":
        gefilterd = gefilterd[gefilterd["conflict_flag"] == True] # Bool = ja conflictland
    elif conflict_filter == "Zonder conflictlanden":
        gefilterd = gefilterd[gefilterd["conflict_flag"] == False] # Bool = nee geen conflictland

    st.markdown(
        f"**{len(gefilterd):,} rijen** voldoen aan de gekozen filters " #laatste uitkomst van elif
        f"(toont de eerste 30)."
    )

    st.dataframe( #toont data in kolom
        gefilterd.head(30).reset_index(drop=True), #reset_index herstart nummering na filtering (drop=True) gooit de oude nummering weg ipv op te slaan als extra kolom
        use_container_width=True,
        column_config={
            "entity": st.column_config.TextColumn("Land"),
            "code": st.column_config.TextColumn("Code"),
            "year": st.column_config.NumberColumn("Jaar", format="%d"),
            "lfpr_female": st.column_config.NumberColumn("LFPR Vrouwen (%)", format="%.2f"),
            "gdp": st.column_config.NumberColumn("GDP per capita ($)", format="$%.0f"),
            "region": st.column_config.TextColumn("Regio"),
            "female_male_ratio": st.column_config.NumberColumn("F/M Ratio", format="%.2f"),
            "male_unemploy_rate": st.column_config.NumberColumn("Werkloosheid Mannen (%)", format="%.2f"),
            "female_unemploy_rate": st.column_config.NumberColumn("Werkloosheid Vrouwen (%)", format="%.2f"),
            "conflict_flag": st.column_config.CheckboxColumn("Conflictland"),
        }
    ) #st.column_config --> per kolom een andere naam geven, en indien NumberColumn formatteren naar een ander getal, decimaal)



########################################################################################################################
#TAB 3: ANALYSE
#######################################################################################################################

# df = ['entity', 'code', 'year', 'lfpr_female', 'gdp', 'region', 'female_male_ratio', 'male_unemploy_rate', 'female_unemploy_rate', 'conflict_flag']


with tab_analysis:
    st.header("Analyse")

    subtab_b, subtab_a, subtab_c = st.tabs([ # tabs aanmaken
        "Tijd & Regio",
        "Welvaart & Gelijkheid",
        "Werkloosheidskloof"
    ])

#********************************************************
    # SUBTAB B: TIJD & REGIO

    with subtab_b:
        st.subheader("Hoe is de female labor force participation rate geëvolueerd sinds 1990?")

        st.caption(
            "Deze subtab onderzoekt hoe de female labor force participation rate (LFPR) "
            "geëvolueerd is sinds 1990. De eerste twee grafieken tonen de wereldwijde trend "
            "en regionale verschillen over de volledige periode. Kies daarna een analysemodus: "
            "vergelijk landen voor een specifiek jaar, of volg de evolutie van één land over de tijd."
        )

        # Grafiek B1: Globale trendlijn
        st.plotly_chart(
            grafiek_trend_wereldwijd_lijn(trend_df),
            use_container_width=True,
            key="b_trend"
        )

        st.caption(
            "De wereldwijde gemiddelde female labor force participation rate steeg licht van **48.1%** in 1990 "
            "naar **51.4%** in 2025 — een toename van slechts 3.3 procentpunt over 35 jaar. "
            "De lijn oogt bewust vlak: achter dit globale gemiddelde schuilen grote regionale verschuivingen "
            "die pas zichtbaar worden in de heatmap hieronder."
        )

        st.divider()

        # Grafiek B2: Evolutie regio per jaar
        st.plotly_chart(
            grafiek_regio_jaar_heatmap(analyse_regio_jaar(df)),
            use_container_width=True,
            key="b_heatmap"
        )

        st.caption(
            "Hoe donkerder de kleur, hoe hoger de female labor force participation rate in die regio en dat jaar. "
            "**Afrika** scoorde in 1990 het hoogst maar daalde licht over de jaren. "
            "**Europa** steeg sterk en is in 2025 de regio met de hoogste participatiegraad. "
            "**Azië** blijft structureel het laagst scoren. "
        )

        st.caption(
            "De onderstaande draaitabel toont dezelfde data als de heatmap — gemiddelde LFPR per regio per jaar. Klik op een kolomhoofd om te sorteren.")
        st.dataframe(analyse_regio_jaar(df).round(1), # dataframe zet het in een tabel
            use_container_width=True
        )

        st.divider()

        # INSTELLEN MODUS
        # *********
        modus = st.radio(
            "Kies een analysemodus",
            ["Vergelijk landen per jaar", "Bekijk evolutie van één land"],
            horizontal=True, # toont de twee opties naast elkaar in plaats van onder elkaar
            key="b_radio"
        )

        st.write("")

        # MODUS 1
        # *********
        if modus == "Vergelijk landen per jaar": #bij elke wijziging herlaadt Streamlit de pagina en wordt deze if terug opnieuw geëvalueerd. Waarde modus bepaalt welk blok getoond wordt

            jaren_beschikbaar = sorted(df["year"].unique().tolist())[::-1] #-1 keert de lijst om
            gekozen_jaar_b = st.selectbox(
                "Kies een jaar",
                options=jaren_beschikbaar,
                key="b_selectbox"
            )

            col_b1, col_b2 = st.columns(2)


            # Grafiek B3: Top 10 hoogste + laagste LFPR gekozen jaar
            with col_b1:
                st.plotly_chart(
                    grafiek_top_bottom_landen_bar(analyse_top_bottom_landen(df, gekozen_jaar_b),gekozen_jaar_b), # grafiek(data,jaartal voor in titel)
                    use_container_width=True,
                    key="b_top10",
                    height=550
                )


            # Grafiek B4: LFPR per land, gekozen jaar
            with col_b2:
                st.plotly_chart(grafiek_geografisch_overzicht_choropleth(analyse_geografisch_overzicht(df, gekozen_jaar_b),gekozen_jaar_b),
                    use_container_width=True,
                    key="b_map",
                    height=550
                )


            st.caption("De onderstaande tabellen tonen de exacte cijfers achter de grafiek.")
            tabel_col1, tabel_col2 = st.columns(2)
            with tabel_col1:
                st.markdown("**Top 10 hoogste**")
                st.dataframe(analyse_top_bottom_landen(df, gekozen_jaar_b)["top"].reset_index(drop=True),
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "entity": st.column_config.TextColumn("Land"),
                        "region": st.column_config.TextColumn("Regio"),
                        "lfpr_female": st.column_config.NumberColumn("LFPR (%)", format="%.1f"),
                    }
                )

            with tabel_col2:
                st.markdown("**Top 10 laagste**")
                st.dataframe(analyse_top_bottom_landen(df, gekozen_jaar_b)["bottom"].reset_index(drop=True),
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "entity": st.column_config.TextColumn("Land"),
                        "region": st.column_config.TextColumn("Regio"),
                        "lfpr_female": st.column_config.NumberColumn("LFPR (%)", format="%.1f"),
                    }
                )


        # MODUS 2
        # *********
        else:

            landen = sorted(df["entity"].unique().tolist())
            gekozen_land = st.selectbox(
                "Kies een land",
                options=landen,
                index=landen.index("Belgium")  # Belgium als standaardwaarde
            )

            # Grafiek B5: LFPR gekozen land, alle jaren, incl wereldgemiddelde
            st.plotly_chart(grafiek_trend_land_lijn(analyse_trend_land(df, gekozen_land),gekozen_land),
                use_container_width=True,
                key="b_country"
            )



#********************************************************
    # SUBTAB A: WELVAART & GELIJKHEID
    with subtab_a:
        st.subheader("Hangt de welvaart van een land samen met gendergelijkheid op de arbeidsmarkt?")

        st.caption(
            "GDP-data is beschikbaar tot en met 2024 — voor 2025 publiceert de World Bank "
            "nog geen cijfers. In modus 'Vergelijk landen per jaar' toont elke punt één land: "
            "hoe verder naar rechts, hoe rijker het land; hoe hoger, hoe meer vrouwen participeren. "
            "In modus 'Bekijk evolutie van één land' is elk punt één jaar, verbonden door een lijn — "
            "zo zie je hoe het land doorheen de tijd bewoog in de GDP/LFPR-ruimte."
        )

        # INSTELLEN MODUS
        # *********
        modus_a = st.radio(
            "Kies een analysemodus",
            ["Vergelijk landen per jaar", "Bekijk evolutie van één land"],
            horizontal=True,
            key="a_radio"
        )

        st.write("")

        # MODUS 1
        # *********
        if modus_a == "Vergelijk landen per jaar":

            jaren_gdp = sorted(df[df["gdp"].notna()]["year"].unique().tolist(), # Alle unieke jaren waar GDP niet null is
                reverse=True
            )

            gekozen_jaar_a = st.selectbox(
                "Kies een jaar",
                options=jaren_gdp,
                key="a_selectbox"
            )

            # Grafiek A1: LFPR tov GDP per capita, gekozen jaar
            st.plotly_chart(grafiek_gdp_vs_participation_scatter(analyse_gdp_vs_participation(df, gekozen_jaar_a),gekozen_jaar_a),
                use_container_width=True,
                key="a_gdp_part",
                height=550
            )

            # Grafiek A2: F/M ratio tov GDP per capita, gekozen jaar
            st.plotly_chart(grafiek_gdp_vs_ratio_scatter(analyse_gdp_vs_ratio(df, gekozen_jaar_a),gekozen_jaar_a),
                use_container_width=True,
                key="a_gdp_ratio",
                height=550
            )

        # MODUS 2
        # *********
        else:

            landen_gdp = sorted(
                df[df["gdp"].notna()]["entity"].unique().tolist() # Alle unieke landen waarvan de GDP niet null is
            )
            gekozen_land_a = st.selectbox(
                "Kies een land",
                options=landen_gdp,
                index=landen_gdp.index("Belgium"), #standaard view
                key="selectbox_a_land"
            )

            # Grafiek A3: Evolutie GDP per capita en LFPR gekozen land, alle jaren
            st.plotly_chart(grafiek_trend_land_gdp_scatter(analyse_trend_land_gdp(df, gekozen_land_a),gekozen_land_a),
                use_container_width=True,
                key="a_country",
                height=900
            )


    #********************************************************
    # SUBTAB C: WERKLOOSHEIDSKLOOF
    with subtab_c:
        st.subheader("Hebben vrouwen wereldwijd een hogere werkloosheidsgraad dan mannen?")

        # INSTELLEN MODUS
        # *********
        modus_c = st.radio(
            "Kies een analysemodus",
            ["Vergelijk regio's per jaar", "Bekijk evolutie van één land"],
            horizontal=True,
            key="radio_c"
        )

        st.write("")

        # MODUS 1
        # *********
        if modus_c == "Vergelijk regio's per jaar":

            jaren_unemploy = sorted(df[df["male_unemploy_rate"].notna()]["year"].unique().tolist(),
                reverse=True
            )

            gekozen_jaar_c = st.selectbox(
                "Kies een jaar",
                options=jaren_unemploy,
                key="selectbox_c"
            )

            # Grafiek C1: Verschil M/F werkloosheidsgraad, gemiddeld per regio
            st.plotly_chart(grafiek_werkloosheid_regio_bar(analyse_werkloosheid_regio(df, gekozen_jaar_c),gekozen_jaar_c),
                use_container_width=True,
                key="c_gap_region"
            )

            st.caption("De onderstaande tabel toont de exacte werkloosheidscijfers achter de grafiek.")
            kloof_tabel = analyse_werkloosheid_regio(df, gekozen_jaar_c).copy() # kopie maken van het gefilterde resultaat om de originele gegevens te beschermen
            kloof_tabel = kloof_tabel.sort_values("female_unemploy_rate", ascending=False).reset_index(drop=True) # deze kopie gaan sorteren op values + index resetten
            kloof_tabel_display = kloof_tabel[["region", "male_unemploy_rate", "female_unemploy_rate"]].copy() # Ook een kopie maken, maar enkel 3 kolommen behouden

            tabel_breedte, _ = st.columns([1, 2]) # ik maak 2 schermindelingen, omdat 1 indeling deze op het scherm volledig wordt uitgevuld en is niet duidelijk

            with tabel_breedte:
                st.dataframe(
                    kloof_tabel_display,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "region": st.column_config.TextColumn("Regio"),
                        "male_unemploy_rate": st.column_config.NumberColumn("Mannen (%)", format="%.2f"),
                        "female_unemploy_rate": st.column_config.NumberColumn("Vrouwen (%)", format="%.2f"),
                    }
                )


        else:
            landen_unemploy = sorted(
                df[df["male_unemploy_rate"].notna()]["entity"].unique().tolist()
            )

            gekozen_land_c = st.selectbox(
                "Kies een land",
                options=landen_unemploy,
                index=landen_unemploy.index("Belgium"),
                key="selectbox_c_land"
            )

            # Grafiek C2: Evolutie werkloosheids graad M/F gekozen land, alle jaren
            st.plotly_chart(grafiek_trend_land_werkloosheid_lijn(analyse_trend_land_werkloosheid(df, gekozen_land_c),gekozen_land_c),
                use_container_width=True,
                key="c_country",
                height=600
            )


        st.divider()

        # Grafiek C3: Evolutie M/F werkloosheidsgraad, per regio, doorheen jaren (Altijd zichtbaar)
        st.plotly_chart(grafiek_werkloosheid_jaren_lijn(analyse_werkloosheid_jaren(df)),
            use_container_width=True,
            key="c_gap_time"
        )

        st.caption(
            "Deze grafiek toont het verschil tussen de werkloosheidsgraad van vrouwen en mannen "
            "per regio, doorheen de tijd. Een waarde boven 0 betekent dat vrouwen gemiddeld vaker "
            "werkloos zijn dan mannen. Merk op dat Europa tussen 2009 en 2013 tijdelijk onder 0 dook: "
            "de financiële crisis trof sectoren met veel mannelijke werknemers het hardst, waardoor "
            "mannen in die jaren gemiddeld een hogere werkloosheidsgraad hadden dan vrouwen."
        )


#######################################################################################################################
# TAB 4: ABOUT THE PROJECT
#######################################################################################################################

# df = ['entity', 'code', 'year', 'lfpr_female', 'gdp', 'region', 'female_male_ratio', 'male_unemploy_rate', 'female_unemploy_rate', 'conflict_flag']

with tab_about:
    st.header("About the project")

    # ONDERZOEKSVRAGEN
    # ****************
    st.subheader("Onderzoeksvraag")
    st.markdown(
        """
        **In welke mate is er sprake van gendergelijkheid op de wereldwijde arbeidsmarkt,
        hoe heeft deze zich ontwikkeld sinds 1990, en welke rol speelt de economische
        welvaart van een land hierin?**

        Deze hoofdvraag werd onderzocht aan de hand van drie subvragen, elk met een
        eigen analysemethode en visualisatie:
        - **Subvraag 1:** Hoe is de female labor force participation rate wereldwijd
          geëvolueerd tussen 1990 en 2025, en zijn er regio's die sterk afwijken?
        - **Subvraag 2:** Is er een verband tussen GDP per capita en gendergelijkheid
          op de arbeidsmarkt?
        - **Subvraag 3:** Is er een verschil in werkloosheidsgraad tussen mannen en
          vrouwen, en verschilt dat per regio?
        """
    )

    st.divider()


    # KERNBEVINDINGEN
    # ****************
    st.subheader("Kernbevindingen in cijfers")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(
        "Landen geanalyseerd",
        "186",
        "6 wereldregio's"
    )
    m2.metric(
        "Wereldwijde LFPR stijging",
        "+3.3 pt",
        "48.1% → 51.4% (1990–2025)"
    )
    m3.metric(
        "Correlatie GDP / LFPR",
        "0.17",
        "Zeer zwak verband"
    )
    m4.metric(
        "Grootste werkloosheidskloof",
        "2.49 pt",
        "Afrika (2023)"
    )

    st.divider()


    # CONCLUSIES
    # ****************
    st.subheader("Conclusies per subvraag")

    # Conclusie 1
    with st.container(border=True): #st.container(border=True) - is de Streamlit manier op een kader rondom de gegevens te trekken
        st.markdown("##### Subvraag 1 — Tijd & Regio")
        st.markdown(
            """
            De wereldwijde LFPR steeg **licht van 48.1% naar 51.4%** over 35 jaar —
            een toename van slechts **3.3 procentpunt**. Dit globale gemiddelde maskeert
            echter grote regionale verschuivingen:
            - **Europa** maakte de sterkste stijging: van 48.9% naar **54.9%** (+6.0 pt)
              en is daarmee in 2025 de regio met de **hoogste vrouwenparticipatie**.
            - **Zuid-Amerika** kende de **grootste inhaalbeweging** van alle regio's:
              van 44.2% naar 53.9% (+9.7 pt).
            - **Afrika** had in 1990 de hoogste participatiegraad ter wereld (54.3%),
              maar daalde licht naar 53.4% — een opmerkelijke **rolwissel met Europa**.
            - **Azië** blijft **structureel achter** met een gemiddelde van 45.0% in 2025.
            """
        )

    st.write("")

    # Conclusie 2
    with st.container(border=True):
        st.markdown("##### Subvraag 2 — Welvaart & Gelijkheid")
        st.markdown(
            """
            De correlatie tussen GDP per capita en LFPR bedraagt slechts **0.17**,
            en tussen GDP en de F/M ratio **0.18** — beide **uiterst zwak**.
            Dit betekent dat de welvaart van een land **nauwelijks verklaart** waarom
            vrouwen meer of minder participeren op de arbeidsmarkt.

            Dit is een **tegenintuïtieve bevinding**: men zou verwachten dat rijkere landen
            automatisch meer gendergelijkheid kennen. De data toont echter dat landen zoals
            **Rwanda** (laag GDP, hoge participatie) hoger scoren dan veel rijkere landen.
            De conclusie is dan ook dat **culturele, juridische en sociale factoren**
            een grotere rol spelen dan economische welvaart alleen.
            """
        )

    st.write("")

    # Conclusie 3
    with st.container(border=True):
        st.markdown("##### Subvraag 3 — Werkloosheidskloof")
        st.markdown(
            """
            In **elke regio wereldwijd** hebben vrouwen een hogere werkloosheidsgraad
            dan mannen. De kloof is het grootst in **Afrika (2.49 pt)** en
            **Azië (2.48 pt)**, en het kleinst in **Europa (0.23 pt)** in 2023.

            Een opvallende uitzondering deed zich voor in **Europa tussen 2009 en 2013**:
            in die periode hadden mannen gemiddeld een hogere werkloosheidsgraad dan vrouwen
            (kloof daalde tot **-0.32 pt** in 2010). Dit was een direct gevolg van de
            **financiële crisis van 2008**, die sectoren met veel mannelijke werknemers
            (bouw, industrie) het hardst trof.

            Dit wijst op **dubbele barrières** voor vrouwen op de arbeidsmarkt:
            niet alleen een lagere participatiegraad, maar ook structureel hogere werkloosheid.
            """
        )

    st.divider()

    # DATABRONNEN & METHODOLOGIE
    # **************************
    st.subheader("Databronnen & methodologie")

    b1, b2 = st.columns(2)
    with b1:
        st.markdown(
            """
            **Bronnen:**
            - International Labour Organization (ILO) via Our World in Data
            - World Bank (GDP per capita) via Our World in Data
            - Periode: 1990–2025 (GDP beschikbaar t/m 2024)
            - Dekking: 186 landen, 6 regio's (OWID-indeling)
            """
        )
    with b2:
        st.markdown(
            """
            **Methodologische bemerkingen:**
            - Geaggregeerde World Bank-groepen (zoals "High-income countries")
              werden verwijderd — dit zijn geen individuele landen.
            - Conflictlanden (Ukraine, Sudan, South Sudan, Palestine, Lebanon)
              werden gemarkeerd maar niet verwijderd.
            - De LFPR per regio is een **ongewogen** gemiddelde over landen —
              elk land telt even zwaar, ongeacht bevolkingsgrootte.
            """
        )
import streamlit as st
from datetime import datetime
from load_data import load_json
import  hospitalized_covid_state_page as hc
import uci_covid_state_page as uc
import ranking_hospitalized_covid_state_page as rc
import occupied_beds_covid_range_page as oc
import deaths_page as dc
from menu import nav

data = load_json()
selected = nav()

if selected == "CAMAS":
    df = hc.preprocess(data)
    hc.show_map_covid_state(df)
    hc.show_map_conclutions(df)
if selected == "UCI":
    df = uc.preprocess(data)
    uc.show_uci_covid_state(df)
    uc.show_uci_conclutions(df)
if selected == "MUERTES":
    df_deaths, df_rel = dc.preprocess(data)
    dc.show_deaths_covid_state(df_deaths)
    dc.show_rel_covid_staff(df_rel)
if selected == "RANKING":
    df = rc.preprocess(data)
    rc.show_ranking_covid_state(df)
    rc.show_ranking_conclutions(df)
if selected == "EXPLORAR":
    st.markdown(""" ### &#8594; Cantidad de camas ocupadas por pacientes covid-19 confirmados entre dos fechas insertadas""")
    slider_range = (datetime(2020,1,1), datetime(2022,8,15))
    slider_range = st.slider(
     "Seleccione los extremos del intervalo de fechas",
     value= (slider_range[0] , slider_range[1]),
     format="YYYY/MM/DD")
    df = oc.preprocess(data, slider_range)
    oc.show_range_covid(df)
    oc.show_range_conclutions(df)





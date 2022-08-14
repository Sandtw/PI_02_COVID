import streamlit as st
import pandas as pd
import numpy as np
import chart_studio.plotly as py
import plotly.offline as po
import plotly.graph_objs as pg

short_state_names = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

def preprocess(data):
    columns = ['date', 'state', 'inpatient_bed_covid_utilization_numerator']
    df = data.copy()
    df = df[columns]
    df['date'] = pd.to_datetime(df['date'])
    df.iloc[:,2:3] = df.iloc[:,2:3].apply(lambda col: col.astype(float))
    df.fillna(0, inplace=True)
    df = pd.pivot_table(index='state', values=['inpatient_bed_covid_utilization_numerator'], data=df, aggfunc='max').sort_values(by='inpatient_bed_covid_utilization_numerator', ascending=False).reset_index()
    return df

def show_map_covid_state(df):
    state_ab = df['state'].values
    state_name = [short_state_names[e] for e in state_ab]
    data = dict(type = 'choropleth', 
                locations = df['state'].values,
                locationmode = 'USA-states', 
                z   = df['inpatient_bed_covid_utilization_numerator'].values,
                text = state_name)
    layout = dict(title = 'Cantidad de hospitalizados debido a la COVID-19 por Estado (2020-01-01 / Actual)', 
              geo = dict(scope = 'usa' , 
                         showlakes = True, 
                         lakecolor = 'rgb(0,191,255)'))
    g = pg.Figure(data = [data] ,
            layout = layout)
    g.update_layout(margin=dict(
                autoexpand=False,
                l=100,
                r=300,
                t=80,
                ),
                   
        )
 
    with st.container():
        st.markdown(""" ### &#8594; Mapa de los estados que conforman USA y sus cantidades de hospitalizados por Covid-19""")             
        st.plotly_chart(g, use_container_width=True)
        
def show_map_conclutions(df):
    st.markdown("""
            ***Nota:*** Se consideró la mayor ocupación de camas comunes ocupadas por pacientes con covid-19 confirmado
            """)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            col1.metric(short_state_names[df['state'][0]], f"{int(df['inpatient_bed_covid_utilization_numerator'][0])} pacientes", "+ Máximo")
        with col2:
            col2.metric(short_state_names[df['state'].iloc[-1]], f"{int(df['inpatient_bed_covid_utilization_numerator'].iloc[-1])} pacientes", "- Mínimo")



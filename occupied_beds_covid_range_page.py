import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
import plotly.express as px
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

def preprocess(data, slider_range):
    columns = ['date', 'state', 'inpatient_bed_covid_utilization_numerator','total_pediatric_patients_hospitalized_confirmed_covid','staffed_icu_adult_patients_confirmed_covid', 'staffed_icu_pediatric_patients_confirmed_covid' ]
    df = data.copy()
    df = df[columns]
    df['date'] = pd.to_datetime(df['date'])
    df = df.query('(date <= @slider_range[1]) & (date >= @slider_range[0])')
    df.iloc[:,2:6] = df.iloc[:,2:6].apply(lambda col: col.astype(float))
    df.fillna(0, inplace=True)
    df['occupied_beds'] = df.iloc[:,2:6].sum(axis=1)
    df = pd.pivot_table(index=['date'], values=['occupied_beds'], data=df, aggfunc='sum').reset_index()
    return df

def show_range_covid(df):
    g = pg.Figure()
    g.add_trace(pg.Scatter(x = df['date'], y = df['occupied_beds'], line = dict(color='royalblue', width=2.5)))


    annotations = []
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                              xanchor='left', yanchor='bottom',
                              text=f'Cantidad de camas ocupadas por Covid-19 en USA',
                              font=dict(family='Arial',
                                        size=25,
                                        color='rgb(37,37,37)'),
                              showarrow=False))

    g.update_layout(annotations = annotations,
                   xaxis_title='Días',
                   yaxis_title='Cantidad de camas ocupadas',
                   plot_bgcolor='rgba(162,222,241,0.15)', 
                   margin=dict(
                     autoexpand=False,
                     l=90,
                     r=70,
                     t=70,
                    ),
                   xaxis=dict(
                     showline=True,
                     linecolor='rgb(204, 204, 204)',
                     linewidth=2,
                     ticks='outside',
                     tickfont=dict(
                      family='Arial',
                      size=12,
                      color='rgb(82, 82, 82)'
                      )
                   ),
                   yaxis=dict(
                     showline=True,     
                     linecolor='rgb(204, 204, 204)',
                     linewidth=2,
                     ticks='outside',
                     tickfont=dict(
                      family='Arial',
                      size=12,
                      color='rgb(82, 82, 82)'
                      )
                   )                  
                 )
    with st.container():            
        st.plotly_chart(g, use_container_width=True)

def show_range_conclutions(df):
    test = df.sort_values(by='occupied_beds', ascending=False).reset_index(drop=True)
    st.markdown("""
            ***Nota:*** Para el total de camas ocupadas por pacientes covid-19 confirmados se consideraron ocupaciones de adultos y pediátricos sobre camas comunes y camas uci
            """)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            col1.metric(str(test['date'][0].date()), f"{int(test['occupied_beds'][0])} camas ocupadas", "+ Máxima cantidad")
        with col2:
            col2.markdown("***Top de los 3 días con mayores cantidades de camas ocupadas por covid-19***")
            col2.markdown(f"""
                | Día | Camas ocupadas |
                |:------:|-----------|
                | {test['date'][0].date()} | {int(test['occupied_beds'][0])} |
                | {test['date'][1].date()} | {int(test['occupied_beds'][1])} |
                | {test['date'][2].date()} | {int(test['occupied_beds'][2])} |
            """)
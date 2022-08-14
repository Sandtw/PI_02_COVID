import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

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
    columns = ['date', 'state', 'staffed_icu_adult_patients_confirmed_covid', 'staffed_icu_pediatric_patients_confirmed_covid']
    df = data.copy()
    df = df[columns]
    df['date'] = pd.to_datetime(df['date'])
    df.iloc[:,2:4] = df.iloc[:,2:4].apply(lambda col: col.astype(float))
    df.fillna(0, inplace=True)
    df['used_icu_beds'] = df['staffed_icu_adult_patients_confirmed_covid'] + df['staffed_icu_pediatric_patients_confirmed_covid']
    df = pd.pivot_table(index='state', values=['used_icu_beds'], data=df, aggfunc='max').sort_values(by='used_icu_beds', ascending=False).reset_index()
    return df


def show_uci_covid_state(df):
    g = px.histogram(df, x="state", y="used_icu_beds")
    annotations = []
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                              xanchor='left', yanchor='bottom',
                              text='Cantidad de uso de camas UCI por Estado (2020-01-01 / Actual)',
                              font=dict(family='Arial',
                                        size=25,
                                        color='rgb(37,37,37)'),
                              showarrow=False))
    g.update_layout(annotations = annotations,
                   xaxis_title='Estados de USA',
                   yaxis_title='Uso de camas UCI',
                   plot_bgcolor='rgba(162,222,241,0.15)', # 'white'
                   margin=dict(
                     autoexpand=False,
                     l=90,
                     r=120,
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
        st.markdown(""" ### &#8594; Mayor ocupación de camas UCI por pacientes covid-19 confirmados por estado""")             
        st.plotly_chart(g, use_container_width=True)

def show_uci_conclutions(df):
    st.markdown("""
            ***Nota:*** Se consideró la mayor ocupación de camas UCI ocupadas por pacientes adultos y pediátricos con covid-19 confirmado
            """)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            col1.metric(short_state_names[df['state'][0]], f"{int(df['used_icu_beds'][0])} pacientes", "+ Máximo")
        with col2:
            col2.markdown("***Los 5 estados que más camas UCI utilizaron***")
            col2.markdown(f"""
                | Estado | Camas UCI |
                |:------:|-----------|
                | {short_state_names[df['state'][0]]} | {int(df['used_icu_beds'][0])} |
                | {short_state_names[df['state'][1]]} | {int(df['used_icu_beds'][1])} |
                | {short_state_names[df['state'][2]]} | {int(df['used_icu_beds'][2])} |
                | {short_state_names[df['state'][3]]} | {int(df['used_icu_beds'][3])} |
                | {short_state_names[df['state'][4]]} | {int(df['used_icu_beds'][4])} |
            """)
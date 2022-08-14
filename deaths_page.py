import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as pg
import matplotlib.pyplot as plt

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
    columns = ['date', 'state', 'deaths_covid', 'critical_staffing_shortage_today_yes']
    df = data.copy()
    df = df[columns]
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['date'].dt.year == 2021]
    df.iloc[:,2:4] = df.iloc[:,2:4].apply(lambda col: col.astype(int))
    df_deaths = pd.pivot_table(index='state', values=['deaths_covid'], data=df, aggfunc='sum').sort_values(by=['deaths_covid'], axis=0, ascending=False).reset_index()
    df_rel = pd.pivot_table(index='date', values=['deaths_covid', 'critical_staffing_shortage_today_yes'], data=df, aggfunc='sum').reset_index().sort_values(by=['date'], axis=0, ascending=True)
    return df_deaths, df_rel

def show_deaths_covid_state(df):
    g = px.histogram(df, x="state", y="deaths_covid")
    annotations = []
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                              xanchor='left', yanchor='bottom',
                              text='Muertes registradas por covid.19 (2020-01-01 / Actual)',
                              font=dict(family='Arial',
                                        size=25,
                                        color='rgb(37,37,37)'),
                              showarrow=False))
    g.update_layout(annotations = annotations,
                   xaxis_title='Estados de USA',
                   yaxis_title='Muertes (pacientes)',
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
        st.markdown(""" ### &#8594; Pacientes con covid-19 que fallecieron en el hospital por estado en el año 2021""")             
        st.plotly_chart(g, use_container_width=True)

    show_deaths_conclutions(df)

def show_rel_covid_staff(df):
    g = pg.Figure()
    g.add_trace(pg.Scatter(x = df['date'], y = df['deaths_covid'], line = dict(color='royalblue', width=2.5), name='Muertes por Covid'))
    g.add_trace(pg.Scatter(x = df['date'], y = df['critical_staffing_shortage_today_yes'], line = dict(color='red', width=2.5), name='Hospitales con personal escaso'))
    annotations = []
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                              xanchor='left', yanchor='bottom',
                              text=f'Relación Muertes por Covid VS Escasez de personal',
                              font=dict(family='Arial',
                                        size=25,
                                        color='rgb(37,37,37)'),
                              showarrow=False))

    g.update_layout(annotations = annotations,
                   xaxis_title='Días del año 2021',
                   plot_bgcolor='rgba(162,222,241,0.15)', # 'white'
                   margin=dict(
                     autoexpand=False,
                     l=90,
                     r=220,
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
        st.markdown("""
        ---
        """)
        st.markdown(""" ### &#8594; Relación entre las Muertes por Covid-19 y el número de hosputales con escacez de personal  """)             
        st.plotly_chart(g, use_container_width=True)

        show_rel_conclutions(df)

def show_deaths_conclutions(df):
    st.markdown("""
            ***Nota:*** Se consideró el total de pacientes con covid-19 presunto o confirmado que fallecieron en el hospital, en el servicio de urgencias o en el lugar de desbordamiento
            """)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            col1.metric(short_state_names[df['state'][0]], f"{int(df['deaths_covid'][0])} pacientes fallecidos", "+ Máximo")
        with col2:
            col2.markdown("***Top 5 de estados con mayor número de muertes***")
            col2.markdown(f"""
                | Estado | Muertes |
                |:------:|-----------|
                | {short_state_names[df['state'][0]]} | {int(df['deaths_covid'][0])} |
                | {short_state_names[df['state'][1]]} | {int(df['deaths_covid'][1])} |
                | {short_state_names[df['state'][2]]} | {int(df['deaths_covid'][2])} |
                | {short_state_names[df['state'][3]]} | {int(df['deaths_covid'][3])} |
                | {short_state_names[df['state'][4]]} | {int(df['deaths_covid'][4])} |
            """)

def show_rel_conclutions(df):
    st.markdown("""
            ***Nota:*** Se consideró el total de pacientes con covid-19 presunto o confirmado que fallecieron en el hospital, en el servicio de urgencias o en el lugar de desbordamiento y los hospitales que confirmaron una escacez de personal
            """)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(1,1)
            ax.scatter(x = df['critical_staffing_shortage_today_yes'], y = df['deaths_covid'])
            plt.xlabel("Nro. de hospitales")
            plt.ylabel("Muertes por covid")
            st.pyplot(fig)
        with col2:
            col2.markdown("***Mediante la gráfica respecto a los días del año 2021, muestra la relación entre los hospitales que confirmaron una escacez de personal vs las muertes por covid 19, cuya correlación lineal entre ambos tipos de datos, da un valor de 0.80, siendo así una relación de proporción directa fuerte***")
            col2.metric("Correlación lineal", round(df.corr().loc['deaths_covid','critical_staffing_shortage_today_yes'],2))

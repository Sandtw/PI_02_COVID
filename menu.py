import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

def nav():
    with st.container():
        selected = option_menu(
            menu_title=None,  # required
            options=["CAMAS", "UCI", "MUERTES","RANKING", "EXPLORAR"],  # required
            icons=["activity", "activity","x-lg", "bar-chart-line", 'wrench'],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#43DCE3"},
                "icon": {"color": "black", "font-size": "20px"},
                "nav-link": {
                    "font-size": "20px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#BBE9EB",
                },
                "nav-link-selected": {"background-color": "#5FA6DE", "color":"black"},
            },
        )
        return selected


   
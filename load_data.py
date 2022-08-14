import requests
import streamlit as st
import pandas as pd


def load_json():
    results_df = pd.read_csv('CDC.csv')
    return results_df
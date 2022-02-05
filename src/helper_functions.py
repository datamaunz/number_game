import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def get_prob_that_your_card_is_lowest(your_card, last_lowest_num, highest_num, number_of_remaining_cards):
    
    interval = highest_num - last_lowest_num
    prob = (your_card - last_lowest_num - 1)  / interval
    card_higher = 1 - prob
    all_cards_higher = card_higher ** (number_of_remaining_cards)
    return all_cards_higher

def replace_by_emotion(number, lowest_prob_thresh, highest_prob_thresh):
    if (number >= lowest_prob_thresh) & (number < highest_prob_thresh):
        return "😃"
    else:
        return "🥱"


def replace_by_binary(number, lowest_prob_thresh, highest_prob_thresh=1):
    if (number >= lowest_prob_thresh) & (number <= highest_prob_thresh):
        return 1
    else:
        return 0

def get_last_relevant_row(df):
    if len(df.columns) > 1:
        last_remaining_row = df[df.duplicated() == False].index[-1]
        df = df.loc[:last_remaining_row]
        return df
    else:
        
        relevant_index = df[df == 0].index[2]
        df = df.loc[:relevant_index]
        return df
    
def calculate_next_lowest_prob_thresh(lowest_prob_thresh, highest_prob_thresh):
    return lowest_prob_thresh + (highest_prob_thresh - lowest_prob_thresh) / 2

def calculate_next_highest_prob_thresh(lowest_prob_thresh, highest_prob_thresh):
    return highest_prob_thresh -  ((highest_prob_thresh - lowest_prob_thresh) / 2)

def create_table_for_step(df_new, lowest_prob_thresh, highest_prob_thresh):
    
    df_table = df_new.copy()
    df_table = df_table[df_table <= highest_prob_thresh].dropna()
    for column in df_new.columns:
        df_table[column] = df_table[column].apply(lambda x: replace_by_binary(x, lowest_prob_thresh))
        lowest_prob_thresh = calculate_next_lowest_prob_thresh(lowest_prob_thresh, highest_prob_thresh)
        if df_table[column].sum() < 2:
            df_table = df_table.drop(column, 1)
            
    df_table = get_last_relevant_row(df_table)
    df_table.columns = [f'round {x+1}' for x in df_table.columns]
    
    if len(df_table) > 0:
        df_table = df_table.applymap(lambda x: {0:"🥱", 1:"😃"}.get(x))
    else:
        df_table = None
    
    return df_table

def create_prob_fig_per_number(remaining_range, all_probs):
    
    fig = go.Figure()
    fig.add_traces(go.Scatter(
        x = remaining_range,
        y = all_probs
        ))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor="lightgrey", title=dict(text="card number")),
        yaxis=dict(gridcolor="lightgrey", title=dict(text="probability<br>that card number is the lowest"))
    )
    st.plotly_chart(fig, use_container_width=True)

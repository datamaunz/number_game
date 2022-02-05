import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


last_lowest_num, highest_num = st.slider("lowest card on table", 0,100,[0,100])
number_of_remaining_cards = st.number_input("How many cards are still in the game?", 1)


remaining_range = np.arange(last_lowest_num + 1, highest_num + 1)



def get_prob_that_your_card_is_lowest(your_card, last_lowest_num, highest_num, number_of_remaining_cards):
    
    interval = highest_num - last_lowest_num
    prob = (your_card - last_lowest_num - 1)  / interval
    card_higher = 1 - prob
    all_cards_higher = card_higher ** (number_of_remaining_cards)
    return all_cards_higher

all_probs = [get_prob_that_your_card_is_lowest(x, last_lowest_num, highest_num, number_of_remaining_cards) for x in remaining_range]

fig = go.Figure()
fig.add_traces(go.Scatter(
    x = remaining_range,
    y = all_probs
    ))

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(gridcolor="lightgrey", title=dict(text="card number")),
    yaxis=dict(gridcolor="lightgrey", title=dict(text="probability that card is the lowest"))
)
st.plotly_chart(fig, use_container_width=True)




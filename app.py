import streamlit as st
from src.helper_functions import *

def main():
    st.set_page_config(
    layout="wide",
    page_title="Number Game",
    page_icon = "🤖")

    last_lowest_num, highest_num = st.sidebar.slider("lowest card on table", 0,100,[0,100])
    number_of_remaining_cards = st.sidebar.number_input("How many cards are still in the game?", 1, 99, 8)


    remaining_range = np.arange(last_lowest_num + 1, highest_num + 1)
    all_probs = [get_prob_that_your_card_is_lowest(x, last_lowest_num, highest_num, number_of_remaining_cards) for x in remaining_range]
    #create_prob_fig_per_number(remaining_range, all_probs)

    df_new = pd.DataFrame([all_probs]*5).T
    df_new["number"] = np.arange(last_lowest_num+1, highest_num+1,1)
    df_new = df_new.set_index("number")

    lowest_prob_thresh = 0.5
    highest_prob_thresh = 1
    df_first = create_table_for_step(df_new, lowest_prob_thresh, highest_prob_thresh)

    lowest_prob_thresh = 0.5
    highest_prob_thresh = 0.75
    df_second = create_table_for_step(df_new, lowest_prob_thresh, highest_prob_thresh)

    lowest_prob_thresh = 0.75
    highest_prob_thresh = 0.875
    df_third = create_table_for_step(df_new, lowest_prob_thresh, highest_prob_thresh)

    st.markdown("## Emotional Robots")

    x = df_first.index[-2]

    f"""
    ### Steps
    
    1. Set the slider to the lowest number on the table. If no card is on the table yet, set it to 0. Set the card counter on the sidebar to the number of cards remaining in the game.
    2. You're the only person smiling? **You have the lowest card**! Put it on the table and start again at step 1.
    3. First round (*table 1*) and everyone is yawning? - Move the slider up to `{x}` and go back to step 2.
    4. More then 1 person is excited? The lowest card is among you (the excited folks). You are about to enter round 2 (*table 1*).
        
        5.1. You're the only person smiling? You are holding the lowest card. Put it on the *table* and go back to step 1.
        
        5.2. More than one person smiling? Same as before: move on to the next round (3, then 4 etc.) in *table* 1 (step 4).
        
        5.3. Everyone yawning at round 2? Go to *table* 2!
        
        5.3. Everyone yawning at round 3? Go to *table* 3!
    """

    col1, col2, col3 = st.columns(3)
        

    with col1:
        if df_first.empty == False:
            st.markdown("### Table 1")    
            st.write(df_first)


    with col2:
        if df_second.empty == False:
            st.markdown("### Table 2")
            st.write(df_second)

    with col3:
        if df_third.empty == False:
            st.markdown("### Table 3")
            st.write(df_third)


if __name__ == '__main__':
    main()
    
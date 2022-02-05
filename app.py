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
    st.markdown("#### Two emotions are enough to navigate *the Mind* with ease: 🥱 and 😃")
    
    """
    [*The Mind*](https://de.wikipedia.org/wiki/The_Mind) is a cooperative game created by [*Wolfgang Marsch*](https://de.wikipedia.org/wiki/The_Mind). 
    It was among the three final nominees for the *game of the year* award in 2018.
    
    The game consists of 100 cards numbered from 1 to 100, can be played by 2 to 4 players, and has twelve levels. 
    In level 1, players receive 1 card, in lelvel 2, 2 cards, in level 3, 3 cards, and so forth. 
    Only they themselves know what numbers they hold. 
    
    The aim of the game is to place the cards on the table in ascending order without talking about numbers or implying them in any way. 
    If a card is laid while one of the players has a lower number in hand, the round is lost. 
    It's thus a collaborative game but players are not allowed to talk numbers. 
    If the players manage to put the numbers on the table in the correct order, they all win and advance to the new level.
    
    According to the legend, in order to be successful, you need special empathy for the other players. 
    But that's a myth. 
    Probability and two simple emotions coupled with a clear process of expressing and interpreting confidence are enough to succeed.
    
    ---
    
    #### Maxims
    
    > Only show confidence if the likelihood of having the lowest card is larger or equal to `0.5`.
    
    > Further refine the assessment of likelihoods depending on whether one person, no person or many persons express confidence (according to a standard procedure).
    
    ---
    
    #### Formula
    
    Calculate the probability that you're holding the card with the lowest number.
    
    """
    
    
    
    colA, colB = st.columns(2)
    
    with colA:
        calculate_probability = r"""
        $$ 
        p = (1 - \frac{(n - n_l -1)}{(n_h - n_l)})^{cards}
        $$ 
        """
        st.write(calculate_probability)
    
    with colB:
        with st.expander("Legend"):
            legend = r"""
            > $n$ ... your lowest number
            
            > $p$ ... probability that you are holding the card with the lowest number
            
            > $n_l$ ... lowest number on the table
            
            > $n_h$ ... highest possible number (under standard conditions 100)
            
            > $cards$ ... number of remaining cards in the game
            """
        
            st.write(legend)
    
    x = df_first.index[-2]

    f"""
    ---
    #### Standard Procedure
    
    1. Set the slider to the lowest number on the table. If no card is on the table yet, set it to 0. Set the card counter on the sidebar to the number of cards remaining in the game.
    2. You're the only person smiling (*table 1*)? **You have the lowest card**! Put it on the table and start again at step 1.
    3. First round (*table 1*) and everyone is yawning? - Move the slider up to `{x}` and go back to step 2.
    4. More then 1 person is excited? The lowest card is among you (the excited folks). You are about to enter round 2 (*table 1*).
        
        5.1. You're the only person smiling? You are holding the lowest card. Put it on the *table* and go back to step 1.
        
        5.2. More than one person smiling? Same as before: move on to the next round (3, then 4 etc.) in *table* 1 (step 4).
        
        5.3. Everyone yawning at round 2? Go to *table* 2!
        
        5.3. Everyone yawning at round 3? Go to *table* 3!
        
    ---
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

    """
    ---
    
    #### Here you can check the probability per number
    """
    create_prob_fig_per_number(remaining_range, all_probs)

if __name__ == '__main__':
    main()
    
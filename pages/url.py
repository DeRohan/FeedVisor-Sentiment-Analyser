from Modules.mods import *

def main():
    st.set_page_config(page_title="FeedVisor: Find Intentions!", layout="wide", initial_sidebar_state="collapsed", page_icon="🖥️")
    st.markdown("<h4><center>FeedVisor: Find The Real Intentions!<center><h4>", unsafe_allow_html=True)
    page_html = """
    <style>
        [tabindex="-1"] {
            background: rgb(0,0,0);
            background: linear-gradient(90deg, rgba(0,0,0,1) 0%, rgba(9,63,121,1) 35%, rgba(20,0,36,1) 100%);
        }
        [data-testid="stAppViewContainer"] {
            background: rgb(0,0,0);
            background: linear-gradient(90deg, rgba(0,0,0,1) 0%, rgba(9,63,121,1) 35%, rgba(20,0,36,1) 100%);
        }
    </style>
    """
    st.markdown(page_html, unsafe_allow_html=True)
    query = st.text_input("", placeholder="Enter a URL to Analyse", label_visibility="collapsed")
    if st.button("Analyse Now!"):
        if query.startswith("https://") or query.startswith("http://"):
            video, analysis = va.main(query)
            class_counts = analysis['Emotion'].value_counts().reset_index()
            class_counts.columns = ['Sentiment Class', 'Number of Frames']

            # Plot sentiment distribution using an area chart
            col1, col2 = st.columns([2, 3])

            # Display tweets DataFrame on the left
            with col1:
                st.subheader("Video Player")
                st.video(video)
            #     with st.expander("Retrieved Tweets", expanded=True):
                    # for i, tweet in enumerate(tweets[['Username', 'Text', 'Likes', 'Retweets']].iterrows(), start=1):
                    #     formatted_tweet = format_tweet(tweet[1])
                    #     st.text_area(f"Tweet {i}", formatted_tweet, height=200)
                pass
            # Display area chart on the right
            with col2:
                st.subheader("Sentiment Distribution")
                st.area_chart(class_counts.set_index("Sentiment Class"))
        else:
            st.error("Invalid Input. Please Re-Enter Your Query")

if __name__ == "__main__":
    main()
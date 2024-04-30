from video_analysis import *

page_css = """
<style>
body {
    background-image: url('');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

@keyframes dropAnimation {
    0% {transform: translateY(-100px);}
    100% {transform: translateY(0);}
}

.emoji {
    animation: dropAnimation 3s ease infinite;
    font-size: 30px; /* Adjust emoji size */
    margin: 10px; /* Adjust emoji margin */
}

#text_input_1 {
    border-radius: 10px;
    border: 2px solid #000000;
}

[data-testid="stApp"] {
    background-color: transparent !important; /* Make Streamlit app background transparent */
}
</style>
"""


# Apply the CSS styles
st.markdown(page_css, unsafe_allow_html=True)


def tweets_analysis():
    st.write("Get your Tweets Analysis!")
    if st.button("Home Page"):
        st.session_state.runpage = main
        # st.rerun()
# Streamlit app
def main():
    # st.set_page_config(page_title="FeedVisor: Sentiment Analyser", page_icon="🔍", layout="wide", initial_sidebar_state="collapsed")
    st.title("FeedVisor")
    
    st.sidebar.header("Navigation")
    selected_page = st.sidebar.radio("Go to", ["Search", "Emotion Analysis"])

    if selected_page == "Search":
        st.write("## Search and Results")

        search_query = st.text_input("Enter Message or URL:", "")

        if search_query:
            if search_query.startswith("http://") or search_query.startswith("https://"):
                st.write("### URL Provided")
                st.write("You entered a URL:", search_query)
                encoded_url = urllib.parse.quote(search_query, safe='')
                # Link to Home.py page with the URL as a query parameter
                # st.page_link("pages/url.py?url=" + encoded_url, label="Analysis", icon="1️⃣")          
            else:
                st.page_link("pages/VA.py", label="Get Results!", icon="1️⃣")
                # st.write("### Message Provided")
                # st.write("You entered a message:", search_query)
                # st.write("Processing the message...")
                # st.write("Message processed successfully.")
                

    elif selected_page == "Emotion Analysis":
        st.error("Error processing video.")
                                
# Footer with animated emojis
footer_html = ""
emoji_dict = {
    "angry": "😡",
    "funny": "😂",
    "smile": "😊",
    "up": "👍",
    "down": "👎"
}
# for emotion_key in emoji_dict.keys():
#     footer_html += f'<p class="emoji">{emoji_dict[emotion_key]}</p>'
# st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
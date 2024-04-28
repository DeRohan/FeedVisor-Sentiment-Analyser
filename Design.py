from tweet_analysis import *
import URL_Analysis as ua
import streamlit as st
import cv2
from deepface import DeepFace
import os
import urllib.request
from pytube import YouTube

# Define the CSS styles including the background image and animation
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

# Streamlit app
def main():
    st.title("FeedVisor: Sentiment Analyser")
    
    st.sidebar.header("Navigation")
    selected_page = st.sidebar.radio("Go to", ["Search", "Messages", "Videos", "Emotion Analysis"])

    if selected_page == "Search":
        st.write("## Search and Results")

        search_query = st.text_input("Enter Message or URL:", "")

        # Automatically switch to the Messages page if a message is entered
        if search_query:
            selected_page = "Messages"

        # Display search results
        if search_query:
            if search_query.startswith("http://") or search_query.startswith("https://"):
                # Assume it's a URL
                st.write("### URL Provided")
                st.write("You entered a URL:", search_query)
                # Add your URL processing logic here
                
                # Embed video
                st.video(search_query, start_time=0)  # Auto-play from the start
                
            else:
                # Assume it's a message
                st.write("### Message Provided")
                st.write("You entered a message:", search_query)
                st.write("Processing the message...")
                st.write("Message processed successfully!")
                
                selected_page = "Messages"
                # Add your message processing logic here

    elif selected_page == "Messages":
        st.write("## Messages Page")

    elif selected_page == "Videos":
        st.write("## Videos Page")
        # Add content for videos page

    elif selected_page == "Emotion Analysis":
        ua.Video_Analysis()

# Footer with animated emojis
footer_html = ""
emoji_dict = {
    "angry": "😡",
    "funny": "😂",
    "smile": "😊",
    "up": "👍",
    "down": "👎"
}
for emotion_key in emoji_dict.keys():
    footer_html += f'<p class="emoji">{emoji_dict[emotion_key]}</p>'
st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
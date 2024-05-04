from Modules.mods import *

#Main Home Page
def main():
    # CSS Styling 
    st.set_page_config(page_title="FeedVisor: Find Intentions!", layout="wide", initial_sidebar_state="collapsed", page_icon="🖥️")  
    page_bg_img = """"
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
    #Start
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.markdown("<h2><center>Welcome to FeedVisor</center><h2>", unsafe_allow_html=True)
    st.markdown("<p><center>Find the Real Intentions</center></p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Tweet Analyser"):
            # Redirect to Page 1
            # subprocess.run(["streamlit", "run", "pages/tweet.py"])
            pass

    with col2:
        if st.button("Video Analyser"):
            # Redirect to Page 2
            # subprocess.run(["streamlit", "run", "pages/url.py"])
            pass


if __name__ == "__main__":
    main()
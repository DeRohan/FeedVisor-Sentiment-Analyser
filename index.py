from Modules.mods import *

#Main Home Page
def main():
    st.set_page_config(page_title="FeedVisor: Find Intentions!", layout="wide", initial_sidebar_state="collapsed", page_icon="🖥️")  
    page_bg_img = """
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
    st.markdown("<h4><center>Find the Real Intentions!</center><h4>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5, gap="medium")
    with col1:
        pass
    with col2:
        if st.button("Tweet Analyser"):
            switch_page("tweet")
    with col3:
        pass
    with col4:
        if st.button("Video Analyser"):
            switch_page("url")
    with col5:
        pass


if __name__ == "__main__":
    main()
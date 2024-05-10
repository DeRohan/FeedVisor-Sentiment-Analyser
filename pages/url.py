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
    st.write("<h4><center>Video Analyser<h4>", page_icon="🎥",unsafe_allow_html=True)
    query = st.text_input("", placeholder="Enter a URL to Analyse", label_visibility="collapsed")
    btn = st.button("Analyse Now!")
    if btn:
        if len(query) <=0:
            st.error("Error. Please Enter a URL.")
        elif query.startswith("https://") or query.startswith("http://"):
            youtube_pattern = re.compile(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$")

            if youtube_pattern.match(query):
                    
                video, analysis = va.main(query)
                if video!=None and analysis!=None:
                    class_counts = analysis['Emotion'].value_counts().reset_index()
                    class_counts.columns = ['Sentiment Class', 'Number of Frames']
                    col1, col2 = st.columns([2, 3])
                    with col1:
                        st.subheader("Video Player")
                        st.video(video)
                    with col2:
                        st.subheader("Sentiment Distribution")
                        st.area_chart(class_counts.set_index("Sentiment Class"))
                else:
                    st.error("Error processing video. Please enter any other Video URL.")
            else:
                st.error("Error. Please only Enter YouTube Video URLs.\nWe are planning to expand to other Platforms soon...")
        else:
            st.error("Invalid Input. Please Re-Enter Your Query")

if __name__ == "__main__":
    main()
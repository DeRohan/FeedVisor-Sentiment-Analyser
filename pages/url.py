import streamlit as st
import cv2
from deepface import DeepFace
import os
from pytube import YouTube
import pandas as pd
import matplotlib.pyplot as plt
import urllib.parse

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


def create_emotion_graph(emotions_excel_path):
    df = pd.read_excel(emotions_excel_path)
    emotion_counts = df['Emotion'].value_counts()
    plt.figure(figsize=(8, 6))
    plt.bar(emotion_counts.index, emotion_counts.values, color='skyblue')
    plt.xlabel('Emotion')
    plt.ylabel('Count')
    plt.title('Emotion Analysis')
    st.pyplot()
# Function to detect faces and analyze emotions
def detect_and_analyze_faces(frame, frame_number):
    emotions = []
    face_model = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_model.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        try:
            emotion = DeepFace.analyze(face, actions=["emotion"], enforce_detection=False)
            if isinstance(emotion, list):
                emotion = emotion[0]  # Take the first result if multiple are returned
            emotion_label = emotion["dominant_emotion"]
            emotions.append(emotion_label)
            cv2.putText(frame, emotion_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
        except Exception as e:
            st.error(f"Error analyzing emotions: {str(e)}")
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)

    return frame, emotions, [frame_number]*len(emotions)

# Function to process video and save with emotion analysis
def process_video_with_emotion_analysis(video_path, output_path):
    capture = cv2.VideoCapture(video_path)
    frame_list = []
    emotions_list = []
    frame_numbers = []

    for i in range(1000):
        ret, frame = capture.read()
        if not ret:
            break
        
        frame_with_faces, frame_emotions, frame_nums = detect_and_analyze_faces(frame, i)
        frame_list.append(frame_with_faces)
        emotions_list.extend(frame_emotions)
        frame_numbers.extend(frame_nums)

    capture.release()

    if frame_list:
        height, width, _ = frame_list[0].shape
        size = (width, height)
        output = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"DIVX"), 60, size)

        for frame in frame_list:
            output.write(frame)

        output.release()

        # Create a DataFrame to store frame numbers and corresponding emotions
        data = {"Frame_Number": frame_numbers, "Emotion": emotions_list}
        df = pd.DataFrame(data)

        # Save DataFrame to Excel
        excel_output_path = os.path.splitext(output_path)[0] + "_emotions.xlsx"
        df.to_excel(excel_output_path, index=False)

        return True
    else:
        return False

# Function to download YouTube video
def download_youtube_video(video_url, output_path):
    st.write("Downloading video...")
    yt = YouTube(video_url)
    yt.streams.filter(file_extension='mp4').first().download(output_path=output_path, filename="video.mp4")
    st.write("Video downloaded successfully!")

# Function to read video file as bytes
def read_video(video_path):
    if os.path.exists(video_path):
        with open(video_path, "rb") as file:
            video_bytes = file.read()
        return video_bytes
    else:
        st.error("Processed video file does not exist. Please make sure the video processing step is completed.")



def main():
    # Retrieve URL from query parameter and decode it
    encoded_url = st.query_params.get("url", [""])[0]
    url = urllib.parse.unquote(encoded_url)
    
    st.write(url)  # Check if URL is correctly retrieved
    
    if url:
        output_path = "downloads"  
        os.makedirs(output_path, exist_ok=True)
        download_youtube_video(url, output_path)
        video_path = os.path.join(output_path, "video.mp4")
                
        emotions_output_path = os.path.join(output_path, "Emotions_With_Hands")
        if process_video_with_emotion_analysis(video_path, f"{emotions_output_path}.mp4"):
            st.write("Video processed successfully!")
            st.write("Download the processed video [here](downloads/Emotions_With_Hands.mp4)")
            emotions_excel_path = f"{emotions_output_path}_emotions.xlsx"
            st.write("Download the emotions data [here](downloads/Emotions_With_Hands_emotions.xlsx)")
            st.write("Creating emotion analysis graph...")
            create_emotion_graph(emotions_excel_path)
                    
            st.write("Playing the processed video...")
            st.video(f"{emotions_output_path}.mp4")
        else:
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
for emotion_key in emoji_dict.keys():
    footer_html += f'<p class="emoji">{emoji_dict[emotion_key]}</p>'
st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

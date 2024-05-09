from pytube import YouTube
import cv2
import os
from deepface import DeepFace
import pandas as pd
import streamlit as st


def create_emotion_graph(emotions_excel_path):
    df = pd.read_csv(emotions_excel_path)
    return df
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
        excel_output_path = os.path.splitext(output_path)[0] + "_emotions.csv"
        df.to_csv(excel_output_path, index=False)

        return True
    else:
        return False

# Function to download YouTube video
def download_youtube_video(video_url, output_path):
    st.spinner("Loading...")
    yt = YouTube(video_url)
    yt.streams.filter(file_extension='mp4').first().download(output_path=output_path, filename="video.mp4")

def read_video(video_path):
    if os.path.exists(video_path):
        with open(video_path, "rb") as file:
            video_bytes = file.read()
        return video_bytes
    else:
        st.error("Processed video file does not exist. Please make sure the video processing step is completed.")



def main(url):
    # Retrieve URL from query parameter and decode it
    # encoded_url = st.query_params.get("url", [""])[0]
    # url = urllib.parse.unquote(url)
    
    # st.write(url)  # Check if URL is correctly retrieved
    
    if url:
        output_path = "downloads"  
        os.makedirs(output_path, exist_ok=True)
        download_youtube_video(url, output_path)
        video_path = os.path.join(output_path, "video.mp4")
                
        emotions_output_path = os.path.join(output_path, "Emotions_With_Hands")
        if process_video_with_emotion_analysis(video_path, f"{emotions_output_path}.mp4"):
            emotions_excel_path = f"{emotions_output_path}_emotions.csv"
            analysis = create_emotion_graph(emotions_excel_path) #Analysis DataFrame
            video_output_file = emotions_output_path + ".mp4"
            return video_output_file, analysis
        else:
            st.error("Error processing video.")

                    
                
if __name__ == "__main__":
    main()

import streamlit as st
import cv2
from deepface import DeepFace
import os
import urllib.request
from pytube import YouTube

# Function to detect faces and analyze emotions
def detect_and_analyze_faces(frame):
    face_model = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_model.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        try:
            emotions = DeepFace.analyze(face, actions=["emotion"], enforce_detection=False)
            if isinstance(emotions, list):
                emotion = emotions[0]  # Take the first result if multiple are returned
            else:
                emotion = emotions
            emotion_label = emotion["dominant_emotion"]
            cv2.putText(frame, emotion_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
        except Exception as e:
            st.error(f"Error analyzing emotions: {str(e)}")
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)

    return frame


# Function to download YouTube video
def download_youtube_video(video_url, output_path):
    st.write("Downloading video...")
    yt = YouTube(video_url)
    yt.streams.filter(file_extension='mp4').first().download(output_path=output_path, filename="video")
    st.write("Video downloaded successfully!")


# Function to process video and save with emotion analysis
def process_video_with_emotion_analysis(video_path, output_path):
    capture = cv2.VideoCapture(video_path)
    frame_list = []

    for i in range(1000):
        ret, frame = capture.read()
        if not ret:
            break
        
        frame_with_faces = detect_and_analyze_faces(frame)
        frame_list.append(frame_with_faces)

    capture.release()

    if frame_list:
        height, width, _ = frame_list[0].shape
        size = (width, height)
        output = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"DIVX"), 60, size)

        for frame in frame_list:
            output.write(frame)

        output.release()
        return True  # Success flag
    else:
        return False  # No 



def Video_Analysis():
    st.write("## Emotion Analysis Page")
            
    video_url = st.text_input("Enter YouTube Video URL:", "")
    if st.button("Process Video"):
        if video_url:
            output_path = "downloads"  
            os.makedirs(output_path, exist_ok=True)
            download_youtube_video(video_url, output_path)
            video_path = os.path.join(output_path, "video.mp4")
                    # video_path = "./downloads/video.mp4"
                    # Now you have downloaded the video, you can process it further
            st.write(video_path)
            process_video_with_emotion_analysis(video_path, "Emotions.mp4")
            st.write("Video processed successfully!")
            st.write("Download the processed video [here](Emotions.avi)")
            st.video("Emotions.mp4")



# Function to read video file as bytes
def read_video(video_path):
    if os.path.exists(video_path):
        with open(video_path, "rb") as file:
            video_bytes = file.read()
        return video_bytes
    else:
        st.error("Processed video file does not exist. Please make sure the video processing step is completed.")
import cv2
from deepface import DeepFace
import numpy as np

# Function to detect faces and analyze emotions
def detect_and_analyze_faces(frame):
    face_model = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_model.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        emotion = DeepFace.analyze(face, actions=["emotion"])
        emotion_label = emotion["dominant_emotion"]
        
        cv2.putText(frame, emotion_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)

    return frame

# Process video
def process_video(video_path):
    capture = cv2.VideoCapture(video_path)
    frame_list = []

    while True:
        ret, frame = capture.read()
        if not ret:
            break
        
        frame_with_faces = detect_and_analyze_faces(frame)
        frame_list.append(frame_with_faces)

    capture.release()

    return frame_list

# Write processed frames to video
def write_to_video(frame_list, output_path):
    if len(frame_list) == 0:
        return

    height, width, _ = frame_list[0].shape
    size = (width, height)
    output = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"DIVX"), 30, size)

    for frame in frame_list:
        output.write(frame)

    output.release()

# Main function
def main():
    video_path = "https://www.youtube.com/watch?v=fnsFJhJvY2s"  # Change to your local video path
    output_path = "Emotions.avi"
    
    frame_list = process_video(video_path)
    write_to_video(frame_list, output_path)

if __name__ == "__main__":
    main()

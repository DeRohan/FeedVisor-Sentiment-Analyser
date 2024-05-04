import streamlit as st
# from streamlit_theme import st_theme
import video_analysis as va
import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import cv2
from deepface import DeepFace
import os
from pytube import YouTube
import tweet_analysis as twa
from streamlit_extras.switch_page_button import switch_page
# from array import array
# from cProfile import label
# from email.mime import audio
# from lib2to3.pgen2 import token
# from os import truncate
# from pyexpat import model
from asyncore import write
import streamlit as st
from transformers import pipeline,AutoTokenizer, AutoModelForCausalLM
# import regex as re
# import random
# #from streamlit_lottie import st_lottie
# import os,requests
# #import gpt_2_simple as gpt2
#from keras.utils import multi_gpu_model
#from textgenrnn import textgenrnn

from gtts import gTTS
# import os
if "base_text" not in st.session_state:
    st.session_state['base_text']=""


text="Your mother is gay"
text=st.text_area(label="Input story prompt")
st.write(text)
st.write("Playing Sound")
#os.mkdir("temp")
if st.button("Submit"):
    st.session_state['base_text']=text
st.write(st.session_state['base_text'])
myobj = gTTS(text=text, lang="en", slow=False)
myobj.save("temp/sound.mp3")
audio_file = open("temp/sound.mp3", "rb")
audio_bytes = audio_file.read()
st.markdown(f"## Your audio:")
st.audio(audio_bytes, format="audio/mp3", start_time=0)
st.write("Sound above.")



* Used for Final Year Individual Project at University Of Glasgow*

The project requirements were to develop a language generation model to generate texts for story plots.

The project was aimed to solve writers block by generating plots of stories based off selected genres.

GPT-2-Models were utilised through GPT-2-Simple package. Finetuning was done using Kaggle datasets and GPT-2-Simple package. 
Where stories were in the dataset were of the following format:
<Genre>: (genre) Title: (Title of movie) Plot: (plot of story)

Usage:
pip install -r requirements.txt

pip install Streamlit

On console: 
streamlit run streamlit.py

Unstable Deployed version of application URL:
https://share.streamlit.io/individualproj/storygenerating/main/streamlit.py
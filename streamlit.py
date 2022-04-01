from array import array
from cProfile import label
from email.mime import audio
from json import load
from lib2to3.pgen2 import token
from os import truncate
import streamlit as st
from transformers import pipeline,AutoTokenizer, AutoModelForCausalLM
import regex as re
import random
#from streamlit_lottie import st_lottie
import os,requests
import gpt_2_simple as gpt2
import nltk
from nltk.translate.bleu_score import corpus_bleu
from nltk import tokenize

from gtts import gTTS

import os

st.set_page_config(page_title="GeneratorStory",page_icon=":book:")

messagetext=["Patience! This is difficult, you know...",
  "Discovering new ways of making you wait...",
  "Your time is very important to us. Please wait while we ignore you...",
  "Please wait while the minions do their work...",
  "Grabbing extra minions...",
  "Doing the heavy lifting...",
  "We're working very Hard .... Really...",
  "Waking up the minions","Please wait while we serve other customers...",
  "Feel free to spin in your chair",
  "Please wait... Consulting the manual...",
    "Ordering 1s and 0s...",
      "If I’m not back in five minutes, just wait longer.",]
def audio(text:str):
            myobj = gTTS(text=text, lang="en", slow=False)
            myobj.save("temp/sound.mp3")
            audio_file = open("temp/sound.mp3", "rb")
            audio_bytes = audio_file.read()
            st.markdown(f"#### Your audio:")
            st.audio(audio_bytes, format="audio/mp3", start_time=0)
#def download(text:str):

def cleantext(text:str):
    
    text=text.replace('\'\'',"\"")
    text=text.replace('•',"(")
    text=text.replace('■',")")
    text=re.sub("[\(\[].*?[\)\]]", "", text)
    text=re.sub('<[^>]+>', '', text)
    return text

# @st.cache(suppress_st_warning=True)
def generateText(inputtext,storylen,genre,page):
    # storylen=len(inputtext)*0.5+storylen
    if page==1:
            tokenizer = AutoTokenizer.from_pretrained("pranavpsv/genre-story-generator-v2")
            model = AutoModelForCausalLM.from_pretrained("pranavpsv/genre-story-generator-v2")
            textinp="<BOS> <"+genre+"> "+inputtext
            story_gen=pipeline('text-generation',"pranavpsv/genre-story-generator-v2")
            generated= story_gen(textinp,max_length=storylen,top_k=96,temperature=1.2)[0]['generated_text'].replace("<BOS> <"+genre+"> ","").replace(" Tell me what happens in the story and how the story ends.","")
            print("method generated text:",generated)

            return(cleantext(generated))
    elif page==0:
        sess=gpt2.start_tf_sess()
        gpt2.load_gpt2(sess, run_name='stories')
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        storylen=len(tokenizer(inputtext)['input_ids'])+storylen
        inputtexts="Genre: "+genre+" Plot: "+inputtext
        
        generated=gpt2.generate(sess,run_name="stories",prefix=inputtexts, include_prefix=False,length=storylen,nsamples=3,truncate="<|endoftext|>",return_as_list=True)
        newgeneratedlist=[]
        for i in generated:
            newgeneratedlist.append(i.replace(inputtexts,""))
        return newgeneratedlist
        
            # if genre=='horror':
            #     print("=============================HORROR GENERATION IN PROGRESS====================================")
            #     @st.cache
            #     def loadhorrormodel():
            #         horrormodel = AutoModelForCausalLM.from_pretrained("wexnertan/storygenhorror")
            #         return horrormodel
            #     model=loadhorrormodel()
            #     tokenizer = AutoTokenizer.from_pretrained("gpt2")
            #     storylen=len(tokenizer(inputtext)['input_ids'])+storylen
            #     story_gen=pipeline('text-generation',model=model,tokenizer=tokenizer)
            #     generated= story_gen(inputtext,max_length=storylen+20,do_sample=True,repetition_penalty=1.00,no_repeat_ngram_size=3,num_return_sequences=3)
                
            #     #generated= story_gen(inputtext,max_length=storylen,do_sample=True,top_k=95,top_p=0.95)[0]['generated_text']
            #     # return generated
            # elif genre=='drama':
            #     print("=============================DRAMA GENERATION IN PROGRESS====================================")
            #     @st.cache
            #     def loaddramamodel():
            #         dramamodel = AutoModelForCausalLM.from_pretrained("wexnertan/storygendrama")
                    
            #         return dramamodel
            #     model=loaddramamodel()
            #     tokenizer = AutoTokenizer.from_pretrained("gpt2")
            #     story_gen=pipeline('text-generation',model=model,tokenizer=tokenizer)
                
            #     generated= story_gen(inputtext,max_length=storylen,do_sample=True,repetition_penalty=1.00,no_repeat_ngram_size=3,nsamples=3)
            #     # return generated
            # elif genre=='sci_fi':

            #     print("=============================SCIFI GENERATION IN PROGRESS====================================")
            #     @st.cache
            #     def loaddramamodel():
            #         scifimodel = AutoModelForCausalLM.from_pretrained("wexnertan/storygenscifi")
            #         return scifimodel
            #     model=loaddramamodel()
            #     tokenizer = AutoTokenizer.from_pretrained("gpt2")
            #     story_gen=pipeline('text-generation',model=model,tokenizer=tokenizer)
            #     generated= story_gen(inputtext,max_length=storylen,do_sample=True,repetition_penalty=1.00,no_repeat_ngram_size=3,nsamples=3)
            # print(generated)
        #return generated
            # sess = gpt2.start_tf_sess()
            # if genre=='horror':
            #     print("loading horror model")
            #     gpt2.load_gpt2(sess, run_name='horror')
            #     textinp=inputtext
            #     generated = gpt2.generate(
            #         sess,
            #         run_name='horror',
            #         prefix=textinp, 
            #         length=storylen,
            #         temperature=1.2,
            #         #truncate=True, 
            #         top_k=65,
            #         top_p=0.90,
            #         return_as_list=True
            #         )[0].replace("\n","")
            # elif genre=='drama':
            #     print("loading drama model")
            #     gpt2.load_gpt2(sess, run_name='drama')
            #     textinp=inputtext
            #     generated = gpt2.generate(
            #         sess,
            #         run_name='drama',
            #         prefix=textinp, 
            #         length=storylen,
            #         #temperature=1.2,
            #         #truncate=True,
            #         #top_p=0.65, 
            #         #top_k=96,
            #         return_as_list=True
            #         )[0].replace("\n","")
            # elif genre=='sci_fi':
            #     print("loading scifi model")
            #     gpt2.load_gpt2(sess, run_name='scifi')
            #     textinp=inputtext
            #     generated = gpt2.generate(
            #         sess,
            #         run_name='scifi',
            #         prefix=textinp, 
            #         length=storylen,
            #         #temperature=1.2,
            #         #truncate=True,
            #         #top_p=0.65, 
            #         #top_k=96,
            #         return_as_list=True
            #         )[0].replace("\n","")

            # prefix to the generate function to force the text to start with a given character sequence and generate text from there (good if you add an indicator when the text starts).
            # length: Number of tokens to generate (default 1023, the maximum)
            # temperature: The higher the temperature, the crazier the text (default 0.7, recommended to keep between 0.7 and 1.0)
            # top_k: Limits the generated guesses to the top k guesses (default 0 which disables the behavior; if the generated output is super crazy, you may want to set top_k=40)
            # top_p: Nucleus sampling: limits the generated guesses to a cumulative probability. (gets good results on a dataset with top_p=0.9)
            # truncate: Truncates the input text until a given sequence, excluding that sequence (e.g. if truncate='<|endoftext|>', the returned text will include everything before the first <|endoftext|>). It may be useful to combine this with a smaller length if the input texts are short.
# include_prefix: If using truncate and include_prefix=False, the specified prefix will not be included in the returned text
            #gpt2.reset_session(sess)
            # return generated

# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()
# lottie_url_hello = "https://assets4.lottiefiles.com/packages/lf20_pnpeymnv.json"
# lottie_hello = load_lottieurl(lottie_url_hello)
# st_lottie(lottie_hello, key="GeneratorStory")
pageno=st.sidebar.selectbox('Choose generator type',["Model Based","Pipeline Based(Huggingface)"])
if pageno=="Pipeline Based(Huggingface)":
    page=1
    st.title("GeneratorStory-Pipeline Based Text Generation")
    #story_gen = pipeline("text-generation", "pranavpsv/genre-story-generator-v2",max_length=400)
    with st.form('textgenform'):
        st.info("Optimal Story Generation at 150-250 words")
        story_start_with=st.text_input(label="Input your story prompt")
        story_length=st.slider("Maximum word length",min_value=50,max_value=400)
        genre=st.selectbox('Choose your genre:',('Horror','Drama','Scifi'))
        genre=genre.lower()
        if genre=="scifi":
            genre="sci_fi"
        
        submit=st.form_submit_button("Submit")
    if submit:
        #st.write("<DEBUGGING PURPOSES>Genre Chosen:",genre)
        textinp="<BOS> <"+genre+"> "+story_start_with
        #st.write("<DEBUGGING PURPOSES>Text input: ",textinp)
        with st.spinner(text=random.choice(messagetext)):
            errorcheck=True
            print("Generation starting:")
            while errorcheck:
                print("Generating........")
                generated=generateText(story_start_with,story_length,genre,page)
                print("Text generated:"+generated)
                if generated!=story_start_with:
                    st.write(generated)
                    nltk.download("punkt")
                    gensentences=tokenize.sent_tokenize(generated)
                    orisentences=tokenize.sent_tokenize(story_start_with)
                    st.write('BLEU score -> {}'.format(corpus_bleu([[x.split() for x in gensentences]] , [y.split() for y in orisentences])))
                    errorcheck=False
            #os.mkdir("temp")
            audio(generated)
            # input=tokenizer(textinp, add_special_tokens=False, return_tensors="pt")["input_ids"]
                    # prompt_length = len(tokenizer.decode(input[0]))
                    # outputs = model.generate(input, max_length=story_length, do_sample=True, top_p=0.95, top_k=60)
                    # generated = story_start_with + tokenizer.decode(outputs[0],skip_special_tokens=True)[prompt_length+1:]
                    # #horror_result= story_gen("<BOS> <horror> "+horror_start_with+ "Tell me what happens in the story and how the story ends.",max_length=horror_length)[0]['generated_text'].replace("<BOS> <horror> ","")
                    # st.write(generated)
if pageno=="Model Based":
    page=0
    #import gpt_2_simple as gpt2_simple

    st.title("GeneratorStory-Model Based Text Generation")
    # # story_gen = pipeline("text-generation", "pranavpsv/genre-story-generator-v2",max_length=400)
    #     st.info("Optimal Story Generation at 150-250 words")
    #     story_start_with=st.text_input(label="Input your story prompt")
    #     story_length=st.slider("Maximum word length",min_value=50,max_value=400)
    #     genre=st.selectbox('Choose your genre:',('Horror','Drama','Scifi'))
    #     genre=genre.lower()
    #     if genre=="scifi":
    #         genre="sci_fi"
    #     submit=st.form_submit_button("Submit")
    #     if submit:
    #         #st.write("<DEBUGGING PURPOSES>Genre Chosen:",genre)
    #         textinp=story_start_with
    #         #st.write("<DEBUGGING PURPOSES>Text input: ",textinp)
    #         with st.spinner(text=random.choice(messagetext)):
    #             errorcheck=True
    #             print("Generation starting:")
    #             while errorcheck:
    #                 print("Generating........")
    #                 generated=generateText(story_start_with,story_length,genre,page)
    #                 print("Text generated:"+generated)
    #                 if generated!=story_start_with:
    #                     st.write(generated)
    #                     #nltk.download("punkt")
    #                     #gensentences=tokenize.sent_tokenize(generated)
    #                     orisentences=tokenize.sent_tokenize(story_start_with)
    #                     st.write('BLEU score -> {}'.format(corpus_bleu([[x.split() for x in gensentences]] , [y.split() for y in orisentences])))   
    #                     errorcheck=False
    #         audio(generated)
    if "text" not in st.session_state:
        st.session_state.text=""
    def updatetext():
        st.session_state.text+=st.session_state.gentexted
    genre=st.selectbox('Choose your genre:',('Horror','Drama','Scifi','Comedy','Thriller','Adventure','Superhero','Romance'))
    genre=genre.lower()
    if genre=="scifi":
        genre="sci_fi"
    story_length=st.slider("Maximum word length",min_value=10,max_value=20)
    story_start_with=st.text_input(label="Input your story prompt(Plot)",key='text')
    generated=generateText(story_start_with,story_length,genre,page)
    print(generated)
    choice=st.radio("Choose one",generated,key="gentexted",on_change=updatetext)
    st.write(st.session_state.text)
    
    #audio(st.session_state.text)
    
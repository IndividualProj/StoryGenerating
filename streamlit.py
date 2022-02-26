from array import array
from cProfile import label
import streamlit as st
from transformers import pipeline,AutoTokenizer, AutoModelForCausalLM
import regex as re
import random
import gpt_2_simple as gpt2

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

def cleantext(text:str):
    
    text=text.replace('\'\'',"\"")
    text=text.replace('•',"(")
    text=text.replace('■',")")
    text=re.sub("[\(\[].*?[\)\]]", "", text)
    text=re.sub('<[^>]+>', '', text)
    return text

# @st.cache(suppress_st_warning=True)
def generateText(inputtext,storylen,genre,page):
    if page==0:
            #tokenizer = AutoTokenizer.from_pretrained("pranavpsv/genre-story-generator-v2")
            #model = AutoModelForCausalLM.from_pretrained("pranavpsv/genre-story-generator-v2")
            textinp="<BOS> <"+genre+"> "+inputtext+ "Tell me what happens in the story and how the story ends."
            story_gen=pipeline('text-generation',"pranavpsv/genre-story-generator-v2")
            generated= story_gen(textinp,max_length=storylen,top_k=96,temperature=1.2)[0]['generated_text'].replace("<BOS> <"+genre+"> ","").replace(" Tell me what happens in the story and how the story ends.","")
            print("method generated text:",generated)

            return(cleantext(generated))
    elif page==1:
            model = AutoModelForCausalLM.from_pretrained('./converted_model')
            print("Model:",model)
            tokenizer = AutoTokenizer.from_pretrained('gpt2')
            generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
            textinp="<BOS> <"+genre+"> "+inputtext+ "What happens in the story and how does the story end?"
            generated = generator(textinp, max_length=storylen,repetition_penalty=1.1,temperature=1.0,top_p=0.65, top_k=96)[0]['generated_text'].replace("\n","")
            #gpt2_simple.reset_session(sess)
            return cleantext(generated)


pageno=st.sidebar.selectbox('Choose generator type',["Pipeline Based(Huggingface)","Model Based"])
if pageno=="Pipeline Based(Huggingface)":
    page=0
    st.title("GeneratorStory-Pipeline Based Text Generation")
    #story_gen = pipeline("text-generation", "pranavpsv/genre-story-generator-v2",max_length=400)
    with st.form('textgenform'):
        story_start_with=st.text_input(label="Input your story prompt")
        story_length=st.slider("Maximum word length",min_value=50,max_value=400)
        genre=st.selectbox('Choose your genre:',('Horror','Drama','Scifi'))
        genre=genre.lower()
        if genre=="scifi":
            genre="sci_fi"
        
        submit=st.form_submit_button("Submit")
        if submit:
            st.write("<DEBUGGING PURPOSES>Genre Chosen:",genre)
            textinp="<BOS> <"+genre+"> "+story_start_with+ "Tell me what happens in the story and how the story ends."
            st.write("<DEBUGGING PURPOSES>Text input: ",textinp)
            with st.spinner(text=random.choice(messagetext)):
                errorcheck=True
                print("Generation starting:")
                while errorcheck:
                    print("Generating........")
                    generated=generateText(story_start_with,story_length,genre,page)
                    print("Text generated:"+generated)
                    if generated!=story_start_with:
                        st.write(generated)
                        errorcheck=False


                # input=tokenizer(textinp, add_special_tokens=False, return_tensors="pt")["input_ids"]
                # prompt_length = len(tokenizer.decode(input[0]))
                # outputs = model.generate(input, max_length=story_length, do_sample=True, top_p=0.95, top_k=60)
                # generated = story_start_with + tokenizer.decode(outputs[0],skip_special_tokens=True)[prompt_length+1:]
                # #horror_result= story_gen("<BOS> <horror> "+horror_start_with+ "Tell me what happens in the story and how the story ends.",max_length=horror_length)[0]['generated_text'].replace("<BOS> <horror> ","")
                # st.write(generated)
if pageno=="Model Based":
    page=1
    import gpt_2_simple as gpt2_simple

    st.title("GeneratorStory-Model Based Text Generation")
    # story_gen = pipeline("text-generation", "pranavpsv/genre-story-generator-v2",max_length=400)
    with st.form('modelgenform'):
        story_start_with=st.text_input(label="Input your story prompt")
        story_length=st.slider("Maximum word length",min_value=50,max_value=400)
        genre=st.selectbox('Choose your genre:',('Horror','Drama','Scifi'))
        genre=genre.lower()
        if genre=="scifi":
            genre="sci_fi"
        submit=st.form_submit_button("Submit")
        if submit:
            st.write("<DEBUGGING PURPOSES>Genre Chosen:",genre)
            textinp="<BOS> <"+genre+"> "+story_start_with+ "Tell me what happens in the story and how the story ends."
            st.write("<DEBUGGING PURPOSES>Text input: ",textinp)
            with st.spinner(text=random.choice(messagetext)):
                errorcheck=True
                print("Generation starting:")
                while errorcheck:
                    print("Generating........")
                    generated=generateText(story_start_with,story_length,genre,page)
                    print("Text generated:"+generated)
                    if generated!=story_start_with:
                        st.write(generated)
                        errorcheck=False


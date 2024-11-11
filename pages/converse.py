import base64, json, streamlit as st

import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

from googletrans import Translator

vision_client = ChatCompletionsClient(
    endpoint="https://Llama-3-2-11B-Vision-Instruct-ga.swedencentral.models.ai.azure.com",
    credential=AzureKeyCredential("credential"),
)


text_client = ChatCompletionsClient(
    endpoint="https://Meta-Llama-3-1-70B-Instruct-brjk.swedencentral.models.ai.azure.com",
    credential=AzureKeyCredential("credential"),
)

@st.cache_data
def describe(picture):
	bytes_data = picture.getvalue()
	base64_image = base64.b64encode(bytes_data).decode('utf-8')

	response = vision_client.complete(
	    messages=[
	    {
	      "role": "user",
	      "content": [
	        {"type": "text",
	          "text": "Give me a detailed utline of what this image contains.",},
	        {"type": "image_url",
	          "image_url": {
	            "url":  f"data:image/jpeg;base64,{base64_image}"},},
	      ],
	    }
	  ])
	     
	      
	return response.choices[0].message.content

@st.cache_data
def generate_sentences(caption):
	response = text_client.complete(
	    messages=[
	    {"role":"system", "content":"You are an AI Language Learning Instructor. You are provided with an an image caption, and are to generate 3 sentences describing contents of the image. "\
	    "Each of these sentences is to have one missing word (Note: Just one missing word per sentence) as <BLANK>. "\
	    "The words you blank out should be simple words which are easy to identify from looking at the concerned image. "\
	    "The user filling in the blanks can only see the image, not the caption. As described below, provide clues which could help the user identify the missing word, by studying the sentences you output and loking at the image. For example if the missing word is 'chair', the clue can be 'something people sit down on', or if it is 'red' the clue can be 'a bright colour'. The clues should only help the user in identifying the missing word - they shouldn't contain the word themselves. "\
	    'From the given caption, formulate 3 sentences, each with one missing word <BLANK> as described. Return your response as a JSON object in the form {"1":["word1 word2 <BLANK> word3 ...", "missing word", "short clue to help identify missing word"], "2":["word1 word2 word3 <BLANK> word4 ...", "missing word", "short clue to help identify missing word"], ...}'},
	    { "role": "user",
	      "content": f"Here is the caption: {caption}"}
	  ])
	     
	      
	return response.choices[0].message.content


def evaluate_response(sentence, entered_word, missing_word):
	response = text_client.complete(
	    messages=[
	    {"role":"system", "content":"You are an AI Language Learning Instructor. You are provided with a sentence describing an image, with one word missing from the sentence. "\
	    "You are also provided with the user's guess of what that missing word is, as well as the actual missing word. "\
	    "Given the context of the sentence, evaluate how similar the guessed word is to the missing word. If it is similar, output 'Yes', else output'No'. "\
	    "Output only Yes or No. Say nothing else."},
	    { "role": "user",
	      "content": f"Here is the sentence: {sentence}, here is the guessed word: {entered_word}, and here is the missing word: {missing_word}"}
	  ])
	      
	return response.choices[0].message.content



def translate(word, language='en'):
	translator = Translator()
	translation = translator.translate(word, dest=language)
	return translation.text

def translate_llamaindex(word, language):
	from llamaindex_module import query_engine
	string = 'Translate '+word+'to '+language
	response = query_engine.query(string)
	return response.response


st.title('Chat with Llama Lingo')

picture = st.session_state.picture
st.image(picture)

caption = describe(picture)
# caption

sentences = generate_sentences(caption)
# sentences

sentences = sentences[sentences.find('{'):sentences.find('}')+1]
# sentences = sentences.replace("'",'"')
sentences_dict = json.loads(sentences)

entered_words = {}
translated_entered_words = {}
missing_words = {}
translated_missing_words = {}
sentences = {}
evaluations = {}


st.header('Fill in the missing words: (in '+ st.session_state.language  +') 🙂')

with st.form("my_form"):
	for i in range(len(sentences_dict)):
		entry = list(sentences_dict.values())[i]
		sentence = entry[0].replace('<BLANK>','_________')
		sentences[i] = sentence
		sentence
		clue = entry[2]
		'(Clue: ', clue, ' )'
		entered_words[i]= st.text_input("Missing word: ", key=str(i))
		translated_entered_words[i] = translate(entered_words[i])
		missing_words[i] = entry[1]
		translated_missing_words[i] = translate(missing_words[i], language='es') #To be switched to translate_llamaindex in the case of low-resourced languages and custom language data.
		st.divider()
	st.session_state.sentences = sentences
	st.session_state.entered_words = entered_words
	st.session_state.missing_words = missing_words
	st.session_state.translated_missing_words = translated_missing_words
	submit = st.form_submit_button('Submit')

	
if submit: #st.button("Next"):
	# st.rerun()
	for i in range(len(sentences)):
		evaluations[i] = evaluate_response(sentences[i], translated_entered_words[i], missing_words[i])

	st.session_state.evaluations = evaluations
	st.switch_page("pages/evaluate.py")

# def encode_image(image_path):
#   with open(image_path, "rb") as image_file:
#     return base64.b64encode(image_file.read()).decode('utf-8')



# print(response)
# print(response.choices[0].message.content)  
# print(picture)


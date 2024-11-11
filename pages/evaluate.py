import os, json, datetime, streamlit as st

st.title('How did You Do?')

picture = st.session_state.picture
st.image(picture)
st.divider()


sentences = st.session_state.sentences
entered_words = st.session_state.entered_words
missing_words = st.session_state.missing_words
evaluations = st.session_state.evaluations
translated_missing_words = st.session_state.translated_missing_words



correct = 0
total = len(sentences)

for i in range(len(sentences)):
	'**Sentence:** ', sentences[i]
	evaluation = evaluations[i]
	if 'Yes' in evaluation:
		st.write('**Your answer:** :green[', entered_words[i], ']')
		correct+= 1
	else:
		st.write('**Your answer:** :red[', entered_words[i], ']')
		'**Actual answer:** ', translated_missing_words[i]
	st.divider()


st.write('**Score:** ', correct, ' out of ', total)



# print(os.listdir())
with open('performance_history.json', 'r') as f:
	history = json.load(f)
current_time = str(datetime.datetime.now())
# correct = list(evaluations.values()).count('Yes')

history['datetime'].append(current_time)
history['correct'].append(correct)
history['total'].append(total)
json.dump(history, open('performance_history.json', 'w'))



if st.button("Another Try"):
	st.switch_page("pages/capture.py")
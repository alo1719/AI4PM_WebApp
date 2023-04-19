import config
import joblib
import streamlit as st
import openai
from streamlit_chat import message
import os
openai.api_key = config.api_key

class Application:
    def __init__(self):
        st.title("Stress Detection")
        st.write("AI4PM Stress Detection Group")
        feature_array = st.text_input("Feature Array:")
        print(feature_array)
        if st.button("Predict"):
            try:
                feature_array = [float(x.strip().replace("[", "").replace("]", "")) for x in feature_array.split(",")]
                model = joblib.load("model.joblib")
                prediction = model.predict([feature_array])[0]
                st.write("Prediction: ", prediction)
            except Exception as e:
                st.write("Invalid feature array. Need 34 comma separated values.")

        #form
        with st.form(key='my_form'):
            name = st.text_input(label='What is your name?')
            gender = st.radio("What is your gender?", ('Male', 'Female', 'Other'))
            age = st.slider('How old are you?', min_value=0, max_value=140)
            mood = st.text_input(label='Please describe your current mood')
            submit = st.form_submit_button(label='Submit')

        #storing the chat
        if 'generated' not in st.session_state:
            st.session_state['generated'] = []
        if 'past' not in st.session_state:
            st.session_state['past'] = []
        if submit:
            description = ('hello, my name is ' + str(name) + ', my gender is ' +
             str(gender) + ', and I am ' + str(age) + ' years old. ' + 'My current mood is as follows: ' +
              str(mood) + '. Shall we have a conversation?')
            user_input=st.text_input("You:",key='input', value=description)
        else:
            user_input=st.text_input("You:",key='input')
        if user_input:
            completion=openai.Completion.create(
                engine='text-davinci-003',
                prompt=user_input,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.6,
            )
            output=completion.choices[0].text
            #store the output
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)
        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])-1, -1, -1):
                message(st.session_state["generated"][i], key=str(i))
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')


if __name__ == "__main__":
    app = Application()

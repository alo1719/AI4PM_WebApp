import joblib
import openai
import streamlit as st
import time
from streamlit_chat import message

import config

openai.api_key = config.api_key


class Application:
    def __init__(self):

        predefined = ["It sounds like you've had a tough day, and I know exactly how you feel. As a graduate student, you are dealing with a lot of academic tasks and stress, which can easily leave you feeling exhausted and overwhelmed.\n\nHowever, what you need to know is that rest and relaxation are also key to successful and productive work. When we work and study too hard, our bodies and brains need to rest to regain energy or we will feel exhausted. So, you can try some relaxation methods to relieve stress and fatigue.", "I know the pressures and difficulties you are facing on the path to your graduate degree. Please believe in yourself that you are already doing an excellent job. Always remember to maintain patience and perseverance in the face of difficulties and challenges. Also, don't forget to allow yourself time to rest and relax, which is equally important for physical and mental health."]

        if 'dialog_user' not in st.session_state:
            st.session_state['dialog_user'] = []
        if 'dialog_bot' not in st.session_state:
            st.session_state['dialog_bot'] = []
        if 'msgs' not in st.session_state:
            st.session_state['msgs'] = []
        if 'predefined_index' not in st.session_state:
            st.session_state['predefined_index'] = 0
        if 'name' not in st.session_state:
            st.session_state['name'] = 'User'
        if 'gender' not in st.session_state:
            st.session_state['gender'] = 'male'
        if 'age' not in st.session_state:
            st.session_state['age'] = '24'
        if 'profession' not in st.session_state:
            st.session_state['profession'] = 'student'
        if 'who' not in st.session_state:
            st.session_state['who'] = ''
        if 'what' not in st.session_state:
            st.session_state['what'] = ''
        if 'other' not in st.session_state:
            st.session_state['other'] = ''

        st.set_page_config(page_title="Stress Detection", page_icon=":sunglasses:", layout="wide")
        st.title("Stress Detection")
        st.write("AI4PM Stress Detection Group")

        st.write("")  # Blank line

        # Form
        with st.form(key='info'):
            name = st.text_input(label='What is your name?')
            gender = st.radio("What is your gender?", ('Male', 'Female', 'Other'))
            age = st.slider('How old are you?', min_value=0, max_value=100)
            profession = st.text_input(label='What is your profession?')
            who = st.text_input(label='Who would you like to talk to when you feel stressed and upset?')
            what = st.text_input(label='In what way would you prefer they communicate with you?')
            other = st.text_input(label='Other information:')
            info_button = st.form_submit_button(label='Submit')

        # Info button action
        if info_button:
            st.session_state['name'] = str(name)
            st.session_state['gender'] = str(gender)
            st.session_state['age'] = str(age)
            st.session_state['profession'] = str(profession)
            st.session_state['who'] = str(who)
            st.session_state['what'] = str(what)
            st.session_state['other'] = str(other)

        st.write("")  # Blank line

        # Prediction
        with st.form(key='prediction'):
            feature_array = st.text_input("Feature Array:")
            pred_button = st.form_submit_button(label='Predict')

        # Prediction button action
        if pred_button:
            try:
                feature_array = [float(x.strip().replace("[", "").replace("]", "")) for x in feature_array.split(",")]
                model = joblib.load("model.joblib")
                prediction = model.predict([feature_array])[0]
                if prediction == 'interruption' or prediction == 'time pressure':
                    st.session_state['dialog_bot'].append("You are experiencing {}! {}, how are you doing? I hope everything is going well in your life! You can tell me what you want to share and I will listen with patience and understanding and share advice and ideas with you. We can chat, share our feelings or discuss something that interests you, whether it's a light-hearted topic or something about your education or life.".format(prediction, st.session_state['name']))
                else:
                    st.write("You are not experiencing any stress.")
            except Exception as e:
                print(e)
                st.write("Invalid feature array. Need 34 comma separated values.")

        user_input = st.text_input("You:", key='input')
        
        if user_input:
            user_input_object = {"role": "user", "content": user_input}
            st.session_state['msgs'].append(user_input_object)
            if len(user_input) >= 2 and user_input[-2:] == "  " and st.session_state['predefined_index'] < len(predefined):
                output = predefined[st.session_state['predefined_index']]
                st.session_state['predefined_index'] += 1
                time.sleep(0.75)
            else:
                chat = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=st.session_state['msgs'],
                )
                output = chat.choices[0].message.content
                st.session_state['msgs'].append(chat.choices[0].message)
            st.session_state['dialog_user'].append(user_input)
            st.session_state['dialog_bot'].append(output)
        
        if st.session_state['dialog_bot']:
            if st.session_state['dialog_bot'] == st.session_state['dialog_user']:
                for i in range(len(st.session_state['dialog_bot'])-1, -1, -1):
                    message(st.session_state["dialog_bot"][i], key=str(i))
                    message(st.session_state['dialog_user'][i], is_user=True, key=str(i) + '_user')
            else: # bot initiates
                for i in range(len(st.session_state['dialog_bot'])-1, 0, -1):
                    message(st.session_state["dialog_bot"][i], key=str(i))
                    message(st.session_state['dialog_user'][i-1], is_user=True, key=str(i) + '_user')
                message(st.session_state["dialog_bot"][0], key=str(0))

if __name__ == "__main__":
    app = Application()
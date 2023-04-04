import joblib
import streamlit as st

import openai
from streamlit_chat import message
import os
openai.api_key = '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'

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

        #storing the chat
        if 'generated' not in st.session_state:
            st.session_state['generated'] = []
        if 'past' not in st.session_state:
            st.session_state['past'] = []
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

    # def generate_response(prompt):
    #     completion=openai.Completion.create(
    #         engine='text-davinci-003',
    #         prompt=prompt,
    #         max_tokens=1024,
    #         n=1,
    #         stop=None,
    #         temperature=0.6,
    #     )
    #     message=completion.choices[0].text
    #     return message


if __name__ == "__main__":
    app = Application()

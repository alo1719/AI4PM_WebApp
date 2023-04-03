import joblib
import streamlit as st


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


if __name__ == "__main__":
    app = Application()

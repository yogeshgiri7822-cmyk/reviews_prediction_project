import streamlit as st
import pickle


# Load CountVectorizer
with open("cv", "rb") as f:
    cv = pickle.load(f)


# Load Logistic Regression Model
with open("lg", "rb") as f:
    model = pickle.load(f)


# App Title
st.set_page_config(page_title="Review Sentiment Predictor")
st.title("📝 Review Sentiment Prediction")
st.write("Enter a review and check whether it is Positive or Negative.")


# User Input
review = st.text_area("Enter Review Here")


# Predict Button
if st.button("Predict Sentiment"):


    if review.strip() == "":
        st.warning("Please enter a review.")
    else:


        # Convert text into vectors
        review_vector = cv.transform([review])


        # Prediction
        result = model.predict(review_vector)


        # Custom Logic for 'not'
        if "not" in review.lower():
            result[0] = 1 - result[0]


        # Probability (if supported)
        try:
            prob = model.predict_proba(review_vector)
            positive_prob = prob[0][1] * 100
            negative_prob = prob[0][0] * 100
        except:
            positive_prob = None
            negative_prob = None


        # Display Result
        if result[0] == 1:
            st.success("😊 Positive Review")
        else:
            st.error("😞 Negative Review")


        # Display Probabilities
        if positive_prob is not None:
            st.subheader("Prediction Confidence")
            st.write(f"Positive: {positive_prob:.2f}%")
            st.write(f"Negative: {negative_prob:.2f}%")

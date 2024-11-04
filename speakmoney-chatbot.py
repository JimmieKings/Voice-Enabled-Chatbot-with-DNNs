import streamlit as st
import speech_recognition as sr #handles speech-to-text transcription
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary NLTK resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Load and preprocess text data from "The Richest Man in Babylon"
def load_text_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def preprocess_text(text):
    from nltk.corpus import stopwords
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.stem import WordNetLemmatizer
    
    sentences = sent_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))
    cleaned_sentences = []

    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        words = [lemmatizer.lemmatize(word) for word in words if word.isalpha() and word not in stop_words]
        cleaned_sentences.append(" ".join(words))
    
    return sentences, cleaned_sentences

# chatbot response function with keywords matching
def chatbot_response(user_input):
    # Dictionary defining the principles and associated keywords from the book.
    principles = {
        "start thy purse to fattening": {
            "keywords": ["save", "income", "budget", "savings", "fattening", "portion"],
            "advice": "Save at least 10% of what you earn to build wealth over time. This is the foundation of growing your wealth."
        },
        "control thy expenditures": {
            "keywords": ["spend", "expenses", "control", "budget", "waste", "expenditures"],
            "advice": "Avoid unnecessary expenses and live within your means to increase your savings."
        },
        "make thy gold multiply": {
            "keywords": ["invest", "growth", "multiply", "return", "interest", "gold"],
            "advice": "Invest your money wisely so that it can generate returns. Consider safe investments that grow over time."
        },
        "guard thy treasures from loss": {
            "keywords": ["loss", "protect", "secure", "risk", "treasures", "safeguard"],
            "advice": "Be cautious with your investments. Avoid get-rich-quick schemes and focus on steady, reliable investments."
        },
        "make of thy dwelling a profitable investment": {
            "keywords": ["home", "house", "dwelling", "investment", "property"],
            "advice": "Own your home to reduce living costs over time and to provide long-term security."
        },
        "insure a future income": {
            "keywords": ["future", "income", "retirement", "pension", "security", "old age"],
            "advice": "Plan for your retirement and old age by setting aside money for the future."
        },
        "increase thy ability to earn": {
            "keywords": ["earn", "skills", "career", "education", "ability", "income"],
            "advice": "Continue to improve your skills and knowledge to increase your income potential."
        }
    }

    user_input = user_input.lower()
    
    # Loop through principles to find matching keywords
    for principle, data in principles.items():
        for keyword in data["keywords"]:
            if keyword in user_input:
                return data["advice"]

    return "The Richest Man in Babylon recommends building wealth gradually. Start by saving a portion of your income, controlling expenses, and making wise investments."

# Speech recognition function
def transcribe_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak now.")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError as e:
            return f"API error: {str(e)}"

# Streamlit app layout
def main():
    st.title("💸 SpeakMoney Chatbot")
    st.write("""
        Welcome to the SpeakMoney Chatbot! Ask questions about budgeting, saving, and personal finance tips.
        The advice here is inspired by **The Richest Man in Babylon**, a classic book on personal finance principles.
    """)
    
    # User input for text or speech
    st.header("Chat with the SpeakMoney Bot 🤖")
    user_input = st.text_input("Type your question here:")
    if st.button("Speak"):
        user_input = transcribe_speech()
        st.write("You said:", user_input)
    
    # Process and respond to input
    if user_input:
        with st.spinner("Thinking..."):
            response = chatbot_response(user_input)
        st.success("Here's some advice:")
        st.write(response)
    
    # Sidebar tips section
    st.sidebar.title("💡 Financial Tips")
    st.sidebar.write("🔸 Save a fixed percentage of your income each month.")
    st.sidebar.write("🔸 Avoid unnecessary debt.")
    st.sidebar.write("🔸 Invest wisely to grow your wealth.")
    st.sidebar.write("🔸 Track expenses and create a budget.")

if __name__ == "__main__":
    main()

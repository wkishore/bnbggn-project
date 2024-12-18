import streamlit as st
from pathlib import Path
from generate_json import give_json
from text_extraction import detect_document
from search_agent_response import answer_query_sample

def process_image(image_path):
    text = detect_document(image_path)
    structed_out = give_json(text)
    return structed_out

def main():
    st.set_page_config(page_title="MediSage", layout="wide")

    st.title("MediSage: Upload prescriptions and get answers in your language ")

    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to:", ["Home", "Chat Interface"])

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "page" not in st.session_state:
        st.session_state.page = "Home"

    # Navigation
    if st.session_state.page == "Home":
        #st.title("Document Processor & Chat Interface")
        st.subheader("Upload a Document")
        uploaded_file = st.file_uploader("Choose a JPEG or PDF file", type=["jpeg", "jpg", "pdf"])

        if uploaded_file is not None:
            # Save the uploaded file temporarily
            file_path = Path("uploaded_file")
            file_path.write_bytes(uploaded_file.read())

            # Call your image processing function
            result = process_image(file_path)
            st.session_state.processed_content = result  # Save the result in session state

            print(st.session_state.processed_content)
            
            st.success("File processed successfully!")
            st.write("Result:", result)

            #st.button("Go to Chat Interface", on_click=lambda: st.sidebar.radio("Go to:", ["Chat Interface"]))

            if st.button("Go to Chat Interface"):
                st.session_state.page = "Chat Interface"

    elif st.session_state.page == "Chat Interface":
        st.title("Chat Interface")

        if "processed_content" in st.session_state:
            st.write("Processed Content:", st.session_state.processed_content)

            user_input = st.text_input("Enter your message:")
            if user_input:
                preamble = "Given the following information about the user, "+ str(st.session_state.processed_content)+"answer the question "
                #print(prompt)
                response = answer_query_sample(preamble,user_input)
                st.session_state.chat_history.append((user_input, response))

        # Display chat history
        for user_msg, bot_msg in st.session_state.chat_history:
            st.write(f"You: {user_msg}")
            st.write(f"Bot: {bot_msg}")

        if st.button("Go Back to Home"):
            st.session_state.page = "Home"

if __name__ == "__main__":
    main()

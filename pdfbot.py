import streamlit as st
import pdfplumber

# Function to extract text from PDF using pdfplumber
def extract_text_from_pdf(file):
    pdf_text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            pdf_text += page.extract_text()
    return pdf_text

# Function to simulate a chatbot response
def get_chatbot_response(prompt, pdf_text):
    # In a real application, you would integrate with an AI model or service.
    # For demonstration, we'll use a simple search-based response.
    if prompt.lower() in pdf_text.lower():
        return "Yes, I found information related to your query in the PDF."
    else:
        return "Sorry, I couldn't find relevant information in the PDF."

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to handle submission from input box or button
def handle_submit():
    user_query = st.session_state.user_input
    if user_query:
        # Get chatbot response
        response = get_chatbot_response(user_query, pdf_text)

        # Append the new interaction to the chat history
        st.session_state.chat_history.append({"user": user_query, "bot": response})

        # Clear input field after submission
        st.session_state.user_input = ""

# Streamlit UI
st.title("🤖 :green[P]:orange[D]:red[F]Bot")
st.markdown('''Upload a :green[PDF] and ask questions about its content. :rocket:''')

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Extract text from the uploaded PDF
    pdf_text = extract_text_from_pdf(uploaded_file)
    
    st.write("PDF content extracted successfully.")
    
    # Display chat history above the input bar
    if st.session_state.chat_history:
        st.write("Chat History:")
        for chat in st.session_state.chat_history:
            st.write(f"**User**: {chat['user']}")
            st.write(f"**Bot**: {chat['bot']}")

    # Input field that triggers submission on Enter key press
    st.text_input("Ask a question about the PDF content:", 
                  key="user_input", 
                  on_change=handle_submit)

    # Submit button
    if st.button("Submit"):
        handle_submit()

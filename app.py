"""Main Streamlit application for the Medical Report Assistant."""

import streamlit as st
import uuid
import logging

# Import custom modules
from config.settings import STREAMLIT_CONFIG
from services import MedicalReportParser, SecurityManager, MedicalChatbot
from utils.helpers import (
    format_lab_results_dataframe,
    create_status_styler,
    get_medical_disclaimer,
    get_privacy_notice
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'lab_results' not in st.session_state:
        st.session_state.lab_results = None


def setup_sidebar(security_manager: SecurityManager) -> tuple:
    """Setup the sidebar with configuration options."""
    with st.sidebar:
        st.header("Configuration")

        # OpenAI API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key"
        )

        if not api_key:
            st.warning("Please enter your OpenAI API key to use the chatbot.")
            return None, None

        st.header("Privacy & Security")
        st.info("🔒 HIPAA Compliance Features:")

        privacy_features = security_manager.get_privacy_info()
        for feature in privacy_features:
            st.markdown(f"- {feature}")

        # Sample data toggle
        use_sample_data = st.checkbox("Use Sample Lab Data", value=False)

        if st.button("Clear Session", type="primary"):
            # Clear all session state variables
            st.session_state.chat_history = []
            st.session_state.lab_results = None
            st.session_state.session_cleared = True

            # Generate new session ID
            st.session_state.session_id = str(uuid.uuid4())

            # Also clear any other session state variables that might exist
            keys_to_clear = ['suggested_query']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]

            # Force a complete rerun
            st.success("Session cleared successfully!")
            st.rerun()

    return api_key, use_sample_data


def display_lab_results_overview(lab_results, chatbot):
    """Display the lab results overview section."""
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Lab Results Overview")

        # Create and display results dataframe
        df = format_lab_results_dataframe(lab_results)

        if not df.empty:
            # Apply styling
            styled_df = df.style.applymap(
                create_status_styler(),
                subset=['Status']
            )
            st.dataframe(styled_df, use_container_width=True)
        else:
            st.info("No lab results to display.")

    with col2:
        st.header("Quick Insights")
        insights = chatbot.get_quick_insights(lab_results)

        st.metric("Normal Results", insights['normal'])
        st.metric("Borderline Results", insights['borderline'])
        st.metric("Abnormal Results", insights['abnormal'])

        if insights['critical'] > 0:
            st.metric("Critical Results", insights['critical'])
            st.error("⚠️ Critical results detected! Consult your healthcare provider immediately.")


def handle_chat_interface(chatbot, lab_results):
    """Handle the chat interface functionality."""
    st.header("Ask Questions About Your Results")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask about your lab results..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.write(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your question..."):
                response = chatbot.process_query(
                    prompt,
                    lab_results,
                    st.session_state.session_id
                )
            st.write(response)

        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})


def display_suggested_questions(chatbot, lab_results):
    """Display suggested questions section."""
    st.header("Suggested Questions")

    suggested_questions = chatbot.get_suggested_questions()

    # Display questions in columns
    cols = st.columns(3)
    for i, question in enumerate(suggested_questions[:6]):  # Display first 6 questions
        col_idx = i % 3
        with cols[col_idx]:
            if st.button(question, key=f"suggested_{i}"):
                st.session_state.suggested_query = question

    # Handle suggested queries
    if 'suggested_query' in st.session_state:
        query = st.session_state.suggested_query
        del st.session_state.suggested_query

        st.session_state.chat_history.append({"role": "user", "content": query})

        response = chatbot.process_query(
            query,
            lab_results,
            st.session_state.session_id
        )

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()


def main():
    """Main application function."""
    # Configure Streamlit page
    st.set_page_config(**STREAMLIT_CONFIG)

    # Initialize components
    initialize_session_state()
    security_manager = SecurityManager()
    parser = MedicalReportParser()

    # App header
    st.title("🏥 Medical Report Assistant")
    st.subheader("HIPAA-Compliant Lab Result Interpretation")

    # Setup sidebar and get configuration
    api_key, use_sample_data = setup_sidebar(security_manager)

    if not api_key:
        st.info("👈 Please enter your OpenAI API key to use the chatbot.\
                    Your API key is used only for this session and is not stored permanently.\
                    Once you close the chat or refresh the page, the key will be discarded,\
                    ensuring your privacy and security.")
        return

    try:
        # Initialize chatbot
        chatbot = MedicalChatbot(api_key)

        # Load lab results
        if use_sample_data and st.session_state.lab_results is None:
            st.session_state.lab_results = parser.parse_sample_report()

        if st.session_state.lab_results:
            # Display medical disclaimer
            st.warning(get_medical_disclaimer())

            # Display lab results overview
            display_lab_results_overview(st.session_state.lab_results, chatbot)

            # Chat interface
            handle_chat_interface(chatbot, st.session_state.lab_results)

            # Suggested questions
            display_suggested_questions(chatbot, st.session_state.lab_results)

        else:
            st.info("Please enable 'Use Sample Lab Data' in the sidebar to get started.")
            st.info(get_privacy_notice())

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An error occurred while initializing the application. Please refresh the page and try again.")


if __name__ == "__main__":
    main()
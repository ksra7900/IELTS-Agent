import streamlit as st
from components.question_generator import speaking_question_generator, writing_question_generator
from components.tools import update_writing_report, get_writing_report
from components.evaluator import evaluate_writing_answer

def show_home_page():
    st.title(f"Welcome {st.session_state.current_user}")
    st.write("Here, you can improve your English skill with AI for IELTS exam!")

'''
=================
This page isn't available !
=================
'''
def show_speaking_page():
    st.header("🗣️ IELTS Speaking Practice")
    # List of common IELTS topics
    common_topics = ["Work", "Study", "Hometown", "Travel", "Technology", "Food", "Hobbies", "Environment", "Family"]
    
    # Use session state to hold the current question
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None

    # Controls for generating a new question
    col1, col2, col3 = st.columns([2, 1, 1.5])
    with col1:
        selected_topic = st.selectbox("Choose a topic:", common_topics, index=0)
    with col2:
        selected_part = st.selectbox("Choose a part:", [1, 2, 3], index=0)
    with col3:
        if st.button("Generate New Question", use_container_width=True):
            with st.spinner("Generating a new question..."):
                st.session_state.current_question = speaking_question_generator(selected_topic, selected_part)

    st.divider()

    # Display the generated question
    if st.session_state.current_question:
        q_data = st.session_state.current_question
        st.subheader(f"Part {q_data['part']} Question | Topic: {q_data['topic']}")

        if q_data['part'] == 1:
            for i, q in enumerate(q_data['questions']):
                st.write(f"**Q{i+1}:** {q}")
        
        elif q_data['part'] == 2:
            st.markdown("##### **Describe " + q_data['questions']['cue_card_topic'] + ".**")
            st.markdown("You should say:")
            for point in q_data['questions']['cue_card_points']:
                st.markdown(f"- {point}")
            st.info("You will have 1 to 2 minutes to talk about this topic. You have 1 minute to think about what you are going to say.")

        elif q_data['part'] == 3:
            for i, q in enumerate(q_data['questions']):
                st.write(f"**Q{i+1}:** {q}")
    else:
        st.info("Click 'Generate New Question' to start your practice.")

def show_writing_page():
    st.header("✍️ IELTS Writing Practice")
    st.write("Select a task and topic, then generate a question to start practicing.")
    
    # List of common IELTS topics
    common_topics = ["Work", "Study", "Hometown", "Travel", "Technology", "Food", "Hobbies", "Environment", "Family"]

    # Initialize session state to hold the question
    if 'writing_question' not in st.session_state:
        st.session_state.writing_question = None

    # --- User Input Section ---
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            task_type = st.selectbox(
                "Select Task Type",
                ("Short Opinion Essay", "Describe a Memory or Place", "Write a Friendly Email"),
                key="writing_task_type"
            )
        with col2:
            topic = st.selectbox("Choose a topic:", common_topics, index=0)

        if st.button("Generate New Question", use_container_width=True, type="primary"):
            with st.spinner("Generating an authentic IELTS question for you..."):
                # Call the generation function and store the result in session state
                st.session_state.writing_question = writing_question_generator(task_type, topic)

    # --- Display Question Section ---
    if st.session_state.writing_question:
        question = st.session_state.writing_question
        st.divider()

        st.subheader(f"Your Question: {question.get('task_type', '')} - {question.get('topic', '')}")

        # If it's an Academic Task 1, show the data description
        if "Academic Task 1" in question.get('task_type', '') and question.get('data_description'):
            st.info(f"**Chart/Graph Description:**\n\n{question['data_description']}")

        # Display the main question prompt
        st.markdown(question.get('prompt_text', ''))

        st.divider()

        # Add a text area for the user's answer
        st.subheader("Your Answer")
        user_answer = st.text_area(
            "Write your essay here. Aim for the recommended word count.",
            height=300,
            key="writing_answer_box"
        )
        include_band8 = st.checkbox(
            "Also generate a Band 8 version",
            value=True,
            key="include_band8_version"
        )

        # This is where the evaluation logic will be triggered later
        if st.button("Submit for Evaluation", use_container_width=True):
            if len(user_answer.split()) < 50:
                st.warning("Your response seems too short. Please write a more detailed essay before submitting.")
                return
        
            user_id = st.session_state.get("current_user_id")
        
            if not user_id:
                st.error("User ID not found. Please log in again.")
                return
        
            previous_report = get_writing_report(user_id)
        
            with st.spinner("Evaluating your writing..."):
                evaluation = evaluate_writing_answer(
                    question=question,
                    user_answer=user_answer,
                    previous_report=previous_report,
                    include_band8=include_band8
                )
        
            if evaluation:
                new_report = evaluation.get("new_report", "")
        
                if new_report:
                    update_writing_report(user_id, new_report)
        
                st.success("Your writing has been evaluated!")
        
                st.subheader("Estimated IELTS Band")
                band = evaluation.get("band_estimate", {})
                st.write(f"**Overall:** {band.get('overall', 'N/A')}")
        
                with st.container(border=True):
                    st.markdown("### Feedback")
        
                    feedback = evaluation.get("feedback", {})
        
                    st.markdown("**Strengths:**")
                    for item in feedback.get("strengths", []):
                        st.write(f"- {item}")
        
                    st.markdown("**Main Problems:**")
                    for item in feedback.get("main_problems", []):
                        st.write(f"- {item}")
        
                    st.markdown("**Next Steps:**")
                    for item in feedback.get("next_steps", []):
                        st.write(f"- {item}")
        
                with st.expander("Corrected Version"):
                    st.write(evaluation.get("corrected_text", ""))
        
                band8_version = evaluation.get("band_8_version", "")
                if band8_version:
                    with st.expander("Band 8 Version"):
                        st.write(band8_version)
        
                with st.expander("Error Examples"):
                    for err in evaluation.get("error_examples", []):
                        st.markdown(f"**Original:** {err.get('original', '')}")
                        st.markdown(f"**Corrected:** {err.get('corrected', '')}")
                        st.markdown(f"**Reason:** {err.get('reason', '')}")
                        st.divider()
        
                with st.expander("Updated Writing Report"):
                    st.write(new_report)
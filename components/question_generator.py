import streamlit as st
from components.tools import load_API
import json

# load API key
client= load_API()

def speaking_question_generator(topic: str, part: int):
    """
    Generates IELTS speaking questions for a given topic and part using an AI model.

    Args:
        topic (str): The topic for the questions (e.g., "Travel", "Technology").
        part (int): The part of the speaking test (1, 2, or 3).

    Returns:
        dict: A dictionary containing the generated questions in a structured format, or None if an error occurs.
    """
    if not client:
        return None
    
    # prompts
    system_prompt = """
        You are an expert IELTS examiner and content creator. Your task is to generate high-quality, 
        realistic IELTS Speaking questions. You must provide the output in a structured JSON format.
        """
    
    user_prompt = f"""
        Generate IELTS Speaking questions for the following criteria:
        - Topic: "{topic}"
        - Part: {part}
    
        The JSON output should contain the following keys: "part", "topic", and "questions".
        - For Part 1, the "questions" value should be a list of 4-5 introductory questions.
        - For Part 2, the "questions" value should be a JSON object containing "cue_card_topic" and "cue_card_points" (a list of 3-4 points the candidate should talk about).
        - For Part 3, the "questions" value should be a list of 4-5 abstract, discussion-style questions that follow up on the Part 2 topic.
        """
        
    try:
        response= client.chat.completions.create(
            model="Qwen3-30B-A3B-ytxpc", 
            messages=[
                {"role" : "system", "content" : system_prompt},
                {"role" : "user", "content" : user_prompt}
                ],
            temperature=0.8,
            response_format={"type" : "json_object"}
            )
        questions_data = json.loads(response.choices[0].message.content)
        return questions_data
   
    except Exception as e:
        st.error(f"An error occurred while generating the question: {e}")
        return None
    
def writing_question_generator(task_type, topic):
    # 2. Define the System and User Prompts
    system_prompt = """
    You are a friendly and encouraging English teacher. Your goal is to create interesting and accessible writing prompts for an intermediate English learner to help them practice and build confidence. The prompts should be clear, simple, and engaging. You must respond in a structured JSON format.
    """

    user_prompt_structure = {
      "instruction": "Generate a writing prompt based on the following specifications.",
      "specifications": {
        "task_type": task_type,
        "topic": topic
      },
      "output_format": {
        "task_type": "string (e.g., 'Short Opinion Essay', 'Describe a Memory or Place', 'Write a Friendly Email')",
        "topic": "string",
        "prompt_text": "string (The full question prompt for the student)"
      }
    }

    # 3. Call the API
    try:
        response = client.chat.completions.create(
            model="Qwen3-30B-A3B-ytxpc",  # A powerful and cost-effective model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_prompt_structure)}
            ],
            response_format={"type": "json_object"},
            temperature=0.8
        )
        # 4. Parse and return the JSON response
        question_data = json.loads(response.choices[0].message.content)
        return question_data
    
    except Exception as e:
        st.error(f"An error occurred while generating the question: {e}")
        return None
from components.tools import load_API
import streamlit as st
import json

# load API key
client= load_API()

def evaluate_writing_answer(
    question: dict,
    user_answer: str,
    previous_report: str = "",
    include_band8: bool = True
):
    """
    Evaluates the user's writing, corrects it, gives feedback,
    creates a compact updated report, and optionally writes a Band 8 version.
    """

    if not client:
        return None

    system_prompt = """
You are an expert IELTS Writing tutor.

Your job:
1. Correct the student's writing.
2. Give useful but concise feedback.
3. Estimate an IELTS writing band.
4. Create a short updated learner report.
5. If requested, write a Band 8 version of the student's answer.

Important rules:
- The new_report must REPLACE the previous report.
- Do NOT append to the previous report.
- Keep new_report compact.
- The Band 8 version should preserve the student's main ideas but improve grammar, vocabulary, coherence, and IELTS style.
- Return only valid JSON.
"""

    output_format = {
        "corrected_text": "Corrected version of the student's answer, preserving the original meaning.",
        "band_estimate": {
            "overall": "Estimated IELTS band as a string, e.g. 5.5",
            "task_response": "short comment",
            "coherence_cohesion": "short comment",
            "lexical_resource": "short comment",
            "grammar": "short comment"
        },
        "feedback": {
            "strengths": ["short bullet 1", "short bullet 2"],
            "main_problems": ["short bullet 1", "short bullet 2"],
            "next_steps": ["short bullet 1", "short bullet 2"]
        },
        "error_examples": [
            {
                "original": "student's sentence or phrase",
                "corrected": "corrected version",
                "reason": "short explanation"
            }
        ],
        "new_report": "A compact updated learner profile, max 90 words. This replaces the previous report."
    }

    if include_band8:
        output_format["band_8_version"] = "Rewrite the student's full answer as an IELTS Band 8 version."

    user_prompt = {
        "previous_writing_report": previous_report or "No previous report yet.",
        "current_question": question,
        "student_answer": user_answer,
        "include_band8_version": include_band8,
        "output_format": output_format
    }

    try:
        response = client.chat.completions.create(
            model="Qwen3-30B-A3B-ytxpc",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_prompt, ensure_ascii=False)}
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            max_tokens=1800
        )

        result = json.loads(response.choices[0].message.content)
        return result

    except Exception as e:
        st.error(f"An error occurred while evaluating the writing: {e}")
        return None
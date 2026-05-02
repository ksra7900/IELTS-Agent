# Prompt Design

This document explains the prompt design strategy used in the IELTS Writing Tutor Agent.

## Overview

The system uses Large Language Models (LLMs) for two main tasks:

1. Generating writing practice questions
2. Evaluating learner responses and producing personalized feedback

The main goal of the prompt design is not only to generate fluent text, but also to make the model return structured, reliable, and reusable outputs. For this reason, the system requests all model responses in JSON format.

---

## Question Generation Prompt

The question generation module creates writing prompts based on two user-selected inputs:

- Task type
- Topic

The model is instructed to behave as a friendly English teacher and generate clear, accessible, and engaging prompts for intermediate English learners.

The expected output contains:

```json
{
  "task_type": "Short Opinion Essay",
  "topic": "Technology",
  "prompt_text": "The full writing question for the student"
}

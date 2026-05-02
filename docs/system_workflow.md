```markdown
# System Workflow

This document explains the end-to-end workflow of the IELTS Writing Tutor Agent.

## Overview

The IELTS Writing Tutor Agent is an LLM-based educational application that helps learners practice IELTS writing. The system generates writing questions, evaluates user responses, provides feedback, estimates IELTS band scores, and updates a compact learner report stored in a database.

The main workflow is:

```text
User Login
    ↓
Select Writing Task and Topic
    ↓
Generate Writing Question
    ↓
Submit Writing Answer
    ↓
Load Previous Learner Report
    ↓
Evaluate Answer with LLM
    ↓
Display Feedback and Band Score
    ↓
Generate Band 8 Version
    ↓
Update Learner Report in Database

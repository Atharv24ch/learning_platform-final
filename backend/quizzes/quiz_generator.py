import os
import asyncio
import json
from pydantic import BaseModel, Field
from typing import List
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner

class QuizQuestion(BaseModel):
    question: str = Field(description="The quiz question")
    option_a: str = Field(description="Option A")
    option_b: str = Field(description="Option B")
    option_c: str = Field(description="Option C")
    option_d: str = Field(description="Option D")
    correct_answer: str = Field(description="Correct option (A, B, C, or D)")
    explanation: str = Field(description="Explanation of the correct answer")

class QuizSet(BaseModel):
    questions: List[QuizQuestion] = Field(description="List of quiz questions")

async def generate_quiz_async(topic, lesson_content, num_questions=5, difficulty="medium"):
    """Generate quiz using Google Gemini AI"""
    
    # Set API key (same as in ai_helpers.py)
    os.environ["GOOGLE_API_KEY"] = "AIzaSyDNVhp_qssFpi2qxtEDdE3uCB4FEmSTxsU"
    
    system_instruction = (
        "You are an expert educator creating quiz questions. "
        "Always respond ONLY with valid JSON matching this schema:\n\n"
        "{\n"
        '  "questions": [\n'
        '    {\n'
        '      "question": "string",\n'
        '      "option_a": "string",\n'
        '      "option_b": "string",\n'
        '      "option_c": "string",\n'
        '      "option_d": "string",\n'
        '      "correct_answer": "A|B|C|D",\n'
        '      "explanation": "string"\n'
        '    }\n'
        '  ]\n'
        "}\n"
    )

    root_agent = Agent(
        name="quiz_generator",
        model="gemini-2.5-flash-lite",
        description="An agent that generates educational quiz questions",
        instruction=system_instruction,
        tools=[]
    )
    
    runner = InMemoryRunner(agent=root_agent)
    
    prompt = (
        f"Generate {num_questions} multiple-choice questions about '{topic}' "
        f"at '{difficulty}' difficulty level.\n\n"
        f"Lesson Content:\n{lesson_content}\n\n"
        f"Requirements:\n"
        f"- Each question should have 4 options (A, B, C, D)\n"
        f"- Include detailed explanations for correct answers\n"
        f"- Questions should test understanding, not just memorization\n"
        f"- Vary the difficulty within the specified level\n\n"
        f"Remember: respond ONLY with JSON as described in the schema above."
    )
    
    # Run the agent (using run_debug like in ai_helpers.py)
    response = await runner.run_debug(prompt)
    
    # Extract the final response from ADK result
    clean_text = response[-1].content.parts[0].text.strip()
    
    # Strip Markdown fences if present
    if clean_text.startswith("```"):
        first_newline = clean_text.find("\n")
        last_ticks = clean_text.rfind("```")
        clean_text = clean_text[first_newline:last_ticks].strip()
    
    # Parse JSON to QuizSet
    quiz_data = json.loads(clean_text)
    return QuizSet(**quiz_data)

def generate_quiz(topic, lesson_content, num_questions=5, difficulty="medium"):
    """Synchronous wrapper for async quiz generation"""
    from asgiref.sync import async_to_sync
    
    # Use Django's async_to_sync to properly handle async code in sync context
    return async_to_sync(generate_quiz_async)(
        topic, lesson_content, num_questions, difficulty
    )

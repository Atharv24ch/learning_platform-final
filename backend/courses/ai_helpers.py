from dotenv import load_dotenv
import os
import asyncio
import json
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types



async def generate_learning_roadmap(topic: str, difficulty_level: str, duration_weeks: int):
    """
    Generate a detailed learning roadmap using Google ADK (Gemini) instead of LangChain.

    Requires:
    - GOOGLE_API_KEY set in your environment (for Gemini auth)
    - google-adk and google-genai installed
    """
    
    os.environ["GOOGLE_API_KEY"] = "AIzaSyDNVhp_qssFpi2qxtEDdE3uCB4FEmSTxsU"
    print("GOOGLE_API_KEY visible?", bool(os.getenv("GOOGLE_API_KEY")))
    system_instruction = (
        "You are an expert educational content designer. "
        "Given a topic, difficulty level, and duration, you create a structured learning roadmap. "
        "Always respond ONLY with valid JSON matching this schema:\n\n"
        "{\n"
        '  "title": "string",\n'
        '  "weeks": ["Week 1: ...", "Week 2: ...", ...],\n'
        '  "milestones": ["...", "..."],\n'
        '  "prerequisites": ["...", "..."]\n'
        "}\n"
    )

    root_agent = Agent(
    name="helpful_assistant",
    model="gemini-2.5-flash-lite",
    description="A simple agent that can make roapmaps",
    instruction=system_instruction,
    tools=[google_search],
    )
    # In-memory runner for local use
    runner = InMemoryRunner(agent=root_agent)
    prompt = (
        f"Create a comprehensive learning roadmap for '{topic}' at "
        f"'{difficulty_level}' level over {duration_weeks} weeks.\n"
        "Remember: respond ONLY with JSON as described in the schema above."
    )

    # Run the agent
    response = await runner.run_debug(prompt)

    # ADK's result.output is a string with the model's response
    clean = response[-1].content.parts[0].text.strip()

    # Strip Markdown `````` fences if present
    if clean.startswith("```"):
        first_newline = clean.find("\n")
        last_ticks = clean.rfind("```")
        clean = clean[first_newline:last_ticks].strip()

    # Now `clean` is the pure JSON
    roadmap = json.loads(clean)
    return roadmap


if __name__ == "__main__":
    
    roadmap = asyncio.run(generate_learning_roadmap("Python Programming", "Beginner", 10))
    print("Generated Roadmap:")
    print(json.dumps(roadmap, indent=2, ensure_ascii=False))
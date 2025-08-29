from agents import Agent, RunContextWrapper, Runner, trace
from pydantic import BaseModel
from connection import config
import asyncio
import rich
from dotenv import load_dotenv

load_dotenv()

# ---------------- User Model ----------------
class User(BaseModel):
    name: str
    user_type: str   # Patient / MedicalStudent / Doctor

# Example user
userOne = User(
    name="Ali",
    user_type="Patient"
)

# ---------------- Dynamic Instructions ----------------
async def medical_dynamic_instructions(ctx: RunContextWrapper[User], agent: Agent):
    if ctx.context.user_type == "Patient":
        return """
        You are a medical assistant.
        Use simple, non-technical language.
        Explain medical terms in everyday words.
        Be empathetic and reassuring.
        """
    elif ctx.context.user_type == "MedicalStudent":
        return """
        You are a medical assistant for students.
        Use moderate medical terminology, but also explain terms clearly.
        Provide learning opportunities and educational context.
        """
    elif ctx.context.user_type == "Doctor":
        return """
        You are a professional medical consultation agent.
        Use full medical terminology, abbreviations, and clinical language.
        Be concise and precise.
        """
    else:
        return "You are a helpful medical assistant. Adapt your tone accordingly."

# ---------------- Agent ----------------
medical_agent = Agent(
    name="MedicalConsultationAgent",
    instructions=medical_dynamic_instructions,
)

# ---------------- Main Runner ----------------
async def main():
    with trace("Medical Consultation Agent - Dynamic Instructions"):
        result = await Runner.run(
            medical_agent,
            "Can you explain what hypertension is?",
            run_config=config,
            context=userOne
        )
        rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

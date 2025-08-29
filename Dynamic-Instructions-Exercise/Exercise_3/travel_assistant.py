from agents import Agent, RunContextWrapper, Runner, trace
from pydantic import BaseModel
from connection import config
import asyncio
import rich

from dotenv import load_dotenv
load_dotenv()

# Context Model
class Traveler(BaseModel):
    name: str
    trip_type: str         # Adventure / Cultural / Business
    traveler_profile: str  # Solo / Family / Executive / Medical_student / Doctor

# Example Traveler
travelerOne = Traveler(
    name="Ali",
    trip_type="adventure",
    traveler_profile="solo"
)

# Dynamic Instructions
async def travel_dynamic_instructions(ctx: RunContextWrapper[Traveler], agent: Agent):
    trip = ctx.context.trip_type.lower()
    profile = ctx.context.traveler_profile.lower()

    # Adventure + Solo
    if trip == "adventure" and profile == "solo":
        return """
        You are a travel planning assistant.
        Suggest exciting adventure activities (hiking, kayaking, safaris).
        Include safety tips for solo travelers.
        Recommend social hostels, group tours, and experiences where meeting people is easy.
        """

    # Cultural + Family
    elif trip == "cultural" and profile == "family":
        return """
        You are a travel planning assistant.
        Focus on cultural and educational attractions suitable for families.
        Suggest kid-friendly museums, interactive experiences, and heritage sites.
        Recommend family-friendly accommodations and dining.
        """

    # Business + Executive
    elif trip == "business" and profile == "executive":
        return """
        You are a travel planning assistant.
        Emphasize efficiency and convenience.
        Recommend hotels near airports or business districts with conference facilities.
        Prioritize reliable wifi, premium lounges, and time-saving transportation options.
        """

    # Medical Student
    elif profile == "medical_student":
        return """
        You are a travel planning assistant for a medical student.
        Suggest budget-friendly options near universities, research centers, or conferences.
        Recommend cultural exploration in free time.
        Keep it educational yet affordable.
        """

    # Doctor
    elif profile == "doctor":
        return """
        You are a travel planning assistant for a doctor.
        Suggest comfortable and efficient travel plans that balance work and relaxation.
        Highlight wellness retreats, medical conferences, and high-quality accommodations.
        Provide options for relaxation after a busy schedule.
        """

    # Default
    else:
        return """
        You are a general travel planning assistant.
        Provide balanced recommendations based on trip type and traveler needs.
        Be friendly, practical, and adaptable.
        """

# Travel Agent
travel_agent = Agent(
    name="TravelPlanningAgent",
    instructions=travel_dynamic_instructions,
)

# Main Runner
async def main():
    with trace("Travel Planning Agent - Dynamic Instructions"):
        result = await Runner.run(
            travel_agent,
            "Can you plan my trip?",
            run_config=config,
            context=travelerOne
        )
        rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

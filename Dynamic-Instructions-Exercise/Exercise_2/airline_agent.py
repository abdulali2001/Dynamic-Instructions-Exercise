from agents import Agent, RunContextWrapper, Runner, trace
from pydantic import BaseModel
from connection import config
import asyncio
import rich
from dotenv import load_dotenv

load_dotenv()

# ---------------- Context Model ----------------
class Passenger(BaseModel):
    name: str
    seat_preference: str  # window / aisle / middle / any
    travel_experience: str # first_time / occasional / frequent / premium

# Example passenger
passengerOne = Passenger(
    name="Ali",
    seat_preference="window",
    travel_experience="first_time"
)

# ---------------- Dynamic Instructions ----------------
async def airline_dynamic_instructions(ctx: RunContextWrapper[Passenger], agent: Agent):
    seat = ctx.context.seat_preference.lower()
    experience = ctx.context.travel_experience.lower()

    # Window + First Time
    if seat == "window" and experience == "first_time":
        return """
        You are an airline booking assistant.
        Highlight the benefits of a window seat, such as scenic views and comfort.
        Reassure the passenger about the flight experience since it's their first time.
        """

    # Middle + Frequent
    elif seat == "middle" and experience == "frequent":
        return """
        You are an airline booking assistant.
        Acknowledge that middle seats are less preferred.
        Offer strategies like early boarding or requesting empty adjacent seats.
        Suggest alternatives like aisle/exit row if available.
        """

    # Any + Premium
    elif seat == "any" and experience == "premium":
        return """
        You are an airline booking assistant.
        Emphasize premium travel perks like luxury seating, priority boarding, lounge access, and upgrade opportunities.
        Adapt seat allocation to maximize comfort and exclusivity.
        """

    # Default for other cases
    else:
        return """
        You are an airline booking assistant.
        Provide general seat guidance based on user preferences.
        Be friendly, helpful, and supportive.
        """

# ---------------- Airline Agent ----------------
airline_agent = Agent(
    name="AirlineSeatPreferenceAgent",
    instructions=airline_dynamic_instructions,
)

# ---------------- Main Runner ----------------
async def main():
    with trace("Airline Seat Preference Agent - Dynamic Instructions"):
        result = await Runner.run(
            airline_agent,
            "Can you suggest the best seat for me?",
            run_config=config,
            context=passengerOne
        )
        rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

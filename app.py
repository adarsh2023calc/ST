import streamlit as st
from openai import OpenAI
import os

# OpenAI API key
client = OpenAI(api_key=os.getenv("openai_SECRET_KEY"))

# Function to get responses from OpenAI
def generate_response(prompts):
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=prompts)
    return response.choices[0].message.content

# Streamlit UI setup
st.title("AI-Powered Travel Planner")
st.write("Plan your perfect trip with a personalized itinerary!")

# Step 1: Initial Inputs
destination = st.text_input("Destination", placeholder="Where would you like to go?")
if destination:
    budget = st.selectbox("Budget", ["Low", "Moderate", "High"], index=1)
    no_of_members = st.number_input("Number of Members", min_value=1, value=1)
    duration = st.number_input("Trip Duration (in days)", min_value=1, max_value=30, value=3)
    purpose = st.text_input("Purpose of the Trip", placeholder="Adventure, relaxation, cultural, etc.")

    # Step 2: Follow-Up Questions
    if purpose:
        preferences = st.text_area(
            "Preferences",
            placeholder="Tell us about your interests, dietary restrictions, or mobility concerns.",
        )
        follow_up_questions = st.checkbox("Do you want to answer follow-up questions?")
        if follow_up_questions:
            st.write("Please answer the following:")
            activities = st.text_area(
                "What activities are you most excited about?",
                placeholder="E.g., hiking, museums, food tours, etc.",
            )
            accommodations = st.selectbox(
                "Preferred type of accommodation",
                ["Hotels", "Hostels", "Vacation Rentals", "Other"],
                index=0,
            )
            transportation = st.selectbox(
                "Preferred mode of local transportation",
                ["Public Transit", "Car Rental", "Biking", "Walking", "Other"],
                index=0,
            )

            # Add follow-up preferences to the main preferences
            if activities or accommodations or transportation:
                preferences += (
                    f"\nActivities: {activities}\n"
                    f"Accommodation: {accommodations}\n"
                    f"Transportation: {transportation}"
                )

    # Step 3: Generate Itinerary
    if st.button("Generate Itinerary"):
        if not destination or not purpose:
            st.error("Please provide at least a destination and the purpose of your trip.")
        else:
            # Build prompts for OpenAI
            system_prompt = {
                "role": "system",
                "content": (
                    "You are a travel planning assistant. Your goal is to gather details from users about their travel preferences and generate a highly personalized travel itinerary."
                ),
            }

            user_prompt = {
                "role": "user",
                "content": (
                    f"I want to plan a trip to {destination} with {no_of_members} members. "
                    f"My budget is {budget}. I will be staying for {duration} days. "
                    f"The purpose of my trip is {purpose}. My preferences are: {preferences}."
                ),
            }

            prompts = [system_prompt, user_prompt]

            with st.spinner("Generating your personalized itinerary..."):
                try:
                    itinerary = generate_response(prompts)
                    st.success("Here is your personalized itinerary:")
                    st.text_area("Itinerary", itinerary, height=300)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

st.write("---")
st.write("Developed with ❤️ using OpenAI and Streamlit by Adarsh Sudheer")

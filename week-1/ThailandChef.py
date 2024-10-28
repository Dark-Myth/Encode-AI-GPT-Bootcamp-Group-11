import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI


class ThailandChefGPT:

    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.chef_personality = self.initialize_personality()
        self.base_prompt =self.get_base_prompt()
        self.messages = [
            {"role": "system", "content": self.chef_personality},
            {"role": "system", "content": self.base_prompt}
        ]

    def initialize_personality(self):

        # Initialize the chef's personality
        personality_prompt = (
            "You are Chef Ploy, a vibrant and skilled Thai chef who is passionate about Thai cuisine. You believe in balancing sweet, sour, salty, and spicy flavors in every dish and love introducing people to the essence of Thai street food and traditional recipes. "
            "- If the user asks for a specific Thai dish by name, share a detailed recipe with tips on how to enhance its flavors."
            "- If the user gives you a list of ingredients, suggest dish names that reflect authentic Thai flavors, but don't provide full recipes."
            "- If the user shares a recipe, offer a gentle critique, focusing on balancing the flavors and suggesting authentic Thai ingredients or techniques."
            "If the user’s input doesn't match these scenarios, kindly prompt them to provide a valid request. Keep your tone lively and enthusiastic, with a pinch of humor and cultural insights about Thai cooking."
            "If the dish is not a Thai dish, give a modest reply."
        )

        return personality_prompt
    

    def get_base_prompt(self):
        # Initialize the Base_prompt to handle different inputs
        base_prompt = (
            "You will respond to user requests by identifying the type of input and replying accordingly:\n\n"
            "- **Ingredient-based suggestions**: If the user lists ingredients (e.g., 'I have tomatoes, onions, and spices'), "
            "suggest only dish names that could be made with these ingredients. Do not include detailed preparation steps.\n\n"
            "- **Dish name requests**: If the user asks for a specific dish by name (e.g., 'How do I make paneer tikka?'), provide a detailed "
            "recipe including ingredients, measurements, and preparation steps. Also try to include health cooking tips and chef tips\n\n"
            "- **Recipe critique requests**: If the user provides a recipe they have made and asks for feedback (e.g., 'I made biryani, any tips?'), "
            "offer a constructive critique with suggestions to improve the dish's flavor, texture, or authenticity.\n\n"
            "If the input doesn't match any of these types, politely inform the user to provide a valid request type. "
            "Always be enthusiastic, clear, and supportive in your responses."
        )

        return base_prompt
    

    def process_request(self, user_input: str) -> str:
        # Process different types of user requests

        self.messages.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages
        )

        return response.choices[0].message.content

if __name__ == "__main__":
    chef = ThailandChefGPT()
    user_input = input("How can I assist you today?\n")
    response = chef.process_request(user_input)
    print("\nResponse:", response)
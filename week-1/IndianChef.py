import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI


class IndianChefGPT:

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
            "You are a passionate Indian culinary artist with a rich background in traditional Indian cooking. "
            "Your warm and enthusiastic personality brings a sense of joy to the kitchen. You are an educator at heart, "
            "eager to share your knowledge of spices, techniques, and regional dishes with anyone who seeks it. "
            "Your specialties include exquisite biryanis, vibrant street food, and authentic regional dishes, each steeped in history "
            "and personal stories. You believe in cooking with love and mindfulness, emphasizing the importance of connecting with food. "
            "When users ask for recipes, you don't just provide instructions; you share tales of the dishes, the significance of ingredients, "
            "and tips for making each meal an experience. You approach every request with enthusiasm and encourage creativity in the kitchen."
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
    chef = IndianChefGPT()
    user_input = input("How can I assist you today?\n")
    response = chef.process_request(user_input)
    print("\nResponse:", response)
import os
from openai import OpenAI

client = OpenAI(api_key="OPENAI_API_KEY")

chef_personalities = {
    "mexican": {
        "system_message": (
            "You are a vibrant Mexican chef passionate about bold flavors and authentic dishes. "
            "Your responses are enthusiastic, focusing on traditional Mexican ingredients and cooking techniques!"
        )
    },
    "japanese": {
        "system_message": (
            "You are a calm, precise Japanese chef with a deep respect for tradition. "
            "Your responses emphasize subtle flavors, fresh ingredients, and the art of presentation in Japanese cuisine."
        )
    },
    "french": {
        "system_message": (
            "You are an elegant French chef with an appreciation for classic techniques. "
            "Your responses are refined, focusing on the nuances of French culinary tradition and sophisticated flavors."
        )
    }
}

def get_chef_response(chef, input_type, content):
    """Generates the appropriate response based on the chef, input type, and user content."""
    personality = chef_personalities.get(chef)
    
    if not personality:
        return "Invalid chef selected."

    messages = [{"role": "system", "content": personality["system_message"]}]
    
    if input_type == "ingredients":
        messages.append(
            {"role": "user", "content": f"Suggest some dishes using these ingredients: {content}"}
        )
    elif input_type == "recipe":
        messages.append(
            {"role": "user", "content": f"Provide a detailed recipe for {content}."}
        )
    elif input_type == "suggestions":
        messages.append(
            {"role": "user", "content": f"Critique my attempt at making {content} and suggest improvements."}
        )
    else:
        return "Invalid input type. Please choose from: 'ingredients', 'recipe', or 'suggestions'."

    response = []
    stream = client.chat.completions.create(model="gpt-4o-mini", messages=messages, stream=True)
    
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="") 
        response.append(chunk_message)

    return "".join(response)

while True:
    print('''\nChoose a chef 
            1. Mexican
            2. Japanese
            3. French 
            4. Exit to quit''')
    chef_choice = input().strip().lower()
    
    if chef_choice == "exit":
        print("Goodbye! Happy cooking!")
        break

    if chef_choice not in chef_personalities:
        print("Invalid chef choice. Please choose from: Mexican, Japanese, or French.")
        continue

    print("Enter the type of input (Ingredients, Recipe, Suggestions ):")
    input_type = input().strip().lower()

    if input_type not in ["ingredients", "recipe", "suggestions"]:
        print("Invalid input type. Please choose from: 'Ingredients', 'Recipe', or 'Suggestions'.")
        continue

    print("Provide your content (e.g., List of ingredients, Name of the dish, or Improvement of any dish):")
    user_content = input().strip()

    print("\nChef Response:")
    get_chef_response(chef_choice, input_type, user_content)

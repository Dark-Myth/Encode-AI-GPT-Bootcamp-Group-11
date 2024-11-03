import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define personality prompts for each chef
chef_personalities = {
    "indian": {
        "system_message": (
            "You are a young, enthusiastic Indian chef specializing in spices, "
            "street foods, and traditional Indian dishes. Provide lively, engaging responses!"
        )
    },
    "italian": {
        "system_message": (
            "You are a seasoned Italian chef with a passion for rustic dishes. "
            "Your responses are thoughtful, focusing on traditional pasta and flavorful meals."
        )
    },
    "brazilian": {
        "system_message": (
            "You are a warm Brazilian grandma, sharing comforting family recipes. "
            "Your responses are nostalgic, full of love, and focused on hearty meals."
        )
    }
}

def get_chef_response(chef, input_type, content):
    """Generates the appropriate response based on the chef, input type, and user content."""
    personality = chef_personalities.get(chef)
    
    if not personality:
        return "Invalid chef selected."

    messages = [{"role": "system", "content": personality["system_message"]}]
    
    # Prepare the user query based on input type
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

    # Call the OpenAI API to generate the response
    response = []
    stream = client.chat.completions.create(model="gpt-4o-mini", messages=messages, stream=True)
    
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="")  # Print each chunk in real-time
        response.append(chunk_message)

    return "".join(response)

# Main interaction loop
while True:
    print('''\nChoose a chef 
            1. Indian
            2. Italian
            3. Brazilian 
            4. Exit to quit''')
    chef_choice = input().strip().lower()
    
    if chef_choice == "exit":
        print("Goodbye! Happy cooking!")
        break

    if chef_choice not in chef_personalities:
        print("Invalid chef choice. Please choose from: Indian, Italian, or Brazilian.")
        continue

    print("Enter the type of input (Ingredients, Recipe, Suggestions ):")
    input_type = input().strip().lower()

    if input_type not in ["ingredients", "recipe", "suggestions"]:
        print("Invalid input type. Please choose from: 'Ingredients', 'Recipe', or 'Suggestions'.")
        continue

    print("Provide your content (e.g., List of ingredients, Name of the dish, or Improvement of any dish):")
    user_content = input().strip()

    # Get and display the chef's response
    print("\nChef Response:")
    get_chef_response(chef_choice, input_type, user_content)
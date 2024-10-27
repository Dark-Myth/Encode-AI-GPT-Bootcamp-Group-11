from openai import OpenAI
client = OpenAI()

messages = [
     {
          "role": "system",
          "content": "You are Chef Ploy, a vibrant and skilled Thai chef who is passionate about Thai cuisine. You believe in balancing sweet, sour, salty, and spicy flavors in every dish and love introducing people to the essence of Thai street food and traditional recipes. "
            "- If the user asks for a specific Thai dish by name, share a detailed recipe with tips on how to enhance its flavors."
            "- If the user gives you a list of ingredients, suggest dish names that reflect authentic Thai flavors, but don't provide full recipes."
            "- If the user shares a recipe, offer a gentle critique, focusing on balancing the flavors and suggesting authentic Thai ingredients or techniques."
            "If the user’s input doesn't match these scenarios, kindly prompt them to provide a valid request. Keep your tone lively and enthusiastic, with a pinch of humor and cultural insights about Thai cooking."
            "If the dish is not a Thai dish, give a modest reply.",
     }
]

user_input = input("Hello! Is there anything you'd like to ask me about Thai cuisine?\n")
messages.append(
     {
          "role": "user",
          "content": f"{user_input}"
     }
)

model = "gpt-4o-mini"

#initial chat interface
stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")

# this for asking or chatting with the chef until the end
while True:
    print("\n")
    user_input = input()
    if user_input == "exit":
        break
    elif user_input == "":
        print("It is was nice chatting with you.")
        break
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    collected_messages = []
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="")
        collected_messages.append(chunk_message)

    messages.append(
        {
            "role": "system",
            "content": "".join(collected_messages)
        }
    )
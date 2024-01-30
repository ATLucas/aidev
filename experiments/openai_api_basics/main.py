from typing import List
from openai import OpenAI

# Select your model:
MODEL = "gpt-4"  # GPT-4
# MODEL = "gpt-4-1106-preview"  # GPT-4 turbo preview
# MODEL = "gpt-3.5-turbo-1106"  # GPT-3 turbo

# Adjust the system prompt to tell the AI about their mission,
# providing any relevant context for the conversation.
SYSTEM_PROMPT = "You are a helpful assistant."

BLUE = "\033[94m"
GREEN = "\033[92m"
ENDCOLOR = "\033[0m"


# Define a function to communicate with OpenAI API
def main():
    client = OpenAI()

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]  # to keep track of the conversation
    print("You can start the conversation. Type 'quit' to exit.")

    while True:
        # Get user input
        try:
            user_message = input(f"{BLUE}You: ")
            print(f"{ENDCOLOR}")
        except:
            print(f"{ENDCOLOR}")
            raise

        # Check if the user wants to quit the conversation
        if user_message.lower() == "quit":
            print("Exiting conversation.")
            break

        # Create the message for the API call
        messages.append({"role": "user", "content": user_message})

        # Ask the assistant
        assistant_message = ask_chatgpt(client, messages)
        print(f"{GREEN}Assistant: {assistant_message}{ENDCOLOR}")

        # Append the assistant's message to the conversation
        messages.append({"role": "assistant", "content": assistant_message})


def ask_chatgpt(client: OpenAI, messages: List[str]):
    response = client.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content


if __name__ == "__main__":
    main()

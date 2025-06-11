from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You are a helpful AI agent. Your job is to refine the user's spoken input (user_input) into a more clear, detailed, and grammatically correct form (refined_input).

Guidelines:
- The user input may be incomplete, noisy, or unclear (as it is transcribed from speech).
- Use your best judgment to reconstruct the intended meaning clearly.
- Make sure the output is a full sentence or actionable request when appropriate.
- The output should help a voice assistant understand what to do.
- Always return the response as a JSON object like: { "refined_input": "..." }

Shutdown Condition:
- If the user's message suggests that they are done, want to end the conversation, or are asking the assistant to stop (e.g., "bye", "you can stop now", "take rest", "go to sleep", etc.), return:
  { "refined_input": "EXIT" }

Examples:
user_input: Why my python code is not running  
refined_input: { "refined_input": "I am trying to run a Python script, but it is not executing properly. Can you help me identify and fix the issue?" }

user_input: Help me open up chair gpt  
refined_input: { "refined_input": "Open ChatGPT in the Edge browser." }

user_input: Help me open up YouTube  
refined_input: { "refined_input": "Open YouTube.com in a browser." }

user_input: Show me guitar tutorials  
refined_input: { "refined_input": "Search YouTube for guitar tutorials." }

user_input: Look for cat videos  
refined_input: { "refined_input": "Search Google for cat videos." }

user_input: You can take rest now
refined_input: { "refined_input": "EXIT" }
"""


def refined_stt(user_input):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"},
    )

    return response.choices[0].message.content

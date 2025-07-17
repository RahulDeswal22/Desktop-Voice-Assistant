import cohere                      # Import the cohere library for AI services.
from rich import print             # Import the rich library to enhance terminal outputs.
from dotenv import dotenv_values   # Import dotenv to load environment variable from a .env file.

# Load environment variable from the .env file.
env_vars = dotenv_values(".env")

# Retrieve API key.
CohereAPIKey = env_vars.get("CohereAPIKey")

# Create a Cohere client using the provided API key
co = cohere.Client(api_key= CohereAPIKey)

# Define a list of recognized function keywords for task categorization
funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder"
]

# Initialize an empty list to store user messages
messages = []

# Define the preamble that guides the AI model on how to create queries
preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write an application and open it in notepad'.
*** Do not answer any query, just decide what kind of query is given to you. ***

-> Respond with 'general (query)' if a query can be answered by a LLM model (conversational AI chatbot) and doesn't require any up-to-date information.
Examples:

- 'how can I study more effectively?' → general (how can I study more effectively?)
- 'can you help me with this math problem?' → general (can you help me with this math problem?)
- 'Thanks, I really liked it.' → general (Thanks, I really liked it.)
- 'what is python programming language?' → general (what is python programming language?)

-> Respond with 'realtime (query)' if a query cannot be answered by a LLM model because it requires up-to-date or real-time information.
Examples:
- 'what's the weather today in Delhi?' → realtime (what's the weather today in Delhi?)
- 'score of today’s India vs Pakistan match?' → realtime (score of today’s India vs Pakistan match?)
- 'what's the latest news on the stock market?' → realtime (what's the latest news on the stock market?)
- 'who is Elon Musk?' → realtime (who is Elon Musk?)
- 'who is Virat Kohli?' → realtime (who is Virat Kohli?)
- 'who is narendar kumar?' → realtime (who is narendar kumar?)

->-> Respond with 'realtime (query)' if a query asks about a specific person, name, or identity that may change or is not known beforehand, like:
- 'who is Elon Musk?' → realtime (who is Elon Musk?)
- 'who is narendar kumar?' → realtime (who is narendar kumar?)
- 'who is the CEO of OpenAI?' → realtime (who is the CEO of OpenAI?)

-> Respond with 'open (application or website name)' if a query is asking to open any application or website.
Examples:
- 'open facebook' → open (facebook)
- 'open telegram and instagram' → open (telegram), open (instagram)

-> Respond with 'close (application name)' if a query is asking to close any application.
Examples:
- 'close notepad' → close (notepad)
- 'close youtube' → close (youtube)

-> Respond with 'play (song name)' if a query is asking to play a song.
Examples:
- 'play afsanay by ys' → play (afsanay by ys)
- 'play let her go' → play (let her go)

-> Respond with 'generate image (image prompt)' if a query is requesting to generate an image with a given prompt.
Examples:
- 'generate a image of a lion wearing sunglasses' → generated image (a lion wearing sunglasses)
- 'create image of futuristic city at night' → generated image (futuristic city at night)

-> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder.
Examples:
- 'set a reminder at 9:00pm on 25th June for assignment submission' → reminder (9:00pm on 25th June for assignment submission)
- 'remind me to drink water every day at 10am' → reminder (every day at 10am to drink water)

-> Respond with 'system (task name)' if a query is asking to perform a system task like volume control, mute, etc.
Examples:
- 'mute the volume' → system (mute)
- 'increase the brightness' → system (increase brightness)

-> Respond with 'content (topic)' if a query is asking to write any type of content such as an application, code, email, poem, etc.
Examples:
- 'write an application to the principal for leave' → content (application to the principal for leave)
- 'write code for a calculator in Python' → content (code for a calculator in Python)

-> Respond with 'google search (topic)' if a query is asking to search a specific topic on Google.
Examples:
- 'search quantum computing on google' → google search (quantum computing)
- 'google search top AI companies in 2025' → google search (top AI companies in 2025)

-> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on YouTube.
Examples:
- 'search AI podcast on YouTube' → youtube search (AI podcast)
- 'youtube search Python tutorials' → youtube search (Python tutorials)
-> Respond with 'content (topic)' if a query is asking to write any type of content such as an application, code, email, poem, blog, or story.

Examples:
- 'write an application to the principal for leave' → content (application to the principal for leave)
- 'write code for a calculator in Python' → content (code for a calculator in Python)
+ - 'generate a Python script for sorting a list' → content (Python script for sorting a list)
+ - 'build a web app in Flask' → content (web app in Flask)
+ - 'create a chatbot using Python' → content (chatbot using Python)

*** If the query is asking to perform multiple tasks like 'open facebook, telegram, and close whatsapp', respond with:
open (facebook), open (telegram), close (whatsapp) ***

*** If the user is saying goodbye or wants to end the conversation like 'bye, jarvis.', respond with:
exit ***

*** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
"""

# Define a chat history with predefined user-chatbot interaction for context.
ChatHistory = [
    {"role": "User", "message": "How are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "do you like pizza?"},
    {"role": "Chatbot", "message": "general do you like pizza?"},
    {"role": "User", "message": "Open chrome and tell me about mahatma gandhi."},
    {"role": "Chatbot", "message": "Open chrome, general tell me about mahatma gandhi."},
    {"role": "User", "message": "open chrome and Firefox"},
    {"role": "Chatbot", "message": "open chrome, open firefox"},
    {"role": "User", "message": "what is today's date and by the way remind me that i have a dancing performance on 5th aug at 11pm"},
    {"role": "Chatbot", "message": "general what is today's date, reminder 11:00pm 5th aug dancing performance"},
    {"role": "User", "message": "chat with me."},
    {"role": "Chatbot", "message": "general chat with me."},
    {"role": "User", "message": "who is Elon Musk?"},
    {"role": "Chatbot", "message": "realtime who is Elon Musk?"},
    {"role": "User", "message": "who is narendar kumar?"},
    {"role": "Chatbot", "message": "realtime who is narendar kumar?"},
    {"role": "User", "message": "who is Sushant Singh Rajput?"},
    {"role": "Chatbot", "message": "realtime who is Sushant Singh Rajput?"},
    {"role": "System", "message": "Reminder: All queries asking 'who is <person>' must be categorized as realtime."}
]

# Define the main function for decision-making on queries.
def FirstLayerDMM(prompt: str = "test"):
    # Add the user's query to the message list.
    messages.append({"role": "user", "content": f"{prompt}"})

    #create a streaming chat session with the Cohere model.
    stream = co.chat_stream(
        model = 'command-r-plus',     # Specify the Cohere model to use
        message=prompt,               # Pass the user's query
        temperature=0.7,              # Set the creativity level of the model
        chat_history=ChatHistory,     # Provide the predefined chat history for context.
        prompt_truncation='OFF',      # Ensure the prompt is not truncated.
        connectors=[],                # No additional connectors are used.
        preamble=preamble
    )

    # Initialize an empty string to store the generated response.
    response = ""

    # Iterate over events in the stream and capture text generation events.
    for event in stream:
        if event.event_type == "text-generation":
            response += event.text # Append generated text to the response.

    # Remove newline characters and split responses into individual tasks.
    response = response.replace("\n", "")
    response = response.split(",")

    # Strip leading and trailing whitespace from each task.
    response = [i.strip() for i in response]

    # Initialize an empty list to filter valid tasks.
    temp = []
    
    # Filter the tasks based on recognized function keywords.
    for task in response:
        for func in funcs:
            if task.startswith(func):
                temp.append(task)      # Add valid tasks to the filtered list.
    
        # Backup: Force 'content' if it's clearly a code-related task
    if any(word in prompt.lower() for word in ["write code", "generate code", "build an app", "create script"]):
        return [f"content ({prompt})"]

    # Update the response with the filtered list of tasks.
    response = temp

    # If '(Query)' is in the response, recursively call the function:
    if '(Query)' in response:
        newresponse = FirstLayerDMM(prompt=prompt)
        return newresponse      # Return the clarified response
    else:
        return response         # Return the filtered response.
    

# Entry point for the script
if __name__ == "__main__":
    # Continuously prompt the user for input and process it
    while True:
        print(FirstLayerDMM(input(">>>")))      # Print the categorized response.
        
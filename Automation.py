# Importing the Required Libraries
from AppOpener import close, open as appopen  # Import functions to open and close apps.
from webbrowser import open as webopen        # Import web browser functionality.
from pywhatkit import search, playonyt        # Import functions for google search and Youtube playback
from dotenv import dotenv_values              # Import dotenv to manage environment variables.
from bs4 import BeautifulSoup                 # Import BeautifulSoup for parsing HTML Content.
from rich import print                        # Import rich for styled console output
from groq import Groq                         # Import Groq for AI char functionalities
import webbrowser                             # Import webbrowser for opening urls
import subprocess                             # Import subprocess for interacting with the system
import requests                               # Import requests for making HTTP requests.
import keyboard                               # Import keyboard for keyboard-related actions
import asyncio                                # Import asyncio for asynchronous programming.
import os                                     # Import os for operating system functionalities.

# Load Environment variables form the .env file.
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")  # Retrieve the Groq API key

# Define CSS Classes for parsing specific elements in HTML content
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe",
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a user-agent for making web requests/
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize the Groq client with the API key
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask."
]

# List to store Chatbot messages
messages = []

# System message to provide context to the chatbot.
SystemChatBot = [{
    "role": "system",
    "content": f"Hello, I am {os.environ['Username']}. You are a versatile assistant who specializes in generating code, automating tasks, and writing content in various formats such as formal letters, emails, scripts, or documentation. The user may specify the language (e.g., Python, JavaScript, HTML, CSS, C++, C, Java, Go etc.) and the type of content or automation needed. Always ensure your output is clean, well-structured, and accurate to the given prompt."
}]

# Function to perform a Google Search.
def GoogleSearch(Topic):
    search(Topic)  # USe pywhatkit's search function to perform Google Search.
    return True

# Function to generate content using AI and Save it to a file.
def Content(Topic):

    # Nested function to open a file in notepad.
    def OpenNotePad(File):
        default_text_editor = 'notepad.exe' # Default text editor.
        subprocess.Popen([default_text_editor, File])  # Opent the file in NotePad.
    
    # Nested function to generate content using the AI chatbot.
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})  # Add the user's prompt to messages.

        completion = client.chat.completions.create(
            model = "deepseek-r1-distill-llama-70b",   # Specify the AI model.
            messages = SystemChatBot + messages,  # Include system instructions and chat history.
            max_tokens = 8192,  # Limit the maximum tokens in the response.
            temperature = 0.7,  # Adjust the response randomness
            top_p = 1,   # Use nucleus sampling for response diversity
            stream= True,  # Enable streaming response.
            stop= None    # Allow the model to determine stopping conditions.
        )

        Answer = "" #Initialize an empty string for the response.

        # Process stramed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:  # Check for content in the current chunk.
                Answer += chunk.choices[0].delta.content  # Append the content to the answer.
        
        Answer = Answer.replace("</s>", "") # Remove unwanted tokens from the response.
        messages.append({"role": "assistant", "content": Answer})  # Add the AI's response to messages/
        return Answer
    
    Topic: str = Topic.replace("Content ", "") # Remove 'Content ' from the topic
    ContentByAI = ContentWriterAI(Topic)       # Generate contetn using AI

    # Save the generatede content to a text file.
    with open(rf"Data\{Topic.lower().replace(' ','')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)  # write the content tot he file
        file.close()
    
    OpenNotePad(rf"Data\{Topic.lower().replace(' ','')}.txt")  # Open the file in Notepad.
    return True  # Indicate Success.

# Function to search for a topic on Youtube.
def YouTubeSearch(Topic):
    Url4Search  = f"https://www.youtube.com/results?search_query={Topic}"  # Construct the YouTube
    webbrowser.open(Url4Search)   # Open the search url in a web browser.
    return True  # Indicate Success.

# Function to play a video on YouTube.
def PlayYouTube(query):
    playonyt(query)  # Use pywhatkit's playonyt function to play the video.
    return True  # Indicate Success.

# Function to open an application or a releavnt webpage.
def OpenApp(app, sess=requests.session()):

    try:
        appopen(app, match_closest=True, output=True, throw_error=True)  # Attemptto open the app.
        return True  # Indicate Success.
    
    except:
        # Nested function to extract links from HTML content.
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML content.
            links = soup.find_all('a', {'jsname': 'UWckNb'})  # Find relevant links.
            return [link.get('href') for link in links]  # Return the links.
        
        # Nested function to perform a Google Search and retrieve HTML.
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"  # Construct the Google search URL
            headers = {"User-Agent": useragent}   # Use the predefined user-agent
            response = sess.get(url, headers=headers)  # peform the GET request.

            if response.status_code == 200:
                return response.text  # Return the HTML content.
            else:
                print("Failed to retrieve search results.")  # Print an error message.
            return None
        
        html = search_google(app)  # Perform the Google search.

        if html:
            link = extract_links(html)[0]   # Extract the first link from the search results.
            webopen(link)  # Open the link in a web browser.
        
        return True   # Indicate success.

# FUnction to close an application.
def CloseApp(app):

    if "chrome" in app:
        pass  # Skip if the app is Chrome.
    else:
        try:
            close(app, match_closest=True, output = True, throw_error=True)  # Attempt to close the app.
            return True  # Indicate success
        except:
            return False # Indicate Failure

# Function to execute system level commands.
def System(command):

    # Nestedd function to mute the system volume.
    def mute():
        keyboard.press_and_release("volume mute")  # Simulate the mute key press.
    
    # Nested function to unmute the system volume.
    def unmute():
        keyboard.press_and_release("volume mute")  # Simulte the unmute key press.

    # Nested function to increase the system volume.
    def volume_up():
        keyboard.press_and_release("volume up")  # Simulate the volume up key press.
    
    # Nested function to decrease the system volume.
    def volume_down():
        keyboard.press_and_release("volume down")  # Simulate the volume down key press.

    # Execute the appropriate command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True # Indicate success

# Asynchronous function to translate and execute user commands.
async def TranslateAndExecute(commands: list[str]):

    funcs = []  # List to store asynchronous tasks.

    for command in commands:

        if command.startswith("open "):   # Handle "open" commands.

            if "open it" in command:   # Ignore "open it" commands.
                pass

            if "open file" == command:  # Ignore "open file" commands.
                pass
            
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))  # Schedule app opening.
                funcs.append(fun)
        
        elif command.startswith("general "):  # Placeholder for general commands.
            pass

        elif command.startswith("realtime "):   # Placeholder for real-time commands.
            pass
        
        elif command.startswith("close "):   # Handle "close" commands.
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))  # Schedule app closing.
            funcs.append(fun)
        
        elif command.startswith("play "):   # Handle 'play' commands.
            fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play "))  # Schedule YouTube Playback.
            funcs.append(fun)

        elif command.startswith("content "):    # Handle  "content" commands.
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("content ")) # Schedule content creation.
            funcs.append(fun)

        elif command.startswith("google search "):  # Handle Google Search commands.
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))  # Schedule google search
            funcs.append(fun)

        elif command.startswith("youtube search "):   # Handle youtbe search.
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))  # Schedule Youtube searcj.
            funcs.append(fun)
        
        elif command.startswith("system "):    # Handle system command.
            fun = asyncio.to_thread(System, command.removeprefix("system "))  # Schedule system command.
            funcs.append(fun)
        
        else:
            print(f"No Function Found. For {command}")  # Print an error for unrecognized commands.
    
    results = await asyncio.gather(*funcs) # Executr all tasks concurrently.

    for result in results:  # Process the results.
        if isinstance(result, str):
            yield result
        else:
            yield result

# Asynchronous function to automate command execution.
async def Automation(commands: list[str]):

    async for result in TranslateAndExecute(commands):   # Translate And Execute commands.
        pass

    return True   # Indicate success.


if __name__ == "__main__":
    import asyncio
    import sys
    
    # Create a directory for storing generated content if it doesn't exist
    if not os.path.exists("Data"):
        os.makedirs("Data")
    
    # Function to process user input and execute appropriate commands
    async def process_command():
        print("[bold green]JARVIS AI Assistant initialized. Ready for commands.[/bold green]")
        
        while True:
            try:
                # Get user input
                user_input = input("\nEnter your command (or 'exit' to quit): ")
                
                # Check if user wants to exit
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("[bold yellow]Shutting down JARVIS AI Assistant. Goodbye![/bold yellow]")
                    break
                
                # Process different types of commands
                if user_input.lower().startswith("content "):
                    # Handle content generation
                    print("[bold blue]Generating content...[/bold blue]")
                    Content(user_input)
                    print(f"[bold green]Content generated successfully for: {user_input.replace('content ', '')}[/bold green]")
                
                elif user_input.lower().startswith(("open ", "close ", "google search ", "youtube search ", "play ", "system ")):
                    # Handle automation commands
                    print(f"[bold blue]Executing command: {user_input}[/bold blue]")
                    commands = [user_input.lower()]
                    result = await Automation(commands)
                    if result:
                        print(f"[bold green]Command executed successfully![/bold green]")
                    else:
                        print(f"[bold red]Failed to execute command.[/bold red]")
                
                # If no specific command pattern is recognized, use AI to respond or execute
                else:
                    # Add the user message to the conversation history
                    messages.append({"role": "user", "content": user_input})
                    
                    # Get a response from the AI
                    print("[bold blue]Processing with AI...[/bold blue]")
                    completion = client.chat.completions.create(
                        model="deepseek-r1-distill-llama-70b",
                        messages=SystemChatBot + messages,
                        max_tokens=1024,
                        temperature=0.7,
                        top_p=1,
                        stream=True,
                        stop=None
                    )
                    
                    # Initialize an empty string for the response
                    answer = ""
                    print("\n[bold cyan]JARVIS AI:[/bold cyan]")
                    
                    # Process the streamed response chunks
                    for chunk in completion:
                        if chunk.choices[0].delta.content:
                            content = chunk.choices[0].delta.content
                            answer += content
                            print(content, end="", flush=True)
                    
                    # Clean up the response and add it to the message history
                    answer = answer.replace("</s>", "")
                    messages.append({"role": "assistant", "content": answer})
                    print("\n")
                    
            except Exception as e:
                print(f"[bold red]Error: {str(e)}[/bold red]")
    
    # Run the main async function
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(process_command())
import os
from openai import OpenAI
from pathlib import Path

role_message = {"role": "system", "content": "You are a helpful assistant"}
chat_history = [role_message]

chat_log_directory = "[INSERT DIRECTORY]"
prompt_directory = "[INSERT DIRECTORY]"
message_terminator = "~*~*~"
prev_file = "default"


client = OpenAI(
        api_key='[INSERT API KEY]',
        base_url="https://api.deepseek.com")


# Prompt the AI
# Prompt: String containing prompt text
def prompt(prompt):
    
    global chat_history
    chat_history.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=chat_history,
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    
    if response.choices[0].message.content == "":
        print("[Received blank response. You probably tripped Deepseek's censor.]")
        chat_history = chat_history[:-1]
    else:
        print("\n" + response.choices[0].message.content + "\n")
        chat_history.append({"role": response.choices[0].message.role, "content": response.choices[0].message.content})


# Roll back conversation by 1 turn
def undo(verbose = True):
    global chat_history
    if len(chat_history) < 2:
        if verbose:
            print("Nothing to undo.")
    else:
        chat_history = chat_history[:-2]
        if verbose:
            print("Undid last turn.")


# Print the last user prompt and AI response
def lastTurn():
    global chat_history
    if len(chat_history) >= 2:
        print("")
        print(chat_history[-2]["content"])
        print(message_terminator)
        print(chat_history[-1]["content"])
        print("")
    else:
        print("Chat history is empty.")


# Clear history and start a new convo
# Path: location to which to save the convo. If none supplied, saves to default.txt
def newChat(path = None):

    global chat_history
    chat_history = [role_message]
    
    global prev_file
    
    if path == None:
        prev_file = "default"
    else:    
        prev_file = path
    
    print("New chat started. Path is " + prev_file + ".txt.")


# Save the current convo
# path: location to which to save the convo
def saveChat(path = None):
    
    global prev_file
    
    if path == None:
        path = prev_file
    else:    
        prev_file = path
    
    file = open(chat_log_directory + path + ".txt", 'w', encoding="utf-8")
    
    for item in chat_history:
        file.write(item["role"].upper() + "\n")
        file.write(item["content"] + "\n")
        file.write(message_terminator + "\n")
    
    file.close()
    
    print("Saved conversation to " + path + ".txt.")


# Load the current convo
# path: location from which to load the convo
def loadChat(path = None):
    
    global prev_file
    
    old_prev_file = prev_file
    
    if path == None:
        path = prev_file
    else:    
        prev_file = path
    
    global chat_history
    
    full_path = chat_log_directory + path + ".txt"
    
    file_path = Path(full_path)
    if not file_path.is_file():
        print("ERROR: File not found.")
        prev_file = old_prev_file
        return
    
    chat_history = []
    chat_history_item = {}
    message = ""
   
    with open(full_path, "r", encoding="utf-8") as file:
        for line in file:
            if not "role" in chat_history_item:
                chat_history_item["role"] = line[:-1].lower()
            else:
                if line[:-1] == message_terminator:
                    chat_history_item["content"] = message[:-1]     # Remove trailing endline
                    chat_history.append(chat_history_item)
                    chat_history_item = {}
                    message = ""
                else:
                    message += line     # In this instance we want to include the terminator

    print("Loaded conversation from " + path + ".txt. You may resume where you left off.")


# Define the assistant's role for the conversation
def assignRole(role):
    chat_history[0]["content"] = "Your purpose: " + role + "."
    print("Role assigned.")


# Feed the assistant a prompt from a file. This is useful for large prompts that are cumbersome to enter from the command line.
def promptFromFile(path = "prompt"):
    with open(prompt_directory + path + ".txt", "r", encoding="utf-8") as file:
        
        prompt_from_file = ""
        
        for line in file:
            prompt_from_file += line
        
    prompt(prompt_from_file)


def showAssistantPurpose():
    global chat_history
    print(chat_history[0]["content"])


# Generate a new response from the same prompt. Overwrites the old response in the chat history.
def regenerate():
    global chat_history
    if len(chat_history) < 2:
        print("Nothing to regenerate.")
    else:
        prev_prompt = chat_history[-2]["content"]
        undo(False)
        prompt(prev_prompt)
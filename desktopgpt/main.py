import openai
import subprocess
import time
from apps.notes import * 
from apps.browser import * 


openai.api_key = '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'

def control_volume(volume_change):
    script = f'''
    osascript -e 'set volume output volume (output volume of (get volume settings) {volume_change})'
    '''
    print(f"Executing AppleScript command: {script}")
    result = subprocess.getoutput(script)
    return result

def execute_command(command):
    if command.lower() == "turn down the volume":
        result = control_volume("- 10")
        print(result)
        time.sleep(3)  # Wait for 3 seconds
    elif command.lower() == "open browser":
        browser.open_browser()
    else:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": command}]
        )
        response = completion['choices'][0]['message']['content'].strip()
        if "action can not be completed" in response:
            print("Action can not be completed, try again later")
        else:
            print(response)

def main():
    while True:
        command = input("Enter a command: ")
        execute_command(command)
        follow_up = input("Do you have another command? (yes/no): ")
        if follow_up.lower() != "yes":
            break

if __name__ == "__main__":
    main()
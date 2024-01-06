import openai
import subprocess

openai.api_key = ''

def execute_command(command):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": command}]
    )
    return response['choices'][0]['message']['content'].strip()

def main():
    command = input("Enter a command: ")
    result = execute_command(command)
    print(result)

if __name__ == "__main__":
    main()
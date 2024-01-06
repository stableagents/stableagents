import openai
import subprocess

openai.api_key = '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'

def execute_command(command):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": command}]
    )
    return completion['choices'][0]['message']['content'].strip()

    script = f'''
    osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'
    '''
    result = subprocess.getoutput(script)
    return result

def main():
    while True:
        command = input("Enter a command: ")
        result = execute_command(command)
        print(result)
        follow_up = input("Do you have another command? (yes/no): ")
        if follow_up.lower() != "yes":
            break

if __name__ == "__main__":
    main()
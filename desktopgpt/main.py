import openai
import subprocess

openai.api_key = ''

def switch_dark_mode():
  script = '''
      tell application "System Events"
          tell appearance preferences
             set dark mode to true
          end tell
      end tell
  '''
  subprocess.run(['osascript', '-e', script])

def decrease_volume():
  script = '''
      tell application "System Events"
          set volume output volume ((output volume of (get volume settings)) - 10)
      end tell
  '''
  subprocess.run(['osascript', '-e', script])

def generate_command(prompt):
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "system", "content": prompt}]
  )
  return response['choices'][0]['message']['content'].strip()

# Map commands to functions
commands = {
  "Switch to dark mode": switch_dark_mode,
  "Decrease volume": decrease_volume
}

command = generate_command("Turn down the volume")
if command in commands:
  commands[command]()
else:
  print(f"Command '{command}' not recognized.")

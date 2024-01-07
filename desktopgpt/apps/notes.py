import subprocess

def open_notes_app():
    script = '''
    osascript -e 'tell application "Notes" to activate'
    osascript -e 'tell application "System Events" to keystroke "hello world"'
    '''
    print(f"Executing AppleScript command: {script}")
    result = subprocess.getoutput(script)
    return result

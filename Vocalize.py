import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import boto3
from contextlib import closing
import os
import sys
from tempfile import gettempdir

# Create the main application window
root = tk.Tk()
root.title("Text to Speech with AWS Polly")
root.geometry("600x400")

# Create a frame for text input and file loading
frame_text = ttk.Frame(root, padding="10 10 10 10")
frame_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create a text widget
textEx = tk.Text(frame_text, height=10, width=70, wrap=tk.WORD)
textEx.grid(row=0, column=0, columnspan=2)

# Create a button to load text from a file
btn_load = ttk.Button(frame_text, text="Load File", command=lambda: load_file())
btn_load.grid(row=1, column=0, sticky=tk.W, pady=5)

# Create a button to clear text input
btn_clear = ttk.Button(frame_text, text="Clear Text", command=lambda: textEx.delete("1.0", tk.END))
btn_clear.grid(row=1, column=1, sticky=tk.E, pady=5)

# Create a frame for voice and language selection
frame_options = ttk.Frame(root, padding="10 10 10 10")
frame_options.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create a dropdown for voice selection
ttk.Label(frame_options, text="Select Voice:").grid(row=0, column=0, sticky=tk.W)
voices = [
    "Emma", "Joanna", "Matthew", "Brian", "Amy", "Joey",
    "Salli", "Kendra", "Ivy", "Justin"
]
voice_var = tk.StringVar(root)
voice_var.set(voices[0])
voice_menu = ttk.OptionMenu(frame_options, voice_var, *voices)
voice_menu.grid(row=0, column=1, sticky=(tk.W, tk.E))

# Create a dropdown for language selection
ttk.Label(frame_options, text="Select Language:").grid(row=1, column=0, sticky=tk.W)
languages = {
    "English": "en-US", "Spanish": "es-ES", "French": "fr-FR", 
    "German": "de-DE", "Italian": "it-IT", "Japanese": "ja-JP"
}
language_var = tk.StringVar(root)
language_var.set("English")
language_menu = ttk.OptionMenu(frame_options, language_var, *languages.keys())
language_menu.grid(row=1, column=1, sticky=(tk.W, tk.E))

# Create a frame for control buttons
frame_controls = ttk.Frame(root, padding="10 10 10 10")
frame_controls.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create a button to start text-to-speech conversion
btn_read = ttk.Button(frame_controls, text="Convert to Speech", command=lambda: getText())
btn_read.grid(row=0, column=0, sticky=tk.W, padx=5)

# Create a button to exit the application
btn_exit = ttk.Button(frame_controls, text="Exit", command=root.quit)
btn_exit.grid(row=0, column=1, sticky=tk.E, padx=5)

def getText():
    aws_mg_con = boto3.session.Session(profile_name='Demo_user')
    client1 = aws_mg_con.client(service_name='polly', region_name='us-east-1')
    
    result = textEx.get("1.0", "end").strip()
    if not result:
        messagebox.showwarning("Input Error", "Please enter text to synthesize.")
        return
    
    voice_id = voice_var.get()
    language_code = languages[language_var.get()]

    try:
        response = client1.synthesize_speech(
            VoiceId=voice_id,
            OutputFormat='mp3',
            Text=result,
            Engine='neural',
            LanguageCode=language_code
        )

        if "AudioStream" in response:
            with closing(response['AudioStream']) as stream:
                output = os.path.join(gettempdir(), "output.mp3")
                with open(output, "wb") as file:
                    file.write(stream.read())

            if sys.platform == 'win32':
                os.startfile(output)
            elif sys.platform == 'darwin':
                os.system(f"open {output}")
            elif sys.platform == 'linux':
                os.system(f"xdg-open {output}")
        else:
            raise Exception("AudioStream not found in response.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        log_error(e)

def log_error(e):
    with open("error_log.txt", "a") as log_file:
        log_file.write(str(e) + "\n")

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            textEx.delete("1.0", tk.END)
            textEx.insert(tk.END, file.read())

# Run the main event loop
root.mainloop()

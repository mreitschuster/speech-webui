import gradio as gr
import requests
import os
from datetime import datetime

# Load environment variables and trim whitespace
SERVER_URL = os.environ['SERVER_URL']
VOICES = [voice.strip() for voice in os.environ.get('VOICES', '').split(',')]
MODELS = [model.strip() for model in os.environ.get('MODELS', '').split(',')]

def generate_file(text, model, voice, serverurl, response_format, speed):
    # Format the current timestamp to include date, hour, and minute
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
    
    # Prepare the payload for the request
    payload = {
        "model": model,
        "input": text,
        "voice": voice,
        "response_format": response_format,
        "speed": speed
    }
    
    # Make the HTTP request to the server URL
    response = requests.post(serverurl, headers={"Content-Type": "application/json"}, json=payload)
    
    if response.status_code == 200:
        filename = f"{timestamp}_{voice}.{response_format}"
        
        with open(filename, 'wb') as file:
            file.write(response.content)
            
        return filename
    else:
        return None

def update_file_component(filename):
    """Helper function for Gradio's File component"""
    if filename is not None:
        return gr.File.update(value=filename)
    else:
        return gr.File()

with gr.Blocks() as demo:
    textbox_large = gr.Textbox(value="The lazy dev needed some defaults to not always have to enter something.", lines=20, label="Text")
    
    with gr.Row():
        with gr.Column(scale=1):
            dropdown_model = gr.Dropdown(choices=MODELS, value=MODELS[0], label="Model")
            
            # Initialize the voice dropdown
            dropdown_voice = gr.Dropdown(choices=VOICES, value=VOICES[0], label="Voice")
        
        with gr.Column():
            textbox_serverurl = gr.Textbox(value=SERVER_URL, lines=1, label="Server URL")
            dropdown_responseformat = gr.Dropdown(choices=["mp3", "opus", "aac", "flac", "wav", "pcm"], value="mp3", label="Response Format")
    
    slider_speed = gr.Slider(value=1.0, minimum=0.25, maximum=4.0, step=0.1, label="Speed (x)")
    
    button_generate = gr.Button("Generate File")
    
    output_file = gr.File()
    
    # Function to handle the button click and generate/download the file
    def on_button_click():
        filename = generate_file(textbox_large.value, dropdown_model.value, dropdown_voice.value, textbox_serverurl.value, dropdown_responseformat.value, slider_speed.value)
        return update_file_component(filename)

    button_generate.click(fn=on_button_click, outputs=output_file)

# Launch the Gradio app
demo.launch(server_name="0.0.0.0")
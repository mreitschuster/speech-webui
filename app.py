import gradio as gr
import requests
import os
from datetime import datetime

# Load environment variables and trim whitespace
SERVER_URL = os.environ['SERVER_URL']
VOICES = [voice.strip() for voice in os.environ.get('VOICES', '').split(',')]
MODELS = [model.strip() for model in os.environ.get('MODELS', '').split(',')]

def generate_speechfile(text, model, voice, serverurl, response_format, filename_append_text, speed):
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
    
    try:
        # Make the HTTP request to the server URL
        response = requests.post(serverurl, headers={"Content-Type": "application/json"}, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        error_message = f"Error: {e}"
        return error_message, None
    
    filename = f"{timestamp}_{voice}_{filename_append_text}.{response_format}"
    with open(filename, 'wb') as file:
        file.write(response.content)
        
    return "Success", filename

with gr.Blocks(title="Speech") as demo:
    textbox_large = gr.Textbox(value="The lazy dev needed some defaults to not always have to enter something.", lines=20, label="Text", interactive=True)

    with gr.Row():
        with gr.Column(scale=1):
            dropdown_model = gr.Dropdown(choices=MODELS, value=MODELS[0], label="Model", interactive=True)
            dropdown_voice = gr.Dropdown(choices=VOICES, value=VOICES[0], label="Voice", interactive=True)

        with gr.Column():
            textbox_serverurl = gr.Textbox(value=SERVER_URL, lines=1, label="Server URL", interactive=True)
            dropdown_responseformat = gr.Dropdown(choices=["mp3", "opus", "aac", "flac", "wav", "pcm"], value="mp3", label="Response Format", interactive=True)

    slider_speed = gr.Slider(value=1.0, minimum=0.25, maximum=4.0, step=0.1, label="Speed (x)")

    with gr.Row():
        with gr.Column():
            textbox_filename_append = gr.Textbox(value="speech", lines=1, label="Filename Appendix", interactive=True) 
        with gr.Column():
            button_generate = gr.Button("Generate File")

    with gr.Row():
        with gr.Column():
            success_box = gr.Textbox(label="Output", scale=5)
        with gr.Column():
            files_output= gr.Files(label="Downloadable output file", scale=3)
    
    button_generate.click(fn=generate_speechfile, 
            inputs=[textbox_large,
                    dropdown_model,
                    dropdown_voice,
                    textbox_serverurl,
                    dropdown_responseformat,
                    textbox_filename_append,
                    slider_speed] , 
            outputs=[success_box,files_output])

demo.launch(server_name="0.0.0.0")


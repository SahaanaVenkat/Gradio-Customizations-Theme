import openai
import gradio as gr
import pandas as pd

openai.api_key = "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"

messages = [
    {"role": "system", "content": "You are a helpful and kind AI Assistant."},
]
headers = {
    'selector': 'th:not(.index_name)',
    'props': 'background-color: #000000; color: #E1F000;'
}
styled_html = ""

def chatbot(file_upload):
    # df = pd.DataFrame({
    #         "A": [14, 4, 5, 4, 1],
    #         "B": [5, 2, 54, 3, 2],
    #         "C": [20, 20, 7, 3, 8],
    #         "D": [14, 3, 6, 2, 6],
    #         "E": [23, 45, 64, 32, 23]
    #     })
    
    df=pd.read_csv(file_upload,sep=';')
    styler = df.style.set_table_styles([headers])
    output=df.describe()
    styled_html = styler.to_html()
    return styled_html,output

# Define the image URL for the header
header_image_url = "linkedin.png"

# Embedding the HTML in a Gradio interface

css = """
#warning {background-color: #E1F000}
#warning {font-family: DIN}
#warning {color:#000000}
#component-11{
    background-color: #000000;
    color: #E1F000;
    font-family: DIN;
    border-radius: 5px;
}
.feedback textarea {font-size: 24px !important}
.feedback textarea {font-family: DIN}
.gr-button{
    background-color: #000000;
    color: #E1F000;
    font-family: DIN;
    border-radius: 5px;
}
"""

js_code ="""
document.addEventListener("DOMContentLoaded", function() {
    var grButton = document.querySelector("..lg secondary gr-button svelte-cmf5ev");
    if (grButton) {
        grButton.style.backgroundColor = "#000000"
    }
});
"""
import base64

# Read image content and encode it to base64
with open("linkedin.png", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

# Use gr.Row to create a row with the header image and the chat interface
with gr.Blocks(css=css) as demo:
    gr.HTML(f'<div style="text-align: center;background-color: #E1F000;width:100%;height:48px;color:#000000;margin-top: -18px;"><p style="padding-top:12px"><b style="font-family: DIN;">Data Description</b></p><img src="data:image/png;base64,{encoded_image}" style="width:10%;height:45px;float: right;margin-top: -40px;"></div>'),
    with gr.Row():
    
        # column for inputs
        with gr.Column():
            inputs=[
    
    gr.File(label="Upload CSV File (Optional)", elem_id="warning")
]
            submit_button = gr.Button("Submit",elem_classes="gr-button")
                   
        # column for outputs
        with gr.Column():
            outputs=[
        gr.HTML(styled_html, elem_id="styled_df"),
        gr.Textbox(lines=7, label="Output", elem_classes="feedback", elem_id="warning")

]
    submit_button.click(
        fn=chatbot,
        inputs=inputs,
        outputs=outputs
    )
    
    #gr.Interface(fn=chatbot, inputs=inputs, outputs=outputs,description="Ask anything you want")
demo.launch(share=True)
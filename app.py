import os
import gradio as gr
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Please set GEMINI_API_KEY in your .env file")

client = genai.Client(api_key=api_key)

def generate_questions(topic, num_questions, question_type):
    if not topic.strip():
        return "Please enter a topic."

    prompt = f"""Generate {int(num_questions)} {question_type}
about the topic: {topic}.

Make the questions clear, useful, and well organized."""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return response.text or "No questions were generated."
    except Exception as e:
        return f"Error: {e}"

with gr.Blocks(title="AI Question Generator") as demo:
    gr.Markdown("# AI Question Generator")
    gr.Markdown("Generate questions on any topic using Gemini AI.")

    text = gr.Textbox(label="Enter Topic", placeholder="e.g. Python")
    num_questions = gr.Slider(
        minimum=1, maximum=20, value=5, step=1,
        label="Number of Questions"
    )
    question_type = gr.Dropdown(
        choices=[
            "multiple choice questions",
            "short answer questions",
            "interview questions",
            "long answer questions"
        ],
        value="multiple choice questions",
        label="Question Type"
    )

    button = gr.Button("Generate Questions", variant="primary")
    output = gr.Textbox(label="Generated Questions", lines=12)

    button.click(
        generate_questions,
        inputs=[text, num_questions, question_type],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(share=True)

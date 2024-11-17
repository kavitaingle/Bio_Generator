from flask import Flask, render_template, request
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os

# Load GPT-2 model and tokenizer
model_id = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Initialize the Flask app
app = Flask(__name__)

# Create a HuggingFacePipeline using GPT-2
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=100)

class BioGenerator:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def generate_bio(self, career, interests, traits, academic_background, research_focus):
        # Refined prompt for generating a professional bio
        prompt = (
            f"As a {career}, I am a motivated individual with a strong interest in {interests}. "
            f"I possess {traits} qualities and hold a degree in {academic_background}. "
            f"My research focus is on {research_focus}. "
            f"I aim to leverage my skills in data analysis, machine learning, and statistical modeling to provide insights. "
            f"Please generate a concise and engaging professional bio that highlights my programming skills and analytical aptitude."
        )
        
        # Generate the bio using the HuggingFacePipeline
        bio = self.pipeline(prompt)
        
        # Debugging: Print the raw output to understand its structure
        print("Raw output:", bio)

        # Check if the output is a list and contains the expected structure
        if isinstance(bio, list):
            if len(bio) > 0:
                # Check if the first element is a dictionary
                if isinstance(bio[0], dict) and 'generated_text' in bio[0]:
                    # Clean the output by removing the prompt
                    cleaned_output = bio[0]['generated_text'].replace(prompt, '').strip()
                    return cleaned_output
                elif isinstance(bio[0], str):
                    # If the output is a string, return it directly
                    return bio[0].strip()
                else:
                    return "Error: Unexpected output format from the model."
            else:
                return "Error: No output generated."
        else:
            return "Error: Unexpected output format from the model."

@app.route('/', methods=['GET', 'POST'])
def home():
    bio = ""
    if request.method == 'POST':
        career = request.form.get('career', '')
        interests = request.form.get('interests', '')
        traits = request.form.get('traits', '')
        academic_background = request.form.get('academic_background', '')
        research_focus = request.form.get('research_focus', '')
        
        # Debugging: Print the received form data
        print("Received data:", career, interests, traits, academic_background, research_focus)

        if career and interests and traits and academic_background and research_focus:
            generator = BioGenerator(pipe)
            bio = generator.generate_bio(career, interests, traits, academic_background, research_focus)
        else:
            bio = "Please fill in all fields."
    
    return render_template('index.html', bio=bio)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Use the PORT environment variable or default to 10000
    app.run(host='0.0.0.0', port=port)

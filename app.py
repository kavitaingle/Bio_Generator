from flask import Flask, render_template, request
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline

# Load GPT-2 model and tokenizer
model_id = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Initialize the Flask app
app = Flask(__name__)

# Create a HuggingFacePipeline using GPT-2
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=200)
hf = HuggingFacePipeline(pipeline=pipe)

class BioGenerator:
    def __init__(self, hf_pipeline):
        self.hf_pipeline = hf_pipeline

    def generate_bio(self, career, interests, traits, academic_background, research_focus):
        # Refined prompt for generating a professional bio
        prompt = (
            f"Create a concise and engaging professional bio for a {career}. "
            f"This individual is {traits} and has a strong interest in {interests}. "
            f"They hold a degree in {academic_background} and focus their research on {research_focus}. "
            f"The bio should highlight their skills in data analysis, machine learning, and statistical modeling. "
            f"Include their unique qualities, such as problem-solving abilities and a passion for leveraging data to drive insights. "
            f"Make sure the bio is relevant, specific, and avoids repetition."
        )
        
        # Generate the bio using the HuggingFacePipeline
        bio = self.hf_pipeline.invoke(prompt)
        return bio

@app.route('/', methods=['GET', 'POST'])
def home():
    bio = ""
    if request.method == 'POST':
        # Use .get() to avoid KeyError
        career = request.form.get('career', '')
        interests = request.form.get('interests', '')
        traits = request.form.get('traits', '')
        academic_background = request.form.get('academic_background', '')
        research_focus = request.form.get('research_focus', '')
        
        # Check if all required fields are provided
        if career and interests and traits and academic_background and research_focus:
            generator = BioGenerator(hf)
            bio = generator.generate_bio(career, interests, traits, academic_background, research_focus)
        else:
            bio = "Please fill in all fields."
    
    return render_template('index.html', bio=bio)

if __name__ == '__main__':
    app.run(debug=True)

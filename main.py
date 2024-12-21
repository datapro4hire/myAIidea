from flask import Flask, request, render_template, jsonify
import argparse
import json
from src import utils as ut
from src import agents
from pathlib import Path

app = Flask(__name__)

# ... existing imports ...

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_quiz():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save uploaded file temporarily
    temp_dir = Path('temp')
    temp_dir.mkdir(exist_ok=True)
    input_path = temp_dir / 'input.txt'
    file.save(input_path)

    # Load the agent and generate questions
    agent = agents.QuizAgent()
    generated_text = agent.generate_questions(text_path=input_path, num_questions=3)

    # Return results
    return jsonify({
        'generated_text': generated_text,
        'steps': [
            {'step': 1, 'description': 'File uploaded and processed'},
            {'step': 2, 'description': 'Questions generated'},
            {'step': 3, 'description': 'Results ready'}
        ]
    })

# Modify main function to run Flask app
def main(datadir, output="results", debug=False):
    app.run(debug=debug)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quiz Generator Web App")
    # ... existing argument parsing ...
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run in debug mode",
    )

    args = parser.parse_args()
    main(args.datadir, args.output, args.debug)
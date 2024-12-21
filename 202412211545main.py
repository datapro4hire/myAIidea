import argparse
import json
from src import utils as ut

from src import agents
from pathlib import Path


def main(datadir, output="results"):
    # Create output directory if it doesn't exist
    output_dir = Path(output)
    output_dir.mkdir(exist_ok=True)

    # Load the input and output data
    input_file = Path(datadir) / "input_1.txt"
    expected_output = Path(datadir) / "output_1.txt"
    try:
        expected_text = expected_output.read_text()
    except FileNotFoundError:
        print(f"Warning: Expected output file {expected_output} not found")
        expected_text = ""

    if not input_file.exists():
        print(f"Error: Input file {input_file} not found")
        return

    # Load the agent
    agent = agents.QuizAgent()

    # Generate quizzes
    generated_text = agent.generate_questions(text_path=input_file, num_questions=3)

    print("Expected Output:")
    print(expected_text)
    print("\n==============\nGenerated Questions:")
    print(generated_text)

    # Compare results
    if expected_text:
        score = ut.compare_outputs(generated_text, expected_text)
        print(f"\n==============\nROUGE-1 F1 score: {score:.4f}")
    else:
        print("\n==============\nNo expected output to compare with.")

    # Save results
    results = {
        "generated_text": generated_text,
    }
    if expected_text:
        results["expected_text"] = expected_text
        results["rouge_score"] = float(score) if'score' in locals() else None

    output_file = output_dir / "pred_1.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quiz Generator")
    parser.add_argument(
        "-d",
        "--datadir",
        type=str,
        default="data",
        dest='datadir',
        help="Directory containing input data",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="results",
        dest='output',
        help="Output directory (default: results)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run in debug mode",
    )

    args = parser.parse_args()
    main(args.datadir, args.output)
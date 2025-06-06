from __future__ import annotations

import os
import sys

from google import genai

# Load API key
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    print("❌ GOOGLE_API_KEY not set. Use `export GOOGLE_API_KEY=your-key`.")
    sys.exit(1)

# Create client
client = genai.Client(api_key=API_KEY)


def read_scenarios(file_path: str) -> list[str]:
    with open(file_path) as f:
        return [line.strip() for line in f if line.strip()]


def generate_test_stubs(scenarios: list[str], test_type: str) -> str:
    prompt = (
        f"You are a senior QA automation engineer.\n"
        f"Generate all possible {test_type} test cases in Python "
        "using pytest format.\n"
        f"Each function should:\n"
        f"- Start with `test_`\n"
        f"- Be in snake_case\n"
        f"- Contain only `pass` as the function body\n"
        f"Here are the high-level scenarios:\n\n"
    )
    for s in scenarios:
        prompt += f"- {s}\n"

    # Use Gemini 2.0 Flash model via the client
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    return response.text  # Return generated Python test code


def write_to_file(output_path: str, content: str):
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        f.write("# Auto-generated test stubs\n\n")
        f.write(content)
    print(f"✅ Test stubs saved to '{output_path}'")


def main():
    if len(sys.argv) != 4:
        print(
            "Usage: python generate_pytest_tests_gemini_client.py "
            "<input_file.txt> <output_file.py> <test_type>"
        )
        print("test_type: smoke, sanity, regression")
        sys.exit(1)

    input_file, output_file, test_type = (
        sys.argv[1],
        sys.argv[2],
        sys.argv[3].lower(),
    )

    if test_type not in ["smoke", "sanity", "regression"]:
        print("❌ Invalid test_type. Choose from: smoke, sanity, regression")
        sys.exit(1)

    if not os.path.exists(input_file):
        print(f"❌ Input file '{input_file}' does not exist.")
        sys.exit(1)

    scenarios = read_scenarios(input_file)
    stub_code = generate_test_stubs(scenarios, test_type)
    write_to_file(output_file, stub_code)


if __name__ == "__main__":
    main()

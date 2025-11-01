import os
import sys
import traceback
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    if not api_key:
        print("Error: GEMINI_API_KEY is missing from environment")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Error: Prompt not provided.")
        sys.exit(1)

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg != "--verbose"]
    user_prompt = " ".join(args)

    system_prompt = """
You are a helpful AI coding agent.

Your task is to inspect, debug, and fix code inside the calculator project.
You may only modify files under the ./calculator/pkg directory, not main.py.

You can reason step-by-step to complete programming tasks.
When a user asks a question or makes a request, decide what to do next and plan accordingly.

You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

Always provide relative paths only. 
Once you have gathered enough information or completed the task, respond with an explanation in plain text.
"""

    try:
        client = genai.Client(api_key=api_key)

        available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_get_file_content,
                schema_run_python_file,
                schema_write_file,
            ]
        )

        messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

        for i in range(20):
            if verbose:
                print(f"\n--- Iteration {i + 1} ---")

            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                ),
            )

            for candidate in response.candidates:
                messages.append(candidate.content)

            # Print function calls if they exist
            if response.function_calls:
                for fn in response.function_calls:
                    function_call_result = call_function(fn, verbose)

                    if not function_call_result.parts:
                        raise RuntimeError(f"Function {fn.name} call failed")
                    
                    # Append the tool result as a message
                    messages.append(function_call_result)
                    
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                continue
            
            if response.text:
                print("Final response:")
                print(response.text.strip())
                break

            else:
                print("No text or function calls found, stopping.")
                break

        else:
            print("Reached maximum iteration limit (20).")

    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
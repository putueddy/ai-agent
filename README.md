# AI Coding Agent

An AI-powered coding agent that uses Google's Gemini API to inspect, debug, and fix code autonomously. The agent can interact with a calculator project through function calling, demonstrating practical AI-assisted software development.

## Features

- **Autonomous Code Analysis**: AI agent can inspect and understand code structure
- **Function Calling**: Implements tool use with Gemini API for file operations
- **Code Modification**: Can write and update files within specified boundaries
- **Python Execution**: Runs Python files with arguments and captures output
- **Iterative Problem Solving**: Uses multi-turn conversations to complete complex tasks

## Project Structure

```
ai-agent/
├── main.py                 # Main AI agent orchestrator
├── functions/              # Function declarations and implementations
│   ├── call_function.py    # Function call dispatcher
│   ├── get_files_info.py   # List files and directories
│   ├── get_file_content.py # Read file contents
│   ├── run_python_file.py  # Execute Python files
│   └── write_file.py       # Write/overwrite files
├── calculator/             # Example project for the agent to work with
│   ├── main.py             # Calculator CLI entry point
│   ├── pkg/
│   │   ├── calculator.py   # Calculator logic with operator precedence
│   │   └── render.py       # JSON output formatting
│   └── tests.py            # Calculator test suite
├── tests.py                # Function testing suite
└── pyproject.toml          # Project dependencies
```

## Requirements

- Python 3.13+
- Google Gemini API key
- Dependencies:
  - `google-genai==1.12.1`
  - `python-dotenv==1.1.0`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-agent
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Or using uv:
uv sync
```

3. Create a `.env` file with your Gemini API key:
```bash
GEMINI_API_KEY=your_api_key_here
```

## Usage

### Running the AI Agent

The AI agent accepts natural language prompts to perform tasks on the calculator project:

```bash
python main.py "your prompt here"
```

**Examples:**

```bash
# Inspect the calculator code
python main.py "Show me what files are in the calculator project"

# Debug and fix issues
python main.py "The calculator is not working correctly, please fix it"

# Run tests
python main.py "Run the calculator tests and show me the results"

# Verbose mode for debugging
python main.py "Check the calculator code" --verbose
```

### Using the Calculator Directly

```bash
cd calculator
python main.py "3 + 5"
# Output: {"expression": "3 + 5", "result": 8}

python main.py "10 * 2 + 5"
# Output: {"expression": "10 * 2 + 5", "result": 25}
```

## How It Works

1. **System Prompt**: The agent is initialized with instructions to work on the calculator project
2. **Function Declarations**: Four tools are available:
   - `get_files_info`: List directory contents
   - `get_file_content`: Read file contents
   - `run_python_file`: Execute Python files
   - `write_file`: Create or modify files
3. **Iterative Loop**: The agent makes up to 20 iterations of:
   - Analyze the task
   - Call functions to gather information or make changes
   - Receive function results
   - Continue until task completion
4. **Safety Constraints**: Agent can only modify files in `./calculator/pkg/`, not core files

## Calculator Features

The calculator project demonstrates:
- **Operator Precedence**: Correctly handles `+`, `-`, `*`, `/` with proper precedence
- **Infix Evaluation**: Evaluates space-separated mathematical expressions
- **JSON Output**: Returns results in structured JSON format
- **Error Handling**: Validates tokens and expression structure
- **Integer Optimization**: Returns integers when results have no decimal component

## Testing

Run the function tests:
```bash
python tests.py
```

Run the calculator tests:
```bash
cd calculator
python tests.py
```

## Configuration

- **Model**: Uses `gemini-2.0-flash-001`
- **Max Iterations**: 20 turns per conversation
- **Working Directory**: `./calculator/pkg/` for modifications
- **Relative Paths**: All file operations use relative paths

## Limitations

- Agent can only modify files under `./calculator/pkg/`
- Maximum 20 iterations per task
- Requires valid Gemini API key
- Calculator only supports basic arithmetic operators

## Development

The project uses:
- **Python 3.13+** for modern Python features
- **uv** for fast dependency management
- **python-dotenv** for environment variable management
- **Google Gemini API** for AI capabilities

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

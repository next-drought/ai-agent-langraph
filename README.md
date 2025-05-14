# Medium Article Analyzer - Go Implementation

A Go-based text analysis tool that uses local LLMs through Ollama to analyze articles and text content.

## Features

The analyzer can:
1. Classify a given text into predefined categories (News, Blog, Research, Other)
2. Extract named entities (Person, Organization, Location) from the text
3. Generate a concise summary of the text

## Requirements

- Go 1.18 or higher
- Ollama running locally with a compatible model (tested with DeepSeek)

## Setup Instructions

### 1. Install Go
Make sure you have Go installed on your system. You can download it from [golang.org](https://golang.org/dl/).

### 2. Set up Ollama
Install Ollama from [ollama.ai](https://ollama.ai) and pull the DeepSeek model:

```bash
ollama pull deepseek-r1:8b
```

### 3. Run the analyzer
Clone this repository and use the provided Makefile:

```bash
git clone https://github.com/next-drought/ai-agent-langraph.git
cd ai-agent-langraph
make run
```

## Usage

The application comes with a Makefile that provides several commands:

```bash
make run         # Run the application
make build       # Build the application
make test        # Test the application
make clean       # Clean build artifacts
make check-ollama # Check if Ollama is running
make help        # Show available commands
```

## How It Works

The analyzer follows a sequential workflow:

1. **Classification**: Determines the type of content (News, Blog, Research, Other)
2. **Entity Extraction**: Identifies people, organizations, and locations mentioned in the text
3. **Summarization**: Creates a concise summary of the content

All processing is done locally using the Ollama API, with no data sent to external services.

## Customization

You can modify the model used by changing the `model` variable in `main.go`:

```go
model := "your-preferred-model" // Replace with any model available in your Ollama installation
```

You can also adjust the prompts in each function to customize how the LLM processes the text.

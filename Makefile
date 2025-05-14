.PHONY: run build test clean help check-ollama

# Default Go command
GO=go

# Application name
APP_NAME=medium-article-analyzer

# Check if Ollama is running
check-ollama:
	@echo "Checking if Ollama is running..."
	@curl -s http://localhost:11434/api/version > /dev/null || (echo "Error: Ollama is not running. Please start Ollama first." && exit 1)
	@echo "Ollama is running."

# Run the application
run: check-ollama
	@echo "Running the Medium Article Analyzer..."
	$(GO) run main.go

# Build the application
build:
	@echo "Building $(APP_NAME)..."
	$(GO) build -o $(APP_NAME) main.go
	@echo "Build complete: $(APP_NAME)"

# Test the application (build and run)
test: check-ollama build
	@echo "Testing the application..."
	./$(APP_NAME)
	@echo "Test complete."

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -f $(APP_NAME)
	@echo "Clean complete."

# Help command
help:
	@echo "Available commands:"
	@echo "  make run          - Run the application"
	@echo "  make build        - Build the application"
	@echo "  make test         - Build and run the application"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make check-ollama - Check if Ollama is running"
	@echo "  make help         - Show this help message"
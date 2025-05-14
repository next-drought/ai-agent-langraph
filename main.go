package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "log"
    "net/http"
    "strings"
)

// AnalyzerState represents the state of our analyzer agent
type AnalyzerState struct {
    Text           string   `json:"text"`
    Classification string   `json:"classification"`
    Entities       []string `json:"entities"`
    Summary        string   `json:"summary"`
}

// OllamaRequest represents a request to the Ollama API
type OllamaRequest struct {
    Model       string  `json:"model"`
    Prompt      string  `json:"prompt"`
    Stream      bool    `json:"stream"`
    Temperature float64 `json:"temperature"`
}

// OllamaResponse represents a response from the Ollama API
type OllamaResponse struct {
    Model     string `json:"model"`
    CreatedAt string `json:"created_at"`
    Response  string `json:"response"`
}

// callOllama sends a request to the Ollama API and returns the response
func callOllama(prompt string, model string) (string, error) {
    ollamaURL := "http://localhost:11434/api/generate"
    
    request := OllamaRequest{
        Model:       model,
        Prompt:      prompt,
        Stream:      false,
        Temperature: 0.0,
    }
    
    requestBody, err := json.Marshal(request)
    if err != nil {
        return "", fmt.Errorf("error marshaling request: %v", err)
    }
    
    resp, err := http.Post(ollamaURL, "application/json", bytes.NewBuffer(requestBody))
    if err != nil {
        return "", fmt.Errorf("error calling Ollama API: %v", err)
    }
    defer resp.Body.Close()
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return "", fmt.Errorf("error reading response body: %v", err)
    }
    
    var ollamaResponse OllamaResponse
    err = json.Unmarshal(body, &ollamaResponse)
    if err != nil {
        return "", fmt.Errorf("error unmarshaling response: %v", err)
    }
    
    return ollamaResponse.Response, nil
}

// classifyText classifies the input text into one of predefined categories
func classifyText(text string, model string) (string, error) {
    fmt.Println("\n--- Executing Classification Node ---")
    
    prompt := fmt.Sprintf(
        "Classify the following text into one of these categories: News, Blog, Research, or Other.\n\n"+
            "Text:\n%s\n\n"+
            "Classification:",
        text,
    )
    
    response, err := callOllama(prompt, model)
    if err != nil {
        return "", err
    }
    
    fmt.Printf("Raw classification from LLM: '%s'\n", response)
    
    // Simple normalization
    validCategories := []string{"News", "Blog", "Research", "Other"}
    normalizedClassification := response
    foundCategory := false
    
    for _, category := range validCategories {
        if strings.Contains(strings.ToLower(response), strings.ToLower(category)) {
            normalizedClassification = category
            foundCategory = true
            break
        }
    }
    
    if !foundCategory {
        normalizedClassification = "Other" // Default if no clear match
    }
    
    fmt.Printf("Final classification: %s\n", normalizedClassification)
    return normalizedClassification, nil
}

// extractEntities extracts named entities from the text
func extractEntities(text string, model string) ([]string, error) {
    fmt.Println("\n--- Executing Entity Extraction Node ---")
    
    prompt := fmt.Sprintf(
        "Extract all named entities (Person, Organization, Location) from the following text. "+
            "List them as comma-separated values. If no entities are found, respond with 'None'.\n\n"+
            "Text:\n%s\n\n"+
            "Entities (comma-separated or None):",
        text,
    )
    
    response, err := callOllama(prompt, model)
    if err != nil {
        return nil, err
    }
    
    var entitiesList []string
    if response != "" && strings.ToLower(response) != "none" {
        // Split by comma and trim spaces
        entities := strings.Split(response, ",")
        for _, entity := range entities {
            trimmed := strings.TrimSpace(entity)
            if trimmed != "" {
                entitiesList = append(entitiesList, trimmed)
            }
        }
    }
    
    fmt.Printf("Extracted entities: %v\n", entitiesList)
    return entitiesList, nil
}

// summarizeText generates a concise summary of the input text
func summarizeText(text string, model string) (string, error) {
    fmt.Println("\n--- Executing Summarization Node ---")
    
    prompt := fmt.Sprintf(
        "Summarize the following text in one short, concise sentence.\n\n"+
            "Text:\n%s\n\n"+
            "Summary:",
        text,
    )
    
    response, err := callOllama(prompt, model)
    if err != nil {
        return "", err
    }
    
    fmt.Printf("Generated summary: %s\n", response)
    return response, nil
}

// runAnalyzerWorkflow runs the complete analyzer workflow
func runAnalyzerWorkflow(text string, model string) (*AnalyzerState, error) {
    state := &AnalyzerState{
        Text: text,
    }
    
    // Step 1: Classification
    classification, err := classifyText(text, model)
    if err != nil {
        return nil, fmt.Errorf("classification error: %v", err)
    }
    state.Classification = classification
    
    // Step 2: Entity Extraction
    entities, err := extractEntities(text, model)
    if err != nil {
        return nil, fmt.Errorf("entity extraction error: %v", err)
    }
    state.Entities = entities
    
    // Step 3: Summarization
    summary, err := summarizeText(text, model)
    if err != nil {
        return nil, fmt.Errorf("summarization error: %v", err)
    }
    state.Summary = summary
    
    return state, nil
}

// checkOllamaAvailability checks if Ollama is running
func checkOllamaAvailability() error {
    resp, err := http.Get("http://localhost:11434/api/version")
    if err != nil {
        return fmt.Errorf("Ollama is not available: %v", err)
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        return fmt.Errorf("Ollama returned non-OK status: %d", resp.StatusCode)
    }
    
    return nil
}

func main() {
    fmt.Println("Starting Medium Article Analyzer Agent Test...")
    
    // Check if Ollama is available
    if err := checkOllamaAvailability(); err != nil {
        log.Fatalf("Error: %v\nPlease make sure Ollama is running.", err)
    }
    
    model := "deepseek-r1:8b" // Use the DeepSeek model
    
    // Sample text for testing
    sampleText := "Anthropic's MCP (Model Context Protocol) is an open-source powerhouse that lets " +
        "developers build applications that can seamlessly interact with various API systems. " +
        "It aims to standardize how models access external knowledge and tools, " +
        "potentially revolutionizing how AI agents are built and deployed across different platforms."
    
    fmt.Printf("\nInput Text:\n'''\n%s\n'''\n", sampleText)
    
    // Run the analyzer workflow
    result, err := runAnalyzerWorkflow(sampleText, model)
    if err != nil {
        log.Fatalf("Error running analyzer workflow: %v", err)
    }
    
    // Print the results
    fmt.Println("\n\n--- Agent Processing Complete ---")
    fmt.Printf("Original Text: '''\n%s'''\n", result.Text)
    fmt.Printf("Classification: %s\n", result.Classification)
    fmt.Printf("Entities: %v\n", result.Entities)
    fmt.Printf("Summary: %s\n", result.Summary)
}

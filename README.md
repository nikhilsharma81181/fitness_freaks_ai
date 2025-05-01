# Fitness Coach AI

An intelligent assistant that helps users manage their fitness journey through natural language interactions.

## Project Overview

Fitness Coach AI is an AI-powered system that allows users to:

- Schedule and customize workout plans
- Log workout sessions in a database
- Track exercise sets, reps, and performance
- Create and monitor diet plans
- Log food intake and nutrition data
- Receive personalized fitness advice and encouragement
- Start and end workout sessions with simple commands

The system architecture consists of two main components:

1. **Python AI Backend** (this repository): Handles all AI-related functionality including natural language processing, intent recognition, and AI agent orchestration
2. **Node.js Backend** (separate repository): Manages database operations, user authentication, and serves as the API for the iOS client application

## Getting Started

### Prerequisites

- Python 3.13+
- uv package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fitness-freaks-ai.git
cd fitness-freaks-ai
```

2. Run the setup script:
```bash
python setup.py
```

3. Activate the virtual environment:
```bash
# On Windows
.venv\Scripts\activate

# On Unix/MacOS
source .venv/bin/activate
```

4. Edit the `.env` file with your API keys:
```
# Required
GOOGLE_API_KEY=your_google_api_key_here
```

5. Run the application:
```bash
python -m src.main
```

The API will be available at http://localhost:8000

## API Endpoints

- **GET /health**: Health check endpoint
- **GET /**: Root endpoint with API information
- **POST /api/v1/chat**: Main chat endpoint for AI interaction

### Chat Endpoint

The chat endpoint accepts POST requests with the following JSON structure:

```json
{
  "messages": [
    {"role": "user", "content": "I want to create a workout plan for building muscle."}
  ],
  "user_id": "optional_user_id",
  "user_context": {
    "profile": {
      "age": 30,
      "weight": 75,
      "height": 180,
      "fitness_level": "intermediate"
    },
    "preferences": {
      "preferred_workout_types": ["weightlifting", "HIIT"],
      "available_equipment": ["dumbbells", "bench"]
    },
    "goals": ["build muscle", "increase strength"]
  }
}
```

The response will include:

```json
{
  "response": "The assistant's response text...",
  "intent": {
    "category": "workout_planning",
    "confidence": 0.95
  },
  "extracted_data": {},
  "suggested_actions": []
}
```

## Project Structure

```
fitness-freaks-ai/
├── src/                      # Source code
│   ├── main.py               # Application entry point
│   ├── api/                  # API endpoints
│   │   ├── routes/           # API routes
│   │   └── models/           # API data models
│   ├── core/                 # Core functionality
│   │   ├── llm/              # LLM integration
│   │   ├── intent/           # Intent classification
│   │   └── agents/           # Agent system (coming soon)
│   └── utils/                # Utility functions
├── tests/                    # Test cases
│   ├── test_api/             # API tests
│   └── test_core/            # Core functionality tests
├── data/                     # Data files
├── .env.example              # Example environment variables
├── config.yaml               # Application configuration
└── README.md                 # This file
```

## Configuration

The application can be configured using:

1. Environment variables (see `.env.example`)
2. Configuration file (`config.yaml`)

### LLM Configuration

This application supports the following LLM providers:

- **Google Gemini**: Set `GOOGLE_API_KEY` in your .env file
- **Groq**: Set `GROQ_API_KEY` in your .env file (optional)

You can specify which provider to use as the default in the `config.yaml` file.

## Development

### Running Tests

```bash
pytest
```

### Adding New Features

1. Create a new feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit them:
```bash
git add .
git commit -m "Add your feature description"
```

3. Push your changes and create a pull request:
```bash
git push origin feature/your-feature-name
```

## Next Steps

The current implementation provides a basic framework for the Fitness Coach AI. The next steps include:

1. Implementing specialized agents for different domains (workout planning, diet planning, etc.)
2. Building knowledge bases for exercises and nutrition
3. Enhancing integration with the Node.js backend
4. Adding more advanced features like personalized recommendations

## License

[MIT License](LICENSE)
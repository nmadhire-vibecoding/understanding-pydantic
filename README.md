# Pydantic Demo with Google Gemini

A simple demonstration of Pydantic features integrated with Google Gemini for structured output.

## Features Demonstrated

1. **Structured Output with Google Gemini**
   - Using Pydantic models as schema for LLM responses
   - Ensuring type-safe AI responses
   - Automatic validation of AI-generated content
2. **Prompt Chaining (Kid-Suitability Check)**
   - Reuse the first model's structured review as input to a second prompt
   - Validates a second JSON response: whether the movie is suitable for kids under 10
   - Returns fields: suitable_for_under_10, reasoning, warnings, suggested_min_age

## Setup

The project uses `uv` for dependency management.

### Install Dependencies

```bash
uv sync
```

### Set up Google Gemini API Key

Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey) and set it:

```bash
export GOOGLE_API_KEY='your-api-key-here'
# or
export GEMINI_API_KEY='your-api-key-here'
```

## Run the Demo

```bash
uv run pydantic_demo.py
```

Or activate the virtual environment:

```bash
source .venv/bin/activate
python pydantic_demo.py
```

### CLI: choose a movie title

You can pass a custom movie title with `--movie` (or `-m`). If omitted, the default is "The Matrix".

```bash
# Default (reviews "The Matrix")
uv run pydantic_demo.py

# Custom movie
uv run pydantic_demo.py --movie "Toy Story"
```

## What You'll Learn

- How to define and validate structured JSON output with Pydantic
- How to use Pydantic with Google Gemini for type-safe AI responses
- How to extract and sanitize JSON from LLM outputs
- How to chain prompts: passing validated output into a second model query
- How to validate a secondary schema (kid suitability assessment)

## Example Output

The script will show:
- 🤖 Structured movie review from Google Gemini, validated with Pydantic
- 🎯 Chained suitability assessment for kids under 10 with validated JSON output

## Dependencies

- `pydantic` - Data validation and settings management
- `google-generativeai` - Google Gemini API (using Gemini 2.5 Flash)
- `email-validator` - Email validation support (indirectly required by Pydantic's EmailStr if used in future extensions)

## Gemini Models

This demo uses **Gemini 2.5 Flash** (stable), which offers the best price-performance ratio. Other available models include:

- `gemini-2.5-pro` - Most advanced for complex reasoning
- `gemini-2.5-flash` - Best price-performance (default)
- `gemini-2.5-flash-lite` - Fastest and most cost-efficient
- `gemini-2.0-flash` - Previous generation workhorse
- `gemini-2.0-flash-lite` - Previous generation small model

For the latest models and details, visit: https://ai.google.dev/gemini-api/docs/models

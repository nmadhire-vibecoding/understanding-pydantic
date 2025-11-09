# Agent Development Notes

This document captures key decisions, best practices, and helpful context for future development of this Pydantic demo project.

## Project Overview

A comprehensive Python demonstration of Pydantic data validation integrated with Google Gemini AI for structured outputs. Built to showcase modern Python type safety and AI integration patterns.

## Technology Stack

- **Python**: 3.11.13 (matches system Python)
- **Package Manager**: uv (modern, fast Python package manager)
- **Key Dependencies**:
  - `pydantic` 2.12.4+ (data validation)
  - `google-generativeai` 0.8.5+ (Gemini API)
  - `email-validator` 2.3.0+ (email validation support)

## Best Practices Implemented

### 1. Pydantic V2 Standards
- ✅ Used `@field_validator` instead of deprecated `@validator`
- ✅ Used `ConfigDict` instead of class-based `Config`
- ✅ Used `model_dump_json()` instead of deprecated methods
- ✅ Proper type hints with `typing` module

### 2. Google Gemini Integration
- ✅ Using **gemini-2.5-flash** (latest stable model as of Nov 2025)
- ✅ Best price-performance ratio for production use
- ✅ Documented all available models in code and README
- ✅ Graceful handling when API key is missing
- ✅ Proper JSON extraction from LLM responses (handles markdown code blocks)

### 3. Project Structure
- ✅ Clean separation: single demo file with clear examples
- ✅ Comprehensive README with setup instructions
- ✅ `.env.example` for API key configuration
- ✅ `.python-version` for consistent Python versioning
- ✅ Removed unnecessary boilerplate files (main.py)

### 4. Code Quality
- ✅ Comprehensive docstrings for all classes and functions
- ✅ Clear example progression: basic → nested → AI integration
- ✅ Demonstrates both success and failure cases
- ✅ Proper error handling with ValidationError
- ✅ User-friendly console output with emojis and formatting

### 5. Dependency Management
- ✅ Using `uv` for fast, reliable dependency management
- ✅ Pinned minimum versions for stability
- ✅ Lock file (`uv.lock`) for reproducible builds

## Key Features Demonstrated

### Example 1: Basic Pydantic Validation
- Type checking (int, str, bool, datetime)
- Email validation with EmailStr
- Field constraints (ge=0, le=150 for age)
- Custom validators with @field_validator
- Default values and default factories
- Automatic type coercion and validation

### Example 2: Nested Models
- Complex nested structures (User inside UserProfile)
- Optional fields with Optional[Type]
- List fields with type hints
- JSON serialization of nested models
- Dictionary initialization of models

### Example 3: Gemini + Pydantic
- Using Pydantic models as schemas for LLM output
- Automatic validation of AI-generated content
- Type-safe AI responses
- Structured data extraction from natural language

## Future Enhancement Ideas

### Additional Pydantic Features to Demo
- [ ] Field aliases and serialization aliases
- [ ] Custom serializers with `@field_serializer`
- [ ] Model inheritance and composition
- [ ] Computed fields with `@computed_field`
- [ ] Model validators with `@model_validator`
- [ ] Custom types and validators
- [ ] Settings management with `BaseSettings`
- [ ] Strict mode vs lax mode

### Gemini Integration Enhancements
- [ ] Add native structured output using `response_schema` parameter
- [ ] Demonstrate function calling with Pydantic models
- [ ] Add streaming responses example
- [ ] Compare different Gemini models (Pro vs Flash vs Flash-Lite)
- [ ] Add token counting example
- [ ] Demonstrate context caching for large schemas

### Testing & Validation
- [ ] Add pytest tests for Pydantic models
- [ ] Add hypothesis for property-based testing
- [ ] Mock Gemini API responses for testing
- [ ] Add performance benchmarks

### Documentation
- [ ] Add API reference documentation
- [ ] Create Jupyter notebook version
- [ ] Add more complex real-world examples
- [ ] Add troubleshooting guide

## Common Commands

```bash
# Install/sync dependencies
uv sync

# Run the demo
uv run pydantic_demo.py

# Run with virtual environment activated
source .venv/bin/activate
python pydantic_demo.py

# Check Python version
uv run python --version

# Add new dependency
uv add <package-name>

# Remove dependency
uv remove <package-name>

# Update all dependencies
uv sync --upgrade
```

## Environment Setup

### Required Environment Variables
```bash
export GOOGLE_API_KEY='your-api-key-here'
# OR
export GEMINI_API_KEY='your-api-key-here'
```

Get your API key from: https://makersuite.google.com/app/apikey

## Gemini Model Reference

As of November 2025, available models:

| Model | Best For | Context Window |
|-------|----------|----------------|
| `gemini-2.5-pro` | Complex reasoning, STEM problems | Large |
| `gemini-2.5-flash` | **Production use** (best price/performance) | 1M tokens |
| `gemini-2.5-flash-lite` | High throughput, cost efficiency | 1M tokens |
| `gemini-2.0-flash` | Previous generation workhorse | 1M tokens |
| `gemini-2.0-flash-lite` | Previous generation small | 1M tokens |

**Current model in use**: `gemini-2.5-flash` (recommended)

Latest models: https://ai.google.dev/gemini-api/docs/models

## Important Notes

### When Updating Dependencies
- Always test the demo after updates
- Check for Pydantic deprecation warnings
- Verify Gemini API compatibility
- Update model names if needed

### When Adding New Examples
- Follow the existing pattern (function per example)
- Include both success and failure cases
- Add clear console output with emojis
- Document the feature being demonstrated
- Update README if adding significant functionality

### Code Style
- Use type hints everywhere
- Keep functions focused and single-purpose
- Add docstrings for public functions and classes
- Use descriptive variable names
- Format with clear separators in console output

## Troubleshooting

### Common Issues

**Issue**: `models/gemini-X not found`
- **Solution**: Check https://ai.google.dev/gemini-api/docs/models for current model names

**Issue**: Pydantic deprecation warnings
- **Solution**: Use Pydantic V2 syntax (field_validator, ConfigDict, model_dump_json)

**Issue**: Email validation not working
- **Solution**: Ensure `email-validator` is installed (`uv add email-validator`)

**Issue**: Import errors
- **Solution**: Run `uv sync` to ensure all dependencies are installed

## Version History

- **v0.1.0** (Nov 9, 2025)
  - Initial implementation
  - Python 3.11 compatibility
  - Pydantic V2 best practices
  - Gemini 2.5 Flash integration
  - Comprehensive examples and documentation

"""
Pydantic Demo with Google Gemini
This script demonstrates key Pydantic features:
- Data validation
- Type checking
- Nested models
- Field constraints
- Using structured output with Google Gemini

Available Gemini Models (as of November 2025):
- gemini-2.5-pro: Most advanced thinking model for complex reasoning
- gemini-2.5-flash: Best price-performance (recommended for production)
- gemini-2.5-flash-lite: Fastest, optimized for cost-efficiency
- gemini-2.0-flash: Previous generation workhorse model
- gemini-2.0-flash-lite: Previous generation small model

For latest models, see: https://ai.google.dev/gemini-api/docs/models
"""

import os
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationError, ConfigDict
import google.generativeai as genai


# Example 1: Basic Pydantic Model
class User(BaseModel):
    """A simple user model demonstrating basic Pydantic features"""
    id: int
    name: str
    email: EmailStr  # Validates email format
    age: int = Field(..., ge=0, le=150)  # Age must be between 0 and 150
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    
    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.title()  # Capitalize name


# Example 2: Nested Models
class Address(BaseModel):
    """Address model"""
    street: str
    city: str
    country: str
    zip_code: str = Field(..., min_length=5, max_length=10)


class UserProfile(BaseModel):
    """User profile with nested address"""
    user: User
    address: Optional[Address] = None
    phone_numbers: List[str] = []


# Example 3: Using Pydantic with Google Gemini for structured output
class MovieReview(BaseModel):
    """Structured movie review"""
    model_config = ConfigDict(
        json_schema_extra={
            "type": "object",
            "required": ["title", "rating", "genre", "summary"]
        }
    )
    
    title: str = Field(..., description="Movie title")
    rating: int = Field(..., ge=1, le=10, description="Rating from 1 to 10")
    genre: str = Field(..., description="Movie genre")
    summary: str = Field(..., description="Brief summary of the movie")
    pros: List[str] = Field(default_factory=list, description="Positive aspects")
    cons: List[str] = Field(default_factory=list, description="Negative aspects")


# Prompt chaining schema: assess suitability for kids under 10
class MovieSuitability(BaseModel):
    """Assessment of whether a movie is suitable for kids under 10"""
    suitable_for_under_10: bool = Field(..., description="True if suitable for children under 10")
    reasoning: str = Field(..., description="Short explanation of the decision")
    warnings: List[str] = Field(default_factory=list, description="Content warnings or concerns")
    suggested_min_age: int = Field(..., ge=0, le=18, description="Suggested minimum viewing age")


def _extract_json_text(response_text: str) -> str:
    """Extract raw JSON from a model response, handling fenced code blocks and extra text.

    Strategy:
    - Trim whitespace
    - Remove leading ```json or ``` fences
    - Slice from first '{' to last '}' as a fallback for robustness
    """
    text = response_text.strip()
    # Remove common markdown fences
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    # Fallback: grab JSON object bounds
    if '{' in text and '}' in text:
        start = text.find('{')
        end = text.rfind('}') + 1
        return text[start:end].strip()
    return text


def demonstrate_basic_pydantic():
    """Demonstrate basic Pydantic validation"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Pydantic Validation")
    print("=" * 60)
    
    # Valid user
    try:
        user = User(
            id=1,
            name="john doe",
            email="john@example.com",
            age=30
        )
        print("\n✅ Valid User Created:")
        print(f"  Name: {user.name}")  # Will be capitalized
        print(f"  Email: {user.email}")
        print(f"  Age: {user.age}")
        print(f"  Created at: {user.created_at}")
        print(f"\n  JSON: {user.model_dump_json(indent=2)}")
    except ValidationError as e:
        print(f"❌ Error: {e}")
    
    # Invalid user - bad email
    print("\n" + "-" * 60)
    print("Testing with invalid email:")
    try:
        invalid_user = User(
            id=2,
            name="Jane Doe",
            email="not-an-email",
            age=25
        )
    except ValidationError as e:
        print(f"❌ Validation Error (as expected):")
        for error in e.errors():
            print(f"  Field: {error['loc'][0]}, Error: {error['msg']}")
    
    # Invalid user - age out of range
    print("\n" + "-" * 60)
    print("Testing with invalid age:")
    try:
        invalid_user = User(
            id=3,
            name="Old Person",
            email="old@example.com",
            age=200
        )
    except ValidationError as e:
        print(f"❌ Validation Error (as expected):")
        for error in e.errors():
            print(f"  Field: {error['loc'][0]}, Error: {error['msg']}")


def demonstrate_nested_models():
    """Demonstrate nested Pydantic models"""
    print("\n\n" + "=" * 60)
    print("EXAMPLE 2: Nested Models")
    print("=" * 60)
    
    try:
        profile = UserProfile(
            user={
                "id": 1,
                "name": "alice wonderland",
                "email": "alice@example.com",
                "age": 28
            },
            address={
                "street": "123 Main St",
                "city": "San Francisco",
                "country": "USA",
                "zip_code": "94102"
            },
            phone_numbers=["+1-555-0100", "+1-555-0101"]
        )
        
        print("\n✅ User Profile Created:")
        print(f"  User: {profile.user.name}")
        print(f"  Email: {profile.user.email}")
        print(f"  City: {profile.address.city}")
        print(f"  Phones: {', '.join(profile.phone_numbers)}")
        print(f"\n  Full JSON:\n{profile.model_dump_json(indent=2)}")
        
    except ValidationError as e:
        print(f"❌ Error: {e}")


def demonstrate_gemini_structured_output():
    """Demonstrate using Pydantic with Google Gemini for structured output"""
    print("\n\n" + "=" * 60)
    print("EXAMPLE 3: Pydantic with Google Gemini")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("\n⚠️  Note: GOOGLE_API_KEY or GEMINI_API_KEY not found in environment variables.")
        print("To run this example, set your API key:")
        print("  export GOOGLE_API_KEY='your-api-key-here'")
        print("\nSkipping Gemini example...")
        return
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Use Gemini 2.5 Flash - latest stable model with best price-performance
        # As of November 2025, this is the recommended model for production use
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        print("\n🤖 Asking Gemini 2.5 Flash to review 'The Matrix' with structured output...")
        
        # Create a prompt that asks for JSON in the Pydantic schema format
        prompt = """Write a review of the movie 'The Matrix' (1999) in JSON format with these fields:
        - title: string (movie title)
        - rating: integer 1-10
        - genre: string
        - summary: string (brief summary)
        - pros: array of strings (positive aspects)
        - cons: array of strings (negative aspects)
        
        Return ONLY the JSON, no other text."""
        
        response = model.generate_content(prompt)

        # Extract JSON and validate against the schema
        review = MovieReview.model_validate_json(_extract_json_text(response.text))
        
        print("\n✅ Structured Movie Review Generated and Validated:")
        print(f"\n  Title: {review.title}")
        print(f"  Genre: {review.genre}")
        print(f"  Rating: {review.rating}/10")
        print(f"\n  Summary: {review.summary}")
        print(f"\n  Pros:")
        for pro in review.pros:
            print(f"    • {pro}")
        print(f"\n  Cons:")
        for con in review.cons:
            print(f"    • {con}")
        
        print(f"\n  Validated Pydantic Model JSON:\n{review.model_dump_json(indent=2)}")

        # Chain another prompt: assess suitability for kids under 10
        print("\n" + "-" * 60)
        print("Chaining: Assessing suitability for kids under 10...")
        suitability = assess_movie_suitability(review, model)

        print("\n🎯 Suitability Assessment:")
        print(f"  Suitable for under 10: {'Yes' if suitability.suitable_for_under_10 else 'No'}")
        print(f"  Suggested minimum age: {suitability.suggested_min_age}")
        print(f"  Reasoning: {suitability.reasoning}")
        if suitability.warnings:
            print("  Warnings:")
            for w in suitability.warnings:
                print(f"    • {w}")
        print(f"\n  Raw JSON:\n{suitability.model_dump_json(indent=2)}")
        
    except ValidationError as e:
        print(f"❌ Validation Error - Gemini response doesn't match schema:")
        for error in e.errors():
            print(f"  Field: {error['loc']}, Error: {error['msg']}")
    except Exception as e:
        print(f"❌ Error: {e}")


def assess_movie_suitability(review: MovieReview, model: "genai.GenerativeModel") -> MovieSuitability:
    """Call Gemini with the movie review to assess suitability for kids under 10.

    Returns a validated MovieSuitability instance.
    """
    review_json = review.model_dump_json()
    print(review_json)
    prompt = f"""
You are a helpful content suitability assistant. Given the following JSON movie review, determine if the movie is suitable for children under 10. Consider violence, language, fear/intensity, sexual content, substance use, and overall themes.

Return ONLY a JSON object with exactly these fields:
- suitable_for_under_10: boolean
- reasoning: string (max 3 sentences)
- warnings: array of strings (list any relevant content warnings)
- suggested_min_age: integer (0-18)

Movie review JSON:
{review_json}
"""

    response = model.generate_content(prompt)
    json_text = _extract_json_text(response.text)
    return MovieSuitability.model_validate_json(json_text)


def main():
    """Run all demonstrations"""
    print("\n" + "🐍 PYDANTIC DEMONSTRATION " + "🐍".center(60))
    
    # Run examples
    demonstrate_basic_pydantic()
    demonstrate_nested_models()
    demonstrate_gemini_structured_output()
    
    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

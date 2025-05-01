"""
Pydantic schemas for API request and response models.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Message(BaseModel):
    """A message in a conversation."""
    role: str = Field(..., description="The role of the message sender (user or assistant)")
    content: str = Field(..., description="The content of the message")

class UserProfile(BaseModel):
    """User profile data."""
    age: Optional[int] = Field(None, description="User's age")
    weight: Optional[float] = Field(None, description="User's weight in kg")
    height: Optional[float] = Field(None, description="User's height in cm")
    fitness_level: Optional[str] = Field(None, description="User's fitness level (beginner, intermediate, advanced)")
    gender: Optional[str] = Field(None, description="User's gender")

class UserPreferences(BaseModel):
    """User preferences."""
    preferred_workout_types: Optional[List[str]] = Field(None, description="Preferred workout types")
    available_equipment: Optional[List[str]] = Field(None, description="Available equipment")
    dietary_restrictions: Optional[List[str]] = Field(None, description="Dietary restrictions")
    workout_frequency: Optional[int] = Field(None, description="Preferred weekly workout frequency")
    workout_duration: Optional[int] = Field(None, description="Preferred workout duration in minutes")

class UserContext(BaseModel):
    """Context about the user."""
    profile: Optional[UserProfile] = Field(None, description="User profile information")
    preferences: Optional[UserPreferences] = Field(None, description="User preferences")
    goals: Optional[List[str]] = Field(None, description="User fitness goals")
    limitations: Optional[List[str]] = Field(None, description="User limitations or health concerns")
    recent_activity: Optional[List[Dict[str, Any]]] = Field(None, description="Recent user activity")

class ChatRequest(BaseModel):
    """Chat request with conversation history."""
    messages: List[Message] = Field(..., description="The conversation history")
    user_id: Optional[str] = Field(None, description="The ID of the user")
    user_context: Optional[UserContext] = Field(None, description="Context about the user")

class IntentInfo(BaseModel):
    """Information about the classified intent."""
    category: str = Field(..., description="The classified intent category")
    confidence: float = Field(..., description="Confidence score for the intent classification")

class SuggestedAction(BaseModel):
    """Suggested follow-up action."""
    type: str = Field(..., description="The type of suggested action")
    label: str = Field(..., description="Display label for the action")
    data: Dict[str, Any] = Field({}, description="Data associated with the action")

class ChatResponse(BaseModel):
    """Chat response with assistant's message and intent classification."""
    response: str = Field(..., description="The assistant's response")
    intent: Optional[IntentInfo] = Field(None, description="Information about the classified intent")
    extracted_data: Optional[Dict[str, Any]] = Field({}, description="Any structured data extracted from the interaction")
    suggested_actions: Optional[List[SuggestedAction]] = Field([], description="Suggested follow-up actions")

# Workout models
class Exercise(BaseModel):
    """Exercise information."""
    name: str = Field(..., description="Exercise name")
    sets: Optional[int] = Field(None, description="Number of sets")
    reps: Optional[List[int]] = Field(None, description="Reps for each set")
    weight: Optional[List[float]] = Field(None, description="Weight for each set (in kg)")
    rest: Optional[int] = Field(None, description="Rest between sets (in seconds)")
    notes: Optional[str] = Field(None, description="Notes about the exercise")

class WorkoutSession(BaseModel):
    """Workout session information."""
    workout_type: str = Field(..., description="Type of workout")
    duration: Optional[int] = Field(None, description="Duration in minutes")
    exercises: List[Exercise] = Field(..., description="Exercises performed")
    notes: Optional[str] = Field(None, description="Notes about the workout")
    user_feedback: Optional[str] = Field(None, description="User feedback about the workout")

# Diet models
class FoodItem(BaseModel):
    """Food item information."""
    name: str = Field(..., description="Food name")
    portion: Optional[str] = Field(None, description="Portion size")
    calories: Optional[int] = Field(None, description="Calories")
    protein: Optional[float] = Field(None, description="Protein in grams")
    carbs: Optional[float] = Field(None, description="Carbohydrates in grams")
    fat: Optional[float] = Field(None, description="Fat in grams")
    notes: Optional[str] = Field(None, description="Notes about the food")

class MealEntry(BaseModel):
    """Meal entry information."""
    meal_type: str = Field(..., description="Type of meal (breakfast, lunch, dinner, snack)")
    time: Optional[str] = Field(None, description="Time of meal")
    foods: List[FoodItem] = Field(..., description="Foods consumed")
    water_intake: Optional[float] = Field(None, description="Water intake in ml")
    notes: Optional[str] = Field(None, description="Notes about the meal")
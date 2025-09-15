# Chatbot Simplification Plan

## Current Structure (Over-engineered)
- Multiple service layers (OpenAI, Anthropic abstractions)
- Complex session/conversation management
- Extensive security features (encryption, rate limiting)
- Multiple UI components
- Heavy dependencies

## Target Structure (Simple)
- Single streamlit_app.py file
- JSON configuration file for chatbot settings
- Environment variables for API keys and model selection
- Minimal dependencies (streamlit, openai, anthropic)
- Direct API calls without abstractions
- Simple session state management

## Key Changes
1. Remove unnecessary abstraction layers
2. Consolidate into single main file
3. Use JSON for all chatbot configuration
4. Simplify to essential features only
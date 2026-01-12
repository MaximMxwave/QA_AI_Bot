import logging
import asyncio
from typing import Optional
from openai import OpenAI, APIError
from anthropic import Anthropic
from config import Config

logger = logging.getLogger(__name__)

class AIService:
    """Unified interface for working with all AI assistants"""
    
    def __init__(self):
        self.openai_client = None
        self.claude_client = None
        self.deepseek_client = None
        self.default_model = Config.DEFAULT_AI_MODEL
        
        self._init_clients()
    
    def _init_clients(self):
        """Initialize clients for all AI services"""
        try:
            if Config.OPENAI_API_KEY:
                self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
                logger.info("✅ OpenAI client initialized")
        except Exception as e:
            logger.warning(f"⚠️ OpenAI init failed: {e}")
        
        try:
            if Config.ANTHROPIC_API_KEY:
                self.claude_client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
                logger.info("✅ Claude client initialized")
        except Exception as e:
            logger.warning(f"⚠️ Claude init failed: {e}")
        
        try:
            if Config.DEEPSEEK_API_KEY:
                self.deepseek_client = OpenAI(
                    api_key=Config.DEEPSEEK_API_KEY,
                    base_url=Config.DEEPSEEK_BASE_URL
                )
                logger.info("✅ DeepSeek client initialized")
        except Exception as e:
            logger.warning(f"⚠️ DeepSeek init failed: {e}")
    
    def generate_text(self, prompt: str, model: str = None, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Generate text with selected model"""
        model = model or self.default_model
        
        try:
            if model == "openai":
                return self._openai_generate(prompt, temperature, max_tokens)
            elif model == "claude":
                return self._claude_generate(prompt, temperature, max_tokens)
            elif model == "deepseek":
                return self._deepseek_generate(prompt, temperature, max_tokens)
            else:
                raise ValueError(f"Unknown model: {model}")
        except Exception as e:
            logger.error(f"Error generating text with {model}: {e}", exc_info=True)
            return f"❌ Error with AI ({model}): {str(e)}"
    
    def _openai_generate(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """OpenAI GPT"""
        if not self.openai_client:
            return "❌ OpenAI API key not found. Check .env file"
        
        try:
            response = self.openai_client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a QA testing expert. Answer in Russian when needed."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def _claude_generate(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """Anthropic Claude"""
        if not self.claude_client:
            return "❌ Claude API key not found. Check .env file"
        
        try:
            response = self.claude_client.messages.create(
                model=Config.ANTHROPIC_MODEL,
                max_tokens=max_tokens,
                system="You are a QA testing expert. Answer in Russian when needed.",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise
    
    def _deepseek_generate(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """DeepSeek"""
        if not self.deepseek_client:
            return "❌ DeepSeek API key not found. Check .env file"
        
        try:
            response = self.deepseek_client.chat.completions.create(
                model=Config.DEEPSEEK_MODEL,
                messages=[
                    {"role": "system", "content": "You are a QA testing expert. Answer in Russian when needed."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"DeepSeek API error: {e}")
            raise
    
    def improve_bug_report(self, bug_data: dict, model: str = None) -> str:
        """Improve bug report with AI"""
        prompt = f"""Please improve the following bug report. Make it more professional and complete:

Title: {bug_data.get('title', 'N/A')}
Description: {bug_data.get('description', 'N/A')}
Repro Steps: {', '.join(bug_data.get('steps', []))}
Actual Result: {bug_data.get('actual_result', 'N/A')}
Expected Result: {bug_data.get('expected_result', 'N/A')}

Return improved bug report in structured format."""
        
        return self.generate_text(prompt, model)
    
    def generate_test_case(self, feature_description: str, model: str = None) -> str:
        """Generate test case from feature description"""
        prompt = f"""Create a detailed test case for the following feature:

{feature_description}

Test case must include:
1. Name (TC_XXX)
2. Preconditions
3. Steps (minimum 5 steps)
4. Expected Result
5. Priority
6. Author"""
        
        return self.generate_text(prompt, model)

# Global AI service instance
ai_service = AIService()

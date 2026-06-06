"""
Core AI Agent for research paper analysis - Updated for Gemini API
"""

import os
import time
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Import modules
from modules.summarizer import SummarizerModule
from modules.extractor import ExtractorModule
from modules.comparer import ComparerModule
from modules.gap_finder import GapFinderModule
from utils.text_processor import TextProcessor

# Load environment variables
load_dotenv()


class LLMClient:
    """Wrapper for LLM API calls"""
    
    def __init__(self, use_gemini: bool = True):
        self.use_gemini = use_gemini
        
        if use_gemini:
            import google.generativeai as genai
            
            # Configure the API
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            
            genai.configure(api_key=api_key)
            
            # Get available models
            try:
                # List all available models
                available_models = []
                for model in genai.list_models():
                    if 'generateContent' in model.supported_generation_methods:
                        available_models.append(model.name)
                
                print(f"📋 Available models: {available_models}")
                
                # Try to find a working model
                working_model = None
                for model_name in available_models:
                    # Extract just the model ID from full name
                    model_id = model_name.split('/')[-1]
                    if any(name in model_id for name in ['gemini', '1.5', '1.0']):
                        try:
                            test_model = genai.GenerativeModel(model_id)
                            # Quick test
                            test_model.generate_content("Test")
                            working_model = model_id
                            print(f"✅ Using model: {working_model}")
                            break
                        except:
                            continue
                
                if working_model:
                    self.model = genai.GenerativeModel(working_model)
                else:
                    # Fallback to gemini model
                    self.model = genai.GenerativeModel('gemini-1.0-pro-latest')
                    print("⚠️ Using default model: gemini-1.0-pro-latest")
                    
            except Exception as e:
                print(f"⚠️ Error listing models: {e}")
                # Try common model names as fallback
                fallback_models = [
                    'gemini-1.0-pro-latest',
                    'gemini-1.0-pro',
                    'gemini-pro'
                ]
                for model_name in fallback_models:
                    try:
                        self.model = genai.GenerativeModel(model_name)
                        print(f"✅ Using fallback model: {model_name}")
                        break
                    except:
                        continue
        else:
            from openai import OpenAI
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-3.5-turbo"
    
    def generate(self, prompt: str, max_tokens: int = 2000, retry_count: int = 2) -> str:
        """Generate response from LLM with retry logic"""
        
        for attempt in range(retry_count):
            try:
                if self.use_gemini:
                    # For Gemini, use generate_content with proper config
                    response = self.model.generate_content(
                        prompt,
                        generation_config={
                            "max_output_tokens": max_tokens,
                            "temperature": 0.7,
                            "top_p": 0.95,
                        },
                        safety_settings={
                            "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
                        }
                    )
                    return response.text
                else:
                    # For OpenAI
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=max_tokens,
                        temperature=0.7
                    )
                    return response.choices[0].message.content
                    
            except Exception as e:
                error_msg = str(e)
                print(f"Attempt {attempt + 1} failed: {error_msg[:100]}")
                
                if "429" in error_msg:  # Rate limit
                    wait_time = 2 ** attempt
                    print(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                elif attempt < retry_count - 1:
                    print("Retrying...")
                    time.sleep(1)
                    continue
                else:
                    return f"Error: {error_msg}"
        
        return f"Failed after {retry_count} attempts."


class ResearchAgent:
    """Main AI Agent for research paper analysis"""
    
    def __init__(self, use_gemini: bool = True):
        """Initialize the agent with all modules"""
        try:
            print("🤖 Initializing Research Agent...")
            self.llm_client = LLMClient(use_gemini=use_gemini)
            self.summarizer = SummarizerModule(self.llm_client)
            self.extractor = ExtractorModule(self.llm_client)
            self.comparer = ComparerModule(self.llm_client)
            self.gap_finder = GapFinderModule(self.llm_client)
            self.text_processor = TextProcessor()
            
            print("✅ Research Agent initialized successfully!")
            print(f"📡 Using {'Gemini' if use_gemini else 'OpenAI'} API")
        except Exception as e:
            print(f"❌ Failed to initialize agent: {str(e)}")
            raise
    
    def process(self, 
                text: str, 
                task: str = "summarize",
                paper_texts: List[str] = None,
                question: str = None) -> str:
        """Process research paper based on task"""
        result = ""
        
        try:
            if task == "summarize":
                result = self.summarizer.generate_summary(text)
                
            elif task == "extract":
                extracted = self.extractor.extract_info(text)
                result = self.extractor.to_markdown(extracted)
                
            elif task == "compare":
                if paper_texts and len(paper_texts) >= 2:
                    result = self.comparer.compare_papers(paper_texts)
                else:
                    result = "Please provide at least 2 papers for comparison."
                    
            elif task == "gap":
                if paper_texts and len(paper_texts) > 1:
                    result = self.gap_finder.identify_gaps(paper_texts, is_multi_doc=True)
                else:
                    result = self.gap_finder.identify_gaps(text, is_multi_doc=False)
                    
            elif task == "qa":
                if question:
                    result = self.answer_question(text, question)
                else:
                    result = "Please provide a question to answer."
            
            else:
                result = "Unknown task. Available tasks: summarize, extract, compare, gap, qa"
                
            return result
            
        except Exception as e:
            return f"Error processing request: {str(e)}"
    
    def answer_question(self, context: str, question: str) -> str:
        """Answer specific question about the research paper"""
        from prompts.templates import get_prompt
        
        # Truncate context to avoid token limits
        max_context_length = 4000
        if len(context) > max_context_length:
            context = context[:max_context_length] + "..."
            
        prompt = get_prompt("qa", context=context, question=question)
        
        return self.llm_client.generate(prompt)
    
    def process_paper_batch(self, papers: List[Dict[str, str]]) -> Dict[str, str]:
        """Process multiple papers"""
        results = {}
        
        for i, paper in enumerate(papers):
            title = paper.get('title', f'Paper {i+1}')
            print(f"Processing: {title}")
            
            results[title] = {
                'summary': self.summarizer.generate_summary(paper['text']),
                'extracted': self.extractor.extract_info(paper['text'])
            }
        
        return results
    
    def get_agent_info(self) -> Dict:
        """Get agent information"""
        return {
            'name': 'Research Paper AI Agent',
            'version': '1.0.0',
            'capabilities': ['summarize', 'extract', 'compare', 'gap_analysis', 'qa'],
            'api': 'Gemini' if self.llm_client.use_gemini else 'OpenAI'
        }


# For testing
if __name__ == "__main__":
    print("Testing Research Agent...")
    print("="*50)
    
    # Test with a simple paper
    test_paper = """
    This paper presents a novel approach to image classification using deep learning.
    We propose a convolutional neural network architecture with attention mechanisms.
    The model achieves 95% accuracy on the CIFAR-10 dataset.
    Key contributions include reduced computational complexity and better feature extraction.
    Limitations include performance on very small datasets.
    Future work will focus on few-shot learning scenarios.
    """
    
    try:
        agent = ResearchAgent(use_gemini=True)
        
        print("\n📝 Testing Summarization...")
        summary = agent.process(test_paper, task="summarize")
        print(summary)
        
        print("\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
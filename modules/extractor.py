"""
Information extraction module
"""

class ExtractorModule:
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def extract_info(self, text):
        """
        Extract structured information from research paper
        
        Args:
            text: Research paper text
            
        Returns:
            Dictionary with extracted information
        """
        from prompts.templates import get_prompt
        
        cleaned_text = self._clean_text(text)
        truncated_text = cleaned_text[:10000]  # Limit for extraction
        
        prompt = get_prompt("extract", text=truncated_text)
        response = self.llm_client.generate(prompt)
        
        return self._parse_extraction(response)
    
    def _clean_text(self, text):
        """Basic text cleaning"""
        import re
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _parse_extraction(self, response):
        """
        Parse the extraction response into structured format
        """
        lines = response.split('\n')
        extracted = {
            "problem_statement": "",
            "proposed_solution": "",
            "methodology": "",
            "dataset": "",
            "evaluation_metrics": "",
            "results": "",
            "limitations": "",
            "future_work": ""
        }
        
        current_key = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for section headers
            if line.startswith('**') and ':' in line:
                header = line.replace('**', '').replace(':', '').lower().strip()
                if 'problem' in header:
                    current_key = 'problem_statement'
                elif 'solution' in header:
                    current_key = 'proposed_solution'
                elif 'methodology' in header:
                    current_key = 'methodology'
                elif 'dataset' in header or 'resource' in header:
                    current_key = 'dataset'
                elif 'evaluation' in header or 'metric' in header:
                    current_key = 'evaluation_metrics'
                elif 'result' in header:
                    current_key = 'results'
                elif 'limitation' in header:
                    current_key = 'limitations'
                elif 'future' in header:
                    current_key = 'future_work'
                else:
                    current_key = None
            elif current_key and line:
                extracted[current_key] += line + "\n"
        
        # Clean up values
        for key in extracted:
            extracted[key] = extracted[key].strip()
            
        return extracted
    
    def to_markdown(self, extracted_info):
        """Convert extracted info to markdown format"""
        markdown = """
## 📋 Extracted Information

### 🎯 Problem Statement
{problem}

### 💡 Proposed Solution
{solution}

### 🔧 Methodology
{methodology}

### 📊 Dataset/Resources
{dataset}

### 📈 Evaluation Metrics
{metrics}

### 📉 Results
{results}

### ⚠️ Limitations
{limitations}

### 🔮 Future Work
{future}
""".format(
            problem=extracted_info.get('problem_statement', 'Not specified'),
            solution=extracted_info.get('proposed_solution', 'Not specified'),
            methodology=extracted_info.get('methodology', 'Not specified'),
            dataset=extracted_info.get('dataset', 'Not specified'),
            metrics=extracted_info.get('evaluation_metrics', 'Not specified'),
            results=extracted_info.get('results', 'Not specified'),
            limitations=extracted_info.get('limitations', 'Not specified'),
            future=extracted_info.get('future_work', 'Not specified')
        )
        return markdown
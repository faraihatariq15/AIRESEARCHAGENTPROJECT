"""
Prompt templates for different tasks
"""

SUMMARIZE_PROMPT = """
You are an expert research assistant. Summarize the following research paper in a clear, concise manner.

Research Paper Content:
{text}

Provide a structured summary with:
1. **Main Objective**: What problem does this paper address?
2. **Key Methodology**: How did they approach the problem?
3. **Major Findings**: What were the key results?
4. **Key Contributions**: What are the main contributions?
5. **Limitations**: What limitations are mentioned?

Keep the summary concise but informative. Focus on the most important points.
"""

EXTRACT_INFO_PROMPT = """
Extract the following key information from the research paper text:

Research Paper Text:
{text}

Extract and present:
- **Problem Statement**: What problem is being solved?
- **Proposed Solution**: What solution is proposed?
- **Methodology Details**: Specific techniques, algorithms, or approaches used
- **Dataset/Resources**: What data or resources were used?
- **Evaluation Metrics**: How was the solution evaluated?
- **Results**: Quantitative results (numbers, percentages, etc.)
- **Limitations**: Explicitly mentioned limitations
- **Future Work**: Suggested future research directions

If information for any category is not found, state "Not specified in paper".
"""

COMPARE_PROMPT = """
Compare the following research papers and provide a detailed analysis.

Paper 1:
{paper1}

Paper 2:
{paper2}

Provide comparison in this format:

**Common Aspects:**
- List similarities in approach, methodology, or findings

**Differences:**
| Aspect | Paper 1 | Paper 2 |
|--------|---------|---------|
| Main Problem | ... | ... |
| Methodology | ... | ... |
| Key Findings | ... | ... |
| Strengths | ... | ... |
| Weaknesses | ... | ... |

**Relative Advantages:**
- What does Paper 1 do better?
- What does Paper 2 do better?

**Synthesis:**
- How do these papers complement each other?
- What can be learned by combining their approaches?
"""

GAP_IDENTIFICATION_PROMPT = """
Analyze the following research papers and identify research gaps and future directions.

Research Paper Context:
{text}

Identify:

**1. Explicitly Mentioned Gaps:**
- Gaps directly stated in the paper

**2. Implicit Gaps:**
- Limitations that suggest unexplored areas
- Assumptions that could be challenged

**3. Emerging Research Questions:**
- Questions that remain unanswered
- Questions arising from the findings

**4. Future Research Directions:**
- Specific suggestions for future work
- Potential extensions of this research

**5. Methodology Gaps:**
- Limitations in experimental design
- Opportunities for better evaluation methods

**6. Practical Implications:**
- Real-world applications not yet explored
- Implementation challenges to address
"""

MULTI_DOCUMENT_GAP_PROMPT = """
Analyze these research papers collectively and identify research gaps and future directions.

Papers:
{texts}

Provide a comprehensive gap analysis:

**Consensus Areas:**
- What do most papers agree on?
- What is well-established?

**Contradictions:**
- Where do findings disagree?
- What conflicting evidence exists?

**Understudied Areas:**
- What important aspects are missing?
- What populations/contexts are not studied?

**Methodological Gaps:**
- Common methodological weaknesses across papers
- Opportunities for better experimental design

**Priority Research Directions:**
- Top 3 most promising research directions
- Specific questions to investigate

**Novel Proposals:**
- Suggest 2-3 novel research ideas based on identified gaps
"""

QA_PROMPT = """
Answer the following question based on the research paper content.

Research Paper:
{context}

Question: {question}

Instructions:
- Answer based ONLY on the information provided in the research paper
- If the answer cannot be found in the paper, say "The paper does not provide information about this"
- Provide specific quotes or references when possible
- Be concise but thorough

Answer:
"""

def get_prompt(task_type, **kwargs):
    """
    Returns the appropriate prompt template for the given task
    """
    prompts = {
        "summarize": SUMMARIZE_PROMPT,
        "extract": EXTRACT_INFO_PROMPT,
        "compare": COMPARE_PROMPT,
        "gap_single": GAP_IDENTIFICATION_PROMPT,
        "gap_multi": MULTI_DOCUMENT_GAP_PROMPT,
        "qa": QA_PROMPT
    }
    
    template = prompts.get(task_type, SUMMARIZE_PROMPT)
    return template.format(**kwargs)
from typing import List, Dict

class PaperTemplate:
    @staticmethod
    def get_section_prompts(topic: str, paper_type: str = "research") -> Dict[str, str]:
        """Get prompts for each section of the paper"""
        
        base_context = f"You are writing an academic {paper_type} paper on the topic: '{topic}'. "
        
        prompts = {
            "abstract": f"{base_context}Write a comprehensive abstract (200-250 words) that summarizes the entire paper. Include the research problem, methodology, key findings, and conclusions.",
            
            "introduction": f"{base_context}Write a detailed introduction (400-500 words) that: 1) Provides background context, 2) States the research problem clearly, 3) Explains the significance of the study, 4) Outlines the paper structure.",
            
            "literature_review": f"{base_context}Write a thorough literature review (600-800 words) that: 1) Reviews existing research in this field, 2) Identifies gaps in current knowledge, 3) Positions this work within the broader academic context, 4) Includes relevant citations and references.",
            
            "methodology": f"{base_context}Write a detailed methodology section (400-600 words) that: 1) Describes the research approach and design, 2) Explains data collection methods, 3) Outlines analysis techniques, 4) Discusses limitations and assumptions.",
            
            "results_discussion": f"{base_context}Write a comprehensive results and discussion section (800-1000 words) that: 1) Presents key findings clearly, 2) Analyzes and interprets results, 3) Compares findings with existing literature, 4) Discusses implications and significance.",
            
            "conclusion": f"{base_context}Write a strong conclusion (300-400 words) that: 1) Summarizes main findings, 2) Discusses broader implications, 3) Suggests areas for future research, 4) Provides final thoughts on the topic.",
            
            "references": f"{base_context}Generate a list of 15-20 realistic academic references in APA format that would be appropriate for this paper. Include a mix of journal articles, books, and recent publications."
        }
        
        return prompts
    
    @staticmethod
    def format_paper(sections: Dict[str, str], topic: str, author: str = "AI Generated") -> str:
        """Format the complete paper"""
        
        paper = f"""
# {topic}

**Author:** {author}  
**Date:** {__import__('datetime').datetime.now().strftime('%B %d, %Y')}

---

## Abstract

{sections.get('abstract', '')}

---

## 1. Introduction

{sections.get('introduction', '')}

---

## 2. Literature Review

{sections.get('literature_review', '')}

---

## 3. Methodology

{sections.get('methodology', '')}

---

## 4. Results and Discussion

{sections.get('results_discussion', '')}

---

## 5. Conclusion

{sections.get('conclusion', '')}

---

## References

{sections.get('references', '')}

---

*This paper was generated using AI assistance and should be used as a starting point for academic research.*
"""
        
        return paper.strip()
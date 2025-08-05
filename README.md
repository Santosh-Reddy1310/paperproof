# 📝 Research Paper Generator with Gemini AI  

*A Streamlit web app that generates academic research papers using Google's Gemini Flash API (free tier).*  


---

## 🚀 Features  
- **AI-Powered Paper Generation**: Creates structured papers with Gemini Flash (free tier).  
- **Customizable Inputs**:  
  - Research topic  
  - Target length (1,000–5,000 words)  
  - Paper type (Research, Review, Case Study)  
- **Parallel Processing**: Generates sections 3x faster using concurrent requests.  
- **Download Options**: Markdown, Text, and PDF (planned).  
- **Secure**: Users provide their own API keys (no hardcoded secrets).  

---

## ⚙️ Setup  

### 1. Prerequisites  
- Python 3.9+  
- [Gemini API Key](https://aistudio.google.com/app/apikey) (free tier)  

### 2. Installation  
```bash
git clone https://github.com/yourusername/research-paper-generator.git
cd research-paper-generator
pip install -r requirements.txt
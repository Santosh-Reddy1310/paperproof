# 📄 PaperProof – AI-Powered Research Paper Generator

**PaperProof** is a powerful AI-driven academic writing tool that generates fully structured, citation-rich research papers based on user-provided topics. Built with **Streamlit** and powered by the **Gemini 1.5 Flash API (Free Tier)**, it produces professional-quality papers including Abstract, Introduction, Literature Review, Methodology, Results, Conclusion, and APA-style References.

> ⚡ Optimized for speed, free-tier limits, and academic structure — built for researchers, students, and knowledge creators.

---

## 🚀 Features

- 🎓 **Generate Full-Length Research Papers**  
  Input any academic topic and receive a multi-section paper with clear structure and logical flow.

- 🧠 **Powered by Gemini 1.5 Flash (Free Tier)**  
  Fast, efficient, and capable of handling structured reasoning — no paid API required.

- ⚙️ **Parallel Section Generation**  
  Generates paper sections concurrently using `ThreadPoolExecutor`, reducing generation time by 3x.

- 📚 **APA-Style Citations**  
  Produces realistic and scholarly references appropriate for academic papers.

- 🔄 **Retry + Rate Limit Handling**  
  Built-in exponential backoff and rate-limiting mechanisms prevent API errors and exceedance.

- 📥 **Download as Markdown or Plain Text**  
  Export the final paper instantly for further use or editing.

---

## 🏗️ Project Structure

```
paperproof/
├── app.py                  # Main Streamlit frontend
├── config.py               # App configuration and model settings
├── .env                    # Gemini API key and app secrets
├── requirements.txt        # Python dependencies
├── utils/
│   ├── __init__.py
│   ├── api_client.py       # Gemini API wrapper with rate limiting
│   ├── paper_formatter.py  # Paper formatting and chunk merging
│   └── validators.py       # Topic/API key validation and filename sanitization
└── templates/
    └── paper_template.py   # Prompt templates and paper generation logic
```

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Santosh-Reddy1310/paperproof.git
cd paperproof
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your `.env` File

Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your_google_gemini_api_key
DEFAULT_MODEL=gemini-1.5-flash
APP_TITLE=PaperProof
```

> 🔑 Get your free Gemini API key from: https://ai.google.dev/

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Open your browser and navigate to `http://localhost:8501`.

---

## ✍️ How to Use

1. Enter your **Gemini API key** in the sidebar.
2. Choose **model**, paper type, word length, and author name.
3. Enter a detailed **research topic**.
4. Click **"Generate Research Paper"**.
5. Wait for sections to load with real-time progress tracking.
6. Download your final paper as `.txt` or `.md`.

---

## 🧠 Example Topics to Try

- *The Role of Artificial General Intelligence in Solving Global Climate Change by 2050*
- *Neuralink and the Future of Brain-Computer Interfaces*
- *The Ethics of AI-Generated Art in the Creative Economy*
- *CRISPR and the Future of Human Genome Editing*
- *The Rise of Decentralized Science (DeSci) in Modern Research*

---

## 🛡️ Free Tier Optimizations

- Limits API calls to **1 request per second**
- Uses **parallel threads (max 3)** to generate sections quickly
- Tracks and reduces **token usage**
- Gracefully handles **rate limits, retries, and timeouts**

---

## 💡 Future Roadmap

- [ ] PDF Export with academic formatting
- [ ] Citation verification via external metadata APIs
- [ ] Research quality score and feedback metrics
- [ ] Field-specific paper templates (STEM, Social Sciences, etc.)
- [ ] Collaboration support (multi-author generation)

---

## 🧑‍💻 Author

**Reddy Santosh Kumar**  
AI/ML Enthusiast | Full Stack Dev | [LinkedIn](https://www.linkedin.com/in/santosh-reddy-kumar)  
Part of the #10Weeks10Projects initiative – Week 8 Project

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- [Gemini API](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- Inspiration from the needs of students, researchers, and the open-source AI community.

---

> 🧠 *“PaperProof is your co-pilot for turning ideas into academically structured insights — fast, free, and future-ready.”*

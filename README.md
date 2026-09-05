<p align="center">
  <img src="https://darshan.ac.in/Content/images/darshan-logo.png" alt="Darshan University Logo" width="120"/>
</p>

<h1 align="center">🤖 Darshan University AI Assistant — RAG Chatbot</h1>

<p align="center">
  <em>An intelligent, context-aware chatbot powered by Retrieval-Augmented Generation (RAG) that answers questions about Darshan University using real, scraped data from the official website.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Flask-3.1-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
  <img src="https://img.shields.io/badge/Ollama-Phi--3-blue?style=for-the-badge" alt="Ollama"/>
  <img src="https://img.shields.io/badge/ChromaDB-Vector_Store-FF6F00?style=for-the-badge" alt="ChromaDB"/>
  <img src="https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge" alt="LangChain"/>
  <img src="https://img.shields.io/badge/Scrapy-Web_Scraping-60A839?style=for-the-badge&logo=scrapy&logoColor=white" alt="Scrapy"/>
</p>

---

## 📖 About The Project

The **Darshan University AI Assistant** is a fully offline, privacy-first RAG (Retrieval-Augmented Generation) chatbot built to answer student queries about Darshan University — including **courses, departments, placements, faculty, and general information** — using real data scraped directly from the [official Darshan University website](https://darshan.ac.in).

Unlike traditional chatbots that rely on cloud APIs, this system runs **entirely locally** using **Ollama + Phi-3**, ensuring zero data leaves the machine. The chatbot retrieves the most relevant information chunks from a ChromaDB vector database and generates accurate, grounded answers — never hallucinating or inventing facts.

### ✨ Key Highlights

- 🔒 **Fully Offline & Private** — No external API calls; everything runs locally via Ollama
- 🎯 **Grounded Answers Only** — Strict prompt engineering ensures the bot only answers from retrieved context
- 🕷️ **Automated Data Pipeline** — Scrapy-based crawler + cleaning + chunking + embedding pipeline
- 📊 **Placement Data Support** — Custom semantic extractor for detailed placement statistics (2016–2026)
- 💬 **Conversational Memory** — Session-based history for follow-up questions (e.g., "And for MCA?")
- 🎨 **Beautiful Chat UI** — Dark-themed, floating chat widget styled to match Darshan University branding

---

## 🏆 Achievements

<table>
  <tr>
    <td>🏅</td>
    <td>
      <strong>Certificate of Appreciation — Darshan University</strong><br/>
      <em>Felicitated by Darshan University for developing the <strong>Darshan University AI Assistant (RAG Chatbot)</strong>.</em><br/><br/>
      Recognized and appreciated by the university administration for building an intelligent AI-powered assistant that serves students and stakeholders with accurate, real-time information about Darshan University.
    </td>
  </tr>
</table>

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DATA PIPELINE                                │
│                                                                     │
│  darshan.ac.in ──► Scrapy Crawler ──► Raw JSONL ──► Dedupe & Clean  │
│                                                          │          │
│                                              Post Clean ◄┘          │
│                                                  │                  │
│                                          Filter for Index           │
│                                                  │                  │
│                                           Make Chunks               │
│                                                  │                  │
│                                    MiniLM Embeddings + ChromaDB     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                        QUERY PIPELINE                               │
│                                                                     │
│  User Question ──► Flask API ──► Similarity Search (ChromaDB)       │
│                                        │                            │
│                              Top-K Relevant Chunks                  │
│                                        │                            │
│                              Build Grounded Prompt                  │
│                                        │                            │
│                              Ollama (Phi-3) LLM                     │
│                                        │                            │
│                              Answer ──► Chat UI                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Web Scraping** | Scrapy, readability-lxml, trafilatura | Crawl & extract content from darshan.ac.in |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` | Convert text chunks into vector embeddings |
| **Vector Database** | ChromaDB | Store and retrieve document embeddings locally |
| **LLM** | Ollama + Phi-3 | Generate grounded answers from retrieved context |
| **Framework** | LangChain | Orchestrate embeddings ↔ vector store integration |
| **Backend** | Flask | REST API (`/api/chat`) for chat interactions |
| **Frontend** | HTML, CSS, JavaScript (Vanilla) | Dark-themed floating chat widget UI |

---

## 📁 Project Structure

```
RAG-Chatbot-DarshanUniversity/
│
├── app.py                      # Flask web server & chat API endpoints
├── main.py                     # Core RAG logic (embeddings, retrieval, prompt, LLM)
├── scrape_placements.py        # Dedicated placement data scraper (2016–2026)
├── run_pipeline.bat            # One-click data pipeline runner (Windows)
├── requirements.txt            # Python dependencies
├── scrapy.cfg                  # Scrapy project configuration
├── planning.md                 # Tech stack & architecture documentation
│
├── du_scraper/                 # Scrapy spider package
│   ├── spiders/
│   │   └── darshan_university.py   # Main spider — crawls darshan.ac.in
│   ├── utils/
│   │   └── extract.py          # HTML extraction & text cleaning utilities
│   ├── extensions.py           # Custom Scrapy extensions
│   ├── items.py                # Scrapy item definitions
│   ├── middlewares.py          # Custom middlewares
│   ├── pipelines.py            # Data processing pipelines
│   └── settings.py             # Scrapy settings (throttle, cache, etc.)
│
├── scripts/                    # Data processing pipeline scripts
│   ├── dedupe_clean.py         # Step 1: Remove duplicate pages
│   ├── post_clean.py           # Step 2: Post-processing & text cleanup
│   ├── filter_for_index.py     # Step 3: Filter pages suitable for indexing
│   ├── make_chunks.py          # Step 4: Split documents into chunks
│   └── build_chroma.py         # Step 5: Build ChromaDB vector store
│
├── templates/
│   └── index.html              # Chat UI (dark-themed floating widget)
│
└── data/                       # Generated data (not committed to git)
    ├── raw/                    # Raw scraped JSONL files
    ├── clean/                  # Cleaned & deduplicated data
    ├── chunks/                 # Chunked documents (chunks.jsonl)
    └── chroma_db/              # ChromaDB vector database files
```

---

## 📋 Prerequisites

Before running this project, make sure you have the following installed:

1. **Python 3.10+** — [Download Python](https://www.python.org/downloads/)
2. **Ollama** — [Download Ollama](https://ollama.com/download)
3. **Git** — [Download Git](https://git-scm.com/downloads) *(for cloning the repo)*

### Pull the Phi-3 Model via Ollama

After installing Ollama, open a terminal and run:

```bash
ollama pull phi3
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/SmitRanipa/rag-ai-chatbot-razorpay-ai-buildathon.git
cd rag-ai-chatbot-razorpay-ai-buildathon
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

**Activate it:**

- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install langchain-community chromadb sentence-transformers beautifulsoup4 lxml requests
```

### 4. Run the Data Pipeline (First Time Only)

This step scrapes the Darshan University website, cleans the data, creates chunks, and builds the ChromaDB vector database.

**Option A — Run the full pipeline via batch script (Windows):**

```bash
run_pipeline.bat
```

**Option B — Run each step manually:**

```bash
# Step 1: Crawl the website
scrapy crawl darshan -O data/raw/pages_full.jsonl

# Step 2: Scrape placement data
python scrape_placements.py

# Step 3: Deduplicate & clean
python scripts/dedupe_clean.py data/raw/pages_full.jsonl data/clean/pages_clean_full_dedup.jsonl

# Step 4: Post-clean
python scripts/post_clean.py data/clean/pages_clean_full_dedup.jsonl data/clean/pages_for_index.jsonl

# Step 5: Filter for indexing
python scripts/filter_for_index.py data/clean/pages_for_index.jsonl data/clean/pages_for_index_filtered.jsonl

# Step 6: Create chunks
python scripts/make_chunks.py data/clean/pages_for_index_filtered.jsonl data/chunks/chunks.jsonl

# Step 7: Build ChromaDB vector store
python scripts/build_chroma.py data/chunks/chunks.jsonl data/chroma_db
```

### 5. Start Ollama (Keep Running)

Make sure Ollama is running in the background:

```bash
ollama serve
```

### 6. Launch the Chatbot

```bash
python app.py
```

The chatbot will automatically open in your browser at **http://127.0.0.1:5000** 🎉

---

## 💬 Usage

1. Click the **red chat icon** (bottom-right corner) to open the chat window
2. Type any question about Darshan University, for example:
   - *"What courses does Darshan University offer?"*
   - *"What is the placement record for B.Tech Computer in 2025?"*
   - *"Tell me about the MCA department"*
   - *"What was the highest package in 2024?"*
3. The bot retrieves relevant information from the vector database and generates a grounded answer
4. Follow-up questions are supported — the chatbot remembers conversation context!

---

## 📤 How to Upload This Project to GitHub (From File Explorer)

If you want to push this project to GitHub directly from your local folder, follow these steps:

### Step 1: Create a Repository on GitHub

1. Go to [github.com](https://github.com) and log in
2. Click the **"+"** button (top-right) → **"New repository"**
3. Fill in the repository name (e.g., `rag-ai-chatbot-razorpay-ai-buildathon`)
4. Set it to **Public** or **Private**
5. **Do NOT** initialize with README, .gitignore, or license (we already have them locally)
6. Click **"Create repository"**

### Step 2: Open Terminal in Your Project Folder

**From File Explorer:**
1. Navigate to your project folder in File Explorer
2. Click on the **address bar** at the top
3. Type `cmd` or `powershell` and press **Enter** — this opens a terminal directly in that folder!

> 💡 **Alternative:** Right-click inside the folder → **"Open in Terminal"** (Windows 11) or **"Open PowerShell window here"** (Windows 10)

### Step 3: Initialize Git & Push to GitHub

Run these commands one by one in the terminal:

```bash
# Initialize a new Git repository
git init

# Add all files to staging
git add .

# Create the first commit
git commit -m "Initial commit: Darshan University RAG Chatbot"

# Set the main branch
git branch -M main

# Add GitHub as the remote origin
git remote add origin https://github.com/SmitRanipa/rag-ai-chatbot-razorpay-ai-buildathon.git

# Push to GitHub
git push -u origin main
```

### Step 4: Verify on GitHub

1. Go to your repository URL: [https://github.com/SmitRanipa/rag-ai-chatbot-razorpay-ai-buildathon](https://github.com/SmitRanipa/rag-ai-chatbot-razorpay-ai-buildathon)
2. You should see all your files uploaded with the README displayed! ✅

> ⚠️ **Note:** If prompted for authentication, use a [Personal Access Token (PAT)](https://github.com/settings/tokens) instead of your password. GitHub no longer accepts passwords for Git operations.

### Updating the Repository Later

Whenever you make changes, run:

```bash
git add .
git commit -m "Your commit message here"
git push
```

---

## ⚙️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the chat UI (index.html) |
| `POST` | `/api/chat` | Send a message and receive an AI-generated response |
| `POST` | `/api/reset` | Reset the conversation history |

### Example API Request

```bash
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the highest package in B.Tech Computer 2025?"}'
```

---

## 🔧 Configuration

Key configuration constants in [`main.py`](main.py):

| Variable | Default | Description |
|----------|---------|-------------|
| `COLLECTION_NAME` | `"darshan"` | ChromaDB collection name |
| `PERSIST_DIR` | `"data/chroma_db"` | Path to ChromaDB storage |
| `OLLAMA_URL` | `http://localhost:11434/api/generate` | Ollama API endpoint |
| `OLLAMA_MODEL` | `"phi3"` | LLM model to use via Ollama |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open an issue or submit a pull request.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Smit Ranipa**

- GitHub: [@SmitRanipa](https://github.com/SmitRanipa)

---

<p align="center">
  Made with ❤️ for Darshan University
</p>

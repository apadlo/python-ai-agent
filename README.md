# 🤖 Python AI Agent

A smart note-taking assistant powered by LangChain and OpenAI that can read and write text files based on natural language instructions.

## ✨ Features

- 🧠 **AI-Powered**: Utilizes OpenAI's GPT models through LangChain
- 📝 **Natural Language Interface**: Interact with your notes using conversational commands
- 🌐 **Web Interface**: Simple and clean web UI for easy interaction
- 💾 **File Management**: Read and write text files with natural language commands
- 🚀 **Vercel Ready**: Easily deployable to Vercel
- ⚡ **FastAPI Backend**: High-performance async API

## 🛠️ Tech Stack

- **FastAPI** - Modern, fast web framework
- **LangChain** - Framework for developing applications powered by language models
- **LangGraph** - Library for building stateful, multi-actor applications with LLMs
- **OpenAI** - GPT models for natural language processing
- **Jinja2** - Template engine for the web interface
- **Python 3.10+** - Modern Python features

## 📋 Prerequisites

- Python 3.10 or higher
- OpenAI API key

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/apadlo/python-ai-agent.git
   cd python-ai-agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   NOTES_DIR=/path/to/notes  # Optional: defaults to system temp directory
   ```

## 💻 Usage

### Running Locally

Start the development server:

```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

### Using the Web Interface

1. Open your browser and navigate to `http://localhost:8000`
2. Enter natural language commands like:
   - "Create a note called shopping.txt with milk, eggs, and bread"
   - "Read the contents of shopping.txt"
   - "Write 'Remember to call mom' to reminder.txt"
3. Download created notes using the download button

### API Usage

You can also interact with the API directly:

```bash
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a note called todo.txt with: Buy groceries, Call dentist"}'
```

**Response:**
```json
{
  "response": "Successfully wrote 30 characters to 'todo.txt'.",
  "filename": "todo.txt",
  "download_url": "/download/todo.txt"
}
```

### API Endpoints

- `GET /` - Web interface
- `POST /agent` - Invoke the AI agent
  - Request body: `{"prompt": "your instruction here"}`
  - Response: `{"response": "...", "filename": "...", "download_url": "..."}`
- `GET /download/{filename}` - Download a note file

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | (required) |
| `NOTES_DIR` | Directory to store notes | System temp directory |

### Customizing the Agent

The agent's behavior can be customized in `agent.py`:

- **Model**: Change the OpenAI model by modifying the `ChatOpenAI` initialization
- **System Message**: Customize the agent's personality in the `SYSTEM_MESSAGE` variable
- **Tools**: Add more tools by defining them with the `@tool` decorator and adding to `TOOLS`

## 🌐 Deployment

### Deploying to Vercel

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   vercel
   ```

3. **Set environment variables**
   
   In your Vercel dashboard, add:
   - `OPENAI_API_KEY`
   - `NOTES_DIR` (optional)

The project is configured with `api/index.py` as the entry point for Vercel's serverless functions.

## 📁 Project Structure

```
python-ai-agent/
├── agent.py           # AI agent logic and tools
├── main.py            # FastAPI application
├── api/
│   └── index.py       # Vercel serverless entry point
├── templates/
│   └── index.html     # Web interface
├── public/            # Static files
├── requirements.txt   # Python dependencies
├── pyproject.toml     # Project metadata
└── .vercelignore      # Vercel deployment config
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain)
- Powered by [OpenAI](https://openai.com/)
- Framework: [FastAPI](https://fastapi.tiangolo.com/)

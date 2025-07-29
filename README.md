# Basic Chatbot with LangGraph

This project is a simple, terminal-based chatbot that leverages the power of [LangGraph](https://langchain-ai.github.io/langgraph/) and Google's Generative AI models to provide intelligent and context-aware responses. The chatbot is designed to be easily extensible with various tools to enhance its capabilities.

## 🌟 Features

- **Conversational AI:** Engage in natural and dynamic conversations.
- **Tool Integration:** Seamlessly integrates with external tools like [Tavily Search](https://tavily.com/) to access real-time information.
- **Extensible Architecture:** Built with LangGraph, allowing for the easy addition of new tools and functionalities.
- **Memory:** Remembers previous turns in the conversation to provide context-aware responses.
- **Docker Support:** Includes a Dockerfile for easy containerization and deployment.

## 🚀 Getting Started

Follow these instructions to get the chatbot up and running on your local machine.

### 📋 Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management (optional but recommended)
- Access to Google's Generative AI API and a Tavily API key.

### ⚙️ Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/basic-chatbot.git
    cd basic-chatbot
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 🔑 Configuration

1.  **Create a `.env` file** by copying the example file:
    ```bash
    cp .env.example .env
    ```

2.  **Add your API keys** to the `.env` file:
    ```
    GOOGLE_API_KEY="your-google-api-key"
    TAVILY_API_KEY="your-tavily-api-key"
    ```

### ▶️ Running the Application

Once you have completed the installation and configuration steps, you can start the chatbot with the following command:

```bash
python src/main.py
```

## 💬 Usage

After running the application, you can start interacting with the chatbot directly in your terminal. Type your message and press Enter.

To exit the chatbot, type `quit`, `exit`, or `q`.

## 🐳 Docker

This project includes a `Dockerfile` for building and running the application in a container.

### 🏗️ Build the Docker Image

```bash
docker build -t basic-chatbot .
```

### 🏃 Run the Docker Container

To run the container, you need to pass the environment variables from your `.env` file.

```bash
docker run -it --env-file .env basic-chatbot
```

This will start the chatbot in interactive mode, allowing you to chat with it directly from your terminal.
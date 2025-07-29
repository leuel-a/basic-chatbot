## Basic Chatbot with Langraph

Basic Chatbot with LangGraph is a terminal‑based conversational AI built on LangGraph and Google’s Generative AI that remembers context, integrates external tools like Tavily Search for real‑time information, and is easily extensible. To get started:

Install:

- Clone the repo: git clone https://github.com/your-username/basic-chatbot.git && cd basic-chatbot

- Create a virtual environment: python -m venv .venv && source .venv/bin/activate

- Install dependencies: pip install -r requirements.txt

- Configure: copy .env.example to .env and add GOOGLE_API_KEY and TAVILY_API_KEY.

Run locally: python src/main.py

Docker:

Build: docker build -t basic-chatbot .

Run: docker run -it --env-file .env basic-chatbot

# 🤖 Chatbot Quinta da Meda

This project is an AI-powered chatbot designed for the local accommodation **Quinta da Meda**. It allows guests to ask any questions they might have about the accommodation, based on information scraped from the official website and Booking.com.

The chatbot uses **Retrieval-Augmented Generation (RAG)** powered by **OpenAI's GPT-4o** model and provides a friendly interface via **Streamlit**.

**Official website:** [Quinta da Meda](https://www.quintadameda.com/en) | Come and visit us 😊

---

## 📦 Project Structure

Chatbot_QuintadaMeda/

├── .env # Environment variables (e.g. API key)

├── .gitignore

├── main.py # Streamlit frontend

├── scraper.py # Script to extract and save raw information

├── requirements.txt

├── rag/

    ├── loader.py # Load data from local .txt files

    ├── retriever.py # Create vector store retriever

    └── rag_chatbot.py # RAG logic to generate responses

├── data/

    ├── info_booking.txt

    ├── info_contact.txt

    ├── info_main_page.txt

    ├── info_region.txt

    └── info_rooms.txt


---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Chatbot_QuintadaMeda.git
cd Chatbot_QuintadaMeda
```

### 2. Install Requirements
It's recommended to use a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

pip install -r requirements.txt
```

### 3. Set the Environment Variables
Create a .env file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 🚀 Running the App
Run the Streamlit app:

```bash
streamlit run main.py
```

Open your browser and go to http://localhost:8501 to start chatting with the bot.

### 📚 How It Works
- Web Scraping: scraper.py extracts information from the website and saves it into .txt files.

- Knowledge Base: These .txt files are loaded and converted into embeddings.

- Retriever: Similar documents are retrieved based on user input using FAISS and OpenAI Embeddings.

- Generation: GPT-4o-mini generates a final answer based on the retrieved context.

### 🔐 Security
Make sure not to commit your .env file. It is excluded by the .gitignore file.

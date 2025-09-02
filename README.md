# Chatbot with Amazon Bedrock & Streamlit

A lightweight, memory‑aware chat UI built with **Streamlit** that talks to **Anthropic Claude 3 Haiku** via **Amazon Bedrock** using **LangChain**. Conversation context is summarized and retained with `ConversationSummaryBufferMemory`.

---

## ✨ Features
- **Chat UI in the browser** with `st.chat_input` / `st.chat_message`.
- **Conversation memory** using LangChain's summary buffer to keep context under a token limit.
- **Amazon Bedrock** integration via `langchain_aws.ChatBedrock`.
- **Configurable model params** (`max_tokens`, `temperature`, `top_p`, `stop_sequences`).
- **Simple, readable codebase** (two Python files).

---

## 🧱 Project Structure
```
.
├── chatbot_app.py          # Streamlit UI
├── chatbot_model.py        # Bedrock + LangChain logic & memory
├── requirements.txt        # Python dependencies (sample below)
└── README.md               # This file
```

---

## 🖼️ How it Works
- `chatbot_app.py` starts a Streamlit app, initializes `st.session_state.memory` using `the_memory()`, renders chat history, collects user input, and calls `the_conversation()` to get a reply.
- `chatbot_model.py` defines:
  - `my_chatbot()` → creates a `ChatBedrock` client targeting `anthropic.claude-3-haiku-20240307-v1:0`.
  - `the_memory()` → creates a `ConversationSummaryBufferMemory` with a `max_token_limit`.
  - `the_conversation(input_text, memory)` → wraps `ChatBedrock` and memory in a `ConversationChain` and returns the model response.

> Note: Each `the_conversation` call currently re‑creates the LLM client. This is simple but not optimal. See the **Improvements** section to reuse the client.

---

## ✅ Prerequisites
- Python **3.10+** (3.11 recommended)
- An **AWS account** with **Bedrock** enabled in a supported region (e.g., `us-east-1`).
- **Access to Anthropic Claude 3 Haiku** provisioned in Bedrock (model ID: `anthropic.claude-3-haiku-20240307-v1:0`).
- AWS credentials configured locally (via `~/.aws/credentials`, environment variables, or an assumed role). This repo uses the **`credentials_profile_name='default'`**.

---

## 🔧 Installation
1. **Clone & enter** the project folder:
   ```bash
   git clone <your-repo-url>
   cd <your-repo>
   ```

2. **Create & activate** a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Sample `requirements.txt`
```txt
streamlit>=1.36
langchain>=0.2
langchain-core>=0.2
langchain-community>=0.2
langchain-aws>=0.1
boto3>=1.34
```

> Depending on your environment you may also need `botocore` pinned alongside `boto3`.

---

## 🔐 AWS & Environment Configuration
This app authenticates to Bedrock using an AWS **named profile** set to `default` in `~/.aws/credentials`. Example:

**~/.aws/credentials**
```ini
[default]
aws_access_key_id=AKIA...
aws_secret_access_key=...
aws_session_token=...        # if using temporary creds
```

**~/.aws/config**
```ini
[profile default]
region=us-east-1
output=json
```

**Required IAM permissions** (attach to the user/role behind your creds):
- `bedrock:InvokeModel`
- `bedrock:InvokeModelWithResponseStream`
- `bedrock:ListFoundationModels`

Also ensure your account has **model access** to Anthropic Claude 3 Haiku in Bedrock (in the console → Bedrock → Model access).

---

## ▶️ Run the App
From the project root:
```bash
streamlit run chatbot_app.py
```
Then open the URL printed in your terminal (usually http://localhost:8501).

---

## ⚙️ Configuration Notes
In `chatbot_model.py` → `my_chatbot()`:
```python
my_llm = ChatBedrock(
    credentials_profile_name='default',
    model_id='anthropic.claude-3-haiku-20240307-v1:0',
    model_kwargs={
        "max_tokens": 300,
        "temperature": 0.1,
        "top_p": 0.9,
        "stop_sequences": ["\n\nHuman:"]
    }
)
```
You can change:
- `credentials_profile_name` → switch to another named profile.
- `model_id` → to a different Bedrock‑hosted model version.
- Sampling params (`temperature`, `top_p`, `max_tokens`, `stop_sequences`).

---

## 🧠 Memory Behavior
- `ConversationSummaryBufferMemory` keeps a running **summary** of the conversation to control token growth.
- The `max_token_limit=300` governs how much context is kept. Increase for longer memory, decrease for lower cost/latency.

---

## 🛠️ Improvements (Optional)
- **Reuse the LLM client**: create the `ChatBedrock` instance once and reuse it across turns (e.g., store in `st.session_state`), instead of re‑initializing inside `the_conversation`.
- **Persist history**: save `chat_history` to disk/DB (e.g., SQLite, DynamoDB) to survive app restarts.
- **Config via env**: read model ID, profile, and params from environment variables.
- **Add system prompts**: use LangChain’s prompt templates to guide tone and persona.
- **Streaming tokens**: enable streamed responses for faster perceived latency.
- **Error handling**: surface friendly messages for auth/permission/timeouts.
- **Multi‑model switcher**: dropdown to pick `haiku/sonnet/opus` (subject to access).

---

## 🧪 Health Checks & Troubleshooting
- **Auth errors (`AccessDeniedException`)** → verify IAM policy and that model access is granted in Bedrock.
- **`Unknown modelId`** → confirm the `model_id` string and region.
- **Timeouts / throttling** → retry with backoff; lower `max_tokens`.
- **Empty responses** → check `stop_sequences` isn’t stopping too early; inspect logs (set `verbose=True`).
- **Region mismatch** → ensure your default AWS region matches where Bedrock is enabled for your account.

---

## 🧭 Common Customizations
- **Change the app title & placeholder**: edit `st.title(...)` and `st.chat_input(...)` in `chatbot_app.py`.
- **Adjust memory size**: tweak `max_token_limit` in `the_memory()`.
- **Add system instructions**: wrap the user input with a prefix, or use a LangChain `PromptTemplate` and `SystemMessage`.

---

## 🧯 Cost & Safety Notes
- Bedrock usage incurs costs per token. Keep `max_tokens` and memory size appropriate.
- Do not log sensitive data. Be mindful of input content and storage if you persist history.

---

## 📦 Minimal Dockerfile (optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV AWS_PROFILE=default \
    AWS_REGION=us-east-1
EXPOSE 8501
CMD ["streamlit", "run", "chatbot_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
> When running in a container, prefer **IAM roles** (e.g., on ECS/EKS) over baking static keys into the image.

---

## 📄 License
MIT (or your preferred license).

---

## 🙌 Acknowledgements
- [Streamlit]
- [LangChain]
- [Amazon Bedrock]
- [Anthropic Claude]

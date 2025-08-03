# 📟 Console Support Agent System

A modular, console-based multi-agent support system built using the OpenAI Agents SDK and Google Gemini API.  
This project demonstrates how to create a scalable AI-powered customer support assistant that handles billing, technical, and general queries by dynamically routing requests to specialized agents.

## ✨ Features

- **🤖 Multi-Agent Architecture:**  
  Includes a triage agent that classifies user queries and routes them to specialized billing, technical, or general support agents.

- **⚙️ Context-Aware Tools:**  
  Each specialized agent uses dedicated tools with conditional logic based on user context (e.g., premium status, issue type).

- **🛡 Async Output Guardrails:**  
  Implements asynchronous guardrails to validate agent responses and prevent undesired outputs like apologies.

- **💬 Console-Based Interface:**  
  Fully interactive CLI allowing users to input queries and receive AI-generated responses in real-time.

- **🌐 Gemini API Integration:**  
  Uses Google Gemini models through the OpenAI SDK for powerful, state-of-the-art language understanding and generation.

## 🚀 Getting Started

### 🛠 Prerequisites

- Python 3.10 or higher  
- An OpenAI-compatible API key for Gemini API (set as `OPENAI_API_KEY` in your environment or `.env` file)  
- Install dependencies:

```bash
pip install -r requirements.txt
```
Setup:

1. Clone the repository:  
   git clone https://github.com/yourusername/console-support-agent-system.git  
   cd console-support-agent-system

2. Create a .env file with your API key:  
   OPENAI_API_KEY=your_gemini_api_key_here

3. Run the application:  
   python main.py

Usage:

- Enter your name and specify if you are a premium user.  
- Type your support queries related to billing, technical issues, or general questions.  
- The triage agent will route your query to the appropriate specialized agent.  
- To exit, type exit or quit.

Code Structure:

- main.py: Entry point; contains the CLI loop and agent orchestration logic.  
- Agents:
  - TriageAgent: Classifies queries and initiates handoffs.  
  - BillingAgent: Handles billing and refund related requests.  
  - TechnicalAgent: Handles technical support issues.  
  - GeneralAgent: Handles general inquiries.  
- Tools: Functions decorated with @function_tool to perform specific tasks.  
- Guardrails: Async functions that validate agent outputs to maintain response quality.

For more details, visit the OpenAI Agents SDK documentation at https://github.com/openai/openai-python/tree/main/agents and Google Gemini API docs at https://ai.google.dev/gemini-api/docs/overview.

---
🤝 Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements.

Thank you ❤



import asyncio
import os
from pydantic import BaseModel
from openai import AsyncOpenAI
from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    output_guardrail,
    Runner,
    GuardrailFunctionOutput,
    function_tool,
    RunConfig,
    enable_verbose_stdout_logging,
)
from dotenv import load_dotenv

load_dotenv()
enable_verbose_stdout_logging()
# --- Context Model ---
class SupportContext(BaseModel):
    user_name: str
    is_premium_user: bool
    issue_type: str = ""

# --- Setup Gemini Client and Model ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=client
)

# --- Tools ---
@function_tool
def refund(context: SupportContext, amount: str) -> str:
    if not context.is_premium_user:
        return "Refunds are only for premium users."
    return f"💰 Refund of ${amount} initiated."

@function_tool
def restart_service(context: SupportContext, service: str) -> str:
    if context.issue_type != "technical":
        return "Restart tool only available for technical issues."
    return f"🔧 Service '{service}' restarted."

@function_tool
def greet(context: SupportContext, message: str) -> str:
    return f"Hello {context.user_name}! How can I assist you today?"

# --- Async Guardrail ---
@output_guardrail
async def no_apology_guardrail(context, agent, agent_output) -> GuardrailFunctionOutput:
    output_text = agent_output.output if hasattr(agent_output, "output") else str(agent_output)
    forbidden_words = ["sorry", "apologize", "apologies"]
    triggered = any(word in output_text.lower() for word in forbidden_words)

    return GuardrailFunctionOutput(
        output_info=agent_output,
        tripwire_triggered=triggered
    )
# --- Agents ---
triage_agent = Agent(
    name="TriageAgent",
    model=model,
    instructions="""
You are a triage agent. Based on user query, set context.issue_type as 'billing', 'technical', or 'general'.
- For billing/refund issues, respond HANDOFF BillingAgent.
- For technical issues, respond HANDOFF TechnicalAgent.
- For general inquiries, respond HANDOFF GeneralAgent.
Use tools as appropriate.
""",
    output_guardrails=[no_apology_guardrail],
)

billing_agent = Agent(
    name="BillingAgent",
    model=model,
    tools=[refund],
    instructions="You handle billing issues. Use the refund tool if user requests a refund and is premium.",
    output_guardrails=[no_apology_guardrail],
)

technical_agent = Agent(
    name="TechnicalAgent",
    model=model,
    tools=[restart_service],
    instructions="You handle technical problems. Use the restart_service tool for 'technical' issues.",
    output_guardrails=[no_apology_guardrail],
)

general_agent = Agent(
    name="GeneralAgent",
    model=model,
    tools=[greet],
    instructions="You handle general inquiries and greetings.",
    output_guardrails=[no_apology_guardrail],
)

# --- RunConfig with guardrail ---
run_config = RunConfig(
    model=model,
    model_provider=client,
    output_guardrails=[no_apology_guardrail]
)

# --- Main async CLI loop ---
async def main():
    print("✅ Welcome to Support Agent. Type 'exit' to quit.")
    name = input("Enter your name: ").strip() or "User"
    premium = input("Are you a premium user? (yes/no): ").strip().lower() == "yes"

    context = SupportContext(
        user_name=name,
        is_premium_user=premium
    )

    # Start agent is triage_agent by default
    current_agent = triage_agent

    while True:
        query = input(f"{name}: ").strip()
        if query.lower() in ("exit", "quit"):
            print("👋 Goodbye!")
            break

        # Run agent with RunConfig
        result = await Runner.run(
            starting_agent=current_agent,
            input=query,
            context=context,
            run_config=run_config
        )
        output = result.final_output
        print("\n🤖 Agent Response:")
        print(output)

        # Simple handoff detection to switch agent based on output text
        if "HANDOFF BillingAgent" in output:
            current_agent = billing_agent
        elif "HANDOFF TechnicalAgent" in output:
            current_agent = technical_agent
        elif "HANDOFF GeneralAgent" in output:
            current_agent = general_agent
        else:
            current_agent = triage_agent

if __name__ == "__main__":
    asyncio.run(main())
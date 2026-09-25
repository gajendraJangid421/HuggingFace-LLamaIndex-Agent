import asyncio
import os

from dotenv import load_dotenv
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from llama_index.core.agent.workflow import AgentWorkflow, ReActAgent
from llama_index.core.utils import set_global_tokenizer

# Windows can block the native tiktoken DLL. LlamaIndex creates tokenizers for
# memory buffers automatically, so register a simple safe fallback early.
def _safe_tokenizer(text: str):
    return text.split()

set_global_tokenizer(_safe_tokenizer)

load_dotenv()

hf_token = os.getenv("HF_TOKEN")

# llm = HuggingFaceInferenceAPI(
#     model_name="Qwen/Qwen2.5-Coder-32B-Instruct",
#     temperature=0.7,
#     max_tokens=100,
#     token=hf_token,
#     provider="auto"
# )

# response = llm.complete("Hello, how are you?")

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiplies two integers and returns the resulting integer"""
    return a * b

llm = HuggingFaceInferenceAPI(
        model_name="Qwen/Qwen2.5-Coder-32B-Instruct",
        temperature=0.5,
        token=hf_token,
        provider="auto"
    )

multiply_agent = ReActAgent(
    name="multiply_agent",
    description="Is able to multiply two integers",
    system_prompt="A helpful assistant that can use a tool to multiply numbers.",
    tools=[multiply],
    llm=llm,
    streaming=False,
)

addition_agent = ReActAgent(
    name="add_agent",
    description="Is able to add two integers",
    system_prompt="A helpful assistant that can use a tool to add numbers.",
    tools=[add],
    llm=llm,
    streaming=False,
)


async def main():
    if not hf_token:
        print("HF_TOKEN is missing. Add it to your .env file before running the app.")
        return

    # Create the workflow
    workflow = AgentWorkflow(
        agents=[multiply_agent, addition_agent],
        root_agent="multiply_agent",
    )

    response = await workflow.run(user_msg="What's 2 plus 5 and 5 times 5?")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())

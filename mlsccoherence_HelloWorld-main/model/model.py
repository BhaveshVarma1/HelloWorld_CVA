from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
# Callbacks support token-wise streaming


MODEL_PATH = "llama-2-7b-chat.Q8_0.gguf"

def load_model() -> LlamaCpp:
    """Loads Llama Models"""
    callback_manager: CallbackManager = CallbackManager([StreamingStdOutCallbackHandler()])

    Llama_model: LlamaCpp = LlamaCpp(model_path=MODEL_PATH,
                           temperature=0.5, 
                           max_tokens= 4096, 
                           top_p= 1, 
                           callback_manager = callback_manager, 
                           verbose=True)
    return Llama_model

llm = load_model()

model_prompt: str = """
Question: what is the largest country on earth?
"""

response: str = llm(model_prompt)
print(response)
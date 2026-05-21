import os
from dotenv import load_dotenv, find_dotenv
from typing import Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq

load_dotenv(find_dotenv())


class ConfigLoader:
    def __init__(self):
        print(f"Loaded config.....")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: str = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        """
        Load and return the LLM model.
        """
        print("LLM loading...")
        print(f"Loading model from provider: {self.model_provider}")
        if self.model_provider != "groq":
            raise ValueError(f"Unsupported model_provider: {self.model_provider}. Only 'groq' is supported.")

        print("Loading LLM from Groq..............")
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY is required when using groq provider")
        model_name = self.config["llm"]["groq"]["model_name"]
        llm = ChatGroq(model=model_name, api_key=groq_api_key)
        return llm
    
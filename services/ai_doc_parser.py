import json
import re

from langchain.chat_models import init_chat_model
from openai import OpenAI

from utils.prompt import jd_prompt, resume_prompt


class AIDocumentParser:
    def __init__(self):
        self.model = init_chat_model("gpt-4o-mini", model_provider="openai")

    def parse_resume(self, resume_text: str) -> str:
        prompt = (resume_prompt + f"\n Resume:{resume_text}\n",)
        response = self.model.invoke(prompt)
        print(response.content)
        return response.content

    def parse_jd(self, job_description: str) -> str:
        prompt = (jd_prompt + f"\n Job Description:{job_description}\n",)
        response = self.model.invoke(prompt)
        print(response.content)
        return response.content

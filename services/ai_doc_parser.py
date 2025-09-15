import json
import re

from openai import OpenAI

from utils.prompt import jd_prompt, resume_prompt


class AIDocumentParser:
    def __init__(self):
        self.client = OpenAI()

    def parse_resume(self, resume_text: str) -> str:
        response = self.client.responses.create(
            model="gpt-4o-mini",
            input=resume_prompt + f"\n Resume:{resume_text}\n",
        )
        print(response.output_text)
        return response.output_text

    def parse_jd(self, job_description: str) -> str:
        response = self.client.responses.create(
            model="gpt-4o-mini",
            input=jd_prompt + f"\n Job Description:{job_description}\n",
        )
        print(response.output_text)
        return response.output_text

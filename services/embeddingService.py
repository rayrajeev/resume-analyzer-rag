import json
import uuid

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from openai import OpenAI


class EmbeddingService:
    def __init__(self):
        self.client = OpenAI()
        self.model_name = "text-embedding-3-small"
        self.chroma_client = chromadb.PersistentClient()
        embedding_function = OpenAIEmbeddingFunction(
            api_key=self.client.api_key, model_name="text-embedding-3-small"
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name="resumes", embedding_function=embedding_function
        )

    def embed_resume_text(self, text: str) -> list[float]:
        text = text.replace("```json", "").replace("```", "").strip()
        resume_data = json.loads(text)
        candidate_name = resume_data["Candidate Details"]["Name"]
        candidate_location = resume_data["Candidate Details"]["Location"]
        self.embed_candidate_skills(resume_data, candidate_name, candidate_location)
        self.embed_candidate_prof_experience(resume_data, candidate_name, candidate_location)
        self.embed_candidate_education(resume_data, candidate_name, candidate_location)

    def embed_candidate_skills(self, resume_data, candidate_name, candidate_location):
        skills_data = resume_data["Skills with Recency Score"]

        records = []
        for category, skills in skills_data.items():
            category_skill = f"category:{category}"
            for skill_name, details in skills.items():
                # Some sections like Certifications might have name as dict key
                rating = details.get("Rating", None)
                usage = details.get("UsageContext", "")
                years_experience = details.get("YearsExperience", 0)
                last_used = details.get("LastUsed", "")

                category_skill += f"\n Skill:{skill_name}, rating: {rating}, usage: {usage}, years_experience: {years_experience}, last_used: {last_used}"

            record_id = str(uuid.uuid4())
            metadata = {
                "candidate_name": candidate_name,
                "candidate_location": candidate_location,
                "category": category,
                "skill_name": skill_name,
                "rating": rating,
                "usage": usage,
                "years_experience": years_experience,
                "last_used": last_used,
            }

            # Add to Chroma collection
            self.collection.add(
                ids=[record_id],
                documents=[category_skill],
                metadatas=[metadata],
            )
            records.append(metadata)

        print(f"Inserted {len(records)} skill embeddings into ChromaDB.")
        
    def embed_candidate_prof_experience(self, resume_data, candidate_name, candidate_location):
        prof_experience = resume_data.get("Professional Experience", [])
        records = []
        for exp in prof_experience:
            title = exp.get("Title", "")
            company = exp.get("Company", "")
            duration = exp.get("Duration", "")
            description = exp.get("Description", "")

            exp_text = f"Title: {title}, Company: {company}, Duration: {duration}, Description: {description}"
            record_id = str(uuid.uuid4())
            metadata = {
                "candidate_name": candidate_name,
                "candidate_location": candidate_location,
                "title": title,
                "company": company,
                "duration": duration,
            }

            # Add to Chroma collection
            self.collection.add(
                ids=[record_id],
                documents=[exp_text],
                metadatas=[metadata],
            )
            records.append(metadata)

        print(f"Inserted {len(records)} professional experience embeddings into ChromaDB.")
        
    def embed_candidate_education(self, resume_data, candidate_name, candidate_location):
        education_data = resume_data.get("Education", [])
        records = []
        for edu in education_data:
            degree = edu.get("Degree", "")
            field = edu.get("Field", "")
            institution = edu.get("Institution", "")
            graduation_year = edu.get("GraduationYear", "")

            edu_text = f"Degree: {degree}, Field: {field}, Institution: {institution}, GraduationYear: {graduation_year}"
            record_id = str(uuid.uuid4())
            metadata = {
                "candidate_name": candidate_name,
                "candidate_location": candidate_location,
                "degree": degree,
                "field": field,
                "institution": institution,
                "graduation_year": graduation_year,
            }

            # Add to Chroma collection
            self.collection.add(
                ids=[record_id],
                documents=[edu_text],
                metadatas=[metadata],
            )
            records.append(metadata)

        print(f"Inserted {len(records)} education embeddings into ChromaDB.")
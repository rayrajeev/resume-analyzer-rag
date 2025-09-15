resume_prompt = """You are an expert technical recruiter.
Analyze the resume below to extract the key information for ranking candidates.

Return the result strictly in this JSON format:

{
  "Candidate Details": {
    "Name": "",
    "Location": "",
    "Email": "",
    "LinkedIn": ""
    "Total Experience (Years)": 0,
  },
  "Skills with Recency Score": {
    "Programming Languages": {
      "SkillName": {
        "Rating": 1-5,
        "YearsExperience": 0,
        "LastUsed": "YYYY"
        "UsageContext": "YYYY-YYYY → short context at Company"
      }
    },
    "Frameworks": {
      "SkillName": {
        "Rating": 1-5,
        "YearsExperience": 0,
        "LastUsed": "YYYY",
        "usageContext": "YYYY-YYYY → short context at Company"
      }
    },
    "Cloud": {
      "SkillName": {
        "Rating": 1-5,
        "YearsExperience": 0,
        "LastUsed": "YYYY"
        "usageContext": "YYYY-YYYY → short context at Company"
      }
    },
    "Databases": {
      "SkillName": {
        "Rating": 1-5,
        "YearsExperience": 0,
        "LastUsed": "YYYY",
        "usageContext": "YYYY-YYYY → short context at Company"
      }
    },
    "Tools": {
      "SkillName": {
        "Rating": 1-5,
        "YearsExperience": 0,
        "LastUsed": "YYYY",
        "usageContext": "YYYY-YYYY → short context at Company"
      }
    },
    "Certifications": {
      "CertificationName": {
        "Year": "YYYY"
      }
    }
  },
  "Professional Experience": [
    {
      "Company": "",
      "Location": "",
      "Title": "",
      "StartDate": "MMM YYYY",
      "EndDate": "MMM YYYY or Present",
      "Description": [
        "Responsibility or achievement 1",
        "Responsibility or achievement 2"
      ]
    }
  ],
  "Education": [
    {
      "Degree": "",
      "Field": "",
      "Institution": "",    
      "GraduationYear": "YYYY"
    }
  ],

Rules:
- Assign a recency score (1-5).
- Include "UsageContext" with timeline and example usage from the resume.
- Do not include extra text or explanation outside JSON.
- Output valid JSON only.
- "UsageContext" must be a **single short sentence or phrase**, not multiple sentences. 
- Format: "YYYY-YYYY → short context at Company".
- Do not include explanations or multiple projects per line; pick the most relevant/longest usage.
- If candidate has many roles, highlight recent ones in more detail, older ones in fewer words.
"""

jd_prompt = """You are an assistant that converts unstructured Job Descriptions (JDs) into a concise, structured JSON format 
for vector database storage and semantic resume matching.  

Given a JD document, extract and normalize its content into the following JSON schema:

{
  "role": "<Job Title>",
  "summary": "<One or two sentences summarizing the role in plain language>",
  "core_responsibilities": [
    "Responsibility 1",
    "Responsibility 2",
    "Responsibility 3"
  ],
  "required_skills": [
    "Skill 1",
    "Skill 2",
    "Skill 3"
  ],
  "preferred_skills": [
    "Skill 1",
    "Skill 2"
  ],
  "education_experience": [
    "Education requirement",
    "Experience requirement"
  ]
}

Guidelines:
- Extract the job title and restate it in a concise form for "role".
- Summarize the description in 1–2 plain sentences for "summary".
- List each responsibility as a short action-oriented bullet (use verbs like design, build, maintain, collaborate, etc.).
- Normalize skills to their standard names (e.g., "Spring Boot, Spring Security, Spring Cloud" → keep as separate items, 
but use consistent capitalization).
- Group frameworks, libraries, and tools into "required_skills" or "preferred_skills" as appropriate.
- Keep "education_experience" concise (degrees, years of experience).
- Exclude generic corporate language (e.g., “collaborates with stakeholders”, “drives consensus”) unless it directly adds to the role requirements.
- Output only valid JSON without extra commentary.

Now, here is the Job Description to process:
"""

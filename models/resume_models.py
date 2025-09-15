from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Literal
from datetime import datetime
from enum import Enum

class ProficiencyLevel(str, Enum):
    EXPERT = "expert"
    ADVANCED = "advanced"
    INTERMEDIATE = "intermediate"
    BEGINNER = "beginner"

class EvidenceStrength(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class CertificationStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"

class SkillTimeline(BaseModel):
    skill: str = Field(..., description="Name of the skill")
    total_experience: str = Field(..., description="Total experience duration (e.g., '4 years')")
    total_experience_months: int = Field(..., description="Total experience in months")
    last_used: str = Field(..., description="Year when skill was last used")
    first_used: str = Field(..., description="Year when skill was first used")
    proficiency_level: ProficiencyLevel = Field(..., description="Skill proficiency level")
    contexts: List[str] = Field(default_factory=list, description="Contexts where skill was used")
    projects: List[str] = Field(default_factory=list, description="Projects using this skill")
    certifications: List[str] = Field(default_factory=list, description="Related certifications")
    evidence_strength: EvidenceStrength = Field(..., description="Strength of evidence for this skill")
    recency_score: float = Field(default=0.0, description="Score based on how recently the skill was used (0-100)")
    
    @validator('last_used', 'first_used')
    def validate_year(cls, v):
        try:
            year = int(v)
            if year < 1990 or year > datetime.now().year + 1:
                raise ValueError("Year must be between 1990 and current year + 1")
            return str(year)
        except ValueError:
            raise ValueError("Year must be a valid integer")

class WorkExperience(BaseModel):
    position: str = Field(..., description="Job position/title")
    company: str = Field(..., description="Company name")
    duration: str = Field(..., description="Duration in format 'YYYY-YYYY' or 'YYYY-Present'")
    start_date: str = Field(..., description="Start date (YYYY or YYYY-MM)")
    end_date: Optional[str] = Field(None, description="End date (YYYY or YYYY-MM), None if current")
    total_months: int = Field(..., description="Total duration in months")
    key_skills_used: List[str] = Field(default_factory=list, description="Key skills used in this role")
    achievements: List[str] = Field(default_factory=list, description="Key achievements and accomplishments")
    responsibilities: List[str] = Field(default_factory=list, description="Key responsibilities")

class Education(BaseModel):
    degree: str = Field(..., description="Degree/qualification name")
    institution: str = Field(..., description="Educational institution name")
    graduation_year: str = Field(..., description="Year of graduation")
    gpa: Optional[str] = Field(None, description="GPA or grade if mentioned")
    relevant_courses: List[str] = Field(default_factory=list, description="Relevant courses or subjects")
    honors: List[str] = Field(default_factory=list, description="Honors, awards, or distinctions")

class Certification(BaseModel):
    name: str = Field(..., description="Certification name")
    issuer: str = Field(..., description="Issuing organization")
    date_obtained: str = Field(..., description="Date when certification was obtained")
    expiry_date: Optional[str] = Field(None, description="Expiry date if applicable")
    status: CertificationStatus = Field(..., description="Current status of certification")
    credential_id: Optional[str] = Field(None, description="Credential ID if mentioned")

class Project(BaseModel):
    name: str = Field(..., description="Project name")
    duration: str = Field(..., description="Project duration")
    duration_months: int = Field(..., description="Project duration in months")
    technologies: List[str] = Field(default_factory=list, description="Technologies and tools used")
    role: str = Field(..., description="Role in the project")
    year: str = Field(..., description="Year when project was completed")
    description: Optional[str] = Field(None, description="Project description")
    achievements: List[str] = Field(default_factory=list, description="Key achievements in the project")

class PersonalDetails(BaseModel):
    name: Optional[str] = Field(None, description="Full name")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="Current location")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    portfolio: Optional[str] = Field(None, description="Portfolio website URL")
    summary: Optional[str] = Field(None, description="Professional summary")

class ResumeAnalysis(BaseModel):
    personal_details: PersonalDetails = Field(default_factory=PersonalDetails)
    skills_timeline: List[SkillTimeline] = Field(default_factory=list)
    work_experience: List[WorkExperience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    certifications: List[Certification] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    total_experience_years: float = Field(default=0.0, description="Total professional experience in years")
    top_skills: List[str] = Field(default_factory=list, description="Top 10 skills based on recency and evidence")
    
    class Config:
        use_enum_values = True

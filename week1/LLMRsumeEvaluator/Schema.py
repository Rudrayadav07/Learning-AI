from pydantic import BaseModel

class Experience(BaseModel):
    company_name:str
    experience:int



class JobDescription(BaseModel):
    role:str
    required_skill:list[str]
    education:str
    experience_years:int
    preferred_skill:list[str]





class Resume(BaseModel):
    personal_information:str
    education:str
    skills:list[str]
    experience:list[Experience]
    projects:list[str]


jobSchema = JobDiscription.model_json_schema()
ResumeSchema = Resume.model_json_schema()


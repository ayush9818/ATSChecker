"""
Author: Ayush Agarwal
"""
import warnings
warnings.filterwarnings('ignore')

import os
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from ats_app.models.ai_models import ResumeScore
from ats_app.resume_utils.prompts import resume_match_prompt
from ats_app.resume_utils.loaders import load_resume_from_docx, load_resume_from_pdf

GOOGLE_API_KEY=os.environ['GEMINI_API_KEY']


def create_ats_chain(model_name="gemini-1.5-pro"):
    llm = GoogleGenerativeAI(model=model_name, 
                            google_api_key=GOOGLE_API_KEY)
    parser = PydanticOutputParser(pydantic_object=ResumeScore)

    new_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)

    prompt = PromptTemplate(
        template=resume_match_prompt,
        input_variables=["resume"],
        partial_variables={"format_instructions": new_parser.get_format_instructions()},
    )

    return prompt | llm | new_parser

def perform_ats_analysis(llm_chain, resume_path, job_description):
    if resume_path.endswith('.pdf'):
        resume_text = load_resume_from_pdf(resume_path)
    elif resume_path.endswith('.docx'):
        resume_text = load_resume_from_docx(resume_path)
    else:
        raise NotImplementedError(f"Received {resume_path}. Currently support .docx and .pdf files")

    resume_analysis = llm_chain.invoke({"text" : resume_text, "jd" : job_description})
    return resume_analysis

    

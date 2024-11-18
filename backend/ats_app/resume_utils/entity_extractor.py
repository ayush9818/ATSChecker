"""
Author: Ayush Agarwal
"""
import warnings
warnings.filterwarnings('ignore')

import os
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from ats_app.models.ai_models import ResumeContent
from ats_app.resume_utils.prompts import entity_extraction_prompt
from ats_app.resume_utils.loaders import load_resume_from_docx, load_resume_from_pdf

GOOGLE_API_KEY=os.environ['GEMINI_API_KEY']

# TODO: Add Better logic to calculate year of experience

def create_entity_extractor_chain(model_name="gemini-1.5-pro"):
    llm = GoogleGenerativeAI(model=model_name, 
                            google_api_key=GOOGLE_API_KEY)
    parser = PydanticOutputParser(pydantic_object=ResumeContent)

    new_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)

    prompt = PromptTemplate(
        template=entity_extraction_prompt,
        input_variables=["resume"],
        partial_variables={"format_instructions": new_parser.get_format_instructions()},
    )

    return prompt | llm | new_parser


def extract_entities(llm_chain, file_path):
    if file_path.endswith('.pdf'):
        resume_text = load_resume_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        resume_text = load_resume_from_docx(file_path)
    else:
        raise NotImplementedError(f"Received {file_path}. Currently support .docx and .pdf files")

    extracted_entities = llm_chain.invoke({"resume" : resume_text})
    return extracted_entities 
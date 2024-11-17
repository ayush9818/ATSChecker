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

GOOGLE_API_KEY=os.environ['GEMINI_API_KEY']


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


def extract_entities(llm_chain, resume):
    # Convert to doc if pdf, otherwise process as it is 
    converted_resume = resume # Add resume conversion code later    

    extracted_entities = llm_chain.invoke({"resume" : converted_resume})
    return extract_entities 
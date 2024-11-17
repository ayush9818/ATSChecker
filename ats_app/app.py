"""
Author: Ayush Agarwal
"""
import pandas as pd
from ats_app.resume_utils.entity_extractor import (
    create_entity_extractor_chain, 
    extract_entities
)

if __name__ == "__main__":
    entity_chain = create_entity_extractor_chain()
    resume_path = "/nfs/home/scg1143/ATSChecker/sample_data/resume.pdf"
    entities = extract_entities(entity_chain, file_path=resume_path)
    import pdb;pdb.set_trace();

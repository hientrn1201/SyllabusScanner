from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from extraction.extraction import Extraction
from notion.syllabus_notion import SyllabusNotion
from typing import Dict
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/extract")
async def extract_syllabus(data: Dict):
    openai_api_key = data.get('openai_api_key')
    text = data.get('text')

    extraction_service = Extraction(openai_api_key=openai_api_key)

    data = extraction_service.extract(text)

    if data is None:
        return JSONResponse(content={"error": "Error extracting data, please check your OpenAI API Key and the length of the syllabus or try again later"}, status_code=500)

    return JSONResponse(content={"data": data}, status_code=200)


@app.post("/save_to_notion")
async def save_to_notion(data: Dict):
    notion_api_key = data.get('notion_api_key')
    notion_database_id = data.get('notion_database_id')
    extracted_data = data.get('data')

    notion_service = SyllabusNotion(
        notion_api_key, notion_database_id, extracted_data)
    response = notion_service.create_syllabus_notion_page()

    if response.status_code == 200:
        return JSONResponse(content={"message": "Successfully created Notion page"}, status_code=200)
    else:
        return JSONResponse(content={"error": f"Error creating Notion page. {response.text}"}, status_code=500)

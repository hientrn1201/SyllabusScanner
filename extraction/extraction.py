import os
from helper.token_helper import num_tokens_from_string
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain_pydantic
from pypdf import PdfReader
from extraction.schemas import Course
import backoff


class Extraction:
    def __init__(self, openai_api_key=None):
        os.environ["OPENAI_API_KEY"] = openai_api_key
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)
        self.data = None
        self.schema = Course
        self.extraction_chain = create_extraction_chain_pydantic(
            pydantic_schema=self.schema, llm=self.llm)

    def scrape(self, file):
        reader = PdfReader(file)
        number_of_pages = len(reader.pages)
        text = ''
        for i in range(number_of_pages):
            page = reader.pages[i]
            text += page.extract_text()
        return text

    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    def extract(self, text):
        if num_tokens_from_string(text, "cl100k_base") > 13000:
            return None
        self.data = self.extraction_chain(text=text)[0].dict()
        return self.data

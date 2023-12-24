<!-- PROJECT LOGO -->
<br />
<div align="center">

<h2 align="center">Syllabus Scanner</h2>

  <p align="center">
    An app to scrape syllabus PDFs, extract information, and populate Notion pages.
    <br />
  </p>
</div>

<!-- ABOUT THE PROJECT -->

## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

The Syllabus Scanner project comes from my love of keeping things organized and a wish to make school life a bit easier. Since I use Notion for notes, I often found myself manually putting syllabus info into these apps. The project aims to automate this process, making it simple to turn syllabus PDFs into organized events in Notion.

### Built With

- Python
- Langchain
- OpenAI
- Streamlit
- Notion API

<!-- GETTING STARTED -->

## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Before you begin, make sure you have the following:

- python and pip installed

  ```sh
  # Example installation for Mac with homebrew
  brew install python3
  ```

- OpenAI API Key

  Get your API Key from https://platform.openai.com

- Notion API

  Set up a new integration following notion's instructions here: https://developers.notion.com/docs/create-a-notion-integration

  Then obtain the integration secret key and the database id that you will perform the integration

### Installation and Start the application

1. Clone the repo
   ```sh
   git clone https://github.com/hientrn1201/SyllabusScanner
   ```
2. Install dependencies
   ```sh
   pip install -r requirement.txt
   ```
3. Run the program
   ```sh
   streamlit run app.py
   ```

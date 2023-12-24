import requests
import json


class Notion:
    def __init__(self, notion_api_key, notion_database_id):
        self.notion_api_key = notion_api_key
        self.notion_database_id = notion_database_id
        self.base_url = "https://api.notion.com/v1"

    def _create_text(self, content, annotations=None, href=None):
        return {
            "type": "text",
            "text": {
                    "content": content,
                    "link": None
            },
            "annotations": annotations or {
                "bold": False,
                "italic": False,
                "strikethrough": False,
                "underline": False,
                "code": False,
                "color": "default"
            },
            "plain_text": content,
            "href": href
        }

    def _create_block(self, type_text, content, annotations=None):
        return {
            "object": "block",
            "type": type_text,
            type_text: {
                "rich_text": [
                    self._create_text(content, annotations)
                ]
            }
        }

    def _create_table_row(self, contents):
        return {
            "type": "table_row",
            "table_row": {
                "cells": [[self._create_text(content)] for content in contents]
            }
        }

    def _create_table(self, data, width, has_column_header=False, has_row_header=False):
        children = [self._create_table_row(
            row_contents) for row_contents in data]

        return {
            "type": "table",
            "table": {
                "table_width": width,
                "has_column_header": has_column_header,
                "has_row_header": has_row_header,
                "children": children
            },
        }

    def _create_columns(self, children):
        children_list = []
        for child in children:
            children_list.append(
                {
                    "object": "block",
                    "type": "column",
                    "column": {
                        "children": child
                    }
                }
            )
        return {
            "object": "block",
            "type": "column_list",
                    "column_list": {
                        "children": children_list
                    }
        }

    def _create_notion_page(self, title, children):
        # Headers for the API request
        headers = {
            "Authorization": f"Bearer {self.notion_api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        # Constructing the data for the request
        data = {
            "parent": {"page_id": self.notion_database_id},
            "properties": {
                "title": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                }
            },
            "children": children
        }

        # API endpoint URL
        url = self.base_url + "/pages"

        # Making the HTTP POST request to create a new page
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Verifying the response
        return response

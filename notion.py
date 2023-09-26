import os
from dotenv import load_dotenv
import requests

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")
VERSION = "2021-05-13"

class NotionApi(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(NotionApi, cls).__new__(cls)
    return cls.instance
  
  def updateStandupPage(self, message):
    url = "https://api.notion.com/v1/blocks/" + NOTION_PAGE_ID + "/children"
    headers = {
      "Authorization": "Bearer " + NOTION_API_KEY, 
      "Content-Type": "application/json", 
      "Notion-Version": VERSION
    }
    
    data = {
      "children": [
        {
          "object": "block",
          "type": "paragraph",
          "paragraph": {
            "text": [{ "type": "text", "text": { "content": message } }]
          }
        }
      ]
    }
    
    response = requests.patch(url, json = data, headers = headers)
    return response.status_code
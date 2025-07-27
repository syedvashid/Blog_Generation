from typing import TypedDict
from pydentic import BaseModel, Field

class Blog(BaseModel):
    title: str = Field( description="The title of the blog post")
    content: str = Field( description="The content of the blog post")

class BlogState(TypedDict):
    topic:str
    blog:Blog
    current_language: str
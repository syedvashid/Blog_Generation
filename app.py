import uvicorn
from fastapi import FastAPI, Request
from src.graphs.graph_builder2 import GraphBuilder
from src.LLms.groq import GroqLLm

import os
from dotenv import load_dotenv
load_dotenv()

app=FastAPI()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
## API's

@app.post("/blogs")
async def create_blogs(request:Request):
    
    data=await request.json()
    topic= data.get("topic","")
    language = data.get("language", '')
    print(language)

    ## get the llm object

    groqllm=GroqLLm()
    llm=groqllm.get_llm()

    ## get the graph
    graph_builder=GraphBuilder(llm)
    if topic and language:
        graph=graph_builder.setup_graph(usecase="language")
        state=graph.invoke({"topic":topic,"current_language":language.lower()})

    elif topic:
        graph=graph_builder.setup_graph(usecase="topic")
        state=graph.invoke({"topic":topic})
    

    return {"data":state}

if __name__=="__main__":
    uvicorn.run("app:app",reload=True)


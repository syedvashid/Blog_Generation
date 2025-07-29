from langgraph.graph import StateGraph,START,END
from src.LLms.groq import GroqLLm
from src.states.blogstate import BlogState
from src.nodes.node import BlogNode

class GraphBuilder:
    def __init__(self,llm):
        self.llm =llm
        self.graph = StateGraph(BlogState)
    
    def build_topic_graph(self):
        """
        Build a graph to generate blogs on topic"""
        self.blog_node_obj =BlogNode(self.llm)
        # nodes
        self.graph.add_node("title_creation",self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation",self.blog_node_obj.content_generation)

        # Edge
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation",END)

        return self.graph

    def setup_graph(self,usecase):
        if usecase =="topic":
           self.build_topic_graph()
        
        return self.graph.compile()
    
    # ?Blew code is for the langsmith lanffraph studio

llm=GroqLLm().get_llm()

# get the graph
graph_builder =GraphBuilder(llm)
graph_builder.build_topic_graph().compile()

from langgraph.graph import StateGraph,START,END
from src.LLms.groq import GroqLLm
from src.states.blogstate import BlogState
from src.nodes.node import BlogNode

class GraphBuilder:
    def __init__(self,llm):
        self.llm=llm
        self.graph=StateGraph(BlogState)

    def build_topic_graph(self):
        """
        Build a graph to generate blogss based on topic
        """
        self.blog_node_obj=BlogNode(self.llm)
        print(self.llm)
        ## Nodes
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation",self.blog_node_obj.content_generation)

        ## Edges
        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation","content_generation")
        self.graph.add_edge("content_generation",END)

        return self.graph
    
    def build_language_graph(self):
        """
        Build a graph for blog generation with inputs topic and language
        """
        self.blog_node_obj=BlogNode(self.llm)
        print(self.llm)
        ## Nodes
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation",self.blog_node_obj.content_generation)
        self.graph.add_node("hindi_translation",lambda state: self.blog_node_obj.translation({**state, "current_language": "hindi"}))
        self.graph.add_node("french_translation",lambda state: self.blog_node_obj.translation({**state, "current_language": "french"}))
        self.graph.add_node("route",self.blog_node_obj.route)

        ## edges and conditional edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", "route")

        ## conditional edge
        self.graph.add_conditional_edges(
            "route",
            self.blog_node_obj.route_decision,
            {
                "hindi":"hindi_translation",
                "french":"french_translation"
            }
        )
        self.graph.add_edge("hindi_translation",END)
        self.graph.add_edge("french_translation",END)
        return self.graph

    
    def setup_graph(self,usecase):
        if usecase=="topic":
            self.build_topic_graph()
        if usecase=="language":
            print("Language block")
            self.build_language_graph()

        return self.graph.compile()
    

## Below code is for the langsmith langgraph studio
llm=GroqLLm().get_llm()

## get the graph
graph_builder=GraphBuilder(llm)
graph=graph_builder.build_language_graph().compile()


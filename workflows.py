from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from rag_store import query

def build_agent():
    llm = ChatOpenAI(model="gpt-4o-mini")

    workflow = StateGraph(dict)

    def draft(state):
        context_docs = query(state["body"], k=3)
        context_text = "\n\n".join([d.page_content for d in context_docs])

        prompt = f"""
        You are an email assistant. 
        Context from files & past emails:\n{context_text}\n
        Incoming email:\n{state['body']}\n
        Write a helpful reply.
        """
        reply = llm.invoke(prompt)
        return {**state, "draft": reply.content}

    def critique(state):
        review = llm.invoke(f"Critique this reply:\n\n{state['draft']}")
        return {**state, "critique": review.content}

    workflow.add_node("draft", draft)
    workflow.add_node("critique", critique)
    workflow.set_entry_point("draft")
    workflow.add_edge("draft", "critique")
    workflow.add_edge("critique", END)

    return workflow.compile()

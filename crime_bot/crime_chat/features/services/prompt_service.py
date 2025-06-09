import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END

from features.models.prompt_model import CrimeScene
from features.repository.prompt_repository import CrimeRepository

load_dotenv()

class PromptService:
    def __init__(self):
        self.repo = CrimeRepository()
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

    def _create_agent(self, role):
        prompt = PromptTemplate.from_template(
            "You are a " + role + ". Analyze the following crime scene:\n{input}\nReturn only your findings."
        )
        return prompt | self.llm | StrOutputParser()

    def analyze_crime_scene(self, description: str):
        # Save to in-memory repository
        self.repo.save_description(description)

        # LangChain agents for each role
        fact_agent = self._create_agent("Fact Extractor Agent. Extract key facts from the following crime scene description.")
        logic_agent = self._create_agent("Logic Reasoner Agent. Based on these facts, what logical inferences can you make?")
        profile_agent = self._create_agent("Profile Matcher Agent. Compare the following facts with the suspect profiles and find matches.")
        scenario_agent = self._create_agent("Scenario Builder Agent. Create a possible crime timeline or hypothesis based on the facts and profiles. No need for suspect analysis, only timeline and conclusion.")

        # Define LangGraph state model
        CrimeState = dict

        # Agent node wrappers (LangGraph expects input/output as dict)
        def fact_node(state: dict):
            result = fact_agent.invoke({"input": state["input"]})
            return {**state, "facts": result, "input": state["input"]}

        def logic_node(state: dict):
            result = logic_agent.invoke({"input": state["input"]})
            return {**state, "logic": result, "input": state["input"]}

        def profile_node(state: dict):
            result = profile_agent.invoke({"input": state["input"]})
            return {**state, "profiles": result, "input": state["input"]}

        def scenario_node(state: dict):
            result = scenario_agent.invoke({"input": state["input"]})
            return {**state, "output": result}

        # Define LangGraph state graph
        workflow = StateGraph(CrimeState)
        workflow.add_node("facts", fact_node)
        workflow.add_node("logic", logic_node)
        workflow.add_node("profiles", profile_node)
        workflow.add_node("scenarios", scenario_node)

        workflow.set_entry_point("facts")
        workflow.add_edge("facts", "logic")
        workflow.add_edge("logic", "profiles")
        workflow.add_edge("profiles", "scenarios")
        workflow.add_edge("scenarios", END)

        app = workflow.compile()

        inputs = {"input": description}
        result = app.invoke(inputs)

        # Optional: format final output (you can customize this)
        formatted_output = f"""### AI Crime Scene Report

**Facts Extracted:**  
{result.get("facts")}

**Logical Deductions:**  
{result.get("logic")}

**Profile Matches:**  
{result.get("profiles")}

**Scenario Hypothesis:**  
{result.get("output")}
"""
        return formatted_output

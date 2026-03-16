import os
from openai import OpenAI
# Initialize the OpenAI client
client = OpenAI(api_key=NOCOMMET)

from schemas import ActionGraph

def generate_action_graph(instruction: str) -> ActionGraph:
    """
    Parses natural language into a structured ActionGraph using LLM Function Calling.
    """
    # System prompt provides context to the model
    system_prompt = (
        "You are an expert Cooking Systems Engineer. "
        "Convert instructions into a directed acyclic graph (DAG) of actions. "
        "Identify constraints: duration, specific resources, and logical dependencies."
    )
    
    # 수정된 부분: 메시지 형식을 표준 딕셔너리 형태로 유지
    response = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": instruction}
        ],
        response_format=ActionGraph,
    )
    
    return response.choices[0].message.parsed
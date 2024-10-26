from typing import Dict, List

from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


class ContentGenerator:
    def __init__(self):
        self.llm = OpenAI(temperature=0.7)
        self.prompt_templates = {
            "story": PromptTemplate(
                input_variables=["query"],
                template="""Create an engaging story about {query}. 
                Make it captivating and suitable for audio narration. 
                Include vivid descriptions and natural dialogue.""",
            ),
            "podcast": PromptTemplate(
                input_variables=["query"],
                template="""Create an informative podcast script about {query}.
                Structure it like a professional podcast with clear sections,
                engaging facts, and natural transitions.""",
            ),
            "sermon": PromptTemplate(
                input_variables=["query"],
                template="""Create an inspiring sermon about {query}.
                Include spiritual insights, relevant scriptures,
                and practical applications for daily life.""",
            ),
            "science": PromptTemplate(
                input_variables=["query"],
                template="""Create an educational scientific explanation about {query}.
                Make it engaging and accessible while maintaining accuracy.
                Include recent research and fascinating details.""",
            ),
        }

    def generate_content(
        self, query: str, content_type: str, chat_history: List[Dict]
    ) -> str:
        # Get the appropriate prompt template
        prompt_template = self.prompt_templates.get(content_type)
        if not prompt_template:
            raise ValueError(f"Invalid content type: {content_type}")

        # Create and run the chain
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        response = chain.run(query=query)

        return response

    def refine_with_chat_history(self, content: str, chat_history: List[Dict]) -> str:
        # Use chat history to refine the content if needed
        relevant_context = "\n".join(
            [
                f"{msg['role']}: {msg['content']}"
                for msg in chat_history[-3:]  # Use last 3 messages for context
            ]
        )

        refine_prompt = PromptTemplate(
            input_variables=["content", "context"],
            template="""Given this conversation context:
            {context}
            
            Please refine this content to better match the user's needs:
            {content}
            
            Refined content:""",
        )

        chain = LLMChain(llm=self.llm, prompt=refine_prompt)
        refined_content = chain.run(content=content, context=relevant_context)

        return refined_content

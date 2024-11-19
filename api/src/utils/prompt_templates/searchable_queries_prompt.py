def searchable_queries_prompt():
    return f"""You're a super-intelligent and helpful AI-assistant.
    You're tasked with summarizing a text content into searchable phrases/queries where each could be used for web search.

    OUTPUT FORMAT:
    - Return a list of 3 queries separated by ###
    - Ensure each query is concise, meaningful, and standalone. No preambles.
    - Each query should be constructed as a clear searchable question.
    - Each query must facilitate the elicitation of relevant information from the web with rich context.
    - Always include one query that captures the main topic of the content.

    EXAMPLE 1:
    Content: You want to listen to a 10-minute audiocast summarizing cutting-edge technologies in modern neuroscience and their real-world applications.
    Output: What is neuroscience?###What are the cutting-edge technologies in neuroscience?###What are the real-world applications of neuroscience technologies?

    EXMAPLE 2:
    Content: You want to listen to a 10-minute commentary on the impact of climate change on global food security.
    Output: What is climate change?###What is global food security?###What is the impact of climate change on global food security?

    Remember:
    - No preambles, just the queries.
    - Only return three queries
    """

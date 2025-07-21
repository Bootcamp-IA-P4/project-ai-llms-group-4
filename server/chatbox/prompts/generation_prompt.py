from langchain.prompts import PromptTemplate

generation_prompt = PromptTemplate(
    input_variables=["topic", "audience", "platform", "style", "call_to_action", "language", "brand", "company", "product"],
    template="""
You are a professional copywriter and social media strategist.
Create a {platform} post about "{topic}" targeted at {audience} in {language} language.
The post should also mention the {brand} and {company} of any {product} or service related to the topic.
Use a {style} tone.
Include a strong call-to-action: {call_to_action}.

Make it engaging, authentic, and optimized for the platform.
"""
)

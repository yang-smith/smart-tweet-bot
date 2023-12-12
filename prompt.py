prompt_metadata = """I have some content that needs to be organized and archived. To facilitate management and retrieval, I need to create metadata to describe these contents in detail. I need your help in generating the metadata for these contents. The metadata can include the source of the content (such as websites, books, etc.), the author, categorization tags.
take a deep breath and think step by step:
First, clarify the components of the metadata, then collect the necessary information based on the characteristics of the content. Next, analyze and organize the information gathered. After that, propose an initial metadata structure plan base on gathered information. Examine and adjust the metadata structure according to the features of the content. Finally, provide the final metadata structure and populate it with specific details.
Restrictions:
The metadata must accurately reflect the main features of the content.
It should not contain information irrelevant to the content.
No more than three tags
Don't tell me your thought process
Directly output json

{format_instruction}\n{query}
"""
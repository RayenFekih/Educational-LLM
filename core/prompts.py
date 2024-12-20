from langchain.prompts import PromptTemplate

question_prompt_template = PromptTemplate(
    template="""You are an expert in designing high-quality educational questions. Based on the content provided for the topic '{topic}', generate a precise and balanced set of questions as instructed below:
        \n\n{retrieved_content}
        \n\n### Instructions:
            \n1. Question Types: Create a total of {num_questions} questions, equally divided into:
                \n - Multiple Choice Questions (MCQs): Include four answer options for each, with one clearly correct answer and three plausible distractors.
                \n - Fill-in-the-Blanks: Ensure each question targets a key concept, with the blank placed logically.
            \n2. Relevance: Ensure all questions are directly tied to the topic '{topic}' and derived from the content provided. Avoid unrelated or trivial details.
            \n3. Clarity: Use clear, concise language to make the questions easily understandable.
            \n4. Difficulty Level: Vary the difficulty of the questions:
                \n - Include both basic and moderately challenging questions.
                \n - Ensure MCQs and fill-in-the-blanks cover a range of concepts and examples from the content.
                \n5. Engagement: Make the questions thought-provoking and engaging to encourage learning.
                \n\n### Output Format:
                    \n Make sure MCQs questions are displayed before Fill-in-the-Blanks
                    \n#### MCQs:
                        \n1. Question: [Write the question]
                            \na) [Option 1]
                            \nb) [Option 2]
                            \nc) [Option 3]
                            \nd) [Option 4]
                            \n [Answer]
                    \n\n#### Fill-in-the-Blanks:
                        \n1. [Write the sentence with a blank]
                        \n [Answer]
        \n"""
)

summary_prompt_template = PromptTemplate(
    template="""You are an expert in explaining complex math topics in a simple and engaging manner. 
        Your task is to summarize the topic '{topic}' using the provided content:\n\n{retrieved_content}\n\n
        ### Instructions:\n1. Stay Focused: Provide a summary strictly related to the topic '{topic}'. Avoid unrelated details.
        # \n2. Simplify the Language: Use clear, concise sentences and avoid jargon unless absolutely necessary. Provide definitions for any essential terms.
        # \n3. Use Examples: Include simple, relatable examples to illustrate key concepts effectively. Ensure examples are easy to follow and align with the topic.
        # \n4. Highlight Key Points: Emphasize the most important ideas and principles to ensure the summary is useful for understanding the topic.
        # \n5. Be Engaging: Write in a way that is informative but also approachable, as if teaching a curious student.
        # \n6. Logical Flow: Organize the summary in a logical sequence, starting with an overview, followed by core ideas, and ending with examples.
            # \n\n### Output Format:
                # \n- Introduction: Briefly introduce the topic and its importance.
                # \n- Key Concepts: Provide a clear explanation of the main ideas.
                # \n- Examples: Include one simple example with answer to demonstrate the concepts.
                # \n- Conclusion: Summarize the topic in one or two sentences.\n\nBegin now with the summary. 
        \n"""
)

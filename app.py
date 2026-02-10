# AI marking logic
if st.button("Mark with AI"):
    with st.spinner("Marking..."):
        improved_prompt = f"""
You are an experienced BTEC assessor for Unit 101 – Health and Safety in ICT (Level 3 NVQ).
Your marking must be based strictly on the following knowledge and assessment criteria:

{knowledge}

Here is the student's assignment:

{assignment_text}

Instructions:
- For each learning outcome (1.1, 1.2, 1.3), state whether it is:
  - Fully met
  - Partially met
  - Not met
- For each outcome, provide a brief reason for your judgement.
- Highlight what the student has done well, using positive and encouraging language.
- Clearly and simply point out any missing or incorrect elements, so the student knows what to improve for their next submission.
- If the assignment is incomplete, review only what is present.
- Do not rewrite the assignment.
- Use UK English throughout.

After reviewing all learning outcomes, provide a final summary stating whether the assignment is sufficient to pass according to the criteria, or if further work is needed. Be clear and positive in your language.

Provide your feedback in the following structure:

1.1 Identify relevant organisational health and safety procedures  
- [Met/Partially met/Not met]: [Reason]  
- Positive feedback: [What is done well]  
- Areas for improvement: [What is missing or needs correction]

1.2 Identify available sources of health and safety information  
- [Met/Partially met/Not met]: [Reason]  
- Positive feedback: [What is done well]  
- Areas for improvement: [What is missing or needs correction]

1.3 Demonstrate how relevant health and safety procedures have been followed  
- [Met/Partially met/Not met]: [Reason]  
- Positive feedback: [What is done well]  
- Areas for improvement: [What is missing or needs correction]

Final Summary:
State clearly whether the assignment is sufficient to pass, or if further work is needed. Be encouraging and constructive.
"""
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": improved_prompt}],
                max_tokens=1200,
                temperature=0.2,
            )
            feedback = response.choices[0].message.content
            st.header("AI-Powered Feedback")
            st.write(feedback)
        except openai.RateLimitError:
            st.error("OpenAI rate limit reached. Please wait and try again later, or check your usage at https://platform.openai.com/usage.")
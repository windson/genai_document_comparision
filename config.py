# Few shots
SHOT_1 = """Human: Compare Document A and Document B, and provide a detailed analysis of all the differences between them. For each change, specify the original text, the updated text, and the location within the documents.
Document A:
The company's annual retreat will be held on June 1st.
All employees are expected to attend the full-day event.
Lunch and refreshments will be provided.
Document B:
The company's annual retreat will be held on June 8th.
Attendance is optional, but employees are encouraged to participate.
Snacks and beverages will be served during breaks.


Assistant: Line 1, Document A: "June 1st" => "June 8th"
Line 2, Document A: "All employees are expected to attend" => "Attendance is optional, but employees are encouraged to participate"
Line 3, Document A: "Lunch and refreshments will be provided" => "Snacks and beverages will be served during breaks"
"""

SHOT_2 = """Human: Compare Document A and Document B, and provide a detailed analysis of all the differences between them. For each change, specify the original text, the updated text, and the location within the documents.
Document A:
I. Project Overview
The new project will commence on July 15th and run for 6 months.
II. Team Structure
The project team will consist of 10 members from various departments.
III. Deliverables
The team will be responsible for delivering a final report and presentation.
Document B:
I. Project Overview
The new project will commence on July 1st and run for 3 months.
II. Team Structure
The project team will consist of 8 members from different departments.
III. Deliverables
The team will be responsible for delivering a final report, presentation, and implementation plan.


Assistant: Section I, Line 1, Document A: "July 15th" => "July 1st"
Section I, Line 1, Document A: "6 months" => "3 months"
Section II, Line 1, Document A: "10 members" => "8 members"
Section III, Line 1, Document B: Added "and implementation plan" clause not present in Document A
"""

SHOT_3 = """Human: Compare Document A and Document B, and provide a detailed analysis of all the differences between them. For each change, specify the original text, the updated text, and the location within the documents.
Document A:
The annual conference will take place on September 15th.
The keynote speaker is Dr. Emily Sinclair.
The event will conclude at 5 pm.
Document B:
The annual conference will take place on September 16th.
The keynote speaker is now Dr. Alex Forrest.
The event will conclude at 6 pm.

Assistant: Line 1, Document A: "September 15th" => "September 16th" Explanation: The conference date was changed from September 15th to September 16th.
Line 2, Document A: "Dr. Emily Sinclair" => "Dr. Alex Forrest" Explanation: The keynote speaker was changed from Dr. Emily Sinclair to Dr. Alex Forrest.
Line 3, Document A: "5 pm" => "6 pm" Explanation: The end time of the event was changed from 5 pm to 6 pm.
"""

SHOT_4 = """Human: Compare Document A and Document B, and provide a detailed analysis of all the differences between them. For each change, specify the original text, the updated text, and the location within the documents.
Document A:
1. Introduction
This report summarizes the quarterly sales performance.
2. Sales Figures
Total revenue for Q2 was $1.5 million.
3. Conclusion
We achieved our targets and expect continued growth.
Document B:
1. Introduction
This report summarizes the quarterly sales performance.
2. Sales Figures
Total revenue for Q2 was $1.5 million.
3. Conclusion
We achieved our targets and expect continued growth.

Assistant: After comparing Document A and Document B, I can confirm that there are no differences between the two documents. They are identical in content and structure:

Both documents have the same three sections: Introduction, Sales Figures, and Conclusion.
The text in each section is exactly the same in both documents.
There are no changes in wording, punctuation, or formatting between Document A and Document B.
In summary, Documents A and B are completely identical, with no variations or modifications present.
"""

SYSTEM_PROMPT = "You are an expert at comparing and identifying provided documents and list out the differences identifying the location, section and the crips change."
PROMPT_TEMPLATE = """
{shot_1} 

{shot_2}

{shot_3}

{shot_4}

Human: Compare Document A and Document B, and provide a detailed analysis of all the differences between them. For each change, specify the original text, the updated text, and the location within the documents.
Document A:
{doc_a}
Document B:
{doc_b}

Assistant:
"""

# File upload settings
ALLOWED_EXTENSIONS = {"pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Storage settings
UPLOAD_FOLDER = "uploads"

# PDF processing settings
MAX_PAGES_TO_DISPLAY = 10

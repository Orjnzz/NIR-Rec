TEMPLATE_1 = """
Candidate Set (candidate movies): {}.
The movies I have watched (watched movies): {}.
Step 1: What features are most important to me when selecting movies (Summarize my preferences briefly)? 
Answer: 
"""

TEMPLATE_2 = """
Candidate Set (candidate movies): {}.
The movies I have watched (watched movies): {}.
Step 1: What features are most important to me when selecting movies (Summarize my preferences briefly)? 
Answer: {}.
Step 2: Selecting the most featured movies from the watched movies according to my preferences (Format: [no. a watched movie.]). 
Answer: 
"""

TEMPLATE_3 = """
Candidate Set (candidate movies): {}.
The movies I have watched (watched movies): {}.
Step 1: What features are most important to me when selecting movies (Summarize my preferences briefly)? 
Answer: {}.
Step 2: Selecting the most featured movies (at most 5 movies) from the watched movies according to my preferences in descending order (Format: [no. a watched movie.]). 
Answer: {}.
Step 3: Can you recommend 10 movies from the Candidate Set similar to the selected movies I've watched (Format: [no. a watched movie - a candidate movie])? 
Answer: 
"""

# Next-Item Recommendation with Zero-Shot Using LLM

The Next-Item Recommendation with Zero-Shot (NIR) method is a prompting strategy designed to guide LLMs in making next-item recommendations without training. It works first using an module to generate candidate items through user-filtering or item-filtering. Then, it applies a three-step prompting process: 
- Capture user's preference prompt.
- Selecte representative items prompt.
- Generate recommendations.
This approach enables LLM to provide effective recommendations without training but high performance.


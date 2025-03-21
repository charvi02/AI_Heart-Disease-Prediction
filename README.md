The project, "Context-Aware Medical Assistant," is an AI-powered tool designed to support doctors in diagnosing diseases using large language models (LLMs). It enhances real-time diagnosis accuracy without replacing traditional doctor check-ups. 
The approach involves:
1. Data Handling: Textbooks used by doctors (e.g., Davidson's, Harrison's) were vectorized using PyPDF2 and ChromaDB. Vector embeddings were generated using nomic-embed-text.
  
2. Model Implementation: Models like Llama 3.1 and BioMistral were deployed using Ollama, integrated into a RAG (Retrieval-Augmented Generation) pipeline using LangChain. Finetuning was performed with Unsloth++.

3. Evaluation: Doctors reviewed model predictions for diagnosis, medication, and severity through a Google Form. Model 3 (finetuned Llama 3.1 with RAG) was preferred for its accuracy.

4. Impact: The assistant aims to reduce diagnosis time, improve healthcare access, and support underserved communities.

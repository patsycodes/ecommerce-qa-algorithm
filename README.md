# ecommerce-qa-algorithm

## The Pivot 

This project originally set out to solve the Human-In-The-Loop Quality Assurance inconvenience in manually verifying e-commerce product data. However, during research, I identified significant constraints in the ability of generic AI sentence transformers to distinguish between contextually similar products (eg. sparkling water vs natural water). Therefore, the project pivoted to become an **E-Commerce Product Matching Recommendation Engine** instead, which is a foundation for high-throughput, human-supervised data validation at scale.

## Internship-Inspired Project

This project was inspired by my internship as a Data Analyst at [Checkafy](https://www.checkafy.com/), a retail-intelligence Hong Kong-based firm. During my time there, I noticed massive operational bottlenecks caused by manual data verification, specifically, confirming whether two highly disparate retailer product titles represented identical items. This project directly addresses that problem by introducing an algorithmic pipeline to surface candidate matches.

## Pipeline

1. **Web Scraping**: Scraping product titles from a major local e-commerce website, HKTVMall 
2. **Data Cleaning**: Extracting product brands, specs, and removing fluff to keep titles concise; mostly automated, but requires human-in-the-loop validation for highly ambiguous naming and missing spec
3. **Candidate Generation (Bi-Encoder Dense Retrieval)**: Pass cleansed titles to a Sentence Transformer model to compute dense vector embeddings and retrieve the nearest neighbour using cosine similarity.
4. **Candidate Re-ranking (Cross-Encoder Optimisation)**: Funnel candidate pairs into a Hugging Face Cross-Encoder. This layer performs deep self-attention across both titles simultaneously to catch subtle context mismatches that Bi-encoders miss.
5. **Human-Supervised Verification Queue**: Route the high-confidence matches directly to the final CSV file (`pairs_ce.csv`) for fast binary human QA review.



## Tech Stack

- **Languages & Core Labs**: Python, Pandas, Jupyter Notebooks
- **Web Scraping**: BeautifulSoup, Playwright
- **Machine Learning & NLP**: Sentence-Transformers, Hugging Face Cross-Encoders





Task: Build NLP pipeline
Pipeline structure:
Name: nlp-pipeline-builder
Domain: data-science
Version: 1
Components:
1. classification
   method: text-classification
   framework: transformers
   sub-tasks:
     - sentiment-analysis
     - topic-labeling
     - intent-detection
2. ner
   method: named-entity-recognition
   framework: spacy
   entity-types:
     - person
     - org
     - location
     - date
     - product
3. summarization
   types:
     extractive:
       method: text-rank
       algorithm: sentence-scoring
     abstractive:
       method: seq2seq
       model: pegasus-or-bart
4. embeddings
   method: sentence-transformers
   store: vector-database
   backends:
     - chromadb
     - faiss
     - qdrant
   embed-models:
     - all-MiniLM-L6-v2
     - all-mpnet-base-v2
     - instructor-large
5. semantic-search
   method: vector-search
   steps:
     - encode-query
     - cosine-similarity
     - top-k-retrieval
Execution order: ingest -> preprocess -> classify-or-ner -> embed -> index -> search
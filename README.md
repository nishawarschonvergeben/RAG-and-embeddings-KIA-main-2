# ai-applications: RAG-based Literary QA System for Pride and Prejudice

# Project Description

This project assists literary enthusiasts and researchers in finding contextual answers about Jane Austen’s *Pride and Prejudice* using a Retrieval-Augmented Generation (RAG) pipeline. The system embeds text passages, retrieves relevant chunks for a user query, and generates precise answers using a language model.

# 🎯 Use Case
Ziel ist es, Leser:innen des Romans zu ermöglichen, in natürlicher Sprache Fragen zur Handlung, zu Charakteren und zur Thematik zu stellen.  

Ich wollte einen Bookish-RAG bauen für mein eigenes zukünfitiges Buch. Also ich feede ein Buch von mir und dann kann man am Schluss so (Fragen) stellen, wie "Wann trafen sich Character A und Charakter B das erste mal?" oder "Wie entwickelt sich ihre Liebesgeschichte?"

Weil immer wenn Band 2 raus kommt, ist es schon eine Weile her seit man Band 1 gelesen hat und man hat sicher vieles vergessen und daher will ich wie so eine Stütze für Leser anbieten. Und weil mein Buch ja noch nicht fertig ist, hätte ich einfach von Projekt Gutenberg aus irgend ein Buch als plain text genommen. z.B. Pride and Prejudice. 

## Name & URL

| Name                          | URL |
|-------------------------------|-----|
| Huggingface Space (optional)  | https://huggingface.co/spaces/nishawarschonvergeben/prideandprejudice  --> es braucht einfach meeega lange (knapp. 100-230 sekunden für die generierung von Antworten) |
| Embedding Model Page          |"sentence-transformers/all-mpnet-base-v2"
| Code Repository               | https://github.com/nishawarschonvergeben/pride_and_prejudice_RAG |

## Data Sources

| Data Source               | Description                             |
|---------------------------|-----------------------------------------|
| [Project Gutenberg Text](https://www.gutenberg.org/ebooks/1342) | Full text of Jane Austen's *Pride and Prejudice* |
| Cleaned Plaintext         | Chapter markers kept, `[Illustration]` and `[COPYRIGHT]` tags removed |

Verwendet wurde der vollständige Roman *Pride and Prejudice* (englische Originalfassung) aus [Project Gutenberg].
Der Text wurde als `.txt` verarbeitet und in semantisch sinnvolle Chunks (Textabschnitte) zerlegt.


# RAG Improvements

| Improvement         | Description |
|---------------------|-------------|
| Query Rewriting     | Vague user questions rewritten into precise literary queries using LLaMA3 - entfernt, da es meistens bei Die Frage ein globales Thema behandelt.. performt eher schlecht |
| Query Expansion     | Added relevant entities or context to improve retrieval (e.g., meryton ball) --> Could be done better, by someone who's a professional and also someone who knows everything about P&P |
| UMAP Visualization  | Semantically visualized query and results to assess cluster relevance |
| Retrieval Debugging | Used distance metrics and outlier analysis to improve chunk coverage |
| Prompt Optimization | Clean structured prompts built dynamically with retrieved chunks |
| Cosine Similarity |Used cosine similarity for re-ranking FAISS retrieval results, improving semantic match over default L2 distance|

# Chunking

### Data Chunking Method

| Type of Chunking                 | Configuration                                  |
|----------------------------------|------------------------------------------------|
| RecursiveCharacterTextSplitter  | 1000 characters, 200 overlap und  separators=["\n\n", "\n", ".", "!", "?", ";", ":"]|
| SentenceTransformersTokenSplitter | 256 tokens per chunk, 40 overlap, `all-mpnet-base-v2` |
| Comparison/Notes                       | Token-based split created more semantically meaningful boundaries for embedding. I also tried different models and stuck with all-mpnet-base-v2. |


## Choice of LLM

| Name           | Link |
|----------------|------|
| llama3-70b-8192  | [Groq API](https://groq.com) |

---
# Test Method

To evaluate the performance of my RAG system, I manually selected **5 questions** targeting key events and character dynamics from *Pride and Prejudice* to find out the following:

- Emotionally complex situations (e.g. Elizabeth's reactions after Darcy's proposal)
- Scenes with potentially multiple proposals, timeline confusions.
- Unanswerable questions where hallucinations might occur (e.g. last question)

For each question, I generated model answers using **five different query expansion methods**:

1. **Baseline** (original question without modification, just cosine similarity and the prompted llm expansion)
2. **Rewrite 1** (semantically rewritten query)
3. **Rewrite 2** (alternative semantic rewrite, often more cautious)
4. **Manual (Simple) Expansion** (handcrafted ideal expansion by MEEEE (not an expert))
5. **LLM Expansion** (automatic query rewriting via LLM)

## Evaluation Approach

For this evaluation, I manually assessed each model output across several qualitative dimensions to better capture not only correctness but also how well the models handled nuance and uncertainty:

- **Accuracy** — Whether the answer correctly reflects the actual content of *Pride and Prejudice*.
- **Depth** — Whether the answer goes beyond surface-level responses, providing emotional, narrative or character nuance.
- **Hallucination** — Whether the model introduced information not supported by the book or invented non-existing details.
- **Handling of unanswerable questions** — Whether the model correctly refused to answer when no relevant information was provided in the retrieved context.

In future, I would also like to evaluate **Context Fit**, by directly linking answers to the actually retrieved chunks.

The entire evaluation was done manually by cross-checking every response against the original book content, with the help of ChatGPT.

---

## Final Results
- **Accuracy**: Correct answers / 5 total questions.
- **Precision**: How often the model stays fully correct when it decides to answer.
- **Recall**: Ability to answer as many questions correctly as possible.

| Model/Method | Accuracy | Depth | Hallucination | Comments |
|---------------|----------|-------|----------------|----------|
| **Baseline** | 2/5 (40%) | Low to Medium | 2 Hallucinations | Occasionally correct when answerable, but sometimes invented content (e.g. Miss King appearing at second ball). Struggled with unanswerable contexts. |
| **Rewrite 1** | 3/5 (60%) | Medium to High | No hallucinations | Generally solid; capable of providing nuanced emotional states. Correctly refused to answer when context was missing. Minor time-shift mistakes occurred. |
| **Rewrite 2** | 2/5 (40%) | Low to Medium | No hallucinations | Very conservative; frequently refused to answer, even when enough context was available. |
| **Manual Expansion** | 4/5 (80%) | High | No hallucinations | Gold standard performance. Consistently correct, book-faithful, and best aligned with the ground truth. Correctly handled missing contexts. |
| **LLM Expansion** | 3/5 (60%) | High | 2 Hallucinations | In most cases delivered excellent, nuanced answers. However, in certain unanswerable questions, hallucinations appeared (again Miss King). Sometimes refused when context was actually sufficient. |

---

## Quick Takeaways

- **Manual Expansion** still remains the cleanest and most stable reference system.
- **Rewrite 1** performs surprisingly well for semantic rewrites, but sometimes struggled with timeline positioning.
- **LLM Expansion** showed very promising depth and language richness, but hallucination risks rise especially when retrieval returns weaker chunks.
- Both **Baseline** and **Rewrite 2** underperformed: Baseline due to occasional hallucinations, Rewrite 2 due to being overly cautious and frequently refusing answers unnecessarily.


Alte Tests unter Appendix.txt auffindbar. 

# References

- Austen, Jane. *Pride and Prejudice*. Project Gutenberg.
- Groq LLaMA3 Models: https://groq.com

=======

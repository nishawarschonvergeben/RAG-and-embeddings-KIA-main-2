# ai-application-rag-literature

# Project Description

This project assists literary enthusiasts and researchers in finding contextual answers about Jane Austen’s *Pride and Prejudice* using a Retrieval-Augmented Generation (RAG) pipeline. The system embeds text passages, retrieves relevant chunks for a user query, and generates precise answers using a language model.

# 🎯 Use Case

Ziel ist es, Leser:innen des Romans zu ermöglichen, in natürlicher Sprache Fragen zur Handlung, zu Charakteren und zur Thematik zu stellen.  
Das System beantwortet diese Fragen mithilfe eines Retrieval-Moduls und eines Large Language Models (LLM).
Ich wollte einen Buch Rag bauen. Also ich feede ihm ein Buch und dann kann man am schluss so querries (Fragen) stellen, wie "Wann trafen sich Character A und Charakter B das erste mal?" oder "Wie entwicklet sich ihre Liebesgeschichte?" Ich will das eben machen, da ich das später dann bei meinem Buch auch machen kann. Weil immer wenn Band 2 raus kommt, ist es schon eine Weile her seit man Band 1 gelesen hat und man hat sicher vieles vergessen und daher will ich wie so eine Stütze für Leser anbieten. Und weil mein Buch ja noch nicht fertig ist, hätte ich einfach von Projekt Gutenberg aus irgend ein Buch als plain text genommen. z.B. Pride and Prejudice. 

## Name & URL

| Name                          | URL |
|-------------------------------|-----|
| Huggingface Space (optional)  | _[not deployed]_ |
| Embedding Model Page          | Zuerst: [MiniLM Huggingface](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) Danach: "sentence-transformers/all-mpnet-base-v2"
|
| Code Repository               | _[your GitHub link here]_ |

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
| Query Rewriting     | Vague user questions rewritten into precise literary queries using LLaMA3 - entfernt, da es meistens bei Die Frage ein globales Thema behandelt.. performt eher schlecht bei Was passiert beim ersten Ball?  |
| Query Expansion     | Added relevant entities or context to improve retrieval (e.g., meryton ball)  |
| UMAP Visualization  | Semantically visualized query and results to assess cluster relevance |
| Retrieval Debugging | Used distance metrics and outlier analysis to improve chunk coverage |
| Prompt Optimization | Clean structured prompts built dynamically with retrieved chunks |
| Cosine Similarity | Text noch hinzufügen!!!! |

# Chunking

### Data Chunking Method

| Type of Chunking                 | Configuration                                  |
|----------------------------------|------------------------------------------------|
| RecursiveCharacterTextSplitter  | 1000 characters, 200 overlap                   |
| SentenceTransformersTokenSplitter | 128 tokens per chunk, 20 overlap, `MiniLM-L12` |
| Comparison/Notes                       | Token-based split created more semantically meaningful boundaries for embedding.  Ich habe das benutzt und wurde dann des besseren belehrt, da es meine Texte zb jedesmal bei einem Chapter geschnitten hat und so vermehrt zu kurze Chunks entstanden sind. |

Dann verbessert? (hopefully)
| Type of Chunking                 | Configuration                                  |
|----------------------------------|------------------------------------------------|
| RecursiveCharacterTextSplitter  | 1000 characters, 200 overlap und  separators=["\n\n", "\n", ".", "!", "?", ";", ":"]|
| SentenceTransformersTokenSplitter | 256 tokens per chunk, 40 overlap, `all-mpnet-base-v2` |
| Comparison/Notes                       | Token-based split created more semantically meaningful boundaries for embedding.  Ich habe das benutzt und wurde dann des besseren belehrt, da es meine Texte zb jedesmal bei einem Chapter geschnitten hat und so vermehrt zu kurze Chunks entstanden sind. |


## Choice of LLM

| Name           | Link |
|----------------|------|
| LLaMA3 8B / 70B | [Groq API](https://groq.com) |
|llama3-70b-8192 | " // Weil ich bemerkt habe, dass meine Resultate zum Teil noch nicht so gut waren |

Used both small (8B) and large (70B) variants to compare quality and performance of completions.

# Test Method

I manually selected 10 diverse literary questions and evaluated:

- **Relevance of Retrieved Chunks** (based on semantic match to the question)
- **Correctness of Generated Answers** (literary accuracy)
- **Faithfulness to the original book**

## Evaluations 
---
## Bewertungs­kriterien  

| Kürzel        | Bedeutung                                                                 |
|---------------|---------------------------------------------------------------------------|
| **context_fit** | Passt die Antwort zur Szene bzw. zum Zeitpunkt der Frage? (1 – 5)        |
| **depth**       | Liefert sie mehr als eine bloße Ja/Nein-Aussage? (1 – 5)                 |
| **accuracy**    | Faktische Richtigkeit gemessen am Romantext (1 – 5)                      |
| **halluc.**     | „Ja“, wenn wesentliche Erfindung oder grober Szenen-/Zitate-Fehler vorliegt |
---

## Aggregierte Kennzahlen

| Variante      | Ø Depth | **accurate (≥ 4)** | Hallucinations |
|---------------|---------|--------------------|----------------|
| **Baseline**  | 2.5     | 22 / 48 ≈ 46 %     | 3              |
| **Rewrite 1** | **3.1** | **25 / 48 ≈ 52 %** | 4              |
| Rewrite 2     | 2.6     | 18 / 48 ≈ 38 %     | **6**          |

---

## Ranking & Empfehlung

| Rang | Variante       | Begründung                                                                                 |
|------|----------------|--------------------------------------------------------------------------------------------|
| **①** | **Rewrite 1** | Höchste Genauigkeit (52 %) **und** beste inhaltliche Tiefe. Halluzinationen moderat.       |
| ②    | Baseline       | Solide & halluziniert selten, aber oberflächlicher und geringere Trefferquote.             |
| ③    | Rewrite 2      | Niedrigste Accuracy, deutlich mehr Halluzinationen; nur bedingt nutzbar.                   |

**Fazit:**  
Für das RAG-System liefert **Rewrite 1** derzeit das beste Kosten-Nutzen-Verhältnis.  
Empfehlung: als Standard nutzen, aber mit zusätzlichem Halluzinations-Filter.  
Die Baseline bleibt als verlässlicher Fallback; Rewrite 2 sollte vor Produktionseinsatz stärker gereinigt werden.
--
Update: Nach dem Ausprobieren wieder einfach erkannt, dass die rewritten querries zum Teil sehr stark halluzinieren. Deshalb habe ich diese wieder entfernt - und dann feststellen müssen, dass jetzt mein RAG sehr vieles nicht mehr findet. Da nicht die relevanten Chunks angezeigt werden ... da das system halt nicht die semantische Wichitgkeit von gewissen Chunks erkennt. *sad*

Es ist mir auch aufgefallen, dass es teils bei einem zweit/dritt "Submit" teils die richtigen Antworten wiedergibt.
Und es ist mir auch aufgefallen, dass wenn es keinen guten Chunk gibt, dass das LLM selber antwortet. RAG sollte aber nur antworten, wenn relevante kontextuelle Belege vorhanden sind. --> Daher den prompt an LLM ein wenig strenger gemacht. 

löst mein problem aber immernoch nicht, dass es bei meryton Ball mir eine andere antwort gibt, wie bei Meryton Assembly


# References

- Austen, Jane. *Pride and Prejudice*. Project Gutenberg.
- Hugging Face: [MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
- Groq LLaMA3 Models: https://groq.com


---


# alte Testings -- irrelevant für Bewertung aber für mich persönlich :D 

## Evaluation 1
| OriginalFrage                                                     | rewritten frage                                                                                                 | Antwort   | context_fit | depth | accuracy | hallucination | final comment                                      |
|-------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|-----------|-------------|-------|----------|----------------|---------------------------------------------------|
| How does Elisabeth feel about Darcy?                              | What are Elisabeth Bennet's evolving emotions and perceptions towards Mr. Darcy?                                | rewrite1  | 5           | 5     | 5        | False          | Clear, insightful, and emotionally layered.        |
| How does Elisabeth feel about Darcy?                              | How do Elizabeth's feelings toward Darcy develop from initial dislike to eventual acceptance and understanding? | rewrite2  | 2           | 4     | 3        | True           | Romanticized and goes beyond given context.        |
| How does Elisabeth feel about Darcy?                              | How does Elisabeth feel about Darcy?                                                                            | baseline  | 4           | 3     | 4        | False          | Solid inference, though emotionally neutral.       |
| Who does Lizzy end up with?                                       | Who does Elizabeth Bennet marry in Jane Austen's Pride and Prejudice?                                           | rewrite1  | 5           | 4     | 5        | False          | Precise and concise.                               |
| Who does Lizzy end up with?                                       | What is the ultimate romantic pairing of Elizabeth Bennet by the novel's conclusion?                            | rewrite2  | 3           | 3     | 4        | True           | Too reliant on outside knowledge.                  |
| Who does Lizzy end up with?                                       | Who does Lizzy end up with?                                                                                      | baseline  | 5           | 4     | 5        | False          | Accurate and warmly phrased.                       |
| how does Lizzy feel about Darcy?                                  | What are Elizabeth Bennet's evolving emotions and perceptions of Mr. Darcy?                                     | rewrite1  | 5           | 5     | 5        | False          | Deep and well-balanced emotional arc.              |
| how does Lizzy feel about Darcy?                                  | How do Elizabeth Bennet's feelings toward Mr. Darcy change throughout the story?                                | rewrite2  | 3           | 4     | 4        | False          | Touches complexity but oversimplifies her motives. |
| how does Lizzy feel about Darcy?                                  | how does Lizzy feel about Darcy?                                                                                | baseline  | 4           | 2     | 4        | False          | Accurate, but emotionally one-sided.               |
| How does Darcy feel about Elisabeth?                              | What are Mr. Darcy's changing attitudes towards Elizabeth?                                                      | rewrite1  | 5           | 5     | 5        | False          | Rich and emotionally intelligent.                  |
| How does Darcy feel about Elisabeth?                              | How do Darcy's feelings toward Elizabeth Bennet change from disapproval to admiration and romantic interest?    | rewrite2  | 4           | 4     | 4        | False          | Accurate, but overlaps with Elizabeth's viewpoint. |
| How does Darcy feel about Elisabeth?                              | How does Darcy feel about Elisabeth?                                                                            | baseline  | 4           | 3     | 4        | False          | Good contextual reading of subtle affection.       |
| Why is Mr. Collins proposing to Elizabeth?                        | What motivates Mr. Collins' marriage proposal to Elizabeth Bennet?                                              | rewrite1  | 5           | 4     | 5        | False          | Balanced and plausible interpretation.             |
| Why is Mr. Collins proposing to Elizabeth?                        | What motivates Mr. Collins' proposal to Elizabeth... influenced by Lady Catherine                               | rewrite2  | 4           | 4     | 4        | False          | Overexplains motives slightly.                     |
| Why is Mr. Collins proposing to Elizabeth?                        | Why is Mr. Collins proposing to Elizabeth?                                                                      | baseline  | 5           | 3     | 5        | False          | Correctly contextualized.                          |
| Who does Elizabeth marry at the end of the novel?                 | Who does Elizabeth Bennet marry at the end of Jane Austen's Pride and Prejudice?                                | rewrite1  | 5           | 3     | 5        | False          | Clean and elegant.                                 |
| Who does Elizabeth marry at the end of the novel?                 | Who does Elizabeth Bennet ultimately marry by the novel's conclusion?                                           | rewrite2  | 5           | 4     | 5        | False          | Adds helpful clarification.                        |
| Who does Elizabeth marry at the end of the novel?                 | Who does Elizabeth marry at the end of the novel?                                                               | baseline  | 5           | 3     | 5        | False          | Simple and factual.                                |
| What is Elisabeth's first impression on Mr. Darcy?                | What is Elizabeth Bennet's opinion of Mr. Darcy at the Meryton ball?                                            | rewrite1  | 5           | 4     | 5        | False          | Direct quote enhances credibility.                 |
| What is Elisabeth's first impression on Mr. Darcy?                | How does Elizabeth's opinion of Mr. Darcy form at the Meryton ball...                                           | rewrite2  | 2           | 2     | 3        | True           | Confuses Darcy’s view with Elizabeth’s.            |
| What is Elisabeth's first impression on Mr. Darcy?                | What is Elisabeth's first impression on Mr. Darcy?                                                              | baseline  | 5           | 3     | 5        | False          | Well summarized with correct tone.                 |
| What character appears for the first time during the second ball? | Which character is introduced during the second ball in Pride and Prejudice?                                    | rewrite1  | 2           | 2     | 2        | True           | Introduces a wrong character.                      |
| What character appears for the first time during the second ball? | Which character is introduced during the Netherfield ball...?                                                   | rewrite2  | 1           | 2     | 1        | True           | Incorrect character and scene.                     |
| What character appears for the first time during the second ball? | What character appears for the first time during the second ball?                                               | baseline  | 5           | 2     | 5        | False          | Correct factual identification.                    |


I also visualized UMAP projections of query, dataset and retrieved results to identify outliers.


## Results

| Model/Method                                    | Accuracy                                 | 
|-------------------------------------------------|-------------------------------------------|
| Retrieved Chunks (FAISS + TokenSplitter)        | Qualitatively good in 18/24 cases          | 
| Generated Answer (Baseline)                     | **100 % faithful to book context** (8/8)   | 
| Generated Answer (Rewrite1)                     | **~88 % faithful** (7/8 accurate)          |
| Generated Answer (Rewrite2)                     | **~38 % faithful** (3/8 accurate)          | 


## Known Issues

- Some rewritten queries led to token overflows or hallucinations (e.g., references to wrong literary works).
- No automated reranking implemented – might improve relevance further.
- Das rewriting der Querries hat beim (2) dafür gesorgt, dass es halt global sucht - und nicht für chunk-based antworten optimal ist. Wie entwickelt sich Elizabeths Meinung über Darcy?“ ist global, dein RAG-System arbeitet aber meist lokal (chunk-basiert).
- Trotz Overlap kann Kontextverlust auftreten, wenn Titel, Kapitelgrenzen oder Szenenwechsel nicht explizit erkennbar sind – insbesondere bei literarischen Texten wie Pride and Prejudice ohne klare Markierungen.

## Evaluation 2 

manuelle Stichproben-Evaluation von 16 Fragen × 3 Antwort-Varianten (Baseline, Rewrite 1, Rewrite 2).
Hier wurden nebst einigen Fragen von Evaluation1 noch weitere detailiertere Fragen mit lautere Keywords (annahme, dass details besser für RAGS sind) gestellt wurden

---

## Bewertungs­kriterien  

| Kürzel        | Bedeutung                                                                 |
|---------------|---------------------------------------------------------------------------|
| **context_fit** | Passt die Antwort zur Szene bzw. zum Zeitpunkt der Frage? (1 – 5)        |
| **depth**       | Liefert sie mehr als eine bloße Ja/Nein-Aussage? (1 – 5)                 |
| **accuracy**    | Faktische Richtigkeit gemessen am Romantext (1 – 5)                      |
| **halluc.**     | „Ja“, wenn wesentliche Erfindung oder grober Szenen-/Zitate-Fehler vorliegt |


---

## Einzel­bewertung  
*(für jede Frage erscheinen die neu formulierten Queries von **rewrite 1** und **rewrite 2**; bei der Baseline steht „–“, weil sie die Original-Frage nutzt)*

| # | Original Frage (Baseline) | Variante | verwendete Query (nur Rewrite) | context_fit | depth | accuracy | halluc. | Kurz-Kommentar |
|---|---------------------------|----------|--------------------------------|-------------|-------|----------|----------|----------------|
| 1 | how does Lizzy feel about Darcy? | baseline | – | 4 | 2 | 3 | – | einseitig, Szene vertauscht |
|   |                               | rewrite 1 | *What are Elizabeth Bennet's evolving opinions and emotions regarding Mr. Darcy throughout Pride and Prejudice?* | 5 | 4 | 4 | – | gute Entwicklungskurve |
|   |                               | rewrite 2 | *How do Elizabeth Bennet's feelings toward Mr. Darcy change throughout the story?* | 5 | 3 | 4 | – | fast wie r1 |
| 2 | What does Elizabeth say in response to Darcy’s first proposal? | baseline | – | 1 | 1 | 1 | – | „Kontext fehlt“ |
|   |                               | rewrite 1 | *What is Elizabeth Bennet's reaction to Mr. Darcy's initial marriage proposal in Pride and Prejudice?* | 3 | 2 | 1 | **Ja** | erfundenes Zitat |
|   |                               | rewrite 2 | *What is the tone and content of Elizabeth's rejection of Darcy's initial marriage proposal … ?* | 2 | 1 | 1 | – | keine Antwort |
| 3 | Why is Mr. Collins proposing to Elizabeth? | baseline | – | 4 | 2 | 3 | – | richtige Szene fehlt |
|   |                               | rewrite 1 | *What motivates Mr. Collins' marriage proposal to Elizabeth Bennet in Pride and Prejudice?* | 5 | 3 | 4 | – | Motivation korrekt |
|   |                               | rewrite 2 | *What motivates Mr. Collins to propose to Elizabeth, given … ?* | 3 | 2 | 2 | – | Szene verwechselt |
| 4 | Who does Elizabeth marry at the end of the novel? | baseline | – | 5 | 1-2 | 5 | – | trivial ✓ |
|   |                               | rewrite 1 | *Who does Elizabeth Bennet choose to marry, Mr. Darcy or Mr. Wickham … ?* | 5 | 1-2 | 5 | – | – |
|   |                               | rewrite 2 | *What is the outcome of Elizabeth's romantic relationships … ?* | 5 | 1-2 | 5 | – | – |
| 5 | What is Elisabeth's first impression on Mr. Darcy? | baseline | – | 4 | 2 | 4 | – | korrekt |
|   |                               | rewrite 1 | *What is Elizabeth Bennet's first impression of Mr. Darcy at the Meryton ball?* | 3 | 1 | 3 | – | „steht hier nicht“ |
|   |                               | rewrite 2 | *How does Elizabeth's opinion of Mr. Darcy form at the Netherfield ball … ?* | 2 | 2 | 2 | Teilw. | Perspektive vertauscht |
| 6 | What character appears for the first time during the second ball? | baseline | – | 3 | 1 | 2 | Teilw. | Captain Carter falsch |
|   |                               | rewrite 1 | *Which character is introduced at the second ball in Pride and Prejudice?* | 3 | 1 | 2 | Teilw. | Mrs Hurst längst da |
|   |                               | rewrite 2 | *Which character is introduced during the Netherfield ball … ?* | 4 | 1 | 3 | – | Wickham richtige Figur, Ball falsch |
| 7 | What are Elizabeth Bennet’s feelings toward Mr. Darcy after his first proposal at Hunsford? | baseline | – | 3 | 2 | 2 | **Ja** | „very disagreeable“ & Liebe |
|   |                               | rewrite 1 | *What are Elizabeth Bennet's emotions … immediately following his rejected marriage proposal … ?* | 5 | 4 | 5 | – | nuanciert & korrekt |
|   |                               | rewrite 2 | *How does Elizabeth Bennet's perception of Mr. Darcy evolve … ?* | 4 | 3 | 4 | – | solide |
| 8 | How does Elizabeth respond verbally and emotionally to Darcy’s first proposal at Hunsford? | baseline | – | 5 | 4 | 5 | – | klar, komplett |
|   |                               | rewrite 1 | *What is Elizabeth's emotional response to Darcy's first marriage proposal at Hunsford … ?* | 4 | 3 | 4 | – | etwas kürzer |
|   |                               | rewrite 2 | *What is Elizabeth's immediate verbal and emotional reaction to Darcy's marriage proposal … ?* | 4 | 3 | 4 | – | ähnlich r1 |
| 9 | What motivates Mr. Collins to propose marriage to Elizabeth Bennet, according to his own reasoning? | baseline | – | 5 | 3 | 4 | – | Entail korrekt |
|   |                               | rewrite 1 | *What motivates Mr. Collins' proposal to Elizabeth Bennet, considering his patroness Lady Catherine … ?* | 4 | 3 | 3 | Teilw. | Fokus zu stark auf Lady C. |
|   |                               | rewrite 2 | *What are Mr. Collins' self-proclaimed reasons for wanting to marry Elizabeth Bennet … ?* | 4 | 3 | 4 | – | ähnlich baseline |
|10 | Whom does Elizabeth Bennet marry … and how is this decision reached? | baseline | – | 5 | 4 | 4 | – | langer Text, kleiner Fehler |
|   |                               | rewrite 1 | *What is the nature of Elizabeth Bennet's marriage to Mr. Darcy … ?* | 5 | 4 | 5 | – | rundes Narrativ |
|   |                               | rewrite 2 | *How does Elizabeth Bennet's perception of Mr. Darcy's proposal evolve … ?* | 4 | 3 | 4 | – | kürzer, korrekt |
|11 | How does Elizabeth Bennet perceive Mr. Darcy after meeting him … Meryton assembly? | baseline | – | 4 | 2 | 3 | – | „vier Tage“ → falscher Ort |
|   |                               | rewrite 1 | *(keine Umformulierung – Query blieb gleich)* | 5 | 3 | 5 | – | Zitat + Erklärung |
|   |                               | rewrite 2 | *What is Elizabeth Bennet's initial opinion of Mr. Darcy at the Meryton assembly … ?* | 5 | 3 | 5 | – | gleich gut |
|12 | Which character is introduced … at the Netherfield ball? | baseline | – | 2 | 1 | 2 | Teilw. | Bingley längst bekannt |
|   |                               | rewrite 1 | *Who is introduced at the Netherfield ball … ?* | 3 | 1 | 3 | – | „keine neue Figur“ korrekt |
|   |                               | rewrite 2 | *How does George Wickham's introduction at the Netherfield ball affect … ?* | 4 | 2 | 3 | Teilw. | Wickham Figur ok, Ball falsch |
|13 | What are Elizabeth Bennet’s thoughts about Mr. Darcy after reading his letter at Rosings Park? | baseline | – | 4 | 4 | 4 | – | differenziert |
|   |                               | rewrite 1 | *What is Elizabeth Bennet's revised opinion of Mr. Darcy's character after reading his explanatory letter … ?* | 5 | 4 | 5 | – | beste Variante |
|   |                               | rewrite 2 | *How does Elizabeth Bennet's opinion of Mr. Darcy change … after reading his letter … ?* | 5 | 4 | 5 | – | gleichwertig |
|14 | How does Lady Catherine de Bourgh confront Elizabeth about the rumored engagement? | baseline | – | 4 | 3 | 4 | Teilw. | Ort vertauscht |
|   |                               | rewrite 1 | *In Chapter 34 … what accusations does Lady Catherine de Bourgh make … ?* | 5 | 2 | 3 | Teilw. | Kapitel falsch |
|   |                               | rewrite 2 | *How does Lady Catherine's confrontation … reflect her snobbery … ?* | 3 | 2 | 3 | – | recht vage |
|15 | Why is Lydia Bennet’s marriage to Mr. Wickham considered scandalous? | baseline | – | 5 | 3 | 4 | – | umfassend |
|   |                               | rewrite 1 | *What social conventions does Lydia Bennet's elopement with George Wickham violate … ?* | 4 | 2 | 3 | Teilw. | nur Benehmen |
|   |                               | rewrite 2 | *How does the Bennet family and societal opinion of Lydia's elopement with Wickham reflect … ?* | 4 | 2 | 3 | – | Fokus auf Wickham |
|16 | What event marks a major turning point in the relationship … ? | baseline | – | 5 | 3 | 4 | – | erster Antrag |
|   |                               | rewrite 1 | *What is the significance of Darcy's first proposal to Elizabeth … ?* | 4 | 3 | 4 | – | Lydia-Episode vertretbar |
|   |                               | rewrite 2 | *How does the rejection of Mr. Darcy's first marriage proposal influence … ?* | 5 | 4 | 5 | – | Brief – oft zitiert |

---

## Aggregierte Kennzahlen

| Variante      | Ø Depth | **accurate (≥ 4)** | Hallucinations |
|---------------|---------|--------------------|----------------|
| **Baseline**  | 2.5     | 22 / 48 ≈ 46 %     | 3              |
| **Rewrite 1** | **3.1** | **25 / 48 ≈ 52 %** | 4              |
| Rewrite 2     | 2.6     | 18 / 48 ≈ 38 %     | **6**          |

---

## Ranking & Empfehlung

| Rang | Variante       | Begründung                                                                                 |
|------|----------------|--------------------------------------------------------------------------------------------|
| **①** | **Rewrite 1** | Höchste Genauigkeit (52 %) **und** beste inhaltliche Tiefe. Halluzinationen moderat.       |
| ②    | Baseline       | Solide & halluziniert selten, aber oberflächlicher und geringere Trefferquote.             |
| ③    | Rewrite 2      | Niedrigste Accuracy, deutlich mehr Halluzinationen; nur bedingt nutzbar.                   |

**Fazit:**  
Für das RAG-System liefert **Rewrite 1** derzeit das beste Kosten-Nutzen-Verhältnis.  
Empfehlung: als Standard nutzen, aber mit zusätzlichem Halluzinations-Filter.  
Die Baseline bleibt als verlässlicher Fallback; Rewrite 2 sollte vor Produktionseinsatz stärker gereinigt werden.
--
Update: Nach dem Ausprobieren wieder einfach erkannt, dass die rewritten querries zum Teil sehr stark halluzinieren. Deshalb habe ich diese wieder entfernt - und dann feststellen müssen, dass jetzt mein RAG sehr vieles nicht mehr findet. Da nicht die relevanten Chunks angezeigt werden ... da das system halt nicht die semantische Wichitgkeit von gewissen Chunks erkennt. *sad*

Es ist mir auch aufgefallen, dass es teils bei einem zweit/dritt "Submit" teils die richtigen Antworten wiedergibt.
Und es ist mir auch aufgefallen, dass wenn es keinen guten Chunk gibt, dass das LLM selber antwortet. RAG sollte aber nur antworten, wenn relevante kontextuelle Belege vorhanden sind. --> Daher den prompt an LLM ein wenig strenger gemacht. 

löst mein problem aber immernoch nicht, dass es bei meryton Ball mir eine andere antwort gibt, wie bei Meryton Assembly

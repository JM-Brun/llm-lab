# File de réconciliation des métadonnées des sources

**Instantané du registre :** `data/sources.yml` au commit `0eb4dc9de3f0a3315631fd4fd1043e018814285d` (branche `main`, 2026-11-19).  
**Périmètre :** 139 entrées du registre. Ce document est un inventaire de travail, pas une validation des licences ni une bibliographie corrigée.

## Résultat du comptage

| Dimension | Valeur | Règle de comptage |
|---|---:|---|
| Entrées du registre | 139 | Enregistrements `sources[]` |
| Dates de publication inconnues | 44 | `publication_date` absent, vide ou `null` |
| Statuts de licence inconnus / incomplets | 127 | `licence.status` égal à `unknown`, ou statut absent/non interprétable |
| Autres statuts de licence | 12 | Statuts explicitement différents de `unknown` |

**Attention au périmètre des droits :** une licence attachée à un article, un dépôt, une page de documentation, un jeu de données ou une figure ne s'étend pas automatiquement aux autres composants. Une URL publique, un dépôt accessible ou une licence déclarée dans un document ne prouvent pas les droits sur les éléments tiers. Les statuts `verified`, `declared` et `known` ne sont pas fusionnés dans ce comptage.

## Protocole de réconciliation

1. Identifier l'objet exact auquel le statut de licence s'applique : texte, code, figures, données, modèle, dépôt ou ensemble de ressources.
2. Chercher d'abord une déclaration primaire : fichier LICENSE/COPYING du dépôt, page officielle de licence de l'éditeur, métadonnées du DOI/éditeur ou déclaration explicite de l'auteur.
3. Conserver l'URL précise, l'identifiant de licence et le périmètre vérifié. Distinguer licence déclarée par le fournisseur et vérification juridique indépendante.
4. Si la source est sous licence multiple, ambiguë, ou inclut des éléments tiers, conserver le statut inconnu pour les éléments non établis.
5. Ne pas remplacer `unknown` par une supposition fondée sur la plateforme, le type de contenu ou l'accessibilité.
6. Pour les dates, privilégier la date de publication de la version citée (éditeur/proceedings/DOI), puis l'historique de versions arXiv ou la page officielle. Ne pas substituer une date de mise à jour, d'accès, de dépôt ou de vidéo à la date de publication sans la qualifier.

## File A — statuts de licence inconnus ou incomplets (127)

- `nishanthan-k-qkv-transformers-devto` — How Query, Key, and Value (QKV) Work in Transformers (DEV Community) — [source](https://dev.to/nishanthan-k/how-query-key-and-value-qkv-work-in-transformers-199a)
- `neha-kk-understanding-qkv-medium` — Understanding Queries, Keys and Values in Transformers (Medium) — [source](https://medium.com/@nkk18072004/understanding-queries-keys-and-values-in-transformers-149ed07c9f8b)
- `huggingface-transformers-kv-cache-explanation` — Caching (Hugging Face Transformers) — [source](https://huggingface.co/docs/transformers/main/en/cache_explanation)
- `andrej-karpathy-gpt-tokenizer-video` — Let's build the GPT Tokenizer (YouTube) — [source](https://www.youtube.com/watch?v=zduSFxRajkE)
- `sebastian-raschka-llms-from-scratch-ch02` — Build a Large Language Model (From Scratch), Chapter 2 (Manning / GitHub) — [source](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch02)
- `huggingface-course-tokenizers-chapter6` — Hugging Face LLM Course — Tokenizers (Hugging Face) — [source](https://huggingface.co/docs/course/chapter6/8)
- `philip-gage-byte-pair-compression-1994` — A New Algorithm for Data Compression (C Users Journal) — [source](https://www.derczynski.com/papers/archive/BPE_Gage.pdf)
- `ahia-do-all-languages-cost-the-same-2023` — Do All Languages Cost the Same? (EMNLP 2023 / ACL Anthology) — [source](https://aclanthology.org/2023.emnlp-main.614/)
- `ali-tokenizer-choice-llm-training-2024` — Tokenizer Choice For LLM Training: Negligible or Crucial? (Findings of NAACL 2024 / ACL Anthology) — [source](https://aclanthology.org/2024.findings-naacl.247/)
- `wegmann-tokenization-language-variation-2025` — Tokenization is Sensitive to Language Variation (Findings of ACL 2025 / ACL Anthology) — [source](https://aclanthology.org/2025.findings-acl.572/)
- `arnett-explaining-mitigating-crosslingual-tokenizer-inequities-2025` — Explaining and Mitigating Crosslingual Tokenizer Inequities (NeurIPS 2025) — [source](https://proceedings.neurips.cc/paper_files/paper/2025/hash/5b91cefbfa52340af2f16f249572dc76-Abstract-Conference.html)
- `chiu-toklens-acl-srw-2026` — TokLens: A Multilingual Lens on Tokenizer Quality for LLMs (ACL Anthology — ACL 2026 Student Research Workshop) — [source](https://aclanthology.org/2026.acl-srw.18/)
- `catherine-arnett-tokenizer-fertility` — Dangers of tokenizer recycling (Hugging Face) — [source](https://huggingface.co/blog/catherinearnett/dangers-of-tokenizer-recycling)
- `mikolov-word2vec-2013` — Efficient Estimation of Word Representations in Vector Space (arXiv) — [source](https://arxiv.org/abs/1301.3781)
- `ethayarajh-contextualized-representations-2019` — How Contextual are Contextualized Word Representations? (EMNLP 2019 / ACL Anthology) — [source](https://aclanthology.org/D19-1006/)
- `li-bert-flow-sentence-embeddings-2020` — On the Sentence Embeddings from Pre-trained Language Models (EMNLP 2020 / ACL Anthology) — [source](https://aclanthology.org/2020.emnlp-main.733/)
- `steck-cosine-similarity-embeddings-2024` — Is Cosine-Similarity of Embeddings Really About Similarity? (WWW 2024 Companion / arXiv) — [source](https://arxiv.org/abs/2403.05440)
- `sentence-transformers-similarity-documentation` — Sentence Transformers — Similarity and SentenceTransformer APIs (Sentence Transformers) — [source](https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html)
- `openai-tiktoken-educational-bpe` — tiktoken educational BPE module (OpenAI / GitHub) — [source](https://github.com/openai/tiktoken/blob/main/tiktoken/_educational.py)
- `huggingface-tokenizers-pipeline-docs` — Hugging Face Tokenizers — Pipeline and Components (Hugging Face) — [source](https://huggingface.co/docs/tokenizers/python/latest/pipeline.html)
- `google-sentencepiece-documentation` — SentencePiece — Overview and Normalization (Google) — [source](https://google.github.io/sentencepiece/)
- `huggingface-tokenizer-algorithms-summary` — Hugging Face Transformers — Tokenizer Summary (Hugging Face) — [source](https://huggingface.co/docs/transformers/main/en/tokenizer_summary)
- `sennrich-subword-nmt-2016` — Neural Machine Translation of Rare Words with Subword Units (ACL Anthology) — [source](https://aclanthology.org/P16-1162/)
- `pytorch-embedding-api` — torch.nn.Embedding (PyTorch) — [source](https://docs.pytorch.org/docs/stable/generated/torch.nn.Embedding.html)
- `su-roformer-rope-2021` — RoFormer: Enhanced Transformer with Rotary Position Embedding (arXiv) — [source](https://arxiv.org/abs/2104.09864)
- `sauravp97-hf-bpe-visualizer-article` — Visualizing BPE Tokenizer Encoding (Hugging Face) — [source](https://huggingface.co/blog/SauravP97/bpe-tokenizer-visualize)
- `sauravp97-hf-bpe-visualizer-repository` — hf-tokenizer-visualizer (GitHub) — [source](https://github.com/SauravP97/hf-tokenizer-visualizer)
- `rushang-chauhan-embeddings-bridge-tokens-context` — Embeddings: The Bridge Between Tokens and Context (LinkedIn) — [source](https://www.linkedin.com/pulse/embeddings-bridge-between-tokens-context-rushang-chauhan-oqpzf/)
- `raschka-bpe-from-scratch-2025` — BPE from Scratch (Sebastian Raschka) — [source](https://sebastianraschka.com/blog/2025/bpe-from-scratch.html)
- `philip-mueller-bpe-explainer` — BPE Explainer (Philip Müller) — [source](https://philipmueller.dev/bpe-visualization/)
- `cornell-byte-pair-visualizer` — Interactive Tokenization Visualizer (Cornell University) — [source](https://www.cs.cornell.edu/courses/cs4782/2026sp/demos/bytepair/)
- `bytebytego-how-llms-learn-from-internet-2025` — How LLMs Learn from the Internet (ByteByteGo) — [source](https://blog.bytebytego.com/p/how-llms-learn-from-the-internet)
- `bytebytego-how-llms-see-world-2025` — How LLMs See the World (ByteByteGo) — [source](https://blog.bytebytego.com/p/how-llms-see-the-world)
- `vizuara-tokenization-from-scratch-bpe` — Tokenization from Scratch: Building Byte-Pair Encoding by Hand (Vizuara) — [source](https://pods.vizuara.ai/courses/build-llm/tokenization-from-scratch-building-byte-pair-encoding-by-han)
- `vizuara-llms-from-30000-feet` — LLMs from 30,000 Feet (Vizuara) — [source](https://mu.vizuara.ai/learn/llms-30k)
- `goldman-unpacking-tokenization-2024` — Unpacking Tokenization: Evaluating Text Compression and its Correlation with Model Performance (Findings of ACL 2024 / ACL Anthology) — [source](https://aclanthology.org/2024.findings-acl.134/)
- `schmidt-tokenization-more-than-compression-2024` — Tokenization Is More Than Compression (EMNLP 2024 / ACL Anthology) — [source](https://aclanthology.org/2024.emnlp-main.40/)
- `mike-x-cohen-llm-breakdown-tokenization-2025` — LLM breakdown 1/6: Tokenization (words to integers) (Substack) — [source](https://mikexcohen.substack.com/p/llm-breakdown-16-tokenization-words)
- `rohan-paul-vocabulary-size-tradeoffs-2025` — Balancing Vocabulary Size in Modern LLMs (GPT-4, LLaMA, Mistral) (Rohan Paul) — [source](https://www.rohan-paul.com/p/tutorial-balancing-vocabulary-size)
- `yael-gomez-tokenization-overview-2025` — How LLMs See the World: The Magic of Tokenization (Part 1) (Substack) — [source](https://yaelgomez.substack.com/p/how-llms-see-the-world-the-magic)
- `codefinity-qkv-building-blocks` — Queries, Keys, and Values: The Building Blocks (Codefinity) — [source](https://codefinity.com/courses/v2/e7ee0772-6b82-4a1c-96ba-69b85ddee608/7ce26687-f7a7-4728-be33-7014c6c7b707/a5ac1dbf-dbec-4dd1-a8d6-f3d83cbb905b)
- `mbrenndoerfer-qkv-attention-mechanism` — Query, Key, Value: The Foundation of Transformer Attention (Michael Brenndoerfer / Language AI Handbook) — [source](https://mbrenndoerfer.com/writing/query-key-value-attention-mechanism)
- `aiedge-how-llm-distillation-trains-smaller-models` — How LLM Distillation Trains Smaller Models (The AiEdge Newsletter) — [source](https://newsletter.theaiedge.io/p/how-llm-distillation-trains-smaller-models)
- `aiedge-how-cuda-graphs-speed-up-llm-inference` — How CUDA Graphs Speed Up LLM Inference (The AiEdge Newsletter) — [source](https://newsletter.theaiedge.io/p/how-cuda-graphs-speed-up-llm-inference)
- `maarten-grootendorst-visual-guide-multimodal-generation` — A Visual Guide to Multimodal Generation (Exploring Language Models (Substack)) — [source](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-multimodal-generation)
- `jay-joshi-transformer-mathematics-positional-embeddings` — The Mathematics of a Transformer Explained With Numbers You Can Check by Hand With Geometric Intutions Using Pytorch. Part-1 Positional Encoding and Embadding Formation. (Medium) — [source](https://medium.com/@jayjj6272/the-mathematics-of-a-transformer-explained-with-numbers-you-can-check-by-hand-with-geometric-96b5873c95be)
- `jay-joshi-transformer-mathematics-attention` — The Mathematics of a Transformer Explained With Numbers You Can Check by Hand With Geometric Intutions Using Pytorch. Part-2 Attention Mechanism. (Medium) — [source](https://medium.com/@jayjj6272/the-mathematics-of-a-transformer-explained-with-numbers-you-can-check-by-hand-with-geometric-3c6abb1181ec)
- `cameron-wolfe-language-model-training-inference` — Language Model Training and Inference: From Concept to Code (Cameron R. Wolfe / Deep (Learning) Focus) — [source](https://cameronrwolfe.substack.com/p/language-model-training-and-inference)
- `cameron-wolfe-score-centering-substack` — Score Centering (Cameron R. Wolfe / Substack) — [source](https://cameronrwolfe.substack.com/p/score-centering)
- `marek-ryabinin-score-centering-off-policy-rl-2026` — Score Centering Stabilizes Off-policy Reinforcement Learning (arXiv) — [source](https://arxiv.org/abs/2609.20807)
- `jay-alammar-illustrated-transformer` — The Illustrated Transformer (Jay Alammar) — [source](https://jalammar.github.io/illustrated-transformer/)
- `jay-alammar-illustrated-gpt2` — The Illustrated GPT-2 (Jay Alammar) — [source](https://jalammar.github.io/illustrated-gpt2/)
- `jay-alammar-how-transformer-llms-work-2025` — How Transformer LLMs Work (DeepLearning.AI) — [source](https://www.deeplearning.ai/courses/how-transformer-llms-work)
- `3blue1brown-attention-transformers-step-by-step-2024` — Attention in Transformers, step by step — Deep Learning Chapter 6 (3Blue1Brown) — [source](https://www.3blue1brown.com/lessons/attention/)
- `3blue1brown-but-what-is-a-gpt-2024` — But what is a GPT? Visual intro to Transformers — Deep Learning Chapter 5 (3Blue1Brown) — [source](https://www.3blue1brown.com/lessons/gpt/)
- `bdtech-next-concept-modeling-2026` — Next-Concept Modeling shows that AI doesn’t need to ‘think’ one token at a time (TechTalks / BD Tech Talks) — [source](https://bdtechtalks.substack.com/p/next-concept-modeling-shows-that)
- `ai-scientist-platonic-representation-jepa-2026` — Do AI models trained on different modalities converge to the same representation of the world? (AI Scientist (Substack)) — [source](https://aiscientist.substack.com/p/do-ai-models-trained-on-different)
- `eleventh-hour-enthusiast-platonic-representation-jepa-2026` — Proving and Improving the Platonic Representation Hypothesis with JEPAs (Medium) — [source](https://medium.com/@EleventhHourEnthusiast/proving-and-improving-the-platonic-representation-hypothesis-with-jepas-80a88aa3766d)
- `youtube-jepa-platonic-representation-j0o8a6ducw` — YouTube video (video ID j0O8Aq6ducw; title and creator unverified) (YouTube) — [source](https://www.youtube.com/watch?v=j0O8Aq6ducw)
- `brij-pandey-inference-generation-linkedin-2026` — You ask LLM a question. It pauses. Then the answer starts appearing, piece by piece. (LinkedIn) — [source](https://www.linkedin.com/posts/brijpandeyji_you-ask-llm-a-question-it-pauses-then-share-7525787285829804032-YNEl)
- `hesam-sheikh-hessani-llm-embeddings-explained-2025` — LLM Embeddings Explained: A Visual and Intuitive Guide (Hugging Face Spaces) — [source](https://huggingface.co/spaces/hesamation/primer-llm-embedding)
- `vaswani-et-al-attention-is-all-you-need-2017` — Attention Is All You Need (NeurIPS) — [source](https://arxiv.org/abs/1706.03762)
- `harvardnlp-annotated-transformer` — The Annotated Transformer (Harvard NLP) — [source](https://nlp.seas.harvard.edu/annotated-transformer/)
- `stanford-ee269-transformers-signal-prediction` — Transformers for Signal Prediction (Stanford University) — [source](https://web.stanford.edu/class/ee269/Lecture_Transformers.pdf)
- `sebastian-raschka-full-to-hybrid-attention-2026` — From Full to Hybrid Attention in LLMs (LinkedIn) — [source](https://www.linkedin.com/posts/sebastianraschka_currently-working-towards-a-bigger-open-llm-share-7525958627799695361-Hprj/)
- `sebastian-raschka-full-to-hybrid-attention-companion-2026` — From Full to Hybrid Attention in LLMs (Sebastian Raschka) — [source](https://sebastianraschka.com/blog/2026/full-to-hybrid-attention.html)
- `sebastian-raschka-understanding-large-language-models-2023` — Understanding Large Language Models: A Cross-Section of the Most Relevant Literature To Get Up to Speed (Sebastian Raschka's Magazine) — [source](https://magazine.sebastianraschka.com/p/understanding-large-language-models)
- `dao-et-al-flashattention-2022` — FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness (Advances in Neural Information Processing Systems 35 (NeurIPS 2022)) — [source](https://arxiv.org/abs/2205.14135)
- `the-ai-edge-how-flashattention-speeds-up-llm-attention` — How FlashAttention Speeds Up LLM Attention (The AI Edge) — [source](https://newsletter.theaiedge.io/p/how-flashattention-speeds-up-llm-attention)
- `karthik-shashidhar-llms-compression-algorithms-2024` — LLMs and compression algorithms (Art of Data Science (Substack)) — [source](https://artofdatascience.substack.com/p/llms-and-compression-algorithms)
- `sasirekha-cota-understanding-llm-compression-2023` — Understanding Compression of Large Language Models (LLMs) (Medium) — [source](https://medium.com/@sasirekharameshkumar/understanding-compression-of-large-language-models-2ee3b8a350a2)
- `wayland-zhang-information-theory-llm-2026` — Information Theory Is All You Need (to Understand LLMs) (Wayland Zhang) — [source](https://waylandz.com/blog/information-theory-and-llm/)
- `xu-et-al-usable-information-2020` — A Theory of Usable Information under Computational Constraints (International Conference on Learning Representations (ICLR)) — [source](https://arxiv.org/abs/2002.10689)
- `sourav-mukherjee-compression-intelligence-2026` — Compression Is Intelligence: The Information Theory Behind LLMs (Medium / Bongquisitive Tech) — [source](https://medium.com/bongquisitive-tech/compression-is-intelligence-the-information-theory-behind-llms-70022356dad8)
- `3blue1brown-reinventing-entropy-compression-intelligence-part-1-2026` — Reinventing Entropy | Compression is Intelligence Part 1 (3Blue1Brown) — [source](https://www.youtube.com/watch?v=l6DKRf-fAAM)
- `fan-compression-intelligence-2026` — Compression Is Intelligence: The Common Ground of Positive Subjectivity and Negative Subjectivity — With a Discussion on the Nature of Intelligence (PhilArchive) — [source](https://philarchive.org/archive/MINCII-3)
- `sebastian-raschka-understanding-positional-embeddings-2026` — Understanding Positional Embeddings in Modern LLMs (Ahead of AI / Sebastian Raschka) — [source](https://magazine.sebastianraschka.com/p/understanding-positional-embeddings)
- `huggingface-llm-course` — Hugging Face LLM Course (Hugging Face) — [source](https://huggingface.co/learn/llm-course/)
- `bbycroft-llm-visualization` — LLM Visualization (Brendan Bycroft) — [source](https://bbycroft.net/llm)
- `tensorflow-playground` — A Neural Network Playground (TensorFlow Playground project) — [source](https://playground.tensorflow.org/)
- `raschka-visual-attention-variants` — A Visual Guide to Attention Variants in Modern LLMs (Ahead of AI) — [source](https://magazine.sebastianraschka.com/p/visual-attention-variants)
- `grootendorst-visual-guide-moe` — A Visual Guide to Mixture of Experts (MoE) (Maarten Grootendorst) — [source](https://www.maartengrootendorst.com/blog/moe/)
- `modular-llm-inference-handbook` — LLM Inference Handbook (Modular) — [source](https://handbook.modular.com/)
- `neuronpedia-interpretability-platform` — Neuronpedia (Neuronpedia) — [source](https://www.neuronpedia.org/)
- `cunningham-sparse-autoencoders-interpretable-features-2024` — Sparse Autoencoders Find Highly Interpretable Features in Language Models (International Conference on Learning Representations (ICLR)) — [source](https://proceedings.iclr.cc/paper_files/paper/2024/hash/1fa1ab11f4bd5f94b2ec20e794dbfa3b-Abstract-Conference.html)
- `bricken-towards-monosemanticity-2023` — Towards Monosemanticity: Decomposing Language Models With Dictionary Learning (Transformer Circuits Thread / Anthropic) — [source](https://transformer-circuits.pub/2023/monosemantic-features/index.html)
- `gao-scaling-evaluating-sparse-autoencoders-2025` — Scaling and Evaluating Sparse Autoencoders (International Conference on Learning Representations (ICLR)) — [source](https://proceedings.iclr.cc/paper_files/paper/2025/hash/42ef3308c230942d223c411adf182c88-Abstract-Conference.html)
- `chanin-feature-absorption-sparse-autoencoders-2025` — A is for Absorption: Studying Feature Splitting and Absorption in Sparse Autoencoders (Advances in Neural Information Processing Systems 38 (NeurIPS 2025)) — [source](https://proceedings.neurips.cc/paper_files/paper/2025/hash/764ff7477b8e24dbe01531f6791e8bdf-Abstract-Conference.html)
- `huggingface-jobs-nanogpt-video-2026` — GPU-POOR? NO PROBLEM!... thanks to Hugging Face Jobs (YouTube) — [source](https://www.youtube.com/watch?v=7Yx_7byZiFU)
- `3blue1brown-cross-entropy-compression-intelligence-part-2-2026` — But what is cross-entropy? | Compression is Intelligence Part 2 (3Blue1Brown) — [source](https://www.youtube.com/watch?v=GlYgs6v2YfU)
- `dailydose-bi-cross-encoders-sentence-similarity-2024` — Bi-encoders and Cross-encoders for Sentence Pair Similarity Scoring (Part 1) (Daily Dose of Data Science) — [source](https://www.dailydoseofds.com/bi-encoders-and-cross-encoders-for-sentence-pair-similarity-scoring-part-1/)
- `dailydose-augsbert-sentence-similarity-2024` — AugSBERT: Bi-encoders + Cross-encoders for Sentence Pair Similarity Scoring – Part 2 (Daily Dose of Data Science) — [source](https://www.dailydoseofds.com/augsbert-bi-encoders-cross-encoders-for-sentence-pair-similarity-scoring-part-2/)
- `dailydose-foundations-rag-2024` — Foundations of RAG systems (Daily Dose of Data Science) — [source](https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-1-with-implementations/)
- `reimers-gurevych-2019-sentence-bert` — Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks (Association for Computational Linguistics) — [source](https://aclanthology.org/D19-1410/)
- `khattab-zaharia-2020-colbert` — ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT (SIGIR 2020 / arXiv) — [source](https://arxiv.org/abs/2004.12832)
- `santhanam-etal-2022-colbertv2` — ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction (Association for Computational Linguistics) — [source](https://aclanthology.org/2022.naacl-main.272/)
- `formal-piwowarski-clinchant-2021-splade` — SPLADE: Sparse Lexical and Expansion Model for First Stage Ranking (SIGIR 2021 / arXiv) — [source](https://arxiv.org/abs/2107.05720)
- `thakur-etal-2021-beir` — BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models (NeurIPS Datasets and Benchmarks 2021 / arXiv) — [source](https://arxiv.org/abs/2104.08663)
- `dailydose-visual-guide-bi-cross-colbert-2025` — Visual Guide to Bi-encoders, Cross-encoders and ColBERT (Daily Dose of Data Science) — [source](https://blog.dailydoseofds.com/p/visual-guide-to-bi-encoders-cross)
- `faysse-etal-2025-colpali` — ColPali: Efficient Document Retrieval with Vision Language Models (International Conference on Learning Representations) — [source](https://proceedings.iclr.cc/paper_files/paper/2025/hash/99e9e141aafc314f76b0ca3dd66898b3-Abstract-Conference.html)
- `jothi-moorthy-llm-processing-linkedin` — When you type a prompt, the LLM sees numbers, not words (LinkedIn) — [source](https://www.linkedin.com/posts/jothi-moorthy_%F0%9D%97%AA%F0%9D%97%B5%F0%9D%97%B2%F0%9D%97%BB-%F0%9D%98%86%F0%9D%97%BC%F0%9D%98%82-%F0%9D%98%81%F0%9D%97%BD%F0%9D%97%BF%F0%9D%97%BC%F0%9D%97%BA%F0%9D%97%BD%F0%9D%98%81-share-7528445050129764353-hs6w/)
- `lewish-intelligence-and-compression-2025` — Intelligence and compression (lewish.io) — [source](https://lewish.io/posts/intelligence-and-compression)
- `deliriumm-llms-do-not-guess-they-optimize-2026` — LLMs do not guess. They optimize. Here is the difference and the math behind it (X Articles) — [source](https://x.com/i/article/2091560754122014781)
- `maor-farid-large-mechanical-model-brep-geometry-2026` — AI and mechanical design: a Large Mechanical Model for B-rep geometry (LinkedIn) — [source](https://www.linkedin.com/posts/maorfaridphd_ai-mechanicaldesign-mehcanicalengineers-ugcPost-7469852823074111490-ZO-w/)
- `kim-et-al-brepcoder-2026` — BrepCoder: A Unified Multimodal Large Language Model for Multi-task B-rep Reasoning (arXiv) — [source](https://arxiv.org/abs/2602.22284)
- `gerstmayr-et-al-meceng-benchmark-2026` — Large Language Models and their Awareness of Mechanics and Spatial Geometry (arXiv) — [source](https://arxiv.org/abs/2608.14615)
- `lu-et-al-omnimech-2026` — OmniMech: All-in-one Multimodal Mechanical Benchmark for 3D Reconstruction (arXiv) — [source](https://arxiv.org/abs/2608.05539)
- `leo-ai-large-mechanical-model-overview-2025` — Why GPT Will Never Match a Freshman Mechanical Engineer (Leo AI) — [source](https://www.getleo.ai/blog/why-gpt-will-never-match-a-freshman-mechanical-engineer)
- `david-chen-compression-is-intelligence-2025` — Compression Is Intelligence (LinkedIn / Decoding A.I.) — [source](https://www.linkedin.com/pulse/compression-intelligence-david-chen-uqtmc/)
- `hesam-sheikh-llm-study-roadmap-2024` — How I Studied LLMs in Two Weeks: A Comprehensive Roadmap (Towards Data Science) — [source](https://towardsdatascience.com/how-i-studied-llms-in-two-weeks-a-comprehensive-roadmap-e8ac19667a31/)
- `alliancy-la-compression-strategie-avenir-llm-2026` — La compression, stratégie d’avenir des LLM (Alliancy) — [source](https://alliancy.fr/la-compression-strategie-davenir-des-llm-19908527-e6dd-4097-b5e5-0d9a2ab2c7e0)
- `notion-intelligence-compression-summary` — Intelligence = Compression (Notion) — [source](https://jealous-speedwell-b32.notion.site/Intelligence-Compression-4c8d01d16ebf4dc98c5c5cb85ea825c8)
- `hutter-universal-algorithmic-intelligence-2007` — Universal Algorithmic Intelligence: A Mathematical Top-Down Approach (Springer / IDSIA) — [source](https://arxiv.org/abs/cs/0701125)
- `leike-hutter-computability-aixi-2015` — On the Computability of AIXI (Proceedings of Machine Learning Research, UAI) — [source](https://arxiv.org/abs/1510.05572)
- `hutter-quarel-catt-universal-ai-2024` — An Introduction to Universal Artificial Intelligence (Open-access textbook) — [source](https://hutter1.net/publ/uaibook2.pdf)
- `jose-parreno-garcia-how-llms-work-three-layers-2025` — LLMs explained (Part 1): The 3-layer framework behind chatGPT & friends (Senior Data Science Lead (Substack)) — [source](https://joseparreogarcia.substack.com/p/how-llms-work-part-1-the-3-essential-layers)
- `huang-zhang-shan-he-compression-intelligence-linearly-2024` — Compression Represents Intelligence Linearly (Conference on Language Modeling (COLM 2024) / arXiv) — [source](https://arxiv.org/abs/2404.09937)
- `andrej-karpathy-deep-dive-llms-chatgpt` — Deep Dive into LLMs like ChatGPT (YouTube) — [source](https://www.youtube.com/watch?v=7xTGNNLPyMI)
- `conmy-automated-circuit-discovery-2023` — Towards Automated Circuit Discovery for Mechanistic Interpretability (Advances in Neural Information Processing Systems 36 (NeurIPS 2023)) — [source](https://papers.nips.cc/paper_files/paper/2023/hash/34e1dbe95d34d7ebaf99b9bcaeb5b2be-Abstract-Conference.html)
- `syed-attribution-patching-2024` — Attribution Patching Outperforms Automated Circuit Discovery (Proceedings of the 7th BlackboxNLP Workshop, Association for Computational Linguistics) — [source](https://aclanthology.org/2024.blackboxnlp-1.25/)
- `kramar-atp-star-2024` — AtP*: Efficient and Scalable Methods for Localizing LLM Behaviour to Components (arXiv / Google DeepMind) — [source](https://arxiv.org/abs/2403.00745)
- `hanna-faithfulness-2024` — Have Faith in Faithfulness: Going Beyond Circuit Overlap When Finding Model Mechanisms (Proceedings of the 2024 Conference on Language Modeling (COLM 2024)) — [source](https://openreview.net/forum?id=zSf8PJyQb2)
- `chan-causal-scrubbing-2022` — Causal Scrubbing: A Method for Rigorously Testing Interpretability Hypotheses (AI Alignment Forum / Redwood Research) — [source](https://www.alignmentforum.org/posts/JvZhhzycHu2Yd57RN/causal-scrubbing-a-method-for-rigorously-testing)
- `marks-sparse-feature-circuits-2025` — Sparse Feature Circuits: Discovering and Editing Interpretable Causal Graphs in Language Models (International Conference on Learning Representations (ICLR 2025)) — [source](https://proceedings.iclr.cc/paper_files/paper/2025/hash/3ba4d47a83e498c2b1a0868cba20f6de-Abstract-Conference.html)
- `shannon-mathematical-theory-communication-1948` — A Mathematical Theory of Communication (The Bell System Technical Journal / Wiley) — [source](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x)
- `rissanen-langdon-arithmetic-coding-1979` — Arithmetic Coding (IBM Journal of Research and Development) — [source](https://doi.org/10.1147/rd.232.0149)
- `witten-neal-cleary-arithmetic-coding-1987` — Arithmetic Coding for Data Compression (Communications of the ACM) — [source](https://doi.org/10.1145/214762.214771)

## File B — dates de publication inconnues (44)

- `nishanthan-k-qkv-transformers-devto` — How Query, Key, and Value (QKV) Work in Transformers (DEV Community) — [source](https://dev.to/nishanthan-k/how-query-key-and-value-qkv-work-in-transformers-199a)
- `huggingface-transformers-kv-cache-explanation` — Caching (Hugging Face Transformers) — [source](https://huggingface.co/docs/transformers/main/en/cache_explanation)
- `andrej-karpathy-gpt-tokenizer-video` — Let's build the GPT Tokenizer (YouTube) — [source](https://www.youtube.com/watch?v=zduSFxRajkE)
- `sebastian-raschka-llms-from-scratch-ch02` — Build a Large Language Model (From Scratch), Chapter 2 (Manning / GitHub) — [source](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch02)
- `huggingface-course-tokenizers-chapter6` — Hugging Face LLM Course — Tokenizers (Hugging Face) — [source](https://huggingface.co/docs/course/chapter6/8)
- `sentence-transformers-similarity-documentation` — Sentence Transformers — Similarity and SentenceTransformer APIs (Sentence Transformers) — [source](https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html)
- `openai-tiktoken-educational-bpe` — tiktoken educational BPE module (OpenAI / GitHub) — [source](https://github.com/openai/tiktoken/blob/main/tiktoken/_educational.py)
- `karpathy-minbpe` — minbpe (GitHub) — [source](https://github.com/karpathy/minbpe)
- `huggingface-tokenizers-pipeline-docs` — Hugging Face Tokenizers — Pipeline and Components (Hugging Face) — [source](https://huggingface.co/docs/tokenizers/python/latest/pipeline.html)
- `google-sentencepiece-documentation` — SentencePiece — Overview and Normalization (Google) — [source](https://google.github.io/sentencepiece/)
- `huggingface-tokenizer-algorithms-summary` — Hugging Face Transformers — Tokenizer Summary (Hugging Face) — [source](https://huggingface.co/docs/transformers/main/en/tokenizer_summary)
- `pytorch-embedding-api` — torch.nn.Embedding (PyTorch) — [source](https://docs.pytorch.org/docs/stable/generated/torch.nn.Embedding.html)
- `openai-tiktoken-repository` — tiktoken (OpenAI / GitHub) — [source](https://github.com/openai/tiktoken)
- `huggingface-tokenizers-repository` — Tokenizers (Hugging Face / GitHub) — [source](https://github.com/huggingface/tokenizers)
- `google-sentencepiece-repository` — SentencePiece (Google / GitHub) — [source](https://github.com/google/sentencepiece)
- `sauravp97-hf-bpe-visualizer-article` — Visualizing BPE Tokenizer Encoding (Hugging Face) — [source](https://huggingface.co/blog/SauravP97/bpe-tokenizer-visualize)
- `sauravp97-hf-bpe-visualizer-repository` — hf-tokenizer-visualizer (GitHub) — [source](https://github.com/SauravP97/hf-tokenizer-visualizer)
- `poloclub-transformer-explainer-repository` — Transformer Explainer (Georgia Tech Polo Club / GitHub) — [source](https://github.com/poloclub/transformer-explainer)
- `philip-mueller-bpe-explainer` — BPE Explainer (Philip Müller) — [source](https://philipmueller.dev/bpe-visualization/)
- `cornell-byte-pair-visualizer` — Interactive Tokenization Visualizer (Cornell University) — [source](https://www.cs.cornell.edu/courses/cs4782/2026sp/demos/bytepair/)
- `vizuara-tokenization-from-scratch-bpe` — Tokenization from Scratch: Building Byte-Pair Encoding by Hand (Vizuara) — [source](https://pods.vizuara.ai/courses/build-llm/tokenization-from-scratch-building-byte-pair-encoding-by-han)
- `vizuara-llms-from-30000-feet` — LLMs from 30,000 Feet (Vizuara) — [source](https://mu.vizuara.ai/learn/llms-30k)
- `codefinity-qkv-building-blocks` — Queries, Keys, and Values: The Building Blocks (Codefinity) — [source](https://codefinity.com/courses/v2/e7ee0772-6b82-4a1c-96ba-69b85ddee608/7ce26687-f7a7-4728-be33-7014c6c7b707/a5ac1dbf-dbec-4dd1-a8d6-f3d83cbb905b)
- `aiedge-how-llm-distillation-trains-smaller-models` — How LLM Distillation Trains Smaller Models (The AiEdge Newsletter) — [source](https://newsletter.theaiedge.io/p/how-llm-distillation-trains-smaller-models)
- `jay-joshi-transformer-mathematics-positional-embeddings` — The Mathematics of a Transformer Explained With Numbers You Can Check by Hand With Geometric Intutions Using Pytorch. Part-1 Positional Encoding and Embadding Formation. (Medium) — [source](https://medium.com/@jayjj6272/the-mathematics-of-a-transformer-explained-with-numbers-you-can-check-by-hand-with-geometric-96b5873c95be)
- `jay-joshi-transformer-mathematics-attention` — The Mathematics of a Transformer Explained With Numbers You Can Check by Hand With Geometric Intutions Using Pytorch. Part-2 Attention Mechanism. (Medium) — [source](https://medium.com/@jayjj6272/the-mathematics-of-a-transformer-explained-with-numbers-you-can-check-by-hand-with-geometric-3c6abb1181ec)
- `cameron-wolfe-score-centering-substack` — Score Centering (Cameron R. Wolfe / Substack) — [source](https://cameronrwolfe.substack.com/p/score-centering)
- `jay-alammar-illustrated-transformer` — The Illustrated Transformer (Jay Alammar) — [source](https://jalammar.github.io/illustrated-transformer/)
- `jay-alammar-illustrated-gpt2` — The Illustrated GPT-2 (Jay Alammar) — [source](https://jalammar.github.io/illustrated-gpt2/)
- `jay-alammar-how-transformer-llms-work-2025` — How Transformer LLMs Work (DeepLearning.AI) — [source](https://www.deeplearning.ai/courses/how-transformer-llms-work)
- `eleventh-hour-enthusiast-platonic-representation-jepa-2026` — Proving and Improving the Platonic Representation Hypothesis with JEPAs (Medium) — [source](https://medium.com/@EleventhHourEnthusiast/proving-and-improving-the-platonic-representation-hypothesis-with-jepas-80a88aa3766d)
- `youtube-jepa-platonic-representation-j0o8a6ducw` — YouTube video (video ID j0O8Aq6ducw; title and creator unverified) (YouTube) — [source](https://www.youtube.com/watch?v=j0O8Aq6ducw)
- `hesam-sheikh-hessani-llm-embeddings-explained-2025` — LLM Embeddings Explained: A Visual and Intuitive Guide (Hugging Face Spaces) — [source](https://huggingface.co/spaces/hesamation/primer-llm-embedding)
- `harvardnlp-annotated-transformer` — The Annotated Transformer (Harvard NLP) — [source](https://nlp.seas.harvard.edu/annotated-transformer/)
- `stanford-ee269-transformers-signal-prediction` — Transformers for Signal Prediction (Stanford University) — [source](https://web.stanford.edu/class/ee269/Lecture_Transformers.pdf)
- `huggingface-llm-course` — Hugging Face LLM Course (Hugging Face) — [source](https://huggingface.co/learn/llm-course/)
- `bbycroft-llm-visualization` — LLM Visualization (Brendan Bycroft) — [source](https://bbycroft.net/llm)
- `tensorflow-playground` — A Neural Network Playground (TensorFlow Playground project) — [source](https://playground.tensorflow.org/)
- `modular-llm-inference-handbook` — LLM Inference Handbook (Modular) — [source](https://handbook.modular.com/)
- `neuronpedia-interpretability-platform` — Neuronpedia (Neuronpedia) — [source](https://www.neuronpedia.org/)
- `huggingface-jobs-nanogpt-video-2026` — GPU-POOR? NO PROBLEM!... thanks to Hugging Face Jobs (YouTube) — [source](https://www.youtube.com/watch?v=7Yx_7byZiFU)
- `jothi-moorthy-llm-processing-linkedin` — When you type a prompt, the LLM sees numbers, not words (LinkedIn) — [source](https://www.linkedin.com/posts/jothi-moorthy_%F0%9D%97%AA%F0%9D%97%B5%F0%9D%97%B2%F0%9D%97%BB-%F0%9D%98%86%F0%9D%97%BC%F0%9D%98%82-%F0%9D%98%81%F0%9D%97%BD%F0%9D%97%BF%F0%9D%97%BC%F0%9D%97%BA%F0%9D%97%BD%F0%9D%98%81-share-7528445050129764353-hs6w/)
- `maor-farid-large-mechanical-model-brep-geometry-2026` — AI and mechanical design: a Large Mechanical Model for B-rep geometry (LinkedIn) — [source](https://www.linkedin.com/posts/maorfaridphd_ai-mechanicaldesign-mehcanicalengineers-ugcPost-7469852823074111490-ZO-w/)
- `notion-intelligence-compression-summary` — Intelligence = Compression (Notion) — [source](https://jealous-speedwell-b32.notion.site/Intelligence-Compression-4c8d01d16ebf4dc98c5c5cb85ea825c8)

## Découpage opérationnel recommandé

- **Lot licence 1 :** dépôts de code et projets logiciels — vérifier LICENSE/COPYING et les sous-répertoires/actifs tiers.
- **Lot licence 2 :** articles scientifiques — vérifier la licence de l'article chez l'éditeur ou dans le dépôt auteur; séparer les figures tierces.
- **Lot licence 3 :** documentation et cours — vérifier les conditions officielles de réutilisation; le droit de consulter n'est pas une licence de reproduction.
- **Lot licence 4 :** vidéos, blogs et contenus de plateformes — conserver le lien seulement en l'absence de licence explicite.
- **Lot dates 1 :** DOI/proceedings/éditeur; **lot dates 2 :** arXiv/versioning; **lot dates 3 :** dépôts et releases; **lot dates 4 :** pages web, blogs et vidéos dont la date est parfois non exposée.

## Limites et critères de clôture

- Cet inventaire ne constitue pas une recherche externe source par source et ne modifie aucun enregistrement de `data/sources.yml`.
- Une entrée n'est clôturée qu'avec une preuve primaire stable, une valeur qualifiée et un périmètre explicite, ou une décision documentée de conserver l'inconnu.
- Les files licence et date sont indépendantes : une source peut être résolue sur une dimension et rester inconnue sur l'autre.
- Aucun KPI de couverture scientifique n'est calculé à partir de ces métadonnées.

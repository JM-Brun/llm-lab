# Source review — A Visual Guide to Multimodal Generation

**Source:** Maarten Grootendorst, *A Visual Guide to Multimodal Generation*, Exploring Language Models, 29 October 2026.  
**Canonical URL:** https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-multimodal-generation  
**Review date:** 2026-11-06  
**Scan status:** partially scanned  
**Integration decision:** reference-only; optional deepening, not part of the minimum learning route.

## 1. Why this source matters

The source addresses a gap in a text-centric introduction to LLMs: multimodal input understanding and multimodal output generation are different capabilities. A model that accepts images, audio or video does not thereby generate those modalities.

The article is useful as an illustrated architectural survey. Its strongest contribution for LLM Lab is the distinction between:

- **Multimodal understanding:** encoding non-text inputs into representations that a language model can consume.
- **Multimodal generation:** producing non-text outputs, either by connecting a separate generator or by extending the model's own output architecture.
- **Unified multimodal interaction:** combining understanding and generation so that the system can interpret and produce multiple modalities.

This distinction should be made explicit in any future multimodal overview. It does not justify adding a multimodal chapter to the core route now.

## 2. Extracted ideas

### 2.1 Image generation foundations

The inspected image-generation material describes diffusion as an iterative denoising process. A noisy image representation is progressively updated; the intermediate state is a tensor, not necessarily a full-resolution image at every step.

The Stable Diffusion example is decomposed into five components:

1. Text encoder: maps the text condition to embeddings.
2. Diffusion model: predicts noise / denoising updates in latent space.
3. Noisy input representation: initialization for the reverse process.
4. Image encoder: maps images to latent representations for image-conditioned workflows.
5. Image decoder: maps latent representations back to images.

The article emphasizes latent-space computation as a way to avoid performing the iterative process directly on full-resolution pixels. It then introduces Diffusion Transformers as a major architectural direction.

**Editorial boundary:** this is a conceptual introduction, not a complete mathematical treatment of the forward/reverse diffusion processes, noise schedules, objectives, samplers, or latent autoencoder training.

### 2.2 Connecting generators to LLMs

The article's central architectural distinction is:

| Strategy | Main idea | Architectural consequence |
|---|---|---|
| Late fusion / output projection | Connect an autoregressive LLM to a separate modality generator, using generated text or projected representations | The language model and modality generator remain distinct components |
| Early fusion / unified generation | Adapt the model architecture so that it emits representations/tokens for multiple modalities | Multimodal generation is integrated into the model's generative path |

**Late fusion** has two variants in the article:
- The LLM writes a textual prompt consumed by an external generator. This is closer to an agent orchestrating a tool than to one unified multimodal model.
- A learned output projector maps LLM representations into a representation accepted by a separate generator.

NExT-GPT is used as an example of a system with modality-specific input/output projectors and pretrained modality encoders/decoders. The article describes a relatively small trainable interface around otherwise frozen components. This is an example, not a universal recipe.

OmniGen2 and BLIP-3o are mentioned as more recent examples of decoupled autoregressive text generation and diffusion-based image generation. Their details have not been independently checked in this scan.

**Early fusion** is illustrated with Janus. The article describes separate visual representations for understanding and generation, then a unified autoregressive language-modeling path that can emit text or image representations. It highlights the difference in representational requirements. The labels *early fusion* and *late fusion* are useful architectural shorthand, not a complete or necessarily mutually exclusive taxonomy: the actual boundary between shared model, modality-specific pathway, projector and decoder must be described per system.
- Understanding benefits from semantic, abstract representations.
- Generation requires more detailed representations.

The article describes a staged training outline for Janus: adaptor/image-head training, unified pretraining, then supervised fine-tuning.

### 2.3 Audio generation: AudioLM

The indexed article section presents AudioLM as an example of autoregressive audio generation. Its important conceptual move is to model a sequence of discrete audio representations rather than predict raw waveform samples directly.

The article identifies three components:

1. **Acoustic tokens from SoundStream.** SoundStream is a neural audio codec: an encoder maps waveform segments to discrete codes and a decoder reconstructs audio from those codes. The article describes a convolutional encoder/decoder and adversarial training for reconstruction quality.
2. **Semantic tokens from w2v-BERT.** These representations capture higher-level linguistic/audio structure. They complement acoustic codes rather than replacing them.
3. **Hierarchical Transformers.** The article describes a staged autoregressive process:
   - model semantic tokens to capture longer-range structure;
   - predict coarse acoustic tokens conditioned on semantic context and past acoustic tokens;
   - refine the acoustic sequence with finer-grained tokens;
   - decode acoustic tokens back to waveform with SoundStream.

The primary AudioLM paper supports the central distinction: semantic tokens are intended to preserve long-term structure, while codec tokens preserve acoustic detail and reconstruction quality. Its demonstrated task is continuation of audio from a short audio prompt (including speech and piano), not a generic claim that the original AudioLM is a text-to-audio model. This distinction matters when reusing the example.

**Transferable concept:** autoregressive next-token modeling can operate over learned discrete representations of audio. The meaning of “token” is modality-dependent; audio tokens are not text tokens and are not necessarily aligned to words.

**Pedagogical value:** high as an optional case study connecting tokenization, discrete latent representations, autoregressive modeling and decoding. It should not be added to the main text-only GPT build.

### 2.4 Video generation

The article explicitly separates video generation from image generation by the temporal dimension. If audio is ignored, a video consists of frames whose evolution over time must be modeled in addition to spatial image content.

The article's high-level account is:
- diffusion-based generation starts from noise and iteratively denoises;
- video generation extends image generation with temporal structure;
- newer approaches use Diffusion Transformers to generate frames / video representations.

The article does not provide, in the indexed extraction, a full treatment of temporal attention, latent video tokenization, motion representations, temporal consistency objectives, or evaluation. Therefore those details must not be inferred from this source.

**Editorial caveat:** a sequence of plausible individual frames is not, by itself, evidence of temporally coherent video. This is a general technical qualification, not a detailed claim established by the article.

### 2.5 Modality markers and output routing

In the LLM integration section, the article describes special modality markers such as `[IMG]`, `[AUD]` and `[VID]` as illustrative control signals. In the described projector-based design, the autoregressive Transformer emits modality-specific markers / representations; a corresponding output projector maps representations into the space expected by a pretrained diffusion decoder.

The article's stated motivation is parameter efficiency: train the interface/projectors rather than retrain all large pretrained encoders and decoders. Treat the reported parameter proportions as specific to the cited system, not a general property of projector-based architectures.

These markers are examples from the architecture under discussion, not universal tokens shared by multimodal models.

## 3. Source-local conceptual structure

The source's conceptual hierarchy, based on the inspected material:

```text
Multimodal generation
├── Generate a modality
│   ├── Images
│   │   ├── Diffusion / denoising
│   │   ├── Latent representations
│   │   └── Diffusion Transformers
│   ├── Audio
│   │   ├── Semantic tokens (w2v-BERT)
│   │   ├── Acoustic tokens (SoundStream)
│   │   └── Hierarchical autoregressive Transformers
│   └── Video
│       └── Temporal dimension + diffusion / DiT
└── Connect generation to multimodal LLMs
    ├── Late fusion
    │   ├── Text prompt → external generator
    │   └── LLM representations → output projector → generator
    └── Early fusion
        └── Unified multimodal token/representation generation
```

This is a source-local outline, not a proposed LLM Lab curriculum tree.

## 4. What should transfer to LLM Lab

### Keep as high-value conceptual distinctions

1. **Understanding ≠ generation.** Treat input modality support and output modality support as separate capabilities.
2. **External generator vs native/unified generation.** This is the most useful architectural axis for comparing multimodal systems.
3. **Text orchestration vs representation projection.** Both can be late-fusion designs, but they imply different interfaces and degrees of integration.
4. **Modality-specific representations.** A shared model does not imply that the same encoder/decoder representation is optimal for understanding and generation.
5. **Latent-space generation.** Introduce as an example of moving expensive iterative generation into a compressed representation space, not as a required LLM concept.

### Keep optional / deepening

- Stable Diffusion component-level walkthrough.
- Forward/reverse diffusion mathematics, noise schedules and samplers.
- Latent autoencoders, VAE/VQ representations and codebooks.
- Diffusion Transformers and modality-specific decoder internals.
- NExT-GPT, Janus, OmniGen2 and BLIP3-o architecture case studies.
- Audio and video generation architectures.

These topics should not be inserted into the text-tokenization → representations → Transformer → prediction → inference spine. They form a separate multimodal extension branch.

## 5. Integration decision and placement

**Decision: register the source and expose it as an optional reference; do not modify the core guided route.**

Recommended future placement, once a concise bilingual landing page exists:

- A multimodal overview / architecture page, linked from the general architecture overview or a dedicated optional multimodal section.
- A clearly marked *Deepen* link, not a required stage in `data/guided-route.yml`.
- A source reference attached to the multimodal overview, not to generic Transformer, generation or diffusion pages until those pages exist.

No new learning-route stage, page, concept-graph edge, computational-graph node or Build milestone is warranted by this scan alone.

## 6. Claims and caveats to preserve

- Do not call every LLM that accepts image/audio/video input a multimodal generator.
- Do not describe a model orchestrating an external generator through text as necessarily one unified multimodal model.
- Do not imply early fusion is always more accurate; the source's comparison is an architectural discussion, not a universal empirical result.
- Do not generalize the trainable-projector/frozen-backbone pattern to every late-fusion model.
- Do not present the Janus/NExT-GPT examples as current exhaustive taxonomy.
- Keep generation modality-specific: image, audio and video pipelines need not share the same latent representation or decoder design.

## 7. Scan limitations and follow-up

The source was retrieved through indexed search content because direct Substack retrieval returned a cache miss. The indexed extraction exposes the main image, audio, video and LLM-integration sections. This is a broad content scan, but not a complete visual or citation audit. Primary-source spot checks were performed for AudioLM, Janus and NExT-GPT.

Remaining work before reader-facing integration:
1. Inspect the figures individually and record their role; link to them rather than copying until reuse rights are known.
2. Verify the remaining cited model papers (Stable Diffusion, SoundStream, w2v-BERT, Diffusion Transformers, OmniGen2 and BLIP-3o) against their primary sources.
3. Compare the source against existing multimodal coverage to identify genuinely complementary material.
4. Decide whether a concise optional multimodal overview page is justified; do not add the source to the main guided route.

## 8. Provenance

The article credits more than 50 custom visuals and describes itself as a free bonus chapter associated with *An Illustrated Guide to AI Agents*. No licence or permission to reproduce its text, figures or code was established during this review. LLM Lab should cite and link to the source, not copy its illustrations or substantial prose.


## 9. Primary-source spot checks

These checks validate selected architectural descriptions; they do not constitute a full reproduction or benchmark audit.

| Topic | Primary source | What it supports | Boundary |
|---|---|---|---|
| AudioLM | [Borsos et al., *AudioLM: A Language Modeling Approach to Audio Generation*](https://arxiv.org/abs/2209.03143) | Audio is represented as discrete tokens; semantic representations and neural-codec acoustic tokens are combined hierarchically for coherent continuation | Original task is audio continuation from audio context; do not imply native text-to-audio in the original paper |
| SoundStream / AudioLM examples | [Google Research AudioLM page](https://google-research.github.io/seanet/audiolm/examples/) | Semantic/acoustic token complementarity and SoundStream reconstruction examples | Does not validate every implementation detail in the newsletter's diagrams |
| Janus | [Wu et al., CVPR 2025 open-access paper](https://openaccess.thecvf.com/content/CVPR2025/html/Wu_Janus_Decoupling_Visual_Encoding_for_Unified_Multimodal_Understanding_and_Generation_CVPR_2025_paper.html) | Separate visual encoding pathways for understanding and generation with a shared autoregressive Transformer | Image-focused case study; not a universal multimodal architecture |
| NExT-GPT | [Wu et al., ICML 2024 paper](https://proceedings.mlr.press/v235/wu24e.html) | LLM connected to modality adaptors and diffusion decoders; paper reports tuning a small subset of projection parameters | The paper's specific system and training setup; not a general parameter-efficiency guarantee |
| Latent Diffusion / Stable Diffusion foundations | [Rombach et al., CVPR 2022](https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html) | Diffusion in the latent space of a pretrained autoencoder; cross-attention supports conditioning such as text | Supports the latent-diffusion principle, not every implementation detail or every Stable Diffusion release |
| SoundStream | [Zeghidour et al., arXiv:2107.03312](https://arxiv.org/abs/2107.03312) | Neural audio codec with a convolutional encoder/decoder and residual vector quantization | Codec / reconstruction component; not by itself an autoregressive generator or semantic representation model |
| w2v-BERT | [Chung et al., arXiv:2108.06209](https://arxiv.org/abs/2108.06209) | Self-supervised speech representation learning; contrastive learning discretizes speech into units and masked prediction learns contextualized representations | The paper describes representation learning, not a general-purpose audio generator; do not equate units with text tokens or word boundaries |
| Diffusion Transformer (DiT) | [Peebles and Xie, ICCV 2023](https://openaccess.thecvf.com/content/ICCV2023/html/Peebles_Scalable_Diffusion_Models_with_Transformers_ICCV_2023_paper.html) | A Transformer backbone operates on latent patches in place of the commonly used U-Net in the studied latent-diffusion setup | A specific diffusion architecture; not the ordinary autoregressive Transformer used for next-token prediction |
| OmniGen2 | [Wu et al., arXiv:2506.18871](https://arxiv.org/abs/2506.18871) | Distinct text/image decoding pathways, unshared parameters and a decoupled image tokenizer | Its design is model-specific; do not collapse it into a universal early-/late-fusion template |
| BLIP3-o | [Chen et al., arXiv:2505.09568](https://arxiv.org/abs/2505.09568) | Unified image understanding/generation study using a diffusion Transformer to generate semantically rich CLIP image features | Distinct design from OmniGen2; preserve the paper's precise representation and training claims |

### Editorial correction to retain

The newsletter is a visual explanatory resource, not the final authority for technical details. Where its shorthand risks conflating distinct mechanisms, LLM Lab should use the primary paper's terminology. In particular, AudioLM's semantic and acoustic streams should remain distinct in any diagram, and its original task should be described as audio continuation.


## 10. Relation to the canonical computational spine

The canonical computational spine in [docs/canonical-computational-spine.md](../canonical-computational-spine.md) describes next-token prediction in a text-oriented autoregressive LLM and its generation, scoring, evaluation and training branches. This source describes adjacent but non-identical generative mechanisms:

- **AudioLM** is autoregressive, but its sequence elements are learned audio representations (semantic and codec tokens), and a neural audio decoder reconstructs the waveform. It is a modality-specific sequence-modeling case, not an extension of the ordinary text-token vocabulary.
- **Latent diffusion / DiT image generation** uses iterative denoising in a learned latent space. Its sampling loop is not the same operation as autoregressive next-token decoding.
- **Video generation** adds temporal structure to the generated visual representation; the inspected article does not specify enough detail to add temporal operations to the canonical graph.
- **Multimodal LLM systems** may combine an autoregressive language-model core with modality-specific encoders, projectors and/or external decoders. Those interfaces should be represented explicitly rather than flattening every component into one generic forward pass.

Consequently, this source belongs to a **multimodal extension branch** linked to (but not inserted into) the text-LM computational spine. Any future canonical representation should distinguish autoregressive sequence generation, iterative diffusion sampling, codec decoding and orchestration of external generators as different operation families. The source-local graph remains a source-analysis artifact, not a proposal to extend the canonical computational registry without a dedicated architecture audit.

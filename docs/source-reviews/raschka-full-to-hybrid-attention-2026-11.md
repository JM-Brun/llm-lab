# From full to hybrid attention in open LLMs — source review

- Author: Sebastian Raschka
- Published: 2026-11-10 (date shown on the author's companion article)
- Primary supplied source: https://www.linkedin.com/posts/sebastianraschka_currently-working-towards-a-bigger-open-llm-share-7525958627799695361-Hprj/
- Author's companion write-up: https://sebastianraschka.com/blog/2026/full-to-hybrid-attention.html
- Review date: 2026-11-12
- Scan status: partially scanned

## Executive synthesis

Raschka reports a continuing shift in the open-LLM architectures he surveyed from dense global attention in every layer toward hybrid stacks and, increasingly, stacks with no dense global-attention layers. His post describes a 50/50 split in the second half of 2026 between (a) models retaining some full/global attention in a hybrid and (b) models using no full attention. The post frames the direction as an effort to reduce the cost of long contexts, especially for long documents, conversations, large codebases and tool-using agents.

The companion article clarifies the chart's categories:

- **Full attention throughout:** Global MHA, GQA, dense MLA or CCA in every layer.
- **Some full attention:** global attention mixed with sliding-window/chunked attention, Gated DeltaNet, KDA, Mamba-2, Lightning Attention, convolutions or sparse attention.
- **No full attention:** zero dense global-attention layers.

The 50/50 figure is a snapshot of the author's selected open-model roundup, not a census of all released models. It should be cited as an observed trend in that sample, not as a universal market statistic.

## Technical interpretation

Two distinct efficiency mechanisms must remain separate:

1. **Attention-computation reduction.** Sliding windows, chunking and sparse/token-selection methods restrict which positions participate in expensive attention operations. Sparse attention can still retrieve distant information when the selection mechanism exposes the relevant positions; it is not equivalent to a strict local window.
2. **Bounded recurrent state.** Recurrent/state-space or linear-recurrent components such as Gated DeltaNet carry a fixed-size state rather than retaining an ever-growing key/value representation of the entire history. This changes the memory-growth profile, but compressing history can make exact retrieval of arbitrary past details harder.

Hybrid architectures combine mechanisms to trade off cost, long-range access and retrieval fidelity. "No full attention" does not mean "no sequence mixing" or "no ability to use context"; it means there are no dense global-attention layers under the author's taxonomy.

## Critical qualifications

- Do not conflate sparse attention with recurrent state compression: one changes the attended positions/computation, the other changes how historical information is represented and retained.
- Do not infer that every hybrid model has constant memory, linear total cost, or identical scaling. Complexity depends on the precise attention pattern, state dimensions, sequence length, implementation, batching and serving stack.
- A fixed-size state is not a lossless KV cache. Exact associative recall and correction of earlier facts remain important evaluation targets.
- The post's percentages depend on the author's model sample, inclusion criteria and architecture classification. The complete roundup is still described as forthcoming.
- Production throughput is not determined by architecture alone; kernels, cache management, batching, hardware and runtime support can change the practical result.

## Educational value for LLM Lab

This source is useful as a current architecture-trend case study linking:
- dense self-attention and KV-cache growth;
- sliding-window, chunked and sparse attention;
- recurrent/state-space sequence models (especially Gated DeltaNet and Mamba-2);
- hybrid layer schedules;
- long-context retrieval and agent/tool-use workloads;
- the distinction between theoretical memory/computation savings and measured serving quality.

Recommended treatment: integrate as a dated, critical source note and use it to motivate a comparative lesson/experiment. Avoid presenting the chart as a definitive taxonomy or the percentages as a benchmark.

## Suggested experiment

Compare a dense-attention baseline, a local/sliding-window model and a hybrid/recurrent design under matched parameter count and serving conditions. Measure:
- prefill latency and throughput as context length grows;
- decode latency and concurrent-request throughput;
- KV-cache and recurrent-state memory;
- exact retrieval of randomly placed facts;
- retrieval after a fact is corrected later in the context;
- multi-hop retrieval across long tool-call traces.

Keep task accuracy, retrieval fidelity, memory and latency as separate axes. Include a control for context truncation and ensure that models receive equivalent information.

## Provenance and limitations

The supplied LinkedIn post text was directly retrieved, including the visible explanatory comments. The author's companion article was also retrieved and supplies the chart legend and fuller explanation. The chart image itself was not independently downloaded or numerically re-analysed; the model list, sample size, inclusion criteria and underlying data were not audited. No model was run and no benchmark was reproduced. Text, chart and image reuse rights were not established; retain link-only treatment.

# FlashAttention benchmark protocol

**Status:** experiment design only; no measurements have been run.  
**Purpose:** compare a materialized attention reference, PyTorch scaled-dot-product attention (SDPA), and an explicitly selected FlashAttention backend without confusing API dispatch, algorithmic correctness, or workload-specific speed.

## 1. Research questions

1. Under which shapes and dtypes does an IO-aware exact attention kernel reduce latency and peak temporary memory relative to a materialized reference?
2. How do the results differ between forward-only inference, forward-plus-backward training, prefill, and one-token decode with a KV cache?
3. Does the selected SDPA backend actually use FlashAttention for each tested configuration?
4. Are output and gradient differences within predeclared numerical tolerances?

Do not reduce the conclusion to one universal “speedup” number.

## 2. Implementations and baselines

- **Reference:** small, readable PyTorch implementation that explicitly computes scaled QKᵀ scores, applies the same mask, softmaxes, and multiplies by V. It is a correctness baseline, not a performance competitor for long sequences; cap its sequence lengths to avoid out-of-memory failures.
- **SDPA:** `torch.nn.functional.scaled_dot_product_attention` with the default eligible backend selection. Record the PyTorch version and the selected/eligible backend conditions.
- **FlashAttention-selected:** use the documented PyTorch backend-selection context or an independently documented FlashAttention implementation to require the Flash backend. Treat unsupported shapes/dtypes/masks as an eligibility result, not as a failed timing sample. Record the exact API and library version.

The three paths must receive identical Q, K, V, mask semantics, scale, dropout setting, dtype and layout. Do not compare causal and non-causal attention accidentally.

## 3. Workload matrix

Keep the initial matrix small and expand only after the harness is stable.

| Phase | Query length | Key/value length | Forward | Backward | Main interpretation |
|---|---:|---:|---|---|---|
| Training | S | S | yes | yes | Activation memory and recomputation trade-off |
| Inference prefill | S | S | yes | no | Prompt processing throughput/latency |
| Decode with KV cache | 1 | S | yes | no | Single-token attention against cached history |

Vary one dimension at a time in the first pass:

- sequence lengths: short, medium and long values supported by the device;
- batch size and number of heads;
- head dimension;
- supported dtypes (for example FP32, FP16 and BF16, where hardware supports them);
- causal and non-causal masks as separate conditions.

Record exact tensor shapes, strides, contiguous/non-contiguous layout, device capability and all mask conventions. Do not infer performance at sequence lengths that were not measured.

### Decode-specific control

For decode, construct the K/V cache as an explicit input and distinguish attention workspace from cache storage. A query of length one attending to all valid cached keys is not the same workload as square prefill. Define the mask so every valid cached key is visible; test any sliding-window or padding constraints separately.

## 4. Correctness before performance

- Use deterministic generated inputs with recorded seeds.
- Compare each optimized output with the materialized reference on identical inputs.
- For training, compare gradients with respect to Q, K and V as well as outputs.
- Define tolerances before running the benchmark and report max absolute and relative error. Tolerances may differ by dtype; do not silently loosen them after observing a failure.
- Test causal masking explicitly: future positions must not contribute.
- Test non-square query/key lengths, padding and any supported attention bias independently.
- Record unsupported configurations and numerical failures; do not discard them from the report.

Mathematical exactness does not imply bitwise-identical floating-point outputs across kernels, accumulation orders and dtypes.

## 5. Measurement procedure

1. Record GPU model, compute capability, driver, CUDA runtime, PyTorch version, FlashAttention implementation/version, operating system and Python version.
2. Use a clean, locked environment and save the exact command/configuration.
3. Warm up each implementation and shape before timing. Exclude compilation and first-use initialization from steady-state timing, but report them separately if relevant.
4. Synchronize the GPU around measurements; use CUDA events or a suitable benchmark harness rather than unsynchronized host wall-clock timing.
5. Run multiple repetitions, randomize implementation order where practical, and report median plus dispersion (for example interquartile range or p90), not only the best run.
6. Reset and record peak allocated and reserved CUDA memory for each run. Report baseline allocation and incremental peak; explain what is included (inputs, outputs, cache, workspace).
7. Avoid concurrent GPU workloads and record thermal/power or clock constraints if they are material.
8. Repeat the run when an apparent improvement is close to run-to-run noise.

Separate first-call latency, steady-state latency and throughput. Do not compare measurements taken with different synchronization or warm-up policies.

## 6. Metrics

Report at least:

- forward latency and tokens/second where meaningful;
- forward-plus-backward latency for training;
- peak allocated and reserved GPU memory, with the accounting boundary stated;
- output and gradient max absolute/relative error;
- backend selected or forced, plus unsupported/eligibility status;
- per-shape repetitions and variability.

For prefill, define throughput denominator (input tokens processed). For decode, report per-token latency and the cache length. Do not combine these into one average.

## 7. Interpretation guardrails

- FlashAttention reduces data movement and avoids materializing the full dense attention score/probability matrices in high-bandwidth memory; it does not remove dense pairwise attention arithmetic.
- SDPA is an interface with backend dispatch. An SDPA call alone is not evidence that FlashAttention ran.
- Treat FlashAttention generations separately. FlashAttention-2 improves parallelism/work partitioning; FlashAttention-3 uses Hopper-specific asynchronous execution and low-precision techniques. Record the exact implementation/version and GPU architecture; do not compare a FlashAttention-3 result on H100 as though it were the same kernel as FlashAttention-2 on another device.
- Peak memory includes more than the attention matrix. Q/K/V, outputs, model activations, allocator reservations and KV cache must be accounted for separately.
- Training, prefill and decode have different shapes and bottlenecks. Results from one phase do not establish results for another.
- Speedups depend on hardware, sequence length, head dimension, batch, dtype, masks, layout, software version and baseline quality.
- A CPU run can test numerical logic but cannot establish GPU kernel speed or GPU memory behavior.
- A Python loop over tiles is an explanatory implementation, not a substitute for a fused GPU kernel.

## 8. Reproduction record

Store each run under a stable experiment directory, for example:

`experiments/2026-11-13-flashattention-io-benchmark/`

Include:

- README with question, hypotheses, environment and exact commands;
- machine-readable configuration and result files;
- implementation commit/version and backend-selection evidence;
- correctness report before timing tables;
- raw timing samples or sufficient summary statistics;
- failures, unsupported configurations and limitations.

Do not commit large checkpoints or unbounded raw traces. No result should be described as reproduced until the experiment has actually run on the stated hardware.

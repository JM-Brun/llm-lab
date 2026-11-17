# Train a small GPT on a remote GPU with Hugging Face Jobs

**Status:** operational recipe documented from the source repository; not independently executed by LLM Lab.  
**Reference repository:** [scienceetonnante/nanogpt-jobs](https://github.com/scienceetonnante/nanogpt-jobs)  
**Revision inspected:** `master`, tree `781d0e4fe0513de8ec74654e75a39e4aa1809853`  
**Companion:** [video source review and evidence limits](../../docs/source-reviews/huggingface-jobs-nanogpt-video-2026-11.md)

## Why this method?

It addresses a common constraint: the training code exists, but the local machine lacks a sufficiently fast GPU or enough memory. The idea is to keep the Python training program and move only its execution to an on-demand managed GPU.

This is an **optional alternative route** in the Build path:
- **local:** develop, understand and test on CPU/MPS/available GPU;
- **managed remote GPU:** run a more expensive experiment without administering a server;
- **back locally:** retrieve checkpoints and analyse results.

It does not replace understanding the training loop, scientific evaluation or local tests.

## Execution architecture

```text
Local machine
  ├── Python code + requirements.txt
  ├── hf sync ─────────────────┐
  └── run_on_hf.sh             │
                               ▼
                      Private Hub Storage Bucket
                        ├── code/
                        └── out/
                               ▲
                               │ mounted volume
                               ▼
                      Hugging Face Job
                        ├── uv / Python image
                        ├── explicitly selected GPU
                        ├── dependency installation
                        ├── TinyStories download from the Hub
                        └── training → out/model.pt
                               │
                               ▼
                      hf sync : retrieve locally
```

The bucket has two distinct roles: staging code into the job and retaining artifacts beyond the machine's lifetime. TinyStories is downloaded by the program through `datasets`; the launcher does not copy it from the local disk.

## What the inspected repository does

| File | Responsibility |
|---|---|
| `train.py` | Downloads TinyStories, tokenizes, defines the GPT, trains and saves `out/model.pt` |
| `requirements.txt` | Declares `torch`, `numpy`, `tiktoken` and `datasets` |
| `run_on_hf.sh` | Creates/syncs the bucket, selects the GPU, launches the job and mounts storage |
| `sample.py` | Reloads the checkpoint and generates three stories |

### Model and training configuration

The source code sets:

- 8 Transformer blocks, embedding dimension 512, 8 attention heads;
- context length 512 and GPT-2 vocabulary of 50,257 tokens;
- about 51 million parameters, with tied token-embedding and output-head weights;
- learned positional embeddings (this example does not use RoPE);
- causal attention through `scaled_dot_product_attention`;
- batch size 16 sequences, or 8,192 tokens per update;
- AdamW, peak learning rate (6\times10^{-4}), warm-up then cosine decay;
- gradient-norm clipping at 1;
- on CUDA, `torch.compile` and bfloat16 autocast.

Training data is downloaded from `roneneldan/TinyStories`, tokenized with the GPT-2 encoding, concatenated into one large array, then sampled as random windows. The step count is computed from total token count and batch size; this is not a strict sequential pass over every possible window.

## Prepare and launch

### Prerequisites

1. A Hugging Face account permitted to use Jobs, with a PRO subscription or sufficient credits according to the account's current terms.
2. A recent Hugging Face CLI, `uv`, Bash and an authenticated session.
3. A maximum budget defined before launch.

From the project directory:

```bash
hf auth login
hf jobs hardware
```

Use `hf jobs hardware` to inspect available flavors and their prices at launch time. The script deliberately has no default GPU: a flavor must be selected explicitly.

### Remote launch

```bash
./run_on_hf.sh train.py a100-large
```

The launcher defaults to a two-hour timeout. It accepts an explicit duration and another flavor:

```bash
./run_on_hf.sh train.py l4x1 4h
```

The script:
1. creates a private bucket named after the project directory;
2. syncs code into `code/`, excluding hidden files, Python caches and local outputs;
3. launches a detached job in `ghcr.io/astral-sh/uv:python3.12-bookworm`;
4. mounts the bucket in the container and links `out/` to the persistent bucket directory;
5. installs dependencies from `requirements.txt` and runs the same Python file.

The job is asynchronous. The launcher prints its ID; follow logs with:

```bash
hf jobs logs -f <job-id>
```

### Retrieve and use the checkpoint

After the job:

```bash
hf sync hf://buckets/<username>/nanogpt-jobs/out ./out
uv run --with-requirements requirements.txt sample.py "Once upon a time"
```

The bucket name depends on the local directory name and Hugging Face username. Verify the actual path before syncing.

## Adapt the pattern to another project

The launcher is deliberately generic. To reuse it:

- the program must write results to `out/` (or the `OUT` variable must be changed);
- code and dependencies must live in the synced directory;
- data must be downloadable from the Hub or a URL, or explicitly placed in storage accessible to the job;
- the script must be compatible with the selected image, Python version and GPU flavor;
- the output path must point to the mounted persistent volume.

“No code changes” is therefore conditional: the program must already be portable, its paths and dependencies must be compatible, and its data must be accessible.

## Checks before and after execution

### Before spending credits

- Run the script locally on CPU/MPS/GPU with a reduced configuration.
- Check imports, data download, tensor dimensions and actual creation of `out/`.
- Check that `sample.py` can reload the checkpoint.
- Read the flavor price, GPU type and timeout; set a cost limit.
- Never put a personal token in the repository or script. Use the provider's documented secrets mechanism when the job needs access to a private resource.

### During the job

- Check status, logs, visible GPU and memory use.
- Monitor tokens/second, losses, OOM errors and progress toward the next checkpoint.
- Plan for timeout, failure or interruption; a detached job is not guaranteed to run to completion.

### After the job

- Check checkpoint presence, size and timestamp in the bucket.
- Download artifacts and test local loading.
- Record code commit, dependency versions, dataset, flavor, timeout, logs, billed duration, cost and metrics.
- Keep training, validation and test data separate.

## Scientific limitations of the repository

This demonstration is primarily an orchestration and portability example. The inspected code has several limitations that should be explicit:

1. **No independent validation.** The printed loss is for the current training batch; no separate validation set or test metric is implemented.
2. **No evidence of generalization.** Falling training loss or generated stories do not establish model quality.
3. **Host memory.** The script tokenizes the whole corpus and concatenates it in memory before training; container RAM matters as well as GPU VRAM.
4. **Periodic checkpointing.** The model is saved every 2,000 steps and at the end. An interruption between saves can lose work since the previous checkpoint.
5. **Incomplete reproducibility.** Random seeds, exact package versions and a complete experiment configuration are not fixed by the repository.
6. **Runtime and cost.** The “about $1” figure depends on the flavor and actual billed duration; it is not a universal rate.

The official A100-large pricing page consulted listed an 80 GB A100 at $2.50/hour, billed per minute while Starting and Running. At that rate, 30 minutes is about $1.25, excluding any other charges. Always recheck [Jobs pricing](https://huggingface.co/docs/hub/en/jobs-pricing).

## Proposed LLM Lab learning experiment

Compare three environments with exactly the same code and protocol:

| Variant | Question |
|---|---|
| Local CPU | Does the pipeline work without an accelerator? |
| Local GPU (if available) | What speedup does local acceleration provide? |
| Managed GPU (Jobs) | How much time is saved, and at what total cost? |

For an interpretable comparison:
- pin the code commit, data, dimensions, batch and number of steps;
- measure data preparation separately from training;
- measure tokens/second, training loss and validation loss;
- record actual billed cost, not only the displayed hourly rate;
- repeat measurements when comparing performance;
- separate startup, corpus download, compilation and GPU compute time.

**Testable hypothesis:** a remote GPU greatly reduces training time under a bounded budget, but the real benefit depends on startup, data loading, compilation and billed duration.

## Sources

- [NanoGPT Jobs repository](https://github.com/scienceetonnante/nanogpt-jobs) — README, `train.py`, `run_on_hf.sh`, `requirements.txt`, `sample.py`.
- [Hugging Face Jobs: run and manage jobs](https://huggingface.co/docs/huggingface_hub/en/guides/jobs).
- [Jobs configuration](https://huggingface.co/docs/hub/en/jobs-configuration).
- [Jobs pricing](https://huggingface.co/docs/hub/en/jobs-pricing).

**Evidence level:** source repository statically inspected; LLM Lab did not execute the job or spend credits.

# Source review — GPU-POOR? NO PROBLEM! Training with Hugging Face Jobs

**Source:** YouTube video, *GPU-POOR? NO PROBLEM!... thanks to 🤗 Jobs*  
**URL:** https://www.youtube.com/watch?v=7Yx_7byZiFU  
**Creator:** David Louapre (attribution corroborated by his public post introducing the video)  
**Reviewed:** 2026-11-16  
**Status:** partial, transcript-assisted. The description and chapter timestamps were supplied by the user; a third-party page reproducing a transcript attributed to the Hugging Face YouTube video was inspected, alongside the creator's public post and current official Hugging Face documentation. The audiovisual video and the truncated GitHub code URL were not inspected.

## Evidence boundary

The supplied description presents a NanoGPT-like training run on an A100 through Hugging Face Jobs. A third-party page reproducing a transcript attributed to the Hugging Face YouTube video adds these details: a GPT-2-style model of about 50M parameters, 8 layers, embedding dimension 512, GPT-2 tokenizer, TinyStories dataset, cosine learning-rate schedule with warm-up, progress output every 100 steps, checkpoint/output saves every 2,000 steps and at the end, and generated samples during training. The creator describes a local run as taking about 12 hours on his Mac and the remote A100 run as taking about 30 minutes for a little over $1. The transcript says the generic launcher creates a Storage Bucket, syncs project files except the existing `out` directory, requests the GPU job, mounts the bucket, runs the Python script using `uv` and `requirements.txt`, and stores the `out` directory in the bucket; after completion, the user syncs outputs back locally. David Louapre's public post independently introduces the same video. Supplied chapters: model/training code (01:21), Jobs (02:57), shell script (04:15), run/results (05:35). The code URL ends in `https://github.com/scienceetonnante/n...`; its repository cannot be identified reliably. No audiovisual inspection, code execution, job launch or reproduction is claimed.

## Technical reconciliation

Hugging Face Jobs runs a command in a selected container image and hardware flavor on managed infrastructure. It can be launched through `hf jobs run` or `huggingface_hub.run_job`; jobs are asynchronous and expose status/logs. Long training runs need an explicit timeout rather than relying on the documented 30-minute default.

Official references:
- https://huggingface.co/docs/huggingface_hub/en/guides/jobs
- https://huggingface.co/docs/hub/en/jobs-configuration
- https://huggingface.co/docs/hub/en/jobs-pricing

Current documented A100-large hardware is one A100 with 80 GB GPU memory at **$2.50/hour**, billed per minute while the job is Starting or Running. The video's approximate $1 is therefore a run-specific estimate, not the current general A100 hourly rate. At the documented rate, $1 corresponds to about 24 billed minutes.

Managed execution avoids administering a remote machine or setting up SSH for this workflow; it does not eliminate data access, authentication or artifact persistence. In the demonstrated design, the Storage Bucket is the explicit bridge: local project sync → mounted bucket in the job → output/checkpoint writes → local sync after completion. Training data is fetched from the Hub through `datasets`, while code and outputs travel through the bucket. The bucket is described in the transcript as persistent after the compute job ends. This is a transcript-level account, not an inspection of the script or an independent test of bucket semantics. Private resources still require safe authentication, and outputs must be written to the mounted persistent location.

## Reconstructed example (transcript-level, not code-verified)

| Element | Reported configuration |
|---|---|
| Model | GPT-2-style, approximately 50M parameters; 8 layers; embedding dimension 512 |
| Tokenizer | GPT-2 tokenizer |
| Dataset | TinyStories, loaded from the Hugging Face Hub with `datasets` |
| Training | PyTorch-style loop; cosine learning-rate schedule with warm-up; periodic progress and checkpointing |
| Runtime | `uv` plus `requirements.txt`; same Python training command locally and remotely |
| Outputs | `out/` directory linked to the mounted Storage Bucket; sync back after the job |
| Remote hardware | A100-large; transcript reports about 30 minutes and a little over $1 |

The transcript reports progress every 100 steps and saves/checkpoints every 2,000 steps and at the end. Exact hyperparameters, training-step count, validation protocol, script contents and logs are not exposed in the retrieved transcript, so they remain unknown.

## Pedagogical value

The key idea is the separation of **training logic** from **execution infrastructure**:

1. Develop and smoke-test the training program locally.
2. Package the runtime environment and command in a repeatable launcher.
3. Select remote hardware independently of the model code.
4. Submit the job and inspect status/logs.
5. Persist outputs and record runtime, hardware, metrics and cost.

Local GPU scarcity is a constraint on local execution, not necessarily a barrier to running a controlled experiment.

## Qualifications and failure modes

- “No code changes” is conditional on compatible dependencies, paths, device selection and runtime configuration.
- “No data transfer” may mean no manual laptop-to-SSH copy; the job still needs an explicit data-access path.
- Checkpoint and result persistence must be deliberate; ephemeral storage is not a durable artifact store.
- Keep secrets out of scripts and source control; use job secrets and least-privilege tokens.
- Verify the GPU is actually visible and used; inspect memory, utilization, throughput and OOM behavior.
- Distinguish a smoke test, tiny-batch overfit and meaningful training with held-out validation.
- Compute cost depends on billed startup/runtime and selected flavor; include retries and relevant storage/network charges.

## Integration decision

**Integrate by reference as an optional operational case study, not a new core learning stage or an implementation claim.** It complements the existing training-loop and experiment-protocol material once a working tiny GPT exists. Keep model/training code provider-independent and the shell launcher thin. A future recipe should document image, hardware, command, timeout, secrets, data access, checkpoint persistence and cost accounting. Preserve a CPU smoke test so the public lab does not depend on paid GPU access.

Do not add Hugging Face Jobs as a mandatory dependency or imply that LLM Lab currently trains NanoGPT.

## Validation still required

Recover the complete repository URL; inspect the script, training code, dependencies, data-loading path and output handling; compare the transcript with the actual video; verify the run duration and cost from logs; then execute only under an explicit spending limit. A third-party transcript is now available, but it is not a substitute for audiovisual inspection or code review. The creator attribution is corroborated, but the linked code repository remains unidentified. No independent reproduction is claimed.


## Code review update — repository recovered (2026-11-17)

The full URL was subsequently supplied: https://github.com/scienceetonnante/nanogpt-jobs. The repository was inspected statically on its `master` branch (tree SHA `781d0e4fe0513de8ec74654e75a39e4aa1809853`). Files inspected: README, `train.py`, `run_on_hf.sh`, `requirements.txt`, and `sample.py`. This supersedes the earlier statement that the repository could not be identified. It does not supersede the limitations about not executing the code or launching a paid job.

### Confirmed implementation details

- `train.py`: 8 Transformer blocks, embedding width 512, 8 heads, context length 512, GPT-2 tokenizer/vocabulary (50,257), learned absolute positional embeddings, tied token embedding/output weights, causal attention via PyTorch scaled dot-product attention; approximately 51M parameters.
- Dataset: `roneneldan/TinyStories`, loaded with `datasets`; each story is encoded with the GPT-2 tokenizer and an end-of-text token, concatenated into a single `uint16` NumPy array, then random windows of 513 tokens are sampled for next-token training.
- Training: batch size 16 × 512 context tokens = 8,192 tokens per update; AdamW; peak learning rate 6e-4; 1,000-step linear warm-up then cosine decay to 10% of peak; gradient norm clipping at 1.0. CUDA path uses `torch.compile` and bfloat16 autocast.
- Progress prints every 100 steps. Samples and checkpoints are written every 2,000 steps; a final checkpoint is written after the loop.
- `run_on_hf.sh`: creates a private Hub bucket named from the current directory, syncs the code into `code/` (excluding hidden files, Python caches and local `out/`), launches a detached Jobs container using `ghcr.io/astral-sh/uv:python3.12-bookworm`, mounts the bucket, links `out/` to the persistent bucket output directory, installs `requirements.txt` with uv and runs the selected Python file. Default timeout is two hours; flavor is mandatory. It prints the job ID and commands to follow logs and retrieve outputs.
- `sample.py`: loads `out/model.pt` on CPU and generates three samples from a supplied prompt or a default prompt.

### Corrections and important nuance

1. The earlier transcript-derived details are now corroborated by source code where noted. The repository is a direct code source, not merely a transcript rendering.
2. The README says the training data is about two million short stories; the implementation downloads and tokenizes the full training split and materializes the concatenated token array in host RAM. This creates a host-memory requirement in addition to GPU VRAM.
3. The number of training steps is derived from total token count divided by batch tokens, but each batch consists of independently sampled random windows. Calling this “one pass” is a step-budget heuristic, not a sequential traversal of every unique window.
4. The script reports the current training-batch loss only. It defines no validation/test split and computes no held-out metric. Generated samples are qualitative illustrations, not a generalization evaluation.
5. Checkpoints are periodic (every 2,000 steps) and final. If a job is interrupted between checkpoints, progress since the last save may be lost.
6. No explicit random seeds or pinned dependency versions are provided in the repository's `requirements.txt`; exact bitwise reproducibility is not established.
7. The launcher uses a two-hour default timeout and a required explicit hardware flavor. The README requires a Hugging Face PRO subscription or credits. The bucket is the code-staging and artifact-persistence boundary; TinyStories is fetched separately from the Hub by the training process.

### Pedagogical integration decision

Integrate as an optional remote-execution recipe that can be applied after a learner has a working training loop. It should not be presented as a new training algorithm or as a replacement for local CPU smoke tests. Preserve three separable concerns:
- model/training implementation (portable Python);
- execution adapter (image, hardware flavor, timeout, job submission);
- data/artifact plane (Hub dataset download, mounted bucket, checkpoints and retrieval).

A controlled LLM Lab comparison should use a fixed commit, dataset and number of steps across CPU/local GPU/managed GPU, record startup and data-loading time separately from training time, report tokens/second and held-out validation loss, and record actual billed cost. The source repository itself does not implement this complete comparison.

### Evidence status

- Repository contents: inspected statically.
- Shell launcher and training code: inspected, not executed.
- Hugging Face account, job logs and reported A100 run: not independently inspected.
- LLM Lab reproduction: not performed; no paid job launched.

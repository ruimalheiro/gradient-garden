# Gradient Garden

Gradient Garden is an open research codebase for experimenting with machine learning models, training methods, data, and evaluation.

The goal is to keep the important parts of the research stack easy to inspect and modify: model architectures, training objectives, optimizers, dataset preparation, distributed execution, checkpointing, inference, and evaluation all live in the same codebase.

The project currently focuses on CUDA-based language-model training, but it is not intended to be limited to language models. The codebase is expected to evolve as I explore new architectures, modalities, training methods, datasets, and evaluation setups.

## Quick start

Gradient Garden uses Python 3.11 or above.

Create and activate an environment:

```bash
conda create -n gradient-garden python=3.11
conda activate gradient-garden
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

The preferred way to run an experiment is through a recipe. A recipe contains both the experiment configuration and the data required by it.

Prepare the data for the pretraining debug recipe:

```bash
python prepare_datasets.py --recipe recipes/pretraining/debug.yaml
```

Run training:

```bash
python train.py --recipe recipes/pretraining/debug.yaml
```

Debug recipes are also available for SFT and DPO:

```text
recipes/pretraining/debug.yaml
recipes/instruct/debug.yaml
recipes/dpo/debug.yaml
```

For the complete CLI options:

```bash
python prepare_datasets.py --help
python train.py --help
python generate.py --help
python evaluate.py --help
python gradio_serve.py --help
```

## Capabilities

### Training

Current training workflows:

- Pretraining
- Supervised fine-tuning / instruct tuning
- Direct Preference Optimization (DPO)
- Optional knowledge distillation
- Gradient accumulation
- Early stopping
- Checkpoint save, load, and resume
- PyTorch compilation support
- Torch profiler integration
- Weights & Biases integration

Supported training precision:

- BF16
- FP16
- FP32

Distributed execution:

- Single GPU
- Multi-GPU
- Multi-node
- Distributed Data Parallel (DDP)
- FSDP2

### Models

Gradient Garden uses a model registry so training and inference are not tied to a single architecture.

Current implementations include:

#### Tendril

A dense decoder-only transformer with:

- Grouped-query attention (GQA)
- Rotary positional embeddings (RoPE)
- Configurable tied embeddings
- KV-cache-compatible autoregressive decoding

#### TendrilMoE

A Mixture-of-Experts variant of Tendril with:

- Configurable number of experts
- Top-k routing
- Expert feed-forward networks
- Load-balancing auxiliary loss
- Router z-loss

#### Hugging Face model wrapper

A wrapper for using supported Hugging Face causal language models with Gradient Garden training and inference.

### Post-training

Current post-training functionality includes:

- Supervised fine-tuning
- DPO
- LoRA
- Optional teacher-model distillation
- Configurable system prompts
- Gradient Garden and Hugging Face chat-template formatting

### Optimization

Supported optimizers include:

#### AdamW

- Configurable minimum and maximum learning rate
- Weight decay
- Configurable betas
- Fused implementation when available

#### Muon

- Applied to supported matrix parameters
- Separate learning-rate and scheduler configuration
- AdamW handles the remaining trainable parameters

Supported learning-rate schedules:

- Cosine
- WSD

### Inference

Gradient Garden supports:

- Batched autoregressive generation
- KV-cache generation
- Temperature sampling
- Top-p sampling
- Repetition penalty
- No-repeat n-gram constraints
- Base-model and instruct-style prompting
- Gradient Garden checkpoints
- Supported Hugging Face checkpoints

A small Gradio chat interface is also available for interactively testing instruct models.

### Evaluation

Gradient Garden supports validation during training and standalone benchmark evaluation.

#### Multiple-choice evaluation

These are scored as causal language-model likelihood tasks rather than using the instruct chat template:

- HellaSwag
- WinoGrande
- ARC-Challenge

#### Instruction-following evaluation

These generate model responses using the instruct pipeline and score the decoded output with deterministic checkers:

- IFEval (no external)
- Custom SFT smoke evaluation

The custom SFT smoke evaluation includes small sanity-check tasks such as:

- Exact answers
- Formatting constraints
- Rewriting
- Summarization
- Role-leak detection

### Data preparation

Dataset preparation currently supports:

- Hugging Face datasets
- Dataset-specific adapters and transforms
- Dataset revision pinning
- Deterministic train/validation splitting
- Weighted dataset mixing
- Explicit per-source token budgets
- Token accounting for supervised training data
- Tokenized pretraining shards
- Resumable pretraining preparation
- Per-source preparation progress
- Per-source physical starting offsets
- Multi-source continuation datasets
- Large Parquet-backed Hugging Face sources
- Parquet cursor/search-based resume

## Recipes

A recipe is the preferred way to describe an experiment.

Recipes contain two main sections:

```yaml
name: ...
description: ...

config:
  # model, runtime, training, optimization, evaluation, etc.

data:
  # dataset preparation and dataset mix
```

`config` maps to the nested `GlobalConfig` used by the training runtime.

`data` describes the datasets needed by the experiment, their preparation and mixing settings, and optional evaluation datasets.

The normal workflow is:

```text
dataset preparation
        ↓
training
        ↓
evaluation / generation
```

For example:

```bash
python prepare_datasets.py --recipe recipes/pretraining/debug.yaml
python train.py --recipe recipes/pretraining/debug.yaml
```

Using the same recipe for preparation and training keeps the training configuration and its data definition together.

Current recipes include:

```text
recipes/
├── pretraining/
│   ├── debug.yaml
│   └── tendril/
│       └── 480m_climbmix_pretraining_200b.yaml
├── instruct/
│   ├── debug.yaml
│   ├── tendril/
│   │   └── 480m_smoltalk_assistant_only_gg_template.yaml
│   └── smollm2-360m/
│       └── smoltalk_assistant_only_gg_template.yaml
└── dpo/
    ├── debug.yaml
    ├── tendril/
    │   └── tendril_480m_ultrafeedback_binarized_dpo_gg_template.yaml
    └── smollm2-360m/
        └── ultrafeedback_binarized_dpo_gg_template.yaml
```

## Dataset preparation and mixing

Training datasets are prepared before being consumed by the trainer.

Pretraining preparation follows this path:

```text
Hugging Face / Parquet source loading
                ↓
       DatasetSourceWrapper
                ↓
          DatasetWrapper
                ↓
       shard_and_tokenize
                ↓
        train / val shards
```

### `DatasetSourceWrapper`

`DatasetSourceWrapper` represents one physical dataset source.

It handles:

- Source identity and metadata
- Dataset revision
- Physical source position
- Configured starting offset
- Committed source progress
- Resume state
- Normal Hugging Face skipping
- Parquet cursor-based positioning

Physical progress is tracked independently for each source.

### `DatasetWrapper`

`DatasetWrapper` handles logical source selection.

The global mixture position is tracked separately from the number of physical documents committed by each source.

This distinction is important for resumable token-budget mixing because a source can be complete while later logical positions still need to advance deterministically.

### `shard_and_tokenize`

`shard_and_tokenize` handles:

- Tokenization
- Deterministic train/validation routing
- Train and validation shard writing
- Global mix token targets
- Per-source token targets
- Token accounting
- Preparation checkpoints
- Resume state

## Reproducible dataset revisions

Pretraining sources can pin a Hugging Face dataset revision:

```yaml
datasets:
  karpathy/climbmix-400b-shuffle:
    default:
      weight: 1.0
      transforms:
        revision: 915333b4f8b8684f39aeaafea600fea6f43fb703
```

Using a commit SHA pins the recipe to the exact dataset snapshot used for preparation.

If `revision` is omitted, Gradient Garden uses the Hugging Face `main` revision at preparation time.

In both cases, the revision is resolved through the Hugging Face API to an immutable commit SHA. That resolved revision is used to load the source and stored in the preparation metadata.

On resume, the source metadata is checked again. Changing the dataset revision underneath an existing preparation therefore raises a metadata mismatch instead of silently continuing from different data.

For long-running experiments, pinning the dataset revision in the recipe is recommended.

## Dataset mixing strategies

Gradient Garden supports two ways of defining source composition.

### Weighted interleave

The default strategy is:

```yaml
datasets_common_settings:
  mix_strategy: legacy_interleave
```

Each source has a weight:

```yaml
datasets:
  source_a:
    default:
      weight: 0.7

  source_b:
    default:
      weight: 0.3
```

The weights are normalized into source-selection probabilities.

This controls how often examples or documents are selected from each source. It does not guarantee a specific token contribution from each source.

An optional global training-token target can also be configured:

```yaml
datasets_common_settings:
  target_tokens: ...
```

The target limits the prepared mixture while preserving the weighted source-selection behavior.

For SFT and DPO, this target is measured in supervised tokens.

For pretraining, it is the prepared training-token target handled by the shard writers.

### Per-source token budgets

The `token_budget` strategy gives each source an explicit token target:

```yaml
datasets_common_settings:
  mix_strategy: token_budget

datasets:
  source_a:
    default:
      target_tokens: 10_000_000_000

  source_b:
    default:
      target_tokens: 2_000_000_000
```

In this mode:

- Per-source weights are not used.
- Every active source has its own token target.
- The common/global `target_tokens` is not used.
- Sources complete independently.
- Whole examples or documents are kept when they cross a target, so the final counts can overshoot slightly.

The token unit depends on the training stage:

| Stage | Per-source token-budget unit |
| --- | --- |
| Pretraining | Training tokens produced from source documents |
| SFT / instruct | Supervised tokens |
| DPO | Supervised tokens from chosen and rejected responses |

For supervised stages, a supervised token is a token whose label is different from the configured `ignore_index`.

### Pretraining token-budget scheduling

Pretraining token-budget mixing uses deterministic round-robin scheduling.

When a source reaches its target:

- It stops consuming physical documents.
- It remains part of the logical scheduling sequence.
- Later positions for that source become logical no-op positions.

This preserves deterministic logical ordering across interruption and resume.

Physical source exhaustion is separate from token-target completion.

If a source runs out of data before reaching its configured token target, preparation fails and reports the actual and target token counts.

### Target overshoot

Token budgets operate on document/example boundaries.

For pretraining, a whole document is kept if it crosses the source target.

For SFT and DPO, a whole example is kept if it crosses the supervised-token target.

Therefore the final number of tokens can be slightly higher than the configured target.

## Validation behavior

### Pretraining

Pretraining documents are deterministically routed to train or validation.

With per-source token budgets:

- Only training tokens count toward the source target.
- Validation tokens do not consume the source training budget.
- A source may need to read more physical data than its token target before enough training tokens have been produced.

When a global pretraining target is configured, the train and validation shard writers maintain corresponding targets based on the validation ratio.

### SFT and DPO

SFT and DPO first prepare tokenized examples and then perform a deterministic train/validation split.

When a global or per-source token target is configured, the selection budget is adjusted before the split so the expected training portion remains close to the configured supervised-token target.

Because splitting happens on whole examples, the final training-token counts are not guaranteed to match the configured targets exactly.

## Resumable pretraining preparation

Pretraining dataset preparation is resumable.

Preparation state includes:

- Global committed progress
- Logical mixture position
- Per-source metadata
- Per-source committed physical positions
- Per-source token counts
- Per-source training-token counts
- Train and validation writer state
- Buffered shard data
- Parquet cursor state when applicable

The logical mixture position is stored independently from committed document counts.

On resume:

- Each source continues from its own committed position.
- Completed token-budget sources are reconstructed from persisted training-token counts.
- Completed sources are not consumed again.
- Logical scheduling resumes from the persisted mix position.
- Existing writer and shard state is restored.

If preparation has already completed, running the preparation command again detects the completed state instead of rebuilding the dataset.

## Per-source starting offsets

Pretraining sources can define an initial physical offset with `start_document`:

```yaml
datasets:
  source_a:
    default:
      target_tokens: ...
      transforms:
        start_document: 1000000

  source_b:
    default:
      target_tokens: ...
```

`start_document` is a per-source physical document offset.

Each source starts from:

```text
start_document + committed documents_seen
```

For a new preparation, `documents_seen` starts at zero.

For a resumed preparation, each source restores its own `documents_seen` from preparation state.

Different sources in the same mix can therefore start at different physical positions.

For example, a new dataset can continue from a previously consumed region of one source while introducing another source from the beginning:

```yaml
datasets_common_settings:
  mix_strategy: token_budget

datasets:
  karpathy/climbmix-400b-shuffle:
    default:
      target_tokens: 80_000_000_000
      transforms:
        revision: 915333b4f8b8684f39aeaafea600fea6f43fb703
        start_document: <PREVIOUS_PHYSICAL_POSITION>
        search_parquet: true

  another/source:
    default:
      target_tokens: 20_000_000_000
```

The two sources progress independently:

```text
ClimbMix:
    previous offset + documents consumed in this preparation

Another source:
    0 + documents consumed in this preparation
```

If preparation is interrupted, both sources resume from their own committed positions.

`start_document` must be greater than or equal to zero.

It is also part of the persisted source metadata, so changing it while resuming an existing preparation results in a metadata mismatch.

## Parquet search

For supported pretraining sources:

```yaml
transforms:
  search_parquet: true
```

enables the Parquet cursor/search path.

This is useful for large Parquet-backed Hugging Face datasets where replaying or linearly skipping a large number of documents would make a large `start_document` or resume position expensive.

The loader:

1. Finds the Parquet files at the resolved dataset revision.
2. Uses Parquet row metadata to find the file and row containing the requested physical position.
3. Loads the remaining files from that point.
4. Persists a per-source cursor as documents are committed.

On resume, the expected physical position is:

```text
start_document + documents_seen
```

The stored cursor is checked against that position.

`search_parquet` is currently supported for pretraining sources.

## Configuration

Configuration can be provided directly through a YAML config or through a recipe.

Recipes are usually preferred because they keep runtime configuration and dataset preparation together.

The main `GlobalConfig` sections are:

- `run`: run metadata
- `runtime`: device, precision, FSDP, torch compile, CPU workers
- `model`: model architecture and model-specific settings
- `prompts`: default prompt and system-prompt configuration
- `training`: stage, seed, batch sizes, steps, early stopping
- `optimizers`: AdamW, Muon, and scheduler configuration
- `paths`: training datasets, eval datasets, source data, and run outputs
- `validation`: validation during training
- `evals`: benchmark configuration during training
- `generation`: generation during training
- `checkpointing`: checkpoint cadence and retention
- `tokenizer`: tokenizer backend, checkpoint, and prompt format
- `lora`: LoRA configuration
- `distillation`: teacher-model distillation
- `dpo`: DPO-specific settings
- `wandb`: Weights & Biases integration
- `torch_profiler`: profiler settings
- `data_preparation`: multiprocessing and Hugging Face preparation settings
- `logging`: run logging behavior

Pydantic models validate the configuration and reject unknown fields.

### Secrets and cache configuration

`.env` is not used for experiment configuration.

It is used for third-party credentials and cache settings:

```bash
WANDB_API_KEY=''
HF_TOKEN=''
HF_HOME='./cache'
```

`HF_TOKEN` may be required for private or gated Hugging Face assets.

## Running

### Prepare datasets

Using a recipe:

```bash
python prepare_datasets.py --recipe recipes/pretraining/debug.yaml
```

Training datasets can also be prepared manually:

```bash
python prepare_datasets.py --pretraining
python prepare_datasets.py --instruct
python prepare_datasets.py --dpo
```

Evaluation datasets can be prepared independently:

```bash
python prepare_datasets.py --hellaswag
python prepare_datasets.py --winogrande
python prepare_datasets.py --arc-challenge
python prepare_datasets.py --ifeval-no-external
python prepare_datasets.py --custom-sft-smoke
```

Manual training-data preparation also supports a custom mix file:

```bash
python prepare_datasets.py \
  --pretraining \
  --mix-file <MIX_FILE>
```

If no mix file is supplied, the built-in default mix for that stage is used.

Default mixes live in:

```text
datasets_preparation/default_mixes.py
```

Dataset preparation can also estimate the token target implied by a training configuration:

```bash
python prepare_datasets.py \
  --config <CONFIG_FILE> \
  --estimate-token-target
```

For all options:

```bash
python prepare_datasets.py --help
```

### Train

Single GPU:

```bash
python train.py --recipe recipes/pretraining/debug.yaml
```

Resume from a Gradient Garden checkpoint:

```bash
python train.py \
  --recipe recipes/pretraining/debug.yaml \
  --checkpoint <CHECKPOINT_FILE>
```

Useful CLI overrides include:

```text
--config <file>
--recipe <file>

--pretraining
--instruct
--dpo

--checkpoint <file>
--reset-optimizers
--reset-dataloaders
--reset-validation-history
--start-step <N>
--micro-batch-size <N>
```

When using `--recipe`, the recipe defines the training stage. The explicit `--pretraining`, `--instruct`, and `--dpo` flags cannot be combined with it.

### Generate

Generation can run against a Gradient Garden checkpoint or a supported Hugging Face checkpoint.

Example:

```bash
python generate.py \
  --checkpoint <CHECKPOINT_FILE> \
  --prompts examples/prompts/pretraining.example.json \
  --max-gen-len 160 \
  --temperature 0.0 \
  --top-p 0.9 \
  --device cuda \
  --dtype bf16 \
  --seed 42 \
  --batch-size 4 \
  --use-kv-cache \
  --output-file-name <OUTPUT_FILE>
```

For all options:

```bash
python generate.py --help
```

### Evaluate

`evaluate.py` can run validation and one or more evaluation tasks against a checkpoint.

For example:

```bash
python evaluate.py \
  --checkpoint <CHECKPOINT_FILE> \
  --hellaswag \
  --winogrande \
  --arc-challenge \
  --device cuda \
  --dtype bf16
```

Instruction checkpoints can additionally run:

```bash
python evaluate.py \
  --checkpoint <CHECKPOINT_FILE> \
  --ifeval-no-external \
  --custom-sft-smoke \
  --device cuda \
  --dtype bf16
```

Supported Hugging Face checkpoints can instead be loaded with `--hf-checkpoint`.

Evaluation outputs are stored as structured JSON.

For the complete CLI:

```bash
python evaluate.py --help
```

### Interactive chat

Instruct checkpoints can be explored through the Gradio interface:

```bash
python gradio_serve.py \
  --checkpoint <CHECKPOINT_FILE>
```

Supported Hugging Face checkpoints can instead be loaded with:

```bash
python gradio_serve.py \
  --hf-checkpoint <MODEL_OR_CHECKPOINT>
```

For server, device, and sharing options:

```bash
python gradio_serve.py --help
```

## Distributed training

### Single-node multi-GPU

Use `torchrun`:

```bash
export OMP_NUM_THREADS=1

torchrun \
  --standalone \
  --nproc_per_node <NUMBER_OF_GPUS> \
  train.py --recipe recipes/pretraining/debug.yaml
```

### Multi-node

Each node runs the same training command with the appropriate distributed configuration.

For Ethernet:

```bash
export NCCL_IB_DISABLE=1
export NCCL_SOCKET_NTHREADS=4
export NCCL_NSOCKS_PERTHREAD=8
```

For InfiniBand:

```bash
export NCCL_IB_DISABLE=0
export NCCL_IB_HCA=$(ls /sys/class/infiniband | paste -sd, -)
```

Common environment configuration:

```bash
export OMP_NUM_THREADS=1
export PYTHONUNBUFFERED=1
export TORCH_NCCL_ASYNC_ERROR_HANDLING=1
export TORCH_DIST_BIND_ADDR=0.0.0.0
export NCCL_DEBUG=WARN

NNODES=<NUMBER_OF_NODES>
NPERNODE=<NUMBER_OF_GPUS>
NODE_RANK=<NODE_RANK>

MASTER_ADDR=<MASTER_NODE_IP>
MASTER_PORT=<MASTER_NODE_PORT>

_IFACE=$(ip -o route get "$MASTER_ADDR" | awk '{for(i=1;i<=NF;i++) if($i=="dev"){print $(i+1); exit}}')
[ -n "$_IFACE" ] && [ "$_IFACE" != "lo" ] && export NCCL_SOCKET_IFNAME="$_IFACE"
```

Static rendezvous:

```bash
torchrun \
  --nnodes ${NNODES} \
  --nproc-per-node ${NPERNODE} \
  --node-rank ${NODE_RANK} \
  --master_addr ${MASTER_ADDR} \
  --master_port ${MASTER_PORT} \
  train.py --recipe recipes/pretraining/debug.yaml
```

Elastic rendezvous:

```bash
RDZV_EP="$MASTER_ADDR:$MASTER_PORT"
RDZV_ID=<SHARED_JOB_NAME>

torchrun \
  --nnodes ${NNODES} \
  --nproc-per-node ${NPERNODE} \
  --rdzv-backend c10d \
  --rdzv-endpoint ${RDZV_EP} \
  --rdzv-id ${RDZV_ID} \
  train.py --recipe recipes/pretraining/debug.yaml
```

The same rendezvous configuration must be used across participating nodes.

## Project structure

```text
cli/
    Shared command-line helpers.

datasets_preparation/
    Dataset loading, adapters, mixing, tokenization, sharding,
    preparation state, and evaluation-dataset preparation.

engine/
    Training runtime, distributed setup, checkpointing,
    dataloaders, optimization, schedulers, logging, profiling,
    snapshots, and workload estimation.

evals/
    Validation and benchmark loading/scoring utilities.

inference/
    Generation runtime, sampling, checkpoint inspection,
    and KV cache.

metrics/
    Metric aggregation utilities.

models/
    Model interfaces, model registry, implementations,
    Hugging Face wrappers, and adapters such as LoRA.

recipes/
    Experiment and data-preparation definitions.

tasks/
    Training objectives including causal language modelling,
    distillation support, and DPO.

tests/
    Unit and integration tests.

tokenization/
    Tokenizer abstraction and Hugging Face tokenizer backend.
```

Main entry points:

```text
prepare_datasets.py    Prepare training and evaluation data
train.py               Run training
generate.py            Run text generation
evaluate.py            Run validation and benchmarks
gradio_serve.py        Interactively test instruct checkpoints
```

Core configuration:

```text
config.py
recipes/config.py
```

## Testing and CI

Run the test suite from the repository root:

```bash
pytest
```

Tests currently cover areas including:

- Dataset source selection
- Dataset mixing
- Independent source offsets
- Multi-source preparation resume
- Global and per-source token budgets
- Token-budget overshoot
- Dataset-preparation resume behavior
- Physical source exhaustion
- Train/validation token accounting
- Parquet resume/search behavior
- SFT and DPO encodings
- Attention behavior
- MoE auxiliary losses
- Post-training loss scaling
- Generation and KV cache
- Evaluation utilities

GitHub Actions runs the test suite on pull requests using Python 3.11.

The workflow is defined in:

```text
.github/workflows/tests.yml
```

## Profiling

Torch profiler support is integrated into the training runtime.

Profiler behavior is configured through:

```text
config.torch_profiler
```

## Local files

Local experiment files can use the naming conventions excluded by `.gitignore`:

```text
*.local.json
*.private.json

*.local.yaml
*.private.yaml

*.local.yml
*.private.yml

*.local.ipynb
*.private.ipynb
```

These are useful for machine-specific recipes, private dataset configurations, local experiments, and notebooks that should not be committed.

## Project status

Gradient Garden is an actively evolving research project.

The codebase currently focuses on language-model training and experimentation, and will continue changing as new models, training methods, datasets, and evaluations are explored.

Current expectations:

- Training is CUDA-focused.
- Hugging Face is currently the main tokenizer backend.
- Recipes are the preferred way to capture reproducible experiments.
- Some APIs and abstractions may change as the project evolves.
- `main` represents the stable/public state of the repository.

Planned work and implementation discussions are tracked through GitHub issues and pull requests.

## Development and contributions

Issues and pull requests are welcome.

The project generally favors:

- Focused changes
- Small, reviewable pull requests
- Tests for behavioral changes
- Explicit configuration semantics
- Adding abstractions when there is a concrete need for them
- Keeping research code understandable and easy to modify

For larger changes, opening an issue first can help define the scope.

## Third-party assets and licenses

Tokenizer files, model weights, and datasets obtained from third parties are not included in this repository unless explicitly stated.

Those assets may be subject to their own licenses, access requirements, and terms of use.

## License

Gradient Garden is licensed under the Apache License 2.0.

See [`LICENSE`](LICENSE) for details.

## Citation

If Gradient Garden is useful in your work, you can cite the repository as:

```bibtex
@software{rui2024gradientgarden,
  author = {Rui Malheiro},
  title = {Gradient Garden},
  year = {2024},
  url = {https://github.com/ruimalheiro/gradient-garden}
}
```

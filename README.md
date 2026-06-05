# Gradient Garden

Gradient Garden is a research platform for model training, evaluation, and experimentation across architectures, benchmarks, and multi stage training recipes.

The project began with a decoder-only transformer baseline and has evolved into a broader codebase for training, evaluation, and experimentation across modern machine learning models, distributed training workflows, and post-training methods.

## Current focus
- Research and experimentation across architectures, benchmarks, and training recipes
- Multi-stage model training and post-training workflows
- Distributed training

## Current capabilities

### Training and distributed execution
- single-GPU training
- multi-GPU / multi-node training
  - DDP
  - FSDP2 (~ZeRO3-like sharding)
- Gradient accumulation
- Mixed precision
  - BF16
  - FP16
  - FP32
- Early stopping
- Checkpoint save / load / resume
- Torch profiler integration
- Weights & Biases (W&B) integration

### Optimization
- AdamW
  - Fused if available on the device
- Muon
  - Separate max LR, min LR, and warmup settings from AdamW
  - Applied to matrix parameters
  - AdamW is applied to the remaining trainable parameters
- Cosine LR scheduling

### Training workflows
- Pretraining
- Supervised fine-tuning (SFT / instruct)
- Direct Preference Optimization (DPO)
- Optional distillation support
  - Teacher models are currently loaded from the Hugging Face Hub, but this can be adapted to other sources if needed

### Models
- Tendril
  - Current default model architecture. Dense decoder-only transformer with GQA and RoPE support.
- TendrilMoE
  - Mixture of Experts (MoE) implementation of Tendril.
  - Reuses the existing FF module for expert MLPs.
  - Includes load balancing and z-loss

### Other features
- LoRA
- KV cache for autoregressive decoding

### Evaluation
- Shared multiple-choice evaluation path
  - HellaSwag
  - WinoGrande
  - ARC-Challenge
- Additional benchmarks can be added through the same multiple-choice evaluation flow

## Notes
- The project is currently focused on CUDA-based training workflows.
- Additional model architectures can be added through the model registry.
- By default, the project uses a Hugging Face tokenizer.
- It also supports a `tiktoken` tokenizer that can be loaded from a local BPE file. For now, this path expects a tokenizer compatible with the Llama 3 tiktoken configuration and chat/control tokens, e.g. (`<|begin_of_text|>`, `<|end_of_text|>`, `<|start_header_id|>`, `<|end_header_id|>`, `<|eot_id|>`). The local tokenizer file is **not** included in this repository and must be provided separately. This will be made more generic later.

## Project structure
- `cli/` Common cli related logic.
- `datasets_preparation/` Components used for downloading, preparing, and tokenizing datasets.
- `engine/` Trainer and runtime core components. The main ones are:
  - `dataloaders/` Dataloader logic for sampling and distributing data.
  - `checkpoints.py` Logic to handle checkpointing.
  - `context.py` Defines context transport classes.
  - `core.py` Defines state object used by the trainer.
  - `distributed.py` Contains the main logic to set up the PyTorch DDP (Distributed Data Parallel) and FSDP2 (Fully Sharded Data Parallel).
    - PyTorch DDP [here](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html)
  - `generation_prompts.py` Default lists of input prompts to try during training. `config.generation.test_prompts` overrides these defaults.
  - `logging.py` Handles different logging tasks used in the trainer.
  - `lr_schedulers.py` Stores learning rate schedulers. At the moment, it includes a cosine and WSD schedulers.
  - `optim.py` Defines and controls the optimizer(s) setup. Also has the necessary logic to build the parameter groups.
  - `snapshot.py` Implements the logic to create and store the setup snapshot.
  - `torch_profiler.py` Adds torch profiler logic and context manager.
  - `trainer.py` The main implementation that orchestrates the entire training process.
  - `wandb.py` A wrapper for Weights & Biases.
    - Weights & Biases [here](https://wandb.ai/site/)
  - `workload_estimation.py` Utilities to estimate token requirements for workload.
- `evals/` Shared evaluation loading and scoring utilities.
  - Multiple choice evals:
    - HellaSwag
    - WinoGrande
    - ARC-Challenge
- `examples/` Templates for local setup files like the `.env` secrets file and dataset mix.
- `inference/` Contains inference related components like KV cache implementation and logic for sampling and text generation.
- `metrics/` Utilities for metric aggregation.
- `models/` Contains the model registry, the builder and the base model interface.
  - `adapters/` Contains PEFT adapters.
    - `lora.py` LoRA module that handles the model modification. Rank, alpha, dropout and target modules can be configured accordingly.
  - `implementations/` Contains model implementations.
- `recipes/` Recipe definitions for training and dataset preparation. More will be added here.
  - `recipes/config.py` Defines the recipe schema and recipe loading logic.
  - `recipes/pretraining/`
    - `debug.yaml`
  - `recipes/instruct/`
    - `debug.yaml`
  - `recipes/dpo/`
    - `debug.yaml`
- `tasks/` Groups the training tasks. Relevant components:
  - `causal.py` Implements the logic for the causal training task (pretraining and instruct)
  - `distillation_utils.py` Logic for distillation loss.
  - `dpo.py` Implements the logic for the DPO training task.
  - `dpo_utils.py` Logic to calculate DPO loss.
- `tests/` Groups tests for different components.
- `tokenization/` Groups any component related to tokenizers.
  - `tokenizer.py` Provides the tokenizer abstraction used by the project and supports two backends:
    - `TikTokenizer`: loads tiktoken BPE weights from a local file path and configures the special tokens used by the project.
    - `HFTokenizer`: loads a tokenizer from Hugging Face via `AutoTokenizer.from_pretrained(...)` and aligns the required special tokens (`bos`, `eos`, headers, `eot`, `pad`).
    - `init_tokenizer(...)` selects the backend based on `config.tokenizer.huggingface_tokenizer`.
- `config.py` Defines the nested `GlobalConfig` used by the trainer, dataset preparation, evaluation, checkpointing, and runtime setup.
  - Most experiment settings currently live as defaults in `config.py`.
  - Recipes define experiment settings under the `config` section.
  - `.env` is only used for third party secrets and local cache settings: `WANDB_API_KEY`, `HF_TOKEN`, and `HF_HOME`.
- `evaluate.py` CLI / entry point for evals / benchmarking.
- `generate` CLI / entry point for inference against prompts.
- `logger.py` Simple reusable logger.
- `prepare_datasets.py` Entry point for data downloading and preparation.
- `train.py` CLI / entry point for training runs.
- `utils.py` Common generic logic that can be reused in different components.

## Setup
- Create a python environment. Example with conda: `conda create -n my_env python=3.11`;
- Activate the environment and run: `pip install -r requirements.txt`;
- Download and prepare the data:
  - Recipes:
    - Example with recipe: `python prepare_datasets.py --recipe recipes/pretraining/debug.yaml`
  - Or manually:
    - Evals:
      - HellaSwag: `python prepare_datasets.py --hellaswag`
      - WinoGrande: `python prepare_datasets.py --winogrande`
      - ARC-Challenge: `python prepare_datasets.py --arc-challenge`
    - Training and validation:
      - Pretraining: `python prepare_datasets.py --pretraining`
      - Instruct: `python prepare_datasets.py --instruct`
      - DPO: `python prepare_datasets.py --dpo`
    - **NOTE**: Dataset paths are configured in `config.py` under `GlobalConfig.paths.datasets` and `GlobalConfig.paths.evals`.
    - In manual mode, the training dataset preparation commands also support a custom mix file by passing `--mix-file <file_path>`. Check `examples/pretraining_data_mix.example.json` for an example. Local custom mix files should use the `.local.json` suffix, for example `pretraining_debug.local.json`, so they are ignored by Git. If no `--mix-file` is provided, the built-in default mix for that stage is used.
      - The default mix can be found in `datasets_preparation/default_mixes.py`
  
- (OPTIONAL) Setup your Weights & Biases API key:
  - Set `WANDB_API_KEY` environment variable if you want to log the progress there.

- **NOTE:** For some scenarios you might need to also pass your Hugging Face API token `HF_TOKEN`. E.g.: If performing knowledge distillation and the teacher model requires access permissions.

## Configuring and training

Configuration can be provided directly through a config YAML file or through a recipe YAML file.

A recipe is the preferred way to define an experiment. It contains:
- `config`: the nested `GlobalConfig` used for training and runtime setup
- `data`: dataset preparation settings, including the dataset mix and optional eval dataset preparation

The main sections are:
- `runtime`: device, precision, FSDP, torch compile, CPU workers
- `model`: model architecture and model-specific settings
- `training`: stage, seed, total batch size, max steps, early stopping
- `optimizers`: AdamW and optional Muon configuration
- `paths`: dataset, evaluation, runs, and prompt paths
- `validation`: validation frequency and number of validation steps
- `evals`: HellaSwag, WinoGrande, and ARC-Challenge settings
- `generation`: text generation frequency and max generation length
- `checkpointing`: checkpoint save frequency and retention
- `tokenizer`: tokenizer backend and checkpoint path
- `lora`: optional LoRA configs
- `distillation`: optional teacher model distillation settings
- `dpo`: DPO configuration
- `wandb`: W&B logging settings
- `torch_profiler`: profiler settings

`.env` is no longer used as the experiment configuration file. It is only used for secrets and local cache settings:
```
WANDB_API_KEY=''
HF_TOKEN=''
HF_HOME='./cache'
```

### Common flags
`train.py` accepts some flags that are useful to load a checkpoint or override some properties:

```bash
  --config <file>                   # Load config directly from a config YAML file
  --recipe <file>                   # Load config from a recipe YAML file
  --pretraining                     # Automatically sets pretraining stage.
  --instruct                        # Automatically sets instruct stage.
  --dpo                             # Automatically sets DPO stage.
  --checkpoint <file>               # Resume training from a specific checkpoint
  --reset-optimizers                # Ignore stored optimizer(s) state
  --start-step <N>                  # Override internal step counter
```
**NOTES:**
  - The project output path can be configured in `config.py` under `GlobalConfig.paths.runs`. By default it will use `./runs`
  - When using `--recipe`, the recipe defines the training stage. The flags `--pretraining`, `--instruct`, and `--dpo` cannot be combined with `--recipe`.

Example recipe commands:
```bash
python prepare_datasets.py --recipe recipes/pretraining/debug.yaml
python train.py --recipe recipes/pretraining/debug.yaml
```

### Running training
- To train on **single-GPU**, run:
    ```bash
    python train.py --recipe recipes/pretraining/debug.yaml
    ```

- To train on **multi-GPU** run:
    ```bash
    export OMP_NUM_THREADS=1

    torchrun \
      --standalone \
      --nproc_per_node <NUMBER_OF_GPUs> \
      train.py --recipe recipes/pretraining/debug.yaml
    ```

- To load a checkpoint and continue training, pass the flag to any of the above commands. E.g.:
    ```bash
    export OMP_NUM_THREADS=1

    torchrun \
      --standalone \
      --nproc_per_node <NUMBER_OF_GPUs> \
      train.py --recipe recipes/pretraining/debug.yaml --checkpoint <CHECKPOINT_FILE_PATH>
    ```

- To train on multiple nodes with **1 or more GPUs per node**, configure each node as follows:
  - Static
    - Ethernet
      ```bash
      export NCCL_IB_DISABLE=1
      export NCCL_SOCKET_NTHREADS=4
      export NCCL_NSOCKS_PERTHREAD=8
      ```
    - InfiniBand
      ```bash
      export NCCL_IB_DISABLE=0
      export NCCL_IB_HCA=$(ls /sys/class/infiniband | paste -sd, -)
      ```
    ```bash
    export OMP_NUM_THREADS=1
    export PYTHONUNBUFFERED=1
    export TORCH_NCCL_ASYNC_ERROR_HANDLING=1
    export TORCH_DIST_BIND_ADDR=0.0.0.0 # only needed in master but no impact on the workers
    export NCCL_DEBUG=WARN

    NNODES=<NUMBER_OF_NODES>
    NPERNODE=<NUMBER_OF_GPUs>
    NODE_RANK=<NODE_RANK>
    MASTER_ADDR=<MASTER_NODE_MACHINE_IP>
    MASTER_PORT=<MASTER_NODE_MACHINE_PORT>

    # make sure we can find the correct NIC
    _IFACE=$(ip -o route get "$MASTER_ADDR" | awk '{for(i=1;i<=NF;i++) if($i=="dev"){print $(i+1); exit}}')
    [ -n "$_IFACE" ] && [ "$_IFACE" != "lo" ] && export NCCL_SOCKET_IFNAME="$_IFACE"

    torchrun \
      --nnodes ${NNODES} \
      --nproc-per-node ${NPERNODE} \
      --node-rank ${NODE_RANK} \
      --master_addr ${MASTER_ADDR} \
      --master_port ${MASTER_PORT} \
      train.py --recipe recipes/pretraining/debug.yaml
    ```  
  - Elastic 
    ```bash
    export OMP_NUM_THREADS=1
    export PYTHONUNBUFFERED=1
    export TORCH_NCCL_ASYNC_ERROR_HANDLING=1
    export TORCH_DIST_BIND_ADDR=0.0.0.0 # only needed in master but no impact on the workers
    export NCCL_DEBUG=WARN

    NNODES=<NUMBER_OF_NODES>
    NPERNODE=<NUMBER_OF_GPUs>
    MASTER_ADDR=<MASTER_NODE_MACHINE_IP>
    MASTER_PORT=<MASTER_NODE_MACHINE_PORT>
    RDZV_EP="$MASTER_ADDR:$MASTER_PORT"
    RDZV_ID=<SOME_SHARED_JOB_NAME>

    # make sure we can find the correct NIC
    _IFACE=$(ip -o route get "$MASTER_ADDR" | awk '{for(i=1;i<=NF;i++) if($i=="dev"){print $(i+1); exit}}')
    [ -n "$_IFACE" ] && [ "$_IFACE" != "lo" ] && export NCCL_SOCKET_IFNAME="$_IFACE"


    torchrun \
      --nnodes ${NNODES} \
      --nproc-per-node ${NPERNODE} \
      --rdzv-backend c10d \
      --rdzv-endpoint ${RDZV_EP} \
      --rdzv-id ${RDZV_ID} \
      train.py --recipe recipes/pretraining/debug.yaml
    ```
  - **NOTE:** The same command needs to be run on all nodes

- More details on torchrun [here](https://pytorch.org/docs/stable/elastic/run.html)
- More details on NCCL [here](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html#environment-variables)

### Running generation
- For all options: `python generate.py --help`
- Example:
    ```bash
    python generate.py \
      --checkpoint <CHECKPOINT_FILE_PATH> \
      --prompts examples/prompts/pretraining.example.json \
      --max-gen-len 160 \
      --temperature 0.0 \
      --top-p 0.9 \
      --device cuda \
      --dtype bf16 \
      --seed 42 \
      --batch-size 4 \
      --use-kv-cache \
      --output-file-name <OUTPUT_FILE_PATH>
    ```

### Running evals
- For all options: `python evaluate.py --help`
- Example:
    ```bash
    python evaluate.py \
      --checkpoint  <CHECKPOINT_FILE_PATH> \
      --validation \
      --validation-steps 1000 \
      --hellaswag \
      --hellaswag-examples 100 \
      --winogrande \
      --winogrande-examples 100 \
      --arc-challenge \
      --arc-challenge-examples 100 \
      --batch-size 4 \
      --device cuda \
      --dtype bf16 \
      --output-file-name <OUTPUT_FILE_PATH>
    ```

## Using Torch Profiler
Torch profiler settings are configured in `config.py` under `GlobalConfig.torch_profiler`.
More details on the profiler API can be found [here](https://docs.pytorch.org/tutorials/recipes/recipes/profiler_recipe.html).

## Running tests
From the root folder:
```bash
pytest
```

## Local files
For convenience local configurations, recipes or other files should use the naming convention as defined in `.gitignore`:
```
*.local.json
*.private.json
*.local.ipynb
*.private.ipynb
*.local.yaml
*.private.yaml
*.local.yml
*.private.yml
```

## Contributions
Feel free to reach out if interested in contributing!

## Third-party assets and licenses
Tokenizer files, model weights, and datasets obtained from third parties are **not** included in this repository unless explicitly stated, and may be subject to their own licenses and terms.

## License
This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.

## Citation
Please cite this project if it was useful in your work:

```bibtex
@software{rui2024gradientgarden,
  author = {Rui Malheiro},
  title = {Gradient Garden},
  year = {2024},
  url = {https://github.com/ruimalheiro/gradient-garden}
}
```
import sys
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
import torch

from tokenizer import init_tokenizer
from models import build_model
from config import ModelConfig


@pytest.fixture(scope='session')
def device():
    return 'cuda' if torch.cuda.is_available() else 'cpu'

@pytest.fixture(scope='session')
def tokenizer():
    return init_tokenizer(
        path='HuggingFaceTB/SmolLM2-360M',
        system_prompt='You are a helpful AI assistant',
        is_huggingface_tokenizer=True
    )

@pytest.fixture(scope='session')
def dummy_prompt_tokens(tokenizer):
    return tokenizer.encode('Language models are')

@pytest.fixture(scope='session')
def model(device, tokenizer):
    model_config = ModelConfig(
        dim=32,
        n_layers=1,
        n_heads=2,
        n_kv_heads=1,
        multiple_of=128,
        ffn_dim_multiplier=1.0,
        norm_eps=1e-05,
        rope_theta=500000.0,
        max_batch_size=2,
        max_seq_len=32
    )

    model = build_model(
        config=model_config,
        pad_token_id=tokenizer.pad_id,
        vocab_size=tokenizer.vocab_size,
        ignore_index=-100
    )
    model.to(device)
    model.eval()
    return model

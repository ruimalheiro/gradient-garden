from config import ModelArchitecture
from models.implementations.tendril import TendrilTransformer
from models.implementations.tendril_moe import TendrilMoETransformer
from models.implementations.hf_wrapper import HFModelWrapper


MODEL_REGISTRY = {
    ModelArchitecture.TENDRIL: TendrilTransformer,
    ModelArchitecture.TENDRIL_MOE: TendrilMoETransformer,
    ModelArchitecture.HF_WRAPPER: HFModelWrapper,
}

def build_model(*, config, pad_token_id, vocab_size, ignore_index):
    model_cls = MODEL_REGISTRY.get(config.architecture)
    if model_cls is None:
        raise ValueError(f'Invalid model architecture: {config.architecture}')

    model_cls.validate_config(config)

    return model_cls(
        config=config,
        pad_token_id=pad_token_id,
        vocab_size=vocab_size,
        ignore_index=ignore_index,
    )

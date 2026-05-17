from config import ModelArchitecture
from models.tendril import TendrilTransformer


MODEL_REGISTRY = {
    ModelArchitecture.TENDRIL: TendrilTransformer,
}

def build_model(*, config, pad_token_id, vocab_size, ignore_index):
    model_cls = MODEL_REGISTRY.get(config.architecture)
    if model_cls is None:
        raise ValueError(f'Invalid model architecture: {config.architecture}')

    return model_cls(
        config=config,
        pad_token_id=pad_token_id,
        vocab_size=vocab_size,
        ignore_index=ignore_index,
    )

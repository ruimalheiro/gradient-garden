import errno
import time

from logger import logger


RETRYABLE_PREPARATION_ERRNOS = {
    errno.EPIPE,
    errno.ECONNRESET,
    errno.ECONNABORTED,
    errno.ETIMEDOUT,
}

def is_retryable_preparation_error(exc):
    current = exc

    while current is not None:
        if (
            isinstance(current, (BrokenPipeError, ConnectionError, TimeoutError)) or
            isinstance(current, OSError) and current.errno in RETRYABLE_PREPARATION_ERRNOS
        ):
            return True

        current = current.__cause__ or current.__context__

    return False

def prepare_with_retries(
    *,
    f,
    max_retries=10
):
    retries = 0

    while True:
        try:
            return f()
        except Exception as e:
            if not is_retryable_preparation_error(e):
                raise
            retries += 1

            if retries > max_retries:
                logger.error(f'Preparation process failed after {max_retries} retries.')
                raise

            delay = min(30 * (2 ** (retries - 1)), 300)

            logger.warning(f'Preparation error: {type(e).__name__}: {e}')
            logger.warning(f'Retrying from preparation state in {delay}s ({retries}/{max_retries})...')

            time.sleep(delay)

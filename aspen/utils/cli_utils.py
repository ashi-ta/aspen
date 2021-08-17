from distutils.util import strtobool as dist_strtobool


def strtobool(x: str) -> bool:
    """Boolean related string convert to boolean
    Inspired from https://github.com/espnet/espnet

    Args:
        x: Boolean string (e.g. `TRUE`, `true`, `T`, `yes`, `1` and so on)

    Returns:
        Boolean Flag
    """

    # distutils.util.strtobool returns integer, but it's confusing,
    return bool(dist_strtobool(x))

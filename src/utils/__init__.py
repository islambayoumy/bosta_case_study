import argparse


def parse_args() -> argparse.Namespace:
    """
    Argument parser
    Returns:
        Args: an argparse object
    """

    parser = argparse.ArgumentParser(description="Parameters for ETL")

    parser.add_argument(
        "--environment",
        help="Environment you would like to run the project in",
        default="tests",
        choices=["prod", "tests"],
        type=str,
    )

    args, _ = parser.parse_known_args()

    if args.environment == "prod":
        args.debug = False
    else:
        args.debug = True
    return args


__all__ = ["parse_args"]

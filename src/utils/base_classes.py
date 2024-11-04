import logging
from colorama import Fore, Style

from src.utils import parse_args


class BaseVariables:
    arguments = parse_args()


class DataExtractor:
    base_variables = BaseVariables()

    def extract(self, **kwargs):
        """Extracts the data from the source"""
        raise NotImplementedError

    def transform(self, **kwargs):
        """Transforms the data"""
        raise NotImplementedError

    def load(self, **kwargs):
        """Loads data into SJ"""
        raise NotImplementedError

    def run(self):
        try:
            self.extract()
        except Exception as err:
            raise RuntimeError(f"Scraper failed at extraction. Error was {err}") from err

        try:
            self.transform()
        except Exception as err:
            raise RuntimeError(f"Scraper failed at dataframe transformation. Error was {err}") from err

        try:
            self.load()
        except Exception as err:
            raise RuntimeError(f"Scraper failed at upload. Error was {err}") from err


class Logger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            f"{Fore.LIGHTWHITE_EX}%(asctime)s - %(name)s - %(levelname)s - %(message)s{Style.RESET_ALL}"
        )
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.propagate = False

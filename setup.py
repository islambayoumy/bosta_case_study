import setuptools
from setuptools import find_packages


with open("./requirements/requirements.in", "r") as req_file:
    REQUIREMENTS = req_file.read().splitlines()

REQUIREMENTS.append("bosta_case_study")

setuptools.setup(
    name="bosta_case_study",
    version="1.0.0",
    description="",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=REQUIREMENTS,
    package_data={"": ["*"]},
    entry_points={
        "console_scripts": [
            "run_data_flatten = src.etls.data_flatten:data_flatten",
        ],
    },
)

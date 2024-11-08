from setuptools import setup, find_packages

setup(
    name="helm_model_autoconfig",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "helm_model_autoconfig=huggingface_tool.cli:main",
        ],
    },
    author="Mateus Matias",
    description="CLI tool to fetch Hugging Face model info and generate YAML files to HELM",
    license="MIT",
    keywords="huggingface, cli, yaml, model metadata",
    url="https://github.com/yourusername/huggingface_cli_tool",
)

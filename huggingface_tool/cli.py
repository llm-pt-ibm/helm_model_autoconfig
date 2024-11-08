import argparse
from huggingface_tool.model_info import get_huggingface_model_info
from huggingface_tool.yaml_writer import (
    write_model_deployment_to_yaml,
    write_model_metadata_to_yaml,
)
import os


def main():
    parser = argparse.ArgumentParser(
        description="Fetch model info from Hugging Face and write metadata to YAML for multiple models."
    )

    parser.add_argument(
        "--model_urls",
        nargs="+",
        required=True,
        help="List of URLs of the Hugging Face models",
    )
    parser.add_argument(
        "--tags",
        nargs="*",
        help="Tags for the model metadata",
        default=["TEXT_MODEL_TAG"],
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default=".",
        help="Directory to save the generated YAML files",
    )

    args = parser.parse_args()

    # Ensure output directory exists
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    # Process each model URL
    for model_url in args.model_urls:
        print(f"Processing model: {model_url}")

        # Fetch model info
        model_info = get_huggingface_model_info(model_url)

        if model_info:
            # Write metadata and deployment YAML files
            write_model_metadata_to_yaml(
                model_info["repo_name"],
                model_info["description"],
                model_info["parameters"],
                model_info["release_date"],
                args.tags,
                output_path=args.output_path,
            )

            write_model_deployment_to_yaml(
                model_info["repo_name"],
                model_info["max_sequence_length"],
                output_path=args.output_path,
            )
            print(f"YAML files generated for {model_url} in {args.output_path}")
        else:
            print(f"Failed to retrieve information for {model_url}")


if __name__ == "__main__":
    main()

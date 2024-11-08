
# Helm Model AutoConfig

**Helm Model AutoConfig** is a command-line tool to fetch Hugging Face model information and generate YAML configuration files for the HELM benchmarking framework. This tool allows users to specify multiple Hugging Face models, add metadata tags, and save the output files to a specified directory.

## Features

- Fetch model information from Hugging Face.
- Generate `model_metadata.yaml` and `model_deployments.yaml` files with HELM-compatible format.
- Support multiple models in a single run.
- Customizable output path for generated YAML files.
- Metadata tags for additional categorization.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/llm-pt-ibm/helm_model_autoconfig
    cd helm_model_autoconfig
    ```

2. Install the package:
    ```bash
    pip install .
    ```

## Usage

This CLI tool can be used by specifying one or more Hugging Face model URLs, metadata tags, and an optional output path.

### Command Syntax

```bash
helm_model_autoconfig --model_urls <model_url1> <model_url2> ... --tags <tag1> <tag2> ... --output_path <path/to/output>
```

### Parameters

- `--model_urls` (**required**): A list of Hugging Face model URLs to be processed.
- `--tags` (*optional*): Tags to be included in the model metadata (default: `["TEXT_MODEL_TAG"]`). You can see tags [here](https://crfm-helm.readthedocs.io/en/latest/adding_new_models/#model-metadata).
- `--output_path` (*optional*): Directory to save the generated YAML files (default: current directory `.`).

### Example Usage

Generate YAML files for multiple Hugging Face models and save them to a specified output directory:

```bash
helm_model_autoconfig --model_urls "https://huggingface.co/ibm-granite/granite-3.0-8b-base" "https://huggingface.co/ibm-granite/granite-3.0-8b-instruct" --tags TEXT_MODEL_TAG, PARTIAL_FUNCTIONALITY_TEXT_MODEL_TAG --output_path /path/to/output
```

This command will:
- Fetch information for each model URL provided.
- Add metadata tags `TEXT_MODEL_TAG` and `PARTIAL_FUNCTIONALITY_TEXT_MODEL_TAG` to the `model_metadata.yaml`.
- Save both `model_metadata.yaml` and `model_deployments.yaml` to `/path/to/output`.

## YAML File Structure

The tool generates two YAML files in HELM format:

1. **model_metadata.yaml**
   - Contains general information about each model, such as `name`, `description`, `creator_organization_name`, and `num_parameters`.

2. **model_deployments.yaml**
   - Specifies model deployment configurations, such as `model_name`, `tokenizer_name`, and `max_sequence_length`.

## Example Output

### model_metadata.yaml

```yaml
models:

    - name: ibm-granite/granite-3.0-8b-base
    display_name: Granite 3.0 8B Base
    description: Granite-3.0-8B-Base is a decoder-only language model to support a variety of text-to-text generation tasks. It is trained from scratch following a two-stage training strategy. In the first stage, it is trained on 10 trillion tokens sourced from diverse domains. During the second stage, it is further trained on 2 trillion tokens using a carefully curated mix of high-quality data, aiming to enhance its performance on specific tasks.
    creator_organization_name: IBM-GRANITE
    access: open
    num_parameters: 8.17B
    release_date: October 21st, 2024
    tags: ['tag1', 'tag2', 'tag3']

```

### model_deployments.yaml

```yaml
model_deployments:

    - name: huggingface/granite-3.0-8b-base
    model_name: ibm-granite/granite-3.0-8b-base
    tokenizer_name: ibm-granite/granite-3.0-8b-base
    max_sequence_length: 4096
    client_spec:
        class_name: "helm.clients.huggingface_client.HuggingFaceClient"
        args:
        pretrained_model_name_or_path: ibm-granite/granite-3.0-8b-base
```

## Development and Contribution

To contribute, please fork this repository and submit a pull request. Ensure all code is linted and tested.

## License

This project is licensed under the MIT License.

## Contact

For issues or feature requests, please [open an issue](https://github.com/llm-pt-ibm/helm_model_autoconfig/issues) on the GitHub repository.

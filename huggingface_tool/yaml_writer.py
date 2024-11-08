import os


def write_model_metadata_to_yaml(
    hf_repo, des, parameters, release_date, tags, output_path="."
):
    org, title = hf_repo.split("/")

    model_metadata = f"""
    - name: {hf_repo}
    display_name: {title.replace("-", " ").title()}
    description: {des}
    creator_organization_name: {org.upper()}
    access: open
    num_parameters: {parameters}
    release_date: {release_date}
    tags: {[tag for tag in tags]}
"""

    # Define the output file path
    metadata_file_path = os.path.join(output_path, "model_metadata.yaml")

    try:
        with open(metadata_file_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = "models:\n"

    if not content.startswith("models:"):
        content = "models:\n" + content

    content += model_metadata

    with open(metadata_file_path, "w") as f:
        f.write(content)


def write_model_deployment_to_yaml(hf_repo, max_seq_length, output_path="."):
    title = hf_repo.split("/")[-1]

    model_deployment = f"""
    - name: huggingface/{title}
    model_name: {hf_repo}
    tokenizer_name: {hf_repo}
    max_sequence_length: {max_seq_length}
    client_spec:
        class_name: "helm.clients.huggingface_client.HuggingFaceClient"
        args:
        pretrained_model_name_or_path: {hf_repo}
"""

    # Define the output file path
    deployment_file_path = os.path.join(output_path, "model_deployments.yaml")

    try:
        with open(deployment_file_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = "model_deployments:\n"

    if not content.startswith("model_deployments:"):
        content = "model_deployments:\n" + content

    content += model_deployment

    with open(deployment_file_path, "w") as f:
        f.write(content)

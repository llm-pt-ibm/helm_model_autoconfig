import os


def write_model_metadata_to_yaml(
    hf_repo: str, des: str, parameters: str | int, release_date: str, tags: list, output_path="."
) -> None:
    """
    Write the model metadata to a yaml file 
    
    Args:
    hf_repo (str): The Hugging Face repository name
    des (str): The description of the model
    parameters (str | int): The number of parameters of the model
    release_date (str): The release date of the model
    tags (list): The tags for the model metadata
    output_path (str): The output path to write the yaml file
    """
    
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


def write_model_deployment_to_yaml(hf_repo: str, max_seq_length: int, output_path=".") -> None:
    """
    Write the model deployment to a yaml file
    
    Args:
    hf_repo (str): The Hugging Face repository name
    max_seq_length (int): The maximum sequence length of the model
    output_path (str): The output path to write the yaml file
    """
    
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
        
def write_tokenizer_configs_to_yaml(hf_repo: str, prefix_token="", end_of_text_token="", output_path=".") -> None:
    """
        Write the tokenizer configs to a yaml file
        
        Args:
        hf_repo (str): The Hugging Face repository name
        prefix_token (str): The prefix token for the tokenizer
        end_of_text_token (str): The end of text token for the tokenizer
        output_path (str): The output path to write the yaml file
    """
    tokenizer_configs = f"""
    - name: {hf_repo}
        tokenizer_spec:
        class_name: "helm.tokenizers.huggingface_tokenizer.HuggingFaceTokenizer"
        args:
            pretrained_model_name_or_path: {hf_repo}
        end_of_text_token: "{end_of_text_token}"
        prefix_token: "{prefix_token}"
    """
    
    # Define the output file path
    tokenizer_file_path = os.path.join(output_path, "tokenizer_configs.yaml")
    
    try:
        with open(tokenizer_file_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = "tokenizer_configs:\n"
        
    if not content.startswith("tokenizer_configs:"):
        content = "tokenizer_configs:\n" + content
        
    content += tokenizer_configs
    
    with open(tokenizer_file_path, "w") as f:
        f.write(content)
        
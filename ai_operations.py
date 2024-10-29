import boto3
from botocore.exceptions import ClientError
from config import PROMPT_TEMPLATE, SHOT_1, SHOT_2, SHOT_4, SYSTEM_PROMPT
from file_operations import read_pdf

bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")
bedrock_client = boto3.client(service_name="bedrock", region_name="us-west-2")


def get_completion(prompt, model_id, max_tokens, system_prompt=None, prefill=None):
    inference_config = {"temperature": 0.0, "maxTokens": max_tokens}
    converse_api_params = {
        "modelId": model_id,
        "messages": [{"role": "user", "content": [{"text": prompt}]}],
        "inferenceConfig": inference_config,
    }
    if system_prompt:
        converse_api_params["system"] = [{"text": system_prompt}]
    if prefill:
        converse_api_params["messages"].append(
            {"role": "assistant", "content": [{"text": prefill}]}
        )
    try:
        response = bedrock_runtime.converse(**converse_api_params)
        text_content = response["output"]["message"]["content"][0]["text"]
        return text_content

    except ClientError as err:
        message = err.response["Error"]["Message"]
        raise Exception(f"Bedrock API error: {message}")


def compare_documents(file_path1, file_path2, model_id, max_tokens):
    try:
        # Read the contents of both PDFs
        doc_a = read_pdf(file_path1)
        doc_b = read_pdf(file_path2)

        # Prepare the prompt for document comparison
        prompt = PROMPT_TEMPLATE.format(
            shot_1=SHOT_1,
            shot_2=SHOT_2,
            shot_3="",
            shot_4=SHOT_4,
            doc_a=doc_a,
            doc_b=doc_b,
        )

        # Use the selected Bedrock model to compare the documents
        comparison_result = get_completion(prompt, model_id, max_tokens, SYSTEM_PROMPT)

        if not comparison_result:
            raise Exception("Model returned empty result")

        return comparison_result

    except Exception as e:
        raise Exception(f"Error in document comparison: {str(e)}")


def get_claude_and_llama_models():
    claude_and_llama_models = [
        # Claude models
        "anthropic.claude-v2",
        "anthropic.claude-v2:1",
        "anthropic.claude-3-sonnet-20240229-v1:0",
        "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "anthropic.claude-3-5-sonnet-20241022-v2:0",
        "anthropic.claude-3-haiku-20240307-v1:0",
        "anthropic.claude-3-opus-20240229-v1:0",
        "anthropic.claude-instant-v1",
        # Llama models
        "meta.llama2-70b-chat-v1",
        "meta.llama3-8b-instruct-v1:0",
        "meta.llama3-70b-instruct-v1:0",
        "meta.llama3-1-8b-instruct-v1:0",
        "meta.llama3-1-70b-instruct-v1:0",
        "meta.llama3-1-405b-instruct-v1:0",
    ]
    return claude_and_llama_models

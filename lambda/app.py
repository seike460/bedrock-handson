import boto3
import json


def invoke_bedrock_runtime(prompt, max_tokens):
    """bedrock-runtimeを呼び出してレスポンスを返す"""
    client = boto3.client('bedrock-runtime')
    body = {
        'prompt': prompt,
        'max_tokens_to_sample': max_tokens
    }
    response = client.invoke_model(
        modelId='anthropic.claude-v2:1', body=json.dumps(body))
    response_body = response['body'].read().decode('utf-8')
    return json.loads(response_body)['completion']


def create_prompt(user_message, assistant_message=''):
    """プロンプトを作成する"""
    return f"Human: {user_message}\nAssistant:{assistant_message}"


def lambda_handler(event, context):
    # クエリパラメータを取得
    query_params = event.get('queryStringParameters')
    # クエリパラメータが存在するか確認し、値を取得
    param_value = ""
    max_tokens = 3000
    if query_params:
        param_value = query_params.get('prompt', '北海道のジンギスカンが名物ですか？')
        max_tokens = query_params.get('max_tokens', 3000)
    # プロンプト生成
    prompt = create_prompt(param_value)
    # Bedrock呼び出し
    completion_1 = invoke_bedrock_runtime(prompt, max_tokens)
    # 結果を返す
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': completion_1},
            ensure_ascii=False)
    }

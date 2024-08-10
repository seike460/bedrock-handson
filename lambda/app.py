import boto3
import json

def invoke_bedrock_runtime_rag(prompt, max_tokens):
    """bedrock-runtimeを呼び出してレスポンスを返す"""
    client = boto3.client('bedrock-agent-runtime')
    model_arn = "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
    knowledgeBase_id = "XxxxxxxxxX" #メモ1を設定する
    response = client.retrieve_and_generate(
        input={
            'text': prompt
        },
        retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': knowledgeBase_id,
            'modelArn': model_arn
        }
    })
    # 実行結果からテキストのみを変数に入れて、画面に出力する
    generated_text = response['output']['text']
    return generated_text

def invoke_bedrock_runtime(prompt, max_tokens):
    bedrock = boto3.client("bedrock-runtime")
    # リクエストボディを定義
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }
    )
    # モデルを定義（Claude 3.5 Sonnet）
    modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    # HTTPヘッダーを定義
    accept = "application/json"
    contentType = "application/json"
    # レスポンスを定義
    response = bedrock.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    response_body = json.loads(response.get("body").read().decode('utf-8'))
    answer = response_body["content"][0]["text"]
    return answer

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
        param_value = query_params.get('prompt', '愛媛の名物を教えてください')
        max_tokens = query_params.get('max_tokens', 3000)
    # プロンプト生成
    prompt = create_prompt(param_value)
    # Bedrock呼び出し
    completion_1 = invoke_bedrock_runtime(prompt, max_tokens)
    #completion_1 = invoke_bedrock_runtime_rag(prompt, max_tokens)
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

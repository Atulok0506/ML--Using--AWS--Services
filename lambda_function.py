import boto3

ENDPOINT_NAME = 'sagemaker-xgboost-2024-09-25-07-58-01-343'

runtime = boto3.client('runtime.sagemaker')
email_client = boto3.client('sns')


def lambda_handler(event, context):
    inputs = event['data']
    result = []
    for input in inputs:
        serialized_input = ','.join(map(str, input))

        response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                           ContentType='text/csv',
                                           Body=serialized_input)
        result.append(response['Body'].read().decode().strip())

    response_sns = email_client.publish(
        TopicArn='arn:aws:sns:ap-south-1:751956059869:MyTopic',
        Message='Prediction is' + str(result),
        Subject='eMC Finance - Daily Prediction')
    return result

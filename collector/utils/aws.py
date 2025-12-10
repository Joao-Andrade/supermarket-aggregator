import boto3
import json
from typing import List, Dict

def send_to_sqs(queue_url: str, messages: List[Dict], batch_size: int = 10):
    """
    Sends a list of messages to an SQS queue.
    SQS supports a maximum of 10 messages per batch.
    """
    sqs = boto3.client('sqs')
    
    for i in range(0, len(messages), batch_size):
        batch = messages[i:i + batch_size]
        entries = []
        for idx, msg in enumerate(batch):
            entries.append({
                'Id': str(idx),
                'MessageBody': json.dumps(msg, ensure_ascii=False)
            })
            
        try:
            response = sqs.send_message_batch(
                QueueUrl=queue_url,
                Entries=entries
            )
            # Check for failures in the batch
            if 'Failed' in response:
                print(f"Failed to send {len(response['Failed'])} messages to SQS.")
                for failure in response['Failed']:
                    print(f"Error: {failure.get('Message')}")
                    
        except Exception as e:
            print(f"Error sending batch to SQS: {e}")

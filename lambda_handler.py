import boto3

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
table = dynamodb.Table('royce-inventory')


def update_item_quantity(item_id, new_quantity):
    table.update_item(
        Key={
            'product_id': item_id
        },
        UpdateExpression="set quantity = :q",
        ExpressionAttributeValues={
            ':q': int(new_quantity)
        },
        ReturnValues="NONE"
    )


def lambda_handler(event, context):
    item_id = event["itemId"]
    quantity_purchased = int(event['quantity_purchased'])

    available_quantity = get_item_quantity(item_id)
    remaining_items = available_quantity - quantity_purchased

    if remaining_items >= 0:
        update_item_quantity(item_id, remaining_items)

    return remaining_items

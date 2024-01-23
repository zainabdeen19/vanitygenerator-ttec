import itertools
import json
import time
import boto3


word_list = []
with open('wordlist.txt', 'r') as file:
    word_list = set(file.read().split())

phone_dict = {
    '0':'0',
    '1':'1',
    '2':['A','B','C'],
    '3':['D','E','F'],
    '4':['G','H','I'],
    '5':['J','K','L'],
    '6':['M','N','O'],
    '7':['P','Q','R','S'],
    '8':['T','U','V'],
    '9':['W','X','Y','Z']
}

def find_vanity_numbers(number):
    number = ''.join(e for e in number if e.isdigit())
    if len(number) < 7:
        return []

    # Generate all possible combinations of letters for each digit
    letter_combos = []
    for digit in number[3:]:
        if digit in phone_dict:
            letter_combos.append(phone_dict[digit])
        else:
            letter_combos.append([digit])

    # Try each combination of letters, starting with the longest
    for length in range(7, 2, -1):
        for combo in itertools.combinations(letter_combos, length):
            words = []
            for letters in itertools.product(*combo):
                word = ''.join(letters).lower()
                if word in word_list:
                    words.append(word)
            if words:
                vanity_number = ''.join(number[:3]) + ''.join(words) + ''.join(number[3+length:])
                score = calculate_score(vanity_number)
                yield (vanity_number, score)
                if len(words) > 1:
                    for i in range(len(words)):
                        modified_words = words[:i] + words[i+1:]
                        modified_vanity_number = ''.join(number[:3]) + ''.join(modified_words) + ''.join(number[3+length:])
                        score = calculate_score(modified_vanity_number)
                        yield (modified_vanity_number, score)

    # If no words were found, try random combinations of letters
    for length in range(7, 2, -1):
        for combo in itertools.product(*letter_combos[:length]):
            word = ''.join(combo).lower()
            vanity_number = ''.join(number[:3]) + word + ''.join(number[3+length:])
            score = calculate_score(vanity_number)
            yield (vanity_number, score)

def calculate_score(vanity_number):
    score = 0
    for word in vanity_number.split(' '):
        if word in word_list:
            score += len(word)
    return score

def create_phone_numbers_table():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
        TableName='VanityNumber',
        KeySchema=[
            {
                'AttributeName': 'PhoneNumber',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'PhoneNumber',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print("Table created:", table.table_status)
    
def store_phone_numbers(phone_number, number_list):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('VanityNumber')
    
    item = {
        'PhoneNumber': phone_number,
        'number1': number_list[0],
        'number2': number_list[1],
        'number3': number_list[2],
        'number4': number_list[3],
        'number5': number_list[4],
    } 
    
    table.put_item(Item=item)
    print("Phone numbers stored successfully!")
    
def table_exists():
    dynamodb = boto3.client('dynamodb')
    try:
        dynamodb.describe_table(TableName="VanityNumber") 
        return True
    except dynamodb.exceptions.ResourceNotFoundException:
        return False

def lambda_handler(event, context):
    number = event['Details']['ContactData']['CustomerEndpoint']['Address']
    
    if table_exists() == False:
        create_phone_numbers_table()
        time.sleep(1000)
        
    
    
    vanity_numbers = list(find_vanity_numbers(number))
    store_numbers = []
    five_numbers = []
    for nums in  list(set(vanity_numbers[:10])):
        five_numbers.append(nums)
        store_numbers.append(nums[0])

    five_numbers.sort(key=lambda x: x[1], reverse=True)
    top_3_vanity_numbers = [vn[0] for vn in five_numbers[:3]]
    tempList = []
    for num in top_3_vanity_numbers:
        if len(num) > 10:
            tempList.append(num[:10])
        else:
            tempList.append(num)
    top_3_vanity_numbers = tempList
    store_phone_numbers(number,store_numbers[:5])

    response = {
        'first_num': top_3_vanity_numbers[0],
        'second_num' : top_3_vanity_numbers[1],
        'third_num' : top_3_vanity_numbers[2]
    }
    return response

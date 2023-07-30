import pymysql.cursors
import openai

openai.api_key = "<API_KEY>"

connection = pymysql.connect(host='',
                             user='',
                             password='',
                             database =''            
                             )
cursor = connection.cursor()

sql ="insert into bot(name)values(%s)"

def lambda_handler(event, context):
    
    message = event['inputTranscript']
    name=event["interpretations"][0]["intent"]["slots"]["fname"]["value"]["originalValue"]    
    cursor.execute(sql,name)
    messages = []
    messages.append({"role": "system", "content": "A doctor assistant"})
    messages.append({"role": "user", "content": message})
    resp = {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": {
                "confirmationState": "Confirmed",
                "name": "NewIntent",
                "state": "Fulfilled",
            },
        },
        "messages": [{"contentType": "PlainText", "content": " "}],
    }
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=1000
    )
    reply = response["choices"][0]["message"]["content"]

    resp["messages"][0]["content"] = reply

    connection.commit()

    return response

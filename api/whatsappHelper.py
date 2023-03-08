import requests


url = 'https://graph.facebook.com/v16.0/108376685469215/messages'
token='Bearer EAARTTbZCZBXcEBAJtJT7FpPLqoIQNUtdVZBn4AZCvLbZAlnpglLrV0sumO20XMmb44XQtHNHv5tMJdQArjIJnq5PxcWDRsv5xk0ZBh2VUzAaZAA2nNBzMKWUInksQsKSmZBnToBnJP7kOU9kNY1FiQS6hXVqCojuZChKvGb0eQrgjOpXHHapRpZAILwSSjtGIZAxYNS7Rl0IzuY7z33QlvjRh6gYLSC0o6CxukZD'

def sendMessage (phonenumber, imgUrl, email, orderId, amount, id):
    headers = {"Authorization":token}
    payload = { "messaging_product":"whatsapp", 
                "recipient_type" : 'individual', 
                "to": phonenumber,
                "type":"template",
                "template":{
                "name":"vecreation",
                "language": { "code": "en" }, 
                "components":[
                    {
                    "type": "header",
                    "parameters": [
                      {
                        "type": "image",
                        "image": {
                           "link": imgUrl
                        }
                      }
                    ]
                  },

                 {"type": "body","parameters": [
                {"type": "text","text": email},
                {"type": "text","text": orderId},
                {"type": "text","text": amount},


                ]},
                 {
                "type": "button",
                "sub_type": "url",
                "index": "0",
                "parameters": [
                  {
                    "type": "text",
                    "text": id
                  }
                ]
              },
                ]
                },}
    response = requests.post(url, headers=headers, json=payload)
    ans = response.json()
    print (ans)


img = 'https://vecreation.in/assets/logo-eb4f68c6.png'
email= 'salmankhna@gmail.com'
orderId = 'WEB_00007'
amount = '5000'
customId = 8





# sendMessage('919957576653', img, email, orderId, amount, customId )
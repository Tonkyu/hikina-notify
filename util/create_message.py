from flask import url_for

def create_message(alt_title, title, content, img_name):
    base_url = 'https://hikina-notify-b57d379fe0b0.herokuapp.com/'
    img_url = base_url + url_for('static', filename=f'img/{img_name}')
    print(img_url)
    return {
            "type": "flex",
            "altText": alt_title,
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "hero": {
                    "type": "image",
                    "url": img_url,
                    "size": "full",
                    "aspectRatio": "10:10",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                            "type": "text",
                            "wrap": True,
                            "text": title,
                            "size": "xs",
                            "align": "center"
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                            "type": "text",
                            "wrap": True,
                            "text": content,
                            "size": "xs",
                            "align": "center"
                            }
                        ],
                        "margin": "5px"
                        }
                    ],
                    "paddingTop": "2%",
                    "paddingBottom": "2%"
                }
            }
        }
from PIL import Image, ImageDraw, ImageFont
from flask import url_for


def create_image(data):
    data_id = data[0]
    start_datetime = data[1]
    end_datetime = data[2]
    location = data[3]

    month = start_datetime.month
    day = start_datetime.month
    start_hour = start_datetime.hour
    start_minute = start_datetime.minute
    end_hour = end_datetime.hour
    end_minute = end_datetime.minute

    temp_img_path = './static/img/template.png'
    img = Image.open(temp_img_path)

    w, h = img.size

    color = (255, 255, 255)  # White color

    interval_size = int(0.08 * h)

    month_day_fontsize = 220  # Coordinates where the month/day will be drawn
    time_fontsize = 220   # Coordinates where the time will be drawn
    title_fontsize = 180
    location_fontsize = 90   # Coordinates where the location will be drawn


    font_path = "./static/font/hiragino.ttc"
    #==============

    month_day_font = ImageFont.truetype(font_path, month_day_fontsize)
    time_font = ImageFont.truetype(font_path, time_fontsize)
    title_font = ImageFont.truetype(font_path, title_fontsize)
    location_font = ImageFont.truetype(font_path, location_fontsize)

    # Create a drawing context
    draw = ImageDraw.Draw(img)

    # Coordinates for the text (this will need to be adjusted to match the image)
    month_day_coord = (int(0.06*w),interval_size)  # Coordinates where the month/day will be drawn
    time_coord = (int(0.06*w), interval_size*2 + month_day_fontsize)   # Coordinates where the time will be drawn
    title_coord = (int(0.06*w), interval_size*3 + month_day_fontsize + time_fontsize)
    location_coord = (int(0.06*w), interval_size*4 + month_day_fontsize + time_fontsize + title_fontsize)   # Coordinates where the location will be drawn

    # The text to be drawn
    month_day_text = f"{month}/{day}"
    time_text = f"{start_hour}:{start_minute} - {end_hour}:{end_minute}"
    title_text = "対面練習　参加調査"
    location_text = "@" + location

    # Draw the text on the image
    draw.text(month_day_coord, month_day_text, font=month_day_font, fill=color, stroke_width=2, stroke_fill="white")
    draw.text(time_coord, time_text, font=time_font, fill=color, stroke_width=2, stroke_fill="white")
    draw.text(title_coord, title_text, font=title_font, fill=color)
    draw.text(location_coord, location_text, font=location_font, fill=color)

    # Save the edited image
    image_name = f'practice_{data_id}.jpg'
    edited_img_path = f"./static/img/practices/{image_name}"
    img.save(edited_img_path)

    return image_name

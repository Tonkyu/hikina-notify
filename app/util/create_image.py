from PIL import Image, ImageDraw, ImageFont

def create_image(data):
    data_id = data[0]
    start_datetime = data[1]
    end_datetime = data[2]
    location = data[3]

    month = start_datetime.month
    day = start_datetime.day
    start_hour = start_datetime.strftime('%H')
    start_minute = start_datetime.strftime('%M')
    end_hour = end_datetime.strftime('%H')
    end_minute = end_datetime.strftime('%M')

    temp_img_path = './static/img/template.jpg'
    img = Image.open(temp_img_path)

    w, h = img.size

    color = (255, 255, 255)  # White color

    interval_size = int(0.08 * h)

    month_day_fontsize = 336
    time_fontsize = 190
    title_fontsize = 180
    location_fontsize = 100


    font_path = "./static/font/hiragino.ttc"
    #==============

    month_day_font = ImageFont.truetype(font_path, month_day_fontsize)
    time_font = ImageFont.truetype(font_path, time_fontsize)
    title_font = ImageFont.truetype(font_path, title_fontsize)
    location_font = ImageFont.truetype(font_path, location_fontsize)

    # Create a drawing context
    draw = ImageDraw.Draw(img)

    # Coordinates for the text (this will need to be adjusted to match the image)
    month_day_coord = (int(0.1*w), interval_size)  # Coordinates where the month/day will be drawn
    time_coord = (int(0.1*w), interval_size*2 + month_day_fontsize)   # Coordinates where the time will be drawn
    title_coord = (int(0.1*w), interval_size*3 + month_day_fontsize + time_fontsize)
    location_coord = (int(0.1*w), interval_size*4 + month_day_fontsize + time_fontsize + title_fontsize)   # Coordinates where the location will be drawn

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

    def draw_rounded_rectangle(draw, xy, rad, fill):
        x0, y0, x1, y1 = xy
        draw.rectangle([x0, y0 + rad, x1, y1 - rad], fill=fill)
        draw.rectangle([x0 + rad, y0, x1 - rad, y1], fill=fill)
        draw.pieslice([x0, y0, x0 + rad * 2, y0 + rad * 2], 180, 270, fill=fill)
        draw.pieslice([x1 - rad * 2, y1 - rad * 2, x1, y1], 0, 90, fill=fill)
        draw.pieslice([x0, y1 - rad * 2, x0 + rad * 2, y1], 90, 180, fill=fill)
        draw.pieslice([x1 - rad * 2, y0, x1, y0 + rad * 2], 270, 360, fill=fill)

    # 角丸四角形の位置とサイズを設定
    rect_x0, rect_y0,  = int(0.7 * w), interval_size,  # 四角形の大きさ（必要に応じて調整）
    rect_x1, rect_y1 = rect_x0 + month_day_fontsize, rect_y0 + month_day_fontsize
    radius = 40  # 角の丸み
    teiki_fontsize = int((rect_x1 - rect_x0) / 2 - 40)
    teiki_font = ImageFont.truetype(font_path, teiki_fontsize)


    # 角丸四角形を背景画像上に描画
    draw_rounded_rectangle(draw, [rect_x0, rect_y0, rect_x1, rect_y1], radius, 'white')

    teiki_text = "定期\n練習"
    text_width, text_height = draw.textsize(teiki_text, font=teiki_font)
    teiki_interval = 10
    text_x = (rect_x0 + rect_x1 - text_width - teiki_interval) / 2
    text_y = (rect_y0 + rect_y1 - text_height - teiki_interval) / 2 - 10  # 少し上に調整
    draw.text((text_x, text_y), "定", fill="red", font=teiki_font)
    draw.text((text_x + teiki_fontsize + teiki_interval, text_y), "期", fill="red", font=teiki_font)
    draw.text((text_x, text_y + teiki_fontsize + teiki_interval), "練", fill="red", font=teiki_font)
    draw.text((text_x + teiki_fontsize + teiki_interval, text_y + teiki_fontsize + teiki_interval), "習", fill="red", font=teiki_font)

    # Save the edited image
    image_name = f'practice_{data_id}.jpg'
    edited_img_path = f"./static/img/practices/{image_name}"
    img.save(edited_img_path)

    return image_name

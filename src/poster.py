import schedule
import glob
import os
import random
import time


def post(insta, source):
    images = list()
    for extension in ['*.jpg', '*.jpeg', '*.png']:
        images.extend(glob.glob(os.path.join(source, extension)))
    image = random.choice(images)
    text_file = os.path.splitext(image)[0] + ".txt"
    with open(text_file, 'r') as file:
        message = file.read()
        print(message)

    insta.post(image, message)
    os.unlink(image)
    os.unlink(text_file)


def run(insta, source):
    post(insta, source)
    schedule.every(2).to(4).hours.do(post, insta=insta, source=source)
    while True:
        schedule.run_pending()
        time.sleep(1)

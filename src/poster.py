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
    insta.post(image, 'Test')


def run(insta, source):
    post(insta, source)
    schedule.every(2).to(4).hours.do(post, insta=insta, source=source)
    while True:
        schedule.run_pending()
        time.sleep(1)

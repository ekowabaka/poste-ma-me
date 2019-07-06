import schedule
import glob
import os
import random
import time
import logging


logger = logging.getLogger('poster')

def post(insta, source):
    images = list()
    for extension in ['*.jpg', '*.jpeg', '*.png']:
        images.extend(glob.glob(os.path.join(source, extension)))
    if not images:
        logger.log(logging.ERROR, "Source directory is empty")
        return

    image = random.choice(images)
    logger.log(logging.INFO, f"Posting image {images}")
    text_file = f"{os.path.splitext(image)[0]}.txt"

    if os.path.exists(text_file):
        logger.log(logging.INFO, f"Reading post message from {text_file}")
        with open(text_file, 'r') as file:
            message = file.read()
    else:
        message = ''

    insta.post(image, message)
    os.unlink(image)
    os.unlink(text_file)


def run(insta, source):
    post(insta, source)
    schedule.every(2).to(4).hours.do(post, insta=insta, source=source)
    while True:
        schedule.run_pending()
        time.sleep(1)

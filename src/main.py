import argparse
import instagram


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str, nargs=1, required=True)
    parser.add_argument('--password', type=str, nargs=1, required=True)
    args = parser.parse_args()

    insta = instagram.WebUIInterface(args.username, args.password)
    insta.login()
    insta.post("/home/ekow/img004.jpg", "First automated test post")


if __name__ == "__main__":
    main()
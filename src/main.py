import argparse
import instagram
import poster


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str, nargs=1, required=True)
    parser.add_argument('--password', type=str, nargs=1, required=True)
    parser.add_argument('--source', type=str, required=True)
    args = parser.parse_args()

    #insta = instagram.Dummy(args.username, args.password) #instagram.WebUIInterface(args.username, args.password)
    insta = instagram.WebUIInterface(args.username, args.password)
    insta.login()
    poster.run(insta, args.source)
    #insta.post("/home/ekow/Pictures/James Ainooson 1 Roll E6 Disc 05.20.2019/000282810001.jpg", "First automated test post", expand=True)



if __name__ == "__main__":
    main()

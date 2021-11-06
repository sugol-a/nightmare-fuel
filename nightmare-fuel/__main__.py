#!/usr/bin/env python3

import argparse
import sys
import os
from bs4 import BeautifulSoup
import requests

BASE_URL = "http://nightmare.mit.edu"
FACES = "/faces"

def get_face_url():
    response = requests.get(BASE_URL + FACES)
    soup = BeautifulSoup(response.content, "html.parser")

    return BASE_URL + "/" + soup.find(name="img", class_="face")["src"]

def download_face(url, output_dir):
    response = requests.get(url)
    base_name = os.path.basename(url)
    with open(output_dir + "/" + base_name, "wb") as f:
        f.write(response.content)

def vprint(args, fmt):
    if args.verbose:
        print(fmt)

def main():
    parser = argparse.ArgumentParser(description="Download nightmare fuel in bulk!")
    parser.add_argument("-o", "--output", type=str, default=".", help="Output directory")
    parser.add_argument("-n", "--number", type=int, default=5, help="Number of faces to download")
    parser.add_argument("-v", "--verbose", action="store_true", help="Be verbose")
    parser.add_argument("-i", "--ignore-error", action="store_true", help="Continue on error")

    args = parser.parse_args()

    vprint(args, f" => Downloading {args.number} faces to \"{args.output}\"")

    # Try to create the output directory, if it doesn't already exist
    try:
        os.makedirs(args.output, exist_ok=True)
    except:
        print(f"Failed to mkdir {args.output}")
        exit(1)

    vprint(args, " => Accumulating face URLs")
    face_urls = [ get_face_url() for x in range(args.number) ]
    vprint(args, "\n".join(face_urls))

    vprint(args, " => Downloading faces")
    for i, url in enumerate(face_urls):
        vprint(args, f" => [{i + 1}/{args.number}] Fetching {url}")
        try:
            download_face(url, args.output)
        except Exception as e:
            print(f"Failed to download {url}: {e.message}")
            if args.ignore_error:
                continue
            else:
                exit(1)

    vprint(args, " => All done! Sweet dreams :)")

if __name__ == "__main__":
    main()

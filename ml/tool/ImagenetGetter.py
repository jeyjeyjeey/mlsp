# coding: utf-8
import sys
import os
import random
from requests import get
from urllib import request


def main():
    base_dir_path = ''
    dir_name = 'others'

    item_list, item_dict = create_id_label_pairs()
    item_ids = random.sample(item_dict.keys(), 500)
    download_multi_labels_in_samedir(item_ids, os.path.join(base_dir_path, dir_name), itr_max=1)


def download_multi_labels_in_samedir(item_ids, dir_name, itr_offset=0, itr_max=10):
    print(dir_name)
    os.makedirs(dir_name, exist_ok=True)
    for item_id in item_ids:
        req_url = f"http://www.image-net.org/api/text/imagenet.synset.geturls?wnid={item_id}"
        urls = download(req_url, decode=True)
        if urls == 'The synset is not ready yet. Please stay tuned!':
            continue
        urls_splited = urls.split()
        i = 0
        for url in urls_splited:
            if i < itr_offset:
                continue
            if i > itr_max:
                break

            file = str()
            try:
                file = os.path.split(url)[1]
                path = f"{dir_name}/{file}"
                write(path, download(url))
                print(f"done:{i}:{file}")
            except Exception as e:
                print(f"Unexpected error:{sys.exc_info()[0]}")
                print(f"error:{i}:{file}")
            i += 1


def download_multi_labels(classes):
    # classes = {"label": "id", ...}
    offset = 0
    max = 10
    for dir, id in classes.items():
        print(dir)
        os.makedirs(dir, exist_ok=True)
        urls = download(f"http://www.image-net.org/api/text/imagenet.synset.geturls?wnid={id}", decode=True).split()
        print(len(urls))
        i = 0
        for url in urls:
            if i < offset:
                continue
            if i > max:
                break

            file = str()
            try:
                file = os.path.split(url)[1]
                path = dir + "/" + file
                write(path, download(url))
                print("done:" + str(i) + ":" + file)
            except Exception as e:
                print("Unexpected error:", sys.exc_info()[0])
                print("error:" + str(i) + ":" + file)
            i = i + 1


def create_id_label_pairs():
    url = 'http://image-net.org/archive/words.txt'
    res = get(url)
    id_label_pairs_list = [line.split('\t') for line in res.text.split('\n')]
    return id_label_pairs_list, {pair[0]: pair[1] for pair in id_label_pairs_list}


def download(url, decode=False):
    response = request.urlopen(url)
    if response.geturl() == "https://s.yimg.com/pw/images/en-us/photo_unavailable.png":
        raise Exception("This photo is no longer available iamge.")

    body = response.read()
    if decode is True:
        body = body.decode()
    return body


def write(path, img):
    file = open(path, 'wb')
    file.write(img)
    file.close()


if __name__ == '__main__':
    main()

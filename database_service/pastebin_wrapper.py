import random
import sys

import requests

sys.path.insert(0, '..')
import config


def _get_next_key():

    nxt = config.PASTEBIN_KEYS.pop(0)
    config.PASTEBIN_KEYS.append(nxt)

    return nxt


def add_paste(new_text):
    possible = list(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")

    random.shuffle(possible)

    paste_name = "".join(possible[:32])

    def try_actual_bin_creation(api_key):
        payload = {
            "api_dev_key": api_key,
            "api_option": 'paste',
            "api_paste_code": new_text,
            "api_paste_private": '0',
            "api_paste_name": paste_name,
            "api_paste_expire_date": '6M'
        }

        url = "https://pastebin.com/api/api_post.php"
        response = requests.request("POST", url, data=payload)

        if not response.text.startswith("http"):
            print(response.text)
            return False, "There was some sort of error in pastebin: " + response.text

        else:
            return True, response.text

    succeeded = (False,)
    i = 0
    while not succeeded[0] or i == len(config.PASTEBIN_KEYS):
        succeeded = try_actual_bin_creation(_get_next_key())
        i += 1

    if not succeeded[0]:
        raise RuntimeError(succeeded[1])

    else:
        paste_id = succeeded[1].split("/")[-1]
        return "https://pastebin.com/raw/" + paste_id


def get_paste(paste_url):
    return requests.request("GET", paste_url).text

import io
import base64
import logging

import bs4
import aiohttp
from nbt import nbt
from nbt.nbt import NBTFile

bs = bs4.BeautifulSoup
logger = logging.getLogger('wrapper')


def get_rank(html):
    soup = bs(html)
    name = bs(str(soup.find(class_="rank-name"))).string if soup.find(class_='rank-name') is not None else ""
    plustext = bs(str(soup.find(class_='rank-plus-text'))).string if soup.find(class_='rank-plus-text') is not None else ""
    return f"{name}{plustext}"


def walk_nbt(_nbt):
    """Walk through an nbtfile/nbt object

    :param _nbt: the nbtfile/nbt object
    :return: dict
    """
    items = {}
    recurse = [
        nbt.TAG_Long_Array,
        nbt.TAG_List,
        nbt.TAG_Compound,
        nbt.TAG_Byte_Array,
        nbt.TAG_Int_Array
    ]
    for i in _nbt:
        if type(i) in recurse:
            walk_nbt(i)
        if len(i) == 0:
            items[i] = None


def unpack_raw(raw):
    """Unpack raw b64 encoded gzipped nbt data
    Steps:
        1. Decode base 64
        2. nbt.nbt.NBTFile(fileobj=io.BytesIO())
        3. Walk tree and return it as json/dict
    """
    decoded = base64.b64decode(raw)
    nbtfile = NBTFile(fileobj=io.BytesIO(decoded))

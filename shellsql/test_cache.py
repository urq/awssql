import os
import time
import shutil

from .cache import TTLCache, FileCache, MemCache

def test_TTLCache():
    c = TTLCache(MemCache())
    c.insert(.016, 'this', 'that') # stash for 1 second
    assert c.get('this') == 'that'
    time.sleep(1)
    assert c.get('this') is None
    c.insert(.016, 'this', 'foo')
    c.remove('this')
    assert c.get('this') is None

def test_filecache():
    cache_dirname = '/tmp/file.cache'
    if os.path.exists(cache_dirname):
        shutil.rmtree(cache_dirname)
    if not os.path.exists(cache_dirname):
        os.mkdir(cache_dirname)
    c = TTLCache(FileCache(cache_dirname))
    c.insert(.016, 'this', 'that') # stash for 1 second
    assert c.get('this') == 'that'
    time.sleep(1)
    assert c.get('this') is None
    c.insert(.016, 'this', 'foo')
    c.remove('this')
    assert c.get('this') is None
    shutil.rmtree(cache_dirname)


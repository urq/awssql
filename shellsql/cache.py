from datetime import datetime
import os
import time

BIN_DELIMITER = '|%|%|'

class FileCache:
    def __init__(self, basepath):
        self.basepath = basepath

    def insert(self, key, *blobs):
        if os.path.exists(os.path.join(self.basepath, key)):
            self.remove(key)
        with open(os.path.join(self.basepath, key), 'wb') as f:
            for i, blob in enumerate(blobs):
                f.write(blob)
                if i < len(blobs)-1:
                    f.write(BIN_DELIMITER)

    def get(self, key):
        if not os.path.exists(os.path.join(self.basepath, key)):
            return None
        with open(os.path.join(self.basepath, key), 'rb') as f:
            ret = f.read()
        return ret.split(BIN_DELIMITER)

    def remove(self, key):
        os.remove(os.path.join(self.basepath, key))

class MemCache:
    def __init__(self):
        self._items = {}

    def insert(self, key, *blobs):
        self._items[key] = blobs

    def get(self, key):
        return self._items.get(key)

    def remove(self, key):
        if self._items.has_key(key):
            del self._items[key]

class TTLCache:
    def __init__(self, backing_cache):
        self.backing_cache = backing_cache

    def insert(self, ttl, key, *blobs):
        if not ttl:
            ttl = 60
        timestamp = str(time.time() + (ttl * 60))
        self.backing_cache.insert(key, timestamp, *blobs)

    def get(self, key, datetime_check=None):
        try:
            timestamp, item = self.backing_cache.get(key)
            item_expiry = datetime.fromtimestamp(float(timestamp))
        except (ValueError, TypeError):
            return None
        if not datetime_check:
            datetime_check = datetime.fromtimestamp(time.time())
        if item_expiry < datetime_check:
            self.remove(key)
            return None
        else:
            return item

    def remove(self, key):
        self.backing_cache.remove(key)


#### Picture Cache — LRU cache for get_pic_list() results ####
# Phase 0.4: Caches filtered picture lists to avoid repeated linear scans
# of all pictures in a girl pack. Invalidated on girl state changes.

init -2 python:

    class PictureCache(object):
        """LRU cache for picture tag-filter results.

        Key: (thing_key, frozenset(tags), frozenset(and_tags), frozenset(not_tags))
        Value: list of (Picture, weight) tuples

        On cache hit, avoids iterating every Picture in a pack and calling
        has_tags() on each one.
        """

        MAX_SIZE = 512
        _cache = {}
        _access_order = []  # Most recently used at the end

        @classmethod
        def _make_key(cls, thing, tags, and_tags, not_tags):
            """Build a hashable cache key from the lookup parameters."""
            if isinstance(thing, Girl):
                thing_key = thing.path
            elif hasattr(thing, 'path'):
                thing_key = thing.path
            else:
                thing_key = id(thing)

            return (
                thing_key,
                frozenset(tags or ()),
                frozenset(and_tags or ()),
                frozenset(not_tags or ()),
            )

        @classmethod
        def get(cls, thing, tags, and_tags, not_tags):
            key = cls._make_key(thing, tags, and_tags, not_tags)
            if key in cls._cache:
                # Move to end (most recently used)
                cls._access_order.remove(key)
                cls._access_order.append(key)
                return cls._cache[key]
            return None

        @classmethod
        def put(cls, thing, tags, and_tags, not_tags, piclist):
            key = cls._make_key(thing, tags, and_tags, not_tags)
            if key in cls._cache:
                cls._access_order.remove(key)
            cls._cache[key] = piclist
            cls._access_order.append(key)
            cls._evict()

        @classmethod
        def evict(cls, thing):
            """Invalidate all cached entries for a specific thing (Girl)."""
            if isinstance(thing, Girl):
                thing_key = thing.path
            elif hasattr(thing, 'path'):
                thing_key = thing.path
            else:
                thing_key = id(thing)

            to_remove = [k for k in cls._cache if k[0] == thing_key]
            for k in to_remove:
                del cls._cache[k]
                cls._access_order.remove(k)

        @classmethod
        def invalidate_all(cls):
            """Clear the entire cache (e.g. after global settings change)."""
            cls._cache.clear()
            cls._access_order = []

        @classmethod
        def _evict(cls):
            """Remove oldest entries when cache exceeds MAX_SIZE."""
            while len(cls._cache) > cls.MAX_SIZE:
                oldest_key = cls._access_order.pop(0)
                del cls._cache[oldest_key]

        @classmethod
        def size(cls):
            return len(cls._cache)

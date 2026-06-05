## BK Phase 6 — Tag Registry
## Replaces the hard-coded tag_dict and tag_list_dict from settings.rpy
## Supports runtime tag registration for Mods and custom girl packs.

init -5 python:

    class TagRegistry(Registry):
        """Registry for picture filename-to-game-tag mappings."""

        def __init__(self):
            super(TagRegistry, self).__init__(name="TagRegistry")
            # tag_list_dict maps old compound tags to their canonical replacements
            self._tag_list = {}

        def register_tag(self, filename_substring, game_tags, tag_list=None):
            """
            Register a filename substring -> game tag(s) mapping.
            :param filename_substring: substring to look for in picture filenames
            :param game_tags: single tag string or tuple/list of tag strings
            :param tag_list: optional tag_list mapping for compound tags
            """
            if isinstance(game_tags, str):
                game_tags = (game_tags,)
            self.register(filename_substring, game_tags, category="tag")
            if tag_list is not None:
                self._tag_list[filename_substring] = tag_list

        def register_tags_bulk(self, tag_dict):
            """Bulk register from a dict {filename_substring: tags}."""
            for substr, tags in tag_dict.items():
                self.register_tag(substr, tags)

        def get_tags(self, filename_substring):
            """Return the game tags for a given filename substring."""
            return self._registry.get(filename_substring, None)

        def get_tag_list(self, old_tag):
            """Return tag_list mapping for an old compound tag."""
            return self._tag_list.get(old_tag, None)

        def get_all_tags(self):
            """Return all registered filename substrings."""
            return list(self._registry.keys())

        def get_tag_list_dict(self):
            """Return the full tag_list dict (for backward compat)."""
            return self._tag_list.copy()

    # Create singleton and proxy
    _tag_registry = TagRegistry()
    tag_registry = _tag_registry

    # Backward-compat proxy: tag_dict[key] now reads from registry
    tag_dict = _RegistryProxy(_tag_registry)

    # Backward-compat alias for tag_list_dict (read-only view)
    def _tag_list_dict_get(tag_name):
        return _tag_registry.get_tag_list(tag_name)

    # We cannot make tag_list_dict a full proxy because it's not a Registry.
    # Instead we expose a wrapper class.
    class _TagListDictProxy(object):
        def __getitem__(self, key):
            return _tag_registry.get_tag_list(key)
        def __contains__(self, key):
            return key in _tag_registry._tag_list
        def get(self, key, default=None):
            return _tag_registry.get_tag_list(key) or default
        def keys(self):
            return _tag_registry._tag_list.keys()
        def values(self):
            return _tag_registry._tag_list.values()
        def items(self):
            return _tag_registry._tag_list.items()
        def __repr__(self):
            return "<_TagListDictProxy %s>" % repr(_tag_registry._tag_list)

    tag_list_dict = _TagListDictProxy()

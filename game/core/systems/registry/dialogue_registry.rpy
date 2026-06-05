## BK Phase 6 — Dialogue Registry
## Replaces the hard-coded dialogue_dict from gameplay/dialogue.rpy
## Supports runtime dialogue registration for Mods and girl packs.

init -5 python:

    class DialogueRegistry(Registry):
        """
        Registry for all Dialogue lines.
        Internal structure: {topic: {key: [Dialogue, ...]}}
        This matches the old dialogue_dict nested defaultdict pattern.
        """

        def __init__(self):
            super(DialogueRegistry, self).__init__(name="DialogueRegistry")
            # We store topics as nested registries
            self._topics = {}

        def _ensure_topic(self, topic):
            if topic not in self._topics:
                self._topics[topic] = {}
            return self._topics[topic]

        def register_dialogue(self, topic, key, dialogue, merge=False):
            """
            Register one or more Dialogue objects under a topic + key.
            :param topic: top-level topic string
            :param key: sub-key (usually personality name or "generic")
            :param dialogue: single Dialogue or list of Dialogue
            :param merge: if True, append to existing; if False, replace
            """
            topic_dict = self._ensure_topic(topic)
            if key not in topic_dict:
                topic_dict[key] = []
            if not isinstance(dialogue, list):
                dialogue = [dialogue]
            if merge:
                topic_dict[key].extend(dialogue)
            else:
                topic_dict[key] = dialogue

        def get_dialogue(self, topic, key="generic"):
            """Return list of Dialogue objects for topic + key."""
            topic_dict = self._topics.get(topic, {})
            return topic_dict.get(key, [])

        def get_topic_keys(self, topic):
            """Return all keys registered under a topic."""
            return list(self._topics.get(topic, {}).keys())

        def get_topics(self):
            """Return all registered topics."""
            return list(self._topics.keys())

        def merge_topic(self, topic, other_topic_dict):
            """Merge an entire topic dict (e.g. from a Mod)."""
            topic_dict = self._ensure_topic(topic)
            for key, dialogues in other_topic_dict.items():
                if key not in topic_dict:
                    topic_dict[key] = []
                topic_dict[key].extend(dialogues)

        # Backward-compat: make DialogueRegistry behave like the old nested dict
        class _TopicProxy(object):
            def __init__(self, topic_dict):
                self._td = topic_dict
            def __getitem__(self, key):
                return self._td.get(key, [])
            def __contains__(self, key):
                return key in self._td
            def keys(self):
                return self._td.keys()
            def values(self):
                return self._td.values()
            def items(self):
                return self._td.items()

        class _DialogueDictProxy(object):
            """Proxy that mimics defaultdict(return_ddict_list)."""
            def __init__(self, registry):
                self._reg = registry
            def __getitem__(self, topic):
                return DialogueRegistry._TopicProxy(self._reg._ensure_topic(topic))
            def __contains__(self, topic):
                return topic in self._reg._topics
            def keys(self):
                return self._reg._topics.keys()
            def values(self):
                return [DialogueRegistry._TopicProxy(v) for v in self._reg._topics.values()]
            def items(self):
                return [(k, DialogueRegistry._TopicProxy(v)) for k, v in self._reg._topics.items()]
            def get(self, topic, default=None):
                if topic in self._reg._topics:
                    return DialogueRegistry._TopicProxy(self._reg._ensure_topic(topic))
                return default

    _dialogue_registry = DialogueRegistry()
    dialogue_registry = _dialogue_registry
    dialogue_dict = DialogueRegistry._DialogueDictProxy(_dialogue_registry)

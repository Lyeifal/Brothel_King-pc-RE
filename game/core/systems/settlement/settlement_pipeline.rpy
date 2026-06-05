## BK Phase 6 — Settlement Pipeline
## Modular settlement system with hook support for Mods.
## 
## The pipeline runs the end-of-day settlement in configurable phases.
## Each phase can be intercepted by Mods via HookManager.

init -3 python:

    class SettlementContext(object):
        """
        Mutable context object passed through all settlement phases.
        Mods can read/write this context via hooks.
        """
        def __init__(self):
            self.log = None
            self.change_log = None
            self.perform_events = []
            self.night_text = ""
            self.working_girls = []
            self.striking_girls = []
            self.resting_girls = []
            self.sick_girls = []
            self.away_girls = []
            self.job_girls = []
            self.whores = []
            self.customers = []
            self.ent_dict = {}
            self.wh_list = []
            self.income = 0
            self.upkeep = 0
            self.costs = 0
            self.net = 0
            self.cancelled = False

        def cancel(self):
            """Allow a Mod hook to cancel the settlement (use with care)."""
            self.cancelled = True

    class SettlementPhase(object):
        """Definition of a settlement phase."""
        def __init__(self, name, handler, order=0):
            self.name = name
            self.handler = handler
            self.order = order

    class SettlementPipeline(object):
        """Manager for settlement phases."""

        _instance = None

        def __new__(cls):
            if cls._instance is None:
                cls._instance = super(SettlementPipeline, cls).__new__(cls)
                cls._instance._phases = []
                cls._instance._built_in = False
            return cls._instance

        @classmethod
        def instance(cls):
            return cls.__new__(cls)

        def register_phase(self, name, handler, order=0):
            """Register a new settlement phase."""
            self._phases.append(SettlementPhase(name, handler, order))
            self._phases.sort(key=lambda p: p.order)

        def unregister_phase(self, name):
            self._phases = [p for p in self._phases if p.name != name]

        def get_phases(self):
            return [p.name for p in self._phases]

        def run_phase(self, phase, context):
            """Run a single phase with pre/post hooks."""
            # Pre-phase hook
            hook_manager.invoke("pre_settlement_phase", phase.name, context)
            hook_manager.invoke("pre_settlement_" + phase.name, context)

            # Run phase handler
            if not context.cancelled:
                phase.handler(context)

            # Post-phase hook
            hook_manager.invoke("post_settlement_" + phase.name, context)
            hook_manager.invoke("post_settlement_phase", phase.name, context)

        def run_phase_by_name(self, name, context):
            """Run a single phase by name with pre/post hooks."""
            for phase in self._phases:
                if phase.name == name:
                    self.run_phase(phase, context)
                    return True
            return False

        def run(self, context):
            """Run all registered phases in order."""
            hook_manager.invoke("on_settlement_start", context)

            for phase in self._phases:
                if context.cancelled:
                    break
                self.run_phase(phase, context)

            hook_manager.invoke("on_settlement_end", context)

    settlement_pipeline = SettlementPipeline.instance()

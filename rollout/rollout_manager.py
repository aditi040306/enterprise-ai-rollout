from dataclasses import dataclass, asdict
from threading import Lock
import random


@dataclass
class RolloutConfig:
    active_model: str = "v1"
    shadow_enabled: bool = True
    canary_enabled: bool = False
    canary_model: str = "v2"
    canary_percent: int = 0


class RolloutManager:
    def __init__(self):
        self._config = RolloutConfig()
        self._lock = Lock()

    def get_config(self):
        with self._lock:
            return asdict(self._config)

    def update_config(self, updates):
        with self._lock:
            for key, value in updates.items():
                if value is not None and hasattr(self._config, key):
                    setattr(self._config, key, value)

            if self._config.canary_percent < 0:
                self._config.canary_percent = 0

            if self._config.canary_percent > 100:
                self._config.canary_percent = 100

            return asdict(self._config)

    def choose_model_for_request(self):
        with self._lock:
            if (
                self._config.canary_enabled
                and self._config.canary_percent > 0
                and random.randint(1, 100) <= self._config.canary_percent
            ):
                return self._config.canary_model, "canary"

            return self._config.active_model, "active"

    def get_shadow_model(self, decision_model):
        with self._lock:
            if not self._config.shadow_enabled:
                return None

            shadow_model = self._config.canary_model

            if shadow_model == decision_model:
                return None

            return shadow_model


rollout_manager = RolloutManager()
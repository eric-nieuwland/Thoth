"""
profile_mixin - mix-in for Pydantic profile classes to add the ability to instances to be evaluated as boolean
"""

from __future__ import annotations

# standard library
from typing import Self

# third party

# own


class ProfileMixIn:
    """
    mix-in for Pydantic profile classes to add the ability to instances to be evaluated as boolean
    """

    @classmethod
    def _as_profile_dict(cls, value: str) -> dict:
        return {
            field_name: value if field_def.annotation == bool else field_def.annotation._as_profile_dict(value)
            for field_name, field_def in cls.model_fields.items()
        }

    @classmethod
    def yes_to_all(cls) -> Self:
        arg = cls._as_profile_dict("true")
        instance = cls.model_validate(arg)
        return instance

    def __bool__(self) -> bool:
        """
        create instance from a YAML definition file
        """
        return any(getattr(self, field) for field in self.model_fields)

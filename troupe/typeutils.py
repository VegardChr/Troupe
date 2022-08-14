"""Type utilities module."""

from typing import Any, Protocol


# Modified from: 
# https://github.com/python/typeshed/blob/7b54854c90aa560d99e353ae2f9fd8b6b9cff40a/stdlib/_typeshed/__init__.pyi#L69
class SupportsRichComparison(Protocol):
    """Rich comparison protocol."""

    def __lt__(self, __other: Any) -> bool:
        ...

    def __gt__(self, __other: Any) -> bool:
        ...

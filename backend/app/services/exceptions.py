"""Domain exceptions for carbon engine and business logic."""


class CarbonEngineError(Exception):
    """Base exception for all carbon engine errors."""


class EmissionFactorNotFoundError(CarbonEngineError):
    """Raised when no matching emission factor exists in the database."""


class UnitMismatchError(CarbonEngineError):
    """Raised when activity unit does not match emission factor unit."""


class InvalidQuantityError(CarbonEngineError):
    """Raised when activity quantity is invalid (e.g. <= 0)."""


class InvalidActivityDataError(CarbonEngineError):
    """Raised when activity data violates business rules."""


class UserNotFoundError(CarbonEngineError):
    """Raised when requested user does not exist in the database."""


class AmbiguousEmissionFactorError(CarbonEngineError):
    """Raised when multiple conflicting emission factors match query criteria."""

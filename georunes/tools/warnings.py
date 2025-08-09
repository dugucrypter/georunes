import warnings


class GeoRunesWarning(Warning):
    """Base warning class for GeoRunes package."""
    pass


class DataFormatWarning(GeoRunesWarning):
    """Raised when input data format is not supported or inconsistent."""
    pass


class DataIntegrityWarning(GeoRunesWarning):
    """Raised when data quality issues are detected (e.g., NaNs, outliers)."""
    pass


class UnitsWarning(GeoRunesWarning):
    """Raised when inconsistent or unexpected units are detected."""
    pass


class FunctionParameterWarning(GeoRunesWarning):
    """Raised when an invalid parameter value is provided."""
    pass


class InsufficientDataWarning(GeoRunesWarning):
    """Raised when input data is insufficient for reliable modal estimation."""
    pass


class ConvergenceWarning(GeoRunesWarning):
    """Raised when optimization methods fail to converge."""
    pass


class PlotDataWarning(GeoRunesWarning):
    """Warning related to issues in data plotting."""
    pass

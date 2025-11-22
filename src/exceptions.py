from json import JSONDecodeError


class VerificationError(Exception):
    pass


class DecodeError(VerificationError, JSONDecodeError):
    pass


class SchemaError(VerificationError):
    pass


class ManualInterruption(VerificationError):
    pass

class InvalidKeys(Exception):
    def __init__(self, valid_keys, invalid_keys) -> None:
        self.message = {
            "valid_keys":valid_keys,
            "invalid_keys":invalid_keys
        }
        super().__init__(self.message)
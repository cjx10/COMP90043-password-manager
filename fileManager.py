import os


class File:
    def __init__(self, file_name: str):
        if os.path.exists(file_name):
            self.file = open(file_name, "r+b")

    def prepare_write(self):
        self.file.seek(0, 2)

    def write(self, data: str):
        self.write_bin(data.encode("utf8"))

    def write_bin(self, data: bytes):
        # Write length of data block as header
        self.file.write(len(data).to_bytes(4, "big"))
        # Write in data itself
        self.file.write(data)

    def read_next(self) -> str:
        return self.read_next_bin().decode("utf8")

    def read_next_bin(self) -> bytes:
        # Read next block length first
        block_length = int.from_bytes(self.file.read(4), "big")
        # Read and return the whole block
        return self.file.read(block_length)

    def skip(self):
        self.read_next_bin()

    def close(self):
        self.file.close()

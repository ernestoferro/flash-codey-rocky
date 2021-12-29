def bytes_to_hex_str(data: bytes) -> str:
    return ' '.join(f'{byte:02x}' for byte in data)

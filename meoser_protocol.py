# Based on https://www.npmjs.com/package/meoser
from struct import pack
from typing import Iterator

FRAME_NECK = b'\x00\x5e'
MEOS_FRAME_HEAD = b'\xf3'
MEOS_FRAME_END = b'\xf4'


def serialize_flash_code_command(code: str) -> Iterator[bytes]:
    path = '/flash/main.py'
    limit_length = 100
    file_content_bytes = code.encode()

    yield create_file_header_packet(path, file_content_bytes)

    for index in range(0, len(file_content_bytes), limit_length):
        data_slice = file_content_bytes[index: index + limit_length]
        yield create_file_body_slice_packet(index, data_slice)


def create_file_header_packet(path: str, file_content_bytes: bytes) -> bytes:
    file_protocol_id_bytes = pack('B', 0x01)
    command_id_bytes = pack('B', 0x01)  # FILE_CMD_ID.HEAD

    # command data
    file_type_bytes = pack('B', 0x00)
    file_size_bytes = pack('<L', len(file_content_bytes))
    file_checksum_bytes = calculate_file_checksum(file_content_bytes)
    filename_bytes = path.encode()
    command_data = (
        file_type_bytes +
        file_size_bytes +
        file_checksum_bytes +
        filename_bytes
    )
    command_length_bytes = pack('<H', len(command_data))

    return create_protocol_packet(
        file_protocol_id_bytes +
        FRAME_NECK +
        command_id_bytes +
        command_length_bytes +
        command_data
    )


def create_file_body_slice_packet(start_index: int, data_slice: bytes) -> bytes:
    command_id_bytes = pack('B', 0x02)  # FILE_CMD_ID.BODY
    offset_bytes = pack('<L', start_index)
    command_length_bytes = pack('<H', len(offset_bytes) + len(data_slice))
    file_protocol_id_bytes = pack('B', 0x01)

    return create_protocol_packet(
        file_protocol_id_bytes +
        FRAME_NECK +
        command_id_bytes +
        command_length_bytes +
        offset_bytes +
        data_slice
    )


def create_protocol_packet(payload: bytes) -> bytes:
    frame_length_bytes = pack('<H', len(payload))
    header_checksum_bytes = calculate_frame_checksum(MEOS_FRAME_HEAD + frame_length_bytes)
    frame_data_checksum_bytes = calculate_frame_checksum(payload)

    return (
        MEOS_FRAME_HEAD +
        header_checksum_bytes +
        frame_length_bytes +
        payload +
        frame_data_checksum_bytes +
        MEOS_FRAME_END
    )


def calculate_frame_checksum(data: bytes) -> bytes:
    return pack('B', sum(data) & 0xff)


def calculate_file_checksum(data: bytes) -> bytes:
    checksum = [0, 0, 0, 0]

    for i in range(len(data)):
        checksum[i % 4] ^= data[i]

    return bytes(checksum)

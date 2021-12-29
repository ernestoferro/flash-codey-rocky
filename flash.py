import sys
from configparser import ConfigParser
from typing import Optional, Tuple

import serial
from meoser_protocol import serialize_flash_code_command
from utils import bytes_to_hex_str


def read_protocol_message(ser: serial.Serial) -> Tuple[Optional[bytes], Optional[str]]:
    start_protocol: bytes = ser.read()

    if start_protocol == b'\xf3':
        protocol_message = start_protocol + b''.join(iter(ser.read, b'\xf4'))
        return protocol_message, None
    elif start_protocol:
        text_message = (start_protocol + ser.read(1000)).decode()
        return None, text_message

    return None, None


def main() -> None:
    if len(sys.argv) < 2:
        print('call it with a file to flash')
        sys.exit(1)

    config = ConfigParser()
    config.read('flash.ini')

    with open(sys.argv[1], 'r', encoding='utf-8') as code_file:
        code = code_file.read()

    change_to_upload_mode_command = b'\xf3\xf6\x03\x00\x0d\x00\x00\x0d\xf4'
    verbose = config.getboolean('general', 'verbose')
    serial_port_device = config['general']['serial_port_device']

    with serial.Serial(serial_port_device, 115200, timeout=1) as ser:
        if verbose:
            print(f'> {bytes_to_hex_str(change_to_upload_mode_command)}')

        ser.write(change_to_upload_mode_command)
        ser.flush()
        read_protocol_message(ser)

        print('flashing program')
        for data_chunk in serialize_flash_code_command(code):
            if verbose:
                print(f'> {bytes_to_hex_str(data_chunk)}')

            ser.write(data_chunk)
            ser.flush()
            protocol_message, _ = read_protocol_message(ser)

            if verbose and protocol_message:
                print(bytes_to_hex_str(protocol_message))

        print('reading stdout (ctrl+c to exit)\n\n')
        while True:
            _, text_message = read_protocol_message(ser)

            if text_message:
                print(text_message)


if __name__ == '__main__':
    main()

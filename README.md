# What?

A command-line tool to flash python code to Codey Rocky without having to use the online mblock5 IDE.

## Description
 
This is a very low-effort project born out of my desire of using Vim when programming Codey. Don't expect much.
It's a super simple command-line tool to flash Codey with micropython code and get the output from `print` in
your terminal.

Why did I do this? Because I wanted to use my preferred text editor instead of the online mblock5 IDE. The IDE is
alright but just too simple for my taste. And the upload of new code takes quite a bit!
Another minor issue is that I just wanted the output from `print` to be shown in the terminal and the serial output in
mblock is a bit clunky in that area.

## Getting Started

### Dependencies

`pip install -r requirements.txt`

### Executing program

Check if the path to your serial port device is what you expect on flash.ini and then run:
`python flash.py some_program.py`

If you get a FileNotFoundException, it's probably because the serial port file in the ini file is incorrect, or Codey is
off. Again, this is a low-effort project.

### Example
```
SHELL$ cat demo.py   # the program to flash
print('it worked!')

SHELL$ python flash.py demo.py   # flashing it to Codey
flashing program
reading stdout (ctrl+c to exit)

it worked!
```

## Thing to improve

Since I didn't put much effort into this, feel free to fork this and improve on:
* Error handling.
* Better command-line interface with flags.
* Not having a config file but instead a template of it that will be used to create the config file if missing.
* Reading and interpreting the protocol messages that Codey send back. Right now they are being ignored.
* In general, better structure in the codebase if this happens to grow.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

This is mostly a port of some of the functions in [meoser.js](https://www.npmjs.com/package/meoser)

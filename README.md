# havoc-ducky
A ducky script generator for havoc. This extension allows you to quickly embed your payloads
inside of ducky scripts with a simple syntax.

![https://github.com/p4p1/havoc-ducky/blob/main/assets/ducky_example.png?raw=true](https://github.com/p4p1/havoc-ducky/blob/main/assets/ducky_example.png?raw=true)

## Installation
It is recommend to install this extention through the [Havoc Extension Tab](https://p4p1.github.io/havoc-store/).

## Syntax
You can configure 2 variables one for base64 data and one for a link that has your payload

| VARIABLE               | Description                               |
|------------------------|-------------------------------------------|
| {DUCKY_BASE64_PAYLOAD} | The base 64 data of a provided .bin file. |
| {DUCKY_REMOTE_URL}     | The url of a .exe payload file.           |

_Custom payloads can also be saved inside of payload/_

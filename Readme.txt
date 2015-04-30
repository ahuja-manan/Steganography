# Steganography---Python

Run steganography.py 

Tasks

1) Convert message to binary digits (optional)
Use the function message_to_bits(message) to convert a string of ASCII characters to a string of binary digits.
eg. message_to_bits('A') will return '01000001'

2) Convert bits to message (optional)
Use the function bits_to_message(message_bits) to convert a string of binary digits to a string of ASCII characters.
eg. bits_to_message('01000001') will return 'A'

3) & 4) Encode message in image & Decode encoded image
The image should be a rectangular list of pixels.
So use the read_image and write_image functions from the SimpleImage library to convert an image to a 2d list of pixels and back.

Use the function encode(image, message) to secretly encode the message in the image.
The function would return the image with pixel values slightly changed (i.e. with the message encoded). 

Use the function decode(image) to decode an encoded message.
The function would return the secret message hidden in the image.

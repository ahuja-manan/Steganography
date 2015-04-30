'''
Steganography
--------------

Steganography is the science of writing secret messages 
in such a way that no one apart from the sender and
recepient suspect the existence of the message.

This program converts a secret message into one long 
string of bits. The message is hidden inside an image by 
setting the least significant bit (LSB)
of each pixel value equal to the message bit.

It is important to note that images a
re represented as rectangular two dimensional
lists of pixels in zero based, row major order.
Each pixel is represented by a three element tuple
of integers that specify the intensity of red, green
and blue component colours of the dot.

'''

#############################################################
# Author : Manan Ahuja
#
# Date created : 29/09/2013
#
# This program is designed to be used with Python 2.7.
#
# Thanks to Bernie Pope and Daniel Williams for their help.
#
#############################################################

#Importing helper libraries to be able to call functions
#defined in these libraries.

import bits
import SimpleImage

#Task 1
'''
Defining a function to convert a message into a long string of bits.
The char_to_bits function in the bits.py module only converts
one ASCII character into an 8 bit string of 1s and 0s.
Thus, it is important to use a loop to call this function for 
every character in the message and then concatenate the outputs
to get one long string of bits.
'''
def message_to_bits(message):
    result = ''
    for char in message:
        result += bits.char_to_bits(char)
    return result

#Task 2 
'''
Defining a function that converts a string of binary digits into 
a string of ASCII characters. The function should stop when either

## There are fewer than 8 bits left.
## There are 8 consecutive 0 bits starting 
   at an index which is a multiple of 8.
'''
def bits_to_message(message_bits):
    result = ''
    while len(message_bits) >= 8:
        if message_bits[:8] == "00000000":
            break
        #The function stops the conversion if there are 8
        #consecutive 0 bits in message_bits.    
        else:
            result += bits.bits_to_char(message_bits[:8])
            #The bits_to_char function converts a string of 8 binary digits
            #(0s and 1s) into a string of ASCII characters.
            message_bits = message_bits[8:] 
            #Slicing message_bits by removing the first 8 characters that
            #have been converted into a string of ASCII characters.   
    return result

#Task 3
'''
Defining a function to encode a secret message into the
pixel values of an image. The message which is a string 
of ASCII characters is first converted into a binary string
using the message_to_bits function defined above. Then, the
LSB of pixel intensity values are set equal to each bit in 
the binary string.

It is important to note: 
##If there are more bits in the binary string than intensity
values in the image, the function should encode as many bits
of the binary string as possible.

##If there are fewer bits in the binary message than
intensity values in the image, the function should set the LSBs 
of any remaining intensity values to 0. 
'''

'''
A helper function called change_lsb is defined which takes 2 arguments
- the image which is a 2 dimensional list of pixels and message_bit 
which is a string of bits containing the secret message.

This function sets the LSB of the pixel intensity values equal to each 
bit in the binary string and returns a new 2 dimensional list containing
the changed pixel intensity values.
'''

def change_lsb(image,message_bit):
    new_image = [] #Defining the new image list.
    for row in image:
        new_row = []
        for a in range(len(image[0])):
            pixel = list(row[a])
            #The tuple consisiting of the intensity values of a pixel
            #is converted to a list. This is done to be able to mutate
            #the list since tuples are immutable.
            for b in range(len(image[0][0])):
                pixel[b] = bits.set_bit(pixel[b], message_bit[0], 0)
                #The set_bit function from the bits.py module is called
                #here and it sets the LSB of the intensity value equal to
                #the first character of message_bit.
                message_bit = message_bit[1:]
                #message_bit is sliced i.e the first character is removed
                #after it has been set equal to the LSB of an intensity value.
            new_row.append(tuple(pixel))
            #A pixel is represented as a tuple in the image which itself
            #is a 2 dimensional list. Hence, the mutated list is converted
            #to a tuple and appended to the new_row list.
        new_image.append(new_row)
        #For every row in the original image, the new_row is appended to
        #the new_image list.        
    return new_image
    #The function returns the encoded image which is a 2 dimensional list
    #consisting of the changed pixel intensity values.

'''
Defining the encode function that takes 2 arguments - the image
and the message that needs to be encoded into it.
This function takes care of the cases when the number of bits
in the binary string maybe more or less than the number of intensity values
in the image. It calls the above defined change_lsb function wherever required.
'''
def encode(image,message):
    message_bit = message_to_bits(message)
    len_image = SimpleImage.get_width(image)*SimpleImage.get_height(image)*3
    #To calculate the no of intensity values in the image, 2 helper
    #functions predefined in the SimpleImage.py module are used. 
    #The get_width and get_height functions return the no of columns 
    #and rows in the image respectively. The number of intensity values
    #is the product of the no of rows, no of columns and the integer 3 
    #(because each pixel has 3 intensity values).
    len_message = len(message_bit)
    #The length of the message string is also calculated.
    if len_image > len_message:
        message_bit += (len_image - len_message) * "0"
        #If there are more intensity values in the image than bits in
        #the binary string, then, the LSBs of the remaining intensity
        #values are set to 0. To achieve this, the message_bit string
        #is concatenated with (len_image - len_message)number of zeroes('0').
        new_image = change_lsb (image,message_bit)
        #The change_lsb function is called and it encodes the message_bit
        #(that has been concatenated with 0s) into the image and returns
        #a new image which is assigned to a variable called new_image.
    elif len_image < len_message:
        #If there are more bits in the binary string than intensity
        #values in the image, the function encodes as many bits of the
        #binary string as possible. To achieve this, message_bit is sliced
        #and only a certain no of bits(certain no is equal to no of
        #intensity values)are encoded into the image.
        new_image = change_lsb(image,message_bit[0:len_image])
        #The change_lsb function is called and it encodes the message_bit
        #sliced from 0 to the number of intensity values into the image.
        #It returns the new image to a variable called new_image.
    else:
        new_image = change_lsb(image,message_bit) 
        #In the case where no of bits and the no of intensity values
        #are equal, change_lsb returns a new image without having to make
        #any changes to the string message_bit.
    return new_image        
          

#Task 4
'''
Defining a function to decode an encoded image. It takes one argument -
an image and returns a string of ASCII characters which was the secret
message that was encoded into the image using the science/art of
Steganography.
'''
def decode(image):
    message_bit = ''
    for row in image:
        for a in range(len(image[0])):
            for b in range(len(image[0][0])):
                #The nested for loops help access the elements inside 
                #the tuples that are the intensity values.
                pixel_int = (row[a][b])
                #The intensity value is assigned to a variable.
                message_bit += bits.get_bit(pixel_int, 0) 
                #The get_bit function in the bits.py module is called here
                #to access the last bit of the intensity value represented
                #in base 2. The last_bit would be '0' or '1'. The last bits
                #of all the intensity values are concatenated and stored
                #in a variable called message_bit.         
    message = bits_to_message(message_bit)
    #The function bits_to_message is used to recover the original message.
    return message

#Bonus Task
'''
This task tries to generalise the steganography scheme and allows to encode
upto 8 bits of a message per intensity value.
'''

def change_lsb_ext(image, message_bit, num_bits):
    new_image = []
    for row in image:
        new_row = []
        for a in range(len(image[0])):
            pixel = list(row[a])
            for b in range(len(image[0][0])):
                for count in range(num_bits):
                    if message_bit == '':
                        break
                    else:    
                        pixel[b] = bits.set_bit(pixel[b], message_bit[0], count)
                        message_bit = message_bit[1:]
            new_row.append(tuple(pixel))
        new_image.append(new_row)            
    return new_image


    
def encode_ext(image, message, num_bits):
    message_bit = message_to_bits(message)
    len_image = SimpleImage.get_width(image)*SimpleImage.get_height(image)*3
    len_message = len(message_bit)
    if len_image > len_message:
        message_bit += (len_image - len_message) * "0"
        new_image = change_lsb_ext (image,message_bit, num_bits)
    elif len_image < len_message:
        new_image = change_lsb_ext(image,message_bit[0:len_image], num_bits)
    else:
        new_image = change_lsb_ext(image,message_bit, num_bits) 
    return new_image


def decode_ext(image, num_bits):
    message_bit = ''
    for row in image:
        for a in range(len(image[0])):
            for b in range(len(image[0][0])):
                pixel_int = (row[a][b])
                for count in range(num_bits):
                    message_bit += bits.get_bit(pixel_int, count)         
    message = bits_to_message(message_bit)
    return message

    
    

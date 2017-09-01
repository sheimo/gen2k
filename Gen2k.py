#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__    = 'irenicus09'
__email__     = 'irenicus09[at]gmail[dot]com'
__license__   = 'BSDv4'
__version__   = '1.1'
__date__      = '8/1/2016'

import sys


"""
###########################################################################
                    
Gen2k - Automated Word List Generator 
Copyright © 2016 irenicus09
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
3. Neither the name of the organization nor the
names of its contributors may be used to endorse or promote products
derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY irenicus09 ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL irenicus09 BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

---------------------------------------------------------------------------



###########################################################################
"""

# TODO
# 1) Make it memory efficient
# 2) Better sorting algorithm
# 3) More practical features
#   - Modular design
#   - Minimal progress bar 
#   - Slice wordlist into smaller chunks


def help():
    print """


         ######   ######## ##    ##  #######  ##    ##
        ##    ##  ##       ###   ## ##     ## ##   ##
        ##        ##       ####  ##        ## ##  ##
        ##   #### ######   ## ## ##  #######  #####
        ##    ##  ##       ##  #### ##        ##  ##
        ##    ##  ##       ##   ### ##        ##   ##
         ######   ######## ##    ## ######### ##    ##  %s

         ======= Automated Word List Generator =======

                Copyright (C) irenicus09 2016


    USAGE: ./gen2k.py -w <wordlist> -o <output> [options]

    [ -c ] Enable word combination among the words in wordlist.

    [ -d ] Custom comma separated values to combine with wordlist.

    [ -e ] Enable wpa/wpa2 fitness check for generated passwords.

    [ -h ] Prints this help.

    [ -n ] Enable frequently used number combination with wordlist.

    [ -o ] Output filename.

    [ -w ] Path to word list file.
           Wordlist must contain info related to Target.

    [ -y ] Enable year combination with wordlist.

    [ -z ] Enable conversion of words to upper & lower case letters.

           Note: Conversion to upper/lowercase & capitalisation
           takes place before other modes are applied to the original list.

    """ % __version__




def main():

    if exist('-h'):
        help()
        sys.exit(0)

    if not (exist('-w') or exist('-o')):
        help()
        sys.exit(1)

    master_list = load_words(find('-w')) # List supplied by user

    data = [] # Final wordlist
    temp = [] # Temporary wordlist

    if exist('-z'):
        master_list = gen_case(master_list)
        data = master_list

    if exist('-c'):
        temp = gen_word_combo(master_list)
        data = list(set(temp+data))

    if exist('-n'):
        temp = gen_numbers(master_list)
        data = list(set(temp+data))

    if exist('-y'):
        temp = gen_year(master_list)
        data = list(set(temp+data))

    if exist('-d'):
        try:
            custom_values = find('-d').split(',')
        except (AttributeError):
            print '[!] Are you kidding me with no values?'
            sys.exit(1)

        temp = gen_custom(master_list, custom_values)
        data = list(set(temp+data))

    if exist('-e'):
        data = wpa_validation_check(data)

    write_file(find('-o'), data)

    print '[*] Total words generated: %d' % (len(data))

    sys.exit(0)


def merge_list(temp_list=[], final_list=[]):
    """
    Merges contents from temp_list (1st param) with final_list (2nd param)
    """
    for word in temp_list:
        if word not in final_list:
            final_list.append(word)


def load_words(path_to_file):
    """
    Function to fetch all possible words.
    """
    data = []

    try:
        handle = open(path_to_file, 'r')
        temp_list = handle.readlines()
        handle.close()

    except(BaseException):
        print '[!] Error occured while reading wordlist.'
        sys.exit(1)

    for word in temp_list:
        word = word.strip()
        if word != '':
            data.append(word)

    return data



def write_file(path_to_file, data=[]):
    """
    Writing to specified file.
    """
    try:
        handle = open(path_to_file, 'wb+')

        for word in data:
            handle.write(word+'\n')

        handle.close()
    except(BaseException):
        print '[!] Error occured while writing to file.'
        sys.exit(1)



def gen_case(words=[]):
    """
    Function to change words to Upper & Lower case.
    """
    custom_list = []

    for x in words:
        custom_list.append(x.lower())
        custom_list.append(x.capitalize())
        custom_list.append(x.upper())

    return list(set(custom_list))



def gen_numbers(words=[]):
    """
    Function to mix words with commonly used numbers patterns.
    """
    word_list = []

    if len(words) <= 0:
        return word_list

    num_list = ['0', '01', '012', '0123', '01234', '012345', '0123456', '01234567', '012345678', '0123456789',
    '1', '12', '123', '1234','12345', '123456','1234567','12345678','123456789', '1234567890', '9876543210',
    '987654321', '87654321', '7654321', '654321', '54321', '4321', '321', '21']

    for word in words:
        for num in num_list:
            word_list.append((word+num))
            word_list.append((num+word))

    return word_list




def gen_year(words=[]):
    """
    Function to mix auto generated year with words from wordlist.

    Hint: Date of birth & special dates are often
          combined with certain words to form
          passwords.
    """
    word_list = []

    if len(words) <= 0:
        return word_list

    # Double digit dates
    start = 1
    while(start <= 99):
        for word in words:
            word_list.append(word + str("%02d") % (start))
            word_list.append(str("%02d") % start + word)
        start += 1

    # Four digit dates
    start = 1900
    while (start <= 2020):
        for word in words:
            word_list.append(word+str(start))
            word_list.append(str(start)+word)
        start += 1

    return word_list




def gen_word_combo(words=[]):
    """
    Function to mix multiple words from given list.
    """
    word_list = []

    if len(words) <= 1:
        return word_list

    for word in words:
        for second_word in words:
            if word != second_word:
                word_list.append(second_word+word)

    return word_list




def gen_custom(words=[], data=[]):
    """
    Funtion to combine user defined input with wordlist.

    > Takes a comma separated list via cmdline as values.
    """
    word_list = []

    if (len(words) <= 0 or len(data) <= 0):
        return word_list

    for item in data:
        for word in words:
            word_list.append(item+word)
            word_list.append(word+item)

    return word_list



def wpa_validation_check(words=[]):
    """
    Function to optimise wordlist for wpa cracking

    > Removes Duplicates.
    > Removes passwords < 8 or > 63 characters in length.
    """
    custom_list =  list(set(words))
    custom_list = [x for x in custom_list if not (len(x) < 8 or len(x) > 63)]

    return custom_list


# S3my0n's argument parsers, thx brah :)
def find(flag):
    try:
        a = sys.argv[sys.argv.index(flag)+1]
    except (IndexError, ValueError):
        return None
    else:
        return a

def exist(flag):
    if flag in sys.argv[1:]:
        return True
    else:
        return False








if __name__ == '__main__':
    main()

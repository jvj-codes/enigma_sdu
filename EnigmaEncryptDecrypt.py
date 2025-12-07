# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 12:06:59 2025

@author: nuffz
"""
from EnigmaModel import EnigmaModel
from EnigmaConstants import ALPHABET
import os
import re

class EnigmaEncrypt:
    """This class enables the user to both encrypt 
        messages using the Enigma-machine. 
    """
    
    def __init__(self, message: str, rotors: str):
        """Initial rotor settings, cipher and message."""
        self._rotors_set = rotors # arbitrary initial rotor settings - left -> right rotor settings.
        self._cipher = ""
        self._message = message
        
        # create Enigma Model
        self._model = EnigmaModel()
        
        # initialize rotor offsets
        for i, letter in enumerate(self._rotors_set):
            self._model._rotors[i]._offset = ALPHABET.index(letter)
    
    def encrypt(self) -> str:
        
        # initialize cipher so it is not dependent on anything else
        self._cipher = ""
        
        
        #loop over characters in message
        for char in self._message:
            
            if char not in ALPHABET: # if character is not in the alphabet, add the character and continue.
                self._cipher += char # this enables punctuation and spaces to function
                continue # next char
            
            # press key to simulate outcome
            self._model.key_pressed(char)
            
            # read lit lamp and store in cipher
            out_char = self._model._lit_lamp 
            self._cipher += out_char
            
            # release key to clear lamp
            self._model.key_released(char)
        
        return self._cipher
    
                        
class EnigmaFindRotors:
    """Find initial rotor settings (letters), assuming we know message/cipher"""

    def __init__(self, message: str, cipher: str):
        self._message = message
        self._cipher = cipher
        self._model = EnigmaModel()

    def FindRotors(self) -> str:
        """Brute force all possible rotor settings (AAA to ZZZ)"""

        for a in ALPHABET:
            for b in ALPHABET:
                for c in ALPHABET:
        
                    if self._test_setting(a, b, c): # if true
                        return a + b + c  # return letters immediately

        return "SETTINGS NOT FOUND"

    def _test_setting(self, a: str, b: str, c: str) -> bool:
        """Check if rotor offsets a,b,c produce the given cipher"""

        # reset rotor settings
        self._model._rotors[0]._offset = ALPHABET.index(a)  # left
        self._model._rotors[1]._offset = ALPHABET.index(b)  # middle
        self._model._rotors[2]._offset = ALPHABET.index(c)  # right

        for i, char in enumerate(self._message):
            if char not in ALPHABET:
                continue  # skip spaces/punctuation as before

            # press key in model (steps rotors)
            self._model.key_pressed(char)
            out_char = self._model._lit_lamp
            self._model.key_released(char)

            if out_char != self._cipher[i]:
                return False  # if mismatch between output character and cipher character try next setting

        return True  # returns true if output characters equals ciphered message

class EnigmaDecrypt:
    """Decrypt a cipher using brute-force rotor settings and dictionary"""

    def __init__(self, cipher: str, words: list):
        self._cipher = cipher.upper()
        self._model = EnigmaModel()
        self._words = set(word.lower() for word in words)  # faster lookup

    def decrypt(self) -> str:

        # Step 1: find correct rotor settings
        a, b, c = self._find_rotor_settings()

        # Step 2: set rotors once
        self._model._rotors[0]._offset = ALPHABET.index(a)
        self._model._rotors[1]._offset = ALPHABET.index(b)
        self._model._rotors[2]._offset = ALPHABET.index(c)

        # Step 3: decrypt full message continuously
        decrypted_message = ""

        for char in self._cipher:
            if char not in ALPHABET:
                decrypted_message += char
                continue

            self._model.key_pressed(char)
            out_char = self._model._lit_lamp
            self._model.key_released(char)
            decrypted_message += out_char

        return decrypted_message

    def _find_rotor_settings(self):
        """Find rotor settings by testing full message against dictionary words"""
    
        split_cipher = re.split(r'[,\s;]+', self._cipher)  # split into words
    
        for a in ALPHABET:
            for b in ALPHABET:
                for c in ALPHABET:
    
                    # set candidate offsets
                    self._model._rotors[0]._offset = ALPHABET.index(a)
                    self._model._rotors[1]._offset = ALPHABET.index(b)
                    self._model._rotors[2]._offset = ALPHABET.index(c)
    
                    # decrypt each word
                    decrypted_words = []
    
                    for cipher_word in split_cipher:
                        decrypted_word = ""
                        for char in cipher_word:
                            if char not in ALPHABET:
                                decrypted_word += char
                                continue
                            self._model.key_pressed(char)
                            decrypted_word += self._model._lit_lamp.lower()
                            self._model.key_released(char)
    
                        decrypted_words.append(decrypted_word)
    
                    # check if all decrypted words are in the dictionary
                    if all(word in self._words for word in decrypted_words):
                        return a, b, c  # found correct rotor settings
    
        return "A", "A", "A"  # fallback


        
        
if __name__ == "__main__":
    
    cwd = os.getcwd()
    word_path = cwd + "\\words\\words_english.txt"
    with open(word_path, "r", encoding="utf-8") as f:
        words = f.read().splitlines()
    
    ### inputs for encryption and decryption
    message = "CODING ENIGMA TODAY" # input message
    rotor_settings = "AGC"
    print(f"Inputs for encryption: \n (1) Message - {message} \n (2) Rotor Settings - {rotor_settings}") # print message
    
    ## encrypt
    e = EnigmaEncrypt(message, rotor_settings) # encrypt message using some rotor setting
    encrypted = e.encrypt() # access the encrypt attribute
    print("Encrypted Message:", encrypted) # print the encrypted messge
    
    ## find rotor settings
    FindRotor = EnigmaFindRotors(message, encrypted) # find the rotors using the message and cipher
    print("Rotor Settings Reverse Engineered:", FindRotor.FindRotors()) # access the FindRotors attribute
        
    ## decrypt
    d = EnigmaDecrypt(encrypted, words)
    decrypted = d.decrypt()
    print("Decrypted Message:", decrypted)
        
        
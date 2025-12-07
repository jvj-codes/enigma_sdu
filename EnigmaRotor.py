# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 15:32:39 2025

@author: nuffz
"""

from EnigmaConstants import ALPHABET, N_ROTORS, ROTOR_PERMUTATIONS, REFLECTOR_PERMUTATION

def apply_permutation(index: int, permutation: str, offset: int) -> int:
    """
    index: integer 0-25 for letter A-Z
    permutation: 26-character string representing rotor wiring
    offset: rotor setting (0-25)

    Returns: integer index of the output letter after applying the rotor
    """
    # Step 1: shift input index by rotor offset
    shifted_index = (index + offset) % 26 # modulus / divisible by 26 (number of rotor settings)

    # Step 2: find the letter at that position in the permutation
    letter = permutation[shifted_index] 

    # Step 3: convert the letter back to an index
    letter_index = ALPHABET.index(letter) 

    # Step 4: undo the offset to get the final output index
    output_index = (letter_index - offset) % 26 # modulus / divisible by 26 (number of rotor settings)

    return output_index



class EnigmaRotor:
    """
    class that defines inherit functions related to the EnigmaRotor.
    """
    def __init__(self, permutation): #init instances of the class
        self._permutation = permutation # defines permutation
        self._offset = 0  # window letter
        self._steps = 0   # counts how many times this rotor has advanced
        
    def get_offset(self): 
        return self._offset # returns offset

    def advance(self): # advances 1 step for each click - dynamic rotors.
        self._offset = (self._offset + 1) % 26
        self._steps += 1
        
    def get_permutation(self):
        """Return the rotor wiring permutation string"""
        return self._permutation
        
# File: EnigmaModel.py

""" This is the starter file for the Enigma project. """

from EnigmaView import EnigmaView
from EnigmaRotor import EnigmaRotor, apply_permutation  # import EngimaRotor class and apply_permutation function.
from EnigmaConstants import ALPHABET, N_ROTORS, ROTOR_PERMUTATIONS, REFLECTOR_PERMUTATION  # import constants 


class EnigmaKey:
    """Initial letter, pressed key and lamps."""
    def __init__(self, letter):  # initial instances, no pressed letter on keyboard, no lamps on.
        self.letter = letter
        self.is_pressed = False
        self.lamp_on = False


class EnigmaModel:

    def __init__(self):
        """Creates a new EnigmaModel with no views."""
        self._views = []
        self._lit_lamp = None  # no lamp lit before a key is pressed
        self._keys = {letter: EnigmaKey(letter) for letter in ALPHABET}  # dictionary holding the keyboard keys
        self._rotors = [EnigmaRotor(perm) for perm in ROTOR_PERMUTATIONS]  # create three rotor objects based on constants

    def add_view(self, view):
        """Adds a view to this model."""
        self._views.append(view)

    def update(self):
        """Sends an update request to all the views."""
        for view in self._views:
            view.update()

    def is_key_down(self, letter):
        """Check if a key is currently pressed on the keyboard."""
        return self._keys[letter].is_pressed  # view uses this to render key in pressed state

    def is_lamp_on(self, letter):
        """Check if a given lamp is currently lit."""
        return self._keys[letter].lamp_on

    def key_pressed(self, letter):
        """Key pressed function:
           - register press
           - advance rotors (fast → medium → slow)
           - forward pass through all rotors
           - reflect in reflector
           - backward pass (inverse mapping)
           - light final output lamp
           - update GUI
        """
        self._keys[letter].is_pressed = True

        # Each key press advances rotors based on stepping logic
        self.advance_rotors()

        # Convert letter to numeric index (A=0, B=1, ...)
        index = ALPHABET.index(letter)

        # Forward pass: rightmost rotor first, then left
        for rotor in reversed(self._rotors):
            index = apply_permutation(index, rotor.get_permutation(), rotor.get_offset())

        # Reflection step using static reflector wiring
        reflected_letter = REFLECTOR_PERMUTATION[index]
        index = ALPHABET.index(reflected_letter)

        # Backward pass: rotors in normal order, but reverse mapping
        for rotor in self._rotors:
            perm = rotor.get_permutation()
            offset = rotor.get_offset()

            # Apply offset before inverse lookup
            shifted_index = (index + offset) % 26
            letter_at_index = ALPHABET[shifted_index]

            # Find which input in the rotor produces this letter (inverse substitution)
            inverse_index = perm.index(letter_at_index)

            # Remove offset again
            index = (inverse_index - offset) % 26

        # Light up the resulting lamp
        lamp_letter = ALPHABET[index]
        self._keys[lamp_letter].lamp_on = True
        self._lit_lamp = lamp_letter

        # Trigger screen redraw
        self.update()

    def key_released(self, letter):
        """Called when key is released. Turns off the key highlight and any lit lamp."""
        self._keys[letter].is_pressed = False

        # If a lamp is currently lit, turn it off
        if hasattr(self, "_lit_lamp") and self._lit_lamp:
            self._keys[self._lit_lamp].lamp_on = False
            self._lit_lamp = None

        self.update()

    def get_rotor_letter(self, index):
        """Return the letter currently visible in the rotor window (based on its offset)."""
        offset = self._rotors[index].get_offset()
        return ALPHABET[offset]

    def rotor_clicked(self, index):
        """User clicks rotor in GUI → manually advance it by one."""
        self._rotors[index].advance()
        print(f"Rotor {index} offset now: {self._rotors[index].get_offset()}")
        self.update()

    def advance_rotors(self):
        """Implements Enigma stepping:
           Fast rotor always steps.
           When fast wraps from Z→A, step medium.
           When medium also wraps, step slow.
        """
        fast = self._rotors[2]     # rightmost rotor
        medium = self._rotors[1]   # middle rotor
        slow = self._rotors[0]     # leftmost rotor

        # Fast rotor always steps
        fast.advance()

        # If fast returns to initial position, advance medium
        if fast.get_offset() == 0:
            medium.advance()

            # If medium also wrapped, advance slow rotor
            if medium.get_offset() == 0:
                slow.advance()


def enigma():
    """Runs the Enigma simulator."""
    model = EnigmaModel()
    view = EnigmaView(model)
    model.add_view(view)


# Startup code
if __name__ == "__main__":
    enigma()

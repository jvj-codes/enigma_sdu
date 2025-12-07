**enigma_sdu — Enigma simulator (SDU course)**

This repository contains a Python implementation of an Enigma‑style encryption machine. It includes rotor logic, a GUI view, and (optional) utilities for decryption/encryption‑search.

***File / Folder - Purpose / Description*** 
1. EnigmaConstants.py	Defines global constants: the alphabet (ALPHABET), number of rotors (N_ROTORS), rotor wirings (ROTOR_PERMUTATIONS), and the reflector permutation (REFLECTOR_PERMUTATION). All rotor wiring/reflector configuration comes from here.
2. EnigmaRotor.py	Implements the EnigmaRotor class, which handles a single rotor: its wiring (permutation), current offset (rotation), and stepping (advance). Also provides the helper function apply_permutation(...) to pass an input index through a rotor with offset.
3. EnigmaModel.py	Core logic of the Enigma machine: holds the set of rotors, keys/lamps (keyboard + lampboard), handles key presses and releases, advances rotors, does forward pass → reflection → backward pass, and tracks which lamp lights up. This is the “engine” of the Enigma simulator.
4. EnigmaView.py	(Optional GUI) Visual representation of the Enigma machine: keyboard, lamps, rotors. Allows the user to press keys, see which lamp lights up, and manually click rotors to change their settings. This is useful for interactive encryption/decryption as if using a physical Enigma.
5. EnigmaEncryptDecrypt.py A helper class for programmatic encryption/decryption without a GUI. You supply a plaintext (or ciphertext) and a rotor setting (e.g., "DMG"), and the code simulates the Enigma to output the result. Useful if you want to encrypt or decrypt messages in code rather than by the GUI.
6. words/ folder	Intended to contain word‑lists (e.g. dictionary files) used by decryptor/dictionary‑based brute‑force utilities. Loading a word list can help in attempting to decrypt messages by matching decrypted text against common words.
7. images/ folder	Needed for EnigmaView GUI to work. 

***How to run/use the code***

Here are several ways you can use the project, depending on what you want to do.

1. Run the GUI simulator
    If you want to interactively press keys and see the Enigma behavior (rotors, lamps, stepping):
    python EnigmaModel.py
    
    The GUI will show a keyboard, lampboard, rotors, etc. You can click keys to encrypt letters. 
    The rotors step automatically, just like a real Enigma. You can also click the “wheels” to manually change offsets if implemented

2. Programmatic encryption/decryption (no GUI)
    If you want to encrypt or decrypt a full message in code, e.g.:

     ```python
    # import libraries
    from EnigmaEncryptDecrypt import EnigmaEncrypt, EnigmaDecrypt
    import os
    
    # load word list from word list to decipher
    cwd = os.getcwd()
    word_path = cwd + "\\words\\words_english.txt"
    with open(word_path, "r", encoding="utf-8") as f:
        words = f.read().splitlines()
    
    # input for encryption
    plaintext = "HELLO WORLD MY NAME IS POTATO"
    rotor_setting = "DMG"   # rotor setting leftmost slow to rightmost fast
    
    # encrypt message
    e = EnigmaEncrypt(plaintext, rotor_setting)
    cipher = e.encrypt()
    print("Encrypted:", cipher)
    
    # decrypt message
    d = EnigmaDecrypt(cipher, words)
    decrypted = d.decrypt()
    print("Decrypted:", decrypted)
    ```


Note: The ReadMe file is generated/inspired by Chatbot GPT.

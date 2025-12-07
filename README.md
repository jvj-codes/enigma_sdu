enigma_sdu — Enigma simulator (SDU course)

This repository contains a Python implementation of an Enigma‑style encryption machine. It includes rotor logic, a GUI view, and (optional) utilities for encryption and decryption/encryption‑search.

📁 What’s in this repo

Here is an overview of the main files and folders, and what each does:

File / Folder	Purpose / Description
EnigmaConstants.py	Defines global constants: the alphabet (ALPHABET), number of rotors (N_ROTORS), rotor wirings (ROTOR_PERMUTATIONS), and the reflector permutation (REFLECTOR_PERMUTATION). All rotor wiring/reflector configuration comes from here.
EnigmaRotor.py	Implements the EnigmaRotor class, which handles a single rotor: its wiring (permutation), current offset (rotation), and stepping (advance). Also provides the helper function apply_permutation(...) to pass an input index through a rotor with offset.
EnigmaModel.py	Core logic of the Enigma machine: holds the set of rotors, keys/lamps (keyboard + lampboard), handles key presses and releases, advances rotors, does forward pass → reflection → backward pass, and tracks which lamp lights up. This is the “engine” of the Enigma simulator.
EnigmaView.py	(Optional GUI) Visual representation of the Enigma machine: keyboard, lamps, rotors. Allows user to press keys, see which lamp lights up, and manually click rotors to change their settings. This is useful for interactive encryption/decryption as if using a physical Enigma.
EnigmaEncryptDecrypt.py A helper class for programmatic encryption/decryption without a GUI. You supply a plaintext (or ciphertext) and a rotor setting (e.g. "DMG"), and the code simulates the Enigma to output the result. Useful if you want to encrypt or decrypt messages in code rather than by the GUI.
words/ folder	Intended to contain word‑lists (e.g. dictionary files) used by decryptor/dictionary‑based brute‑force utilities. Loading a word-list can help in attempting to decrypt messages by matching decrypted text against common words.
images/ folder	(Possibly for GUI assets) — depends on how EnigmaView.py uses it. Could contain images for keyboard, lampboard, background, etc.
Other files (e.g. README.md)	Documentation, usage instructions, and possibly examples.
🛠 How to run/use the code

Here are several ways you can use the project, depending on what you want to do.

🔹 1. Run the GUI simulator

If you want to interactively press keys and see the Enigma behavior (rotors, lamps, stepping):

python EnigmaModel.py


or (depending on how EnigmaView.py is set up — it may run by default when the script is executed).
The GUI will show a keyboard, lampboard, rotors, etc.

You can click keys to encrypt letters

The rotors step automatically as in a real Enigma

You can also click rotor “wheels” to manually change offsets if implemented

Use this mode for manual encryption/decryption or experimentation.

🔹 2. Programmatic encryption/decryption (no GUI)

If you want to encrypt or decrypt a full message in code, e.g.:

from EngimaEncryptDecrypt import EnigmaEncryptDecrypt

plaintext = "HELLOWORLD"
rotor_setting = "DMG"   # for example

e = EnigmaEncryptDecrypt(plaintext, rotor_setting)
cipher = e.encrypt()
print("Encrypted:", cipher)

# To decrypt (since Enigma is symmetric)
d = EnigmaEncryptDecrypt(cipher, rotor_setting)
decrypted = d.encrypt()
print("Decrypted:", decrypted)


This is useful for batch processing messages, automated testing, or embedding Enigma logic in other applications.

🔹 3. (Optional) Dictionary‑based brute force / decryption attempt

If you have a ciphertext and a word‑list (e.g. English words), you can attempt to brute‑force rotor settings and check whether decrypting yields real words.
To do this you would:

Place a word‑list (e.g. words_english.txt) in the words/ folder.

Load the list in Python, e.g.:

with open("words/words_english.txt", "r", encoding="utf-8") as f:
    words = [w.strip().lower() for w in f if w.strip()]


Use/extend a decryptor class (or write your own) that tries all rotor settings (e.g. "AAA" to "ZZZ"), decrypts the ciphertext with each, and checks if the result is composed of valid words from the list.

⚠️ Note: Because there are 26³ = 17,576 possible rotor settings, and you may test full messages for each, this brute‑force method can be time‑consuming for longer messages.

✅ What you should check / might need to adjust

The file EngimaEncryptDecrypt.py — note the name typo (“Engima” instead of “Enigma”). You might want to rename it to EnigmaEncryptDecrypt.py for clarity.

Ensure your Python environment uses UTF‑8 encoding (especially if you extend to more characters).

If you want to add a method to directly set rotor offset (instead of only stepping), you might need to modify EnigmaRotor.py to add a set_offset() method.

For dictionary‑based decryption: make sure the dictionary file is in the correct folder and loaded correctly (watch relative paths).

🧪 Example: encrypt and decrypt from command line / script
# example_script.py
from EngimaEncryptDecrypt import EnigmaEncryptDecrypt

message = "HELLO WITH YOU"
rotors = "DMG"

# Encrypt
encryptor = EnigmaEncryptDecrypt(message, rotors)
cipher = encryptor.encrypt()
print("Cipher:", cipher)

# Decrypt (since symmetric)
decryptor = EnigmaEncryptDecrypt(cipher, rotors)
print("Decrypted:", decryptor.encrypt())


Run:

python example_script.py


Expected output:

Cipher: <some ciphertext>
Decrypted: HELLO WITH YOU

Note: The ReadMe file is generated by Chatbot GPT.

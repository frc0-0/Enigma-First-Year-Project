import Enigma as e

message = "SecretMessage"

machine = e.enigma([2,4,3], ["C", "E", "Y"], ["D", "S", "T"])

machine.plugboard.add("S", "G")
machine.plugboard.add("F", "X")
machine.plugboard.add("H", "B")
machine.plugboard.add("K", "M")
machine.plugboard.add("Q", "L")
machine.plugboard.add("R", "U")
machine.plugboard.add("Z", "Y")
machine.plugboard.add("T", "P")
machine.plugboard.add("C", "D")
machine.plugboard.add("A", "I")


encryptedMessage = machine.op(message)

machine = e.enigma([2,4,3], ["C", "E", "Y"], ["D", "S", "T"])

machine.plugboard.add("S", "G")
machine.plugboard.add("F", "X")
machine.plugboard.add("H", "B")
machine.plugboard.add("K", "M")
machine.plugboard.add("Q", "L")
machine.plugboard.add("R", "U")
machine.plugboard.add("Z", "Y")
machine.plugboard.add("T", "P")
machine.plugboard.add("C", "D")
machine.plugboard.add("A", "I")

decryptedMessage = machine.op(encryptedMessage)

print("Encrypted text:", encryptedMessage)
print()
print("Decrypted text:", decryptedMessage)

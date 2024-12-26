"""
Vigenere Cipher Assignment
"""



# Function that takes in input (text and key) and returns the encrypted text for the same 
def Vigenere(plaintext: str, key: str) -> str:   
    # Preprocessing the plaintext and key by making it uppercase and removing the spaces.
    plaintext = plaintext.upper().replace(" ","")
    key = key.upper()
    plaintext_size = len(plaintext)  #size of plaintext
    key_size = len(key)  #size of plaintext
    ciphertext = ""   #variable to store ciphertext
    for i in range(plaintext_size):   # processing the plaintext character by character
        # adding the ascii value of the key to the ascii value of the plaintext character by character
        c = chr((ord(plaintext[i]) + ord(key[i%key_size]) - 2*ord('A'))%26 + ord('A'))    
        ciphertext+=c   # saving the encrypted character to the ciphertext
    return ciphertext   # function finally returns the cipher text


# Function to decrypt the Vigenere encrypted Cipher text with known key
def Decrypt(ciphertext: str, key: str)-> str:
    #preprocessing the cipher text and key changing it to upper case
    ciphertext = ciphertext.upper()
    key = key.upper()
    ciphertext_size = len(ciphertext)    #size of the ciphertext
    key_size = len(key)    #size of the key
    plaintext = ""    #variable to save the plaintext
    for i in range(ciphertext_size):  #processing the ciphertext character by character
        # subtracting the ascii value of the key to the ascii value of the plaintext character by character
        c = chr((ord(ciphertext[i]) - ord(key[i%key_size]) - 2*ord('A'))%26 + ord('A'))
        plaintext+=c  #saving the decrypted character to the plaintext
    return plaintext



if __name__ == "__main__":

    #handling the error handling in text and key -> only alphabets are allowed no special character no numeric
    while(True):
        text = input("please enter the text you want to encrypt using Vigenere Cipher: ").replace(" ","")
        if(not text.isalpha() and len(text)!=0):
            print("Error Wrong Input: please enter only alphabets")
        else:
            break

    while(True):
        key = input("Please enter the key for your Cipher: ").replace(" ","")
        if(not key.isalpha()):
            print("Error Wrong Input: please enter only alphabets")
        else:
            break
        

    cipher = Vigenere(text,key)  #storing the encrypted text
    print("-"*100)
    print("encrypted text: ",cipher)  #printing the ciphertext
    decrypted = Decrypt(cipher,key)  #decrypted text from cipher and key
    print("-"*100)
    print("decrypted text(from cipher with known key): ",decrypted)
    print("-"*100)



"""
Error Handling:
1.) Only alphabets and spaces allowed in text and key \
    (while spaces we be removed while preprocessing for encryption and insertion of \
        spaces can also be handled with if condition but no handled in this because of the example)
2.) If key is empty -> ask the user to input key properly
"""
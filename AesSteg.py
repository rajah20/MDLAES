from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import b64encode, b64decode
from PIL import Image
import numpy as np

class AesSteg:
    
    # e = b"F45248B6D1CC41D2"
    
    e = b"G44248B61DCC41D2"
    
    # e = b"4G4248B61DCC41D2"
    # # e = b"F44248B6D1CC41D2"
    
    # e = b"F42448B6D1CC41D2"
    
    # e = b"2123456789ABCDEFFFFFAABC"
    # e = b"F44248B6D1CC41C289ABCDEFFFFFAABC"
    key = e.hex()

    message = 'This is a secret Message'

    
    def aes_encrypt(self, message, key):
        backend = default_backend()
        iv = b'\x00' * 16  # This generates a random IV for each encryption in practice
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_message = padder.update(message.encode()) + padder.finalize()
        ciphertext = encryptor.update(padded_message) + encryptor.finalize()
        return b64encode(ciphertext)

    def aes_decrypt(self, ciphertext, key):
        backend = default_backend()
        iv = b'\x00' * 16  # This uses the same IV used during encryption
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        padded_message = decryptor.update(b64decode(ciphertext)) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        message = unpadder.update(padded_message) + unpadder.finalize()
        return message.decode()
    def __fillMSB(self, inp):
        '''
        0b01100 -> [0,0,0,0,1,1,0,0]
        '''
        inp = inp.split("b")[-1]
        inp = '0' * (7 - len(inp)) + inp
        return [int(x) for x in inp]

    def __decrypt_pixels(self, pixels):
        '''
        Given list of 7 pixel values -> Determine 0/1 -> Join 7 0/1s to form binary -> integer -> character
        '''
        pixels = [str(x % 2) for x in pixels]
        bin_repr = "".join(pixels)
        return chr(int(bin_repr, 2))

    def encrypt_text_in_image(self, image_path, msg, target_path=""):
        '''
        Read image -> Flatten -> encrypt images using LSB -> reshape and repack -> return image
        '''
        img = np.array(Image.open(image_path))
        imgArr = img.flatten()
        # The 'line below gives you integers for each Image pixel

        msg += "<-END->"
        msgArr = [self.__fillMSB(bin(ord(ch))) for ch in msg]
   

        idx = 0
        for char in msgArr:
            for bit in char:
                if bit == 1:
                    imgArr[idx] |= 1
                else:
                    imgArr[idx] &= 254  # This sets the least significant bit to 0
                idx += 1

        save_path = target_path + image_path.split(".")[0] + "_encrypted.png"

        res_img = Image.fromarray(np.reshape(imgArr, img.shape))
        res_img.save(save_path)
        
    def decrypt_text_in_image(self, image_path, target_path=""):
        '''
        Read image -> Extract Text -> Return
        '''
        img = np.array(Image.open(image_path))
        imgArr = np.array(img).flatten()

        decrypted_message = ""
        for i in range(0, len(imgArr), 7):
            decrypted_char = self.__decrypt_pixels(imgArr[i:i + 7])
            decrypted_message += decrypted_char

            if len(decrypted_message) > 10 and decrypted_message[-7:] == "<-END->":
                break

        return decrypted_message[:-7]
# Example usage



from cryptography.hazmat.backends import default_backend
from base64 import b64decode
import numpy as np
from AesSteg import AesSteg
import time
import psutil
from memory_profiler import profile

img = AesSteg()
@profile
def hybridSys():

    start_time = time.time()
    
    # Numerical equivalent for secret text
    # res_data_str = str([87, 54, 85, 76, 71, 110, 116, 112, 77, 74, 68, 85, 109, 107, 72, 110, 54, 79, 90, 66, 113, 118, 57, 85, 90, 111, 104, 101, 68, 102, 97, 51, 102, 88, 98, 85, 89, 52, 49, 117, 50, 54, 72, 90, 84, 48, 79, 118, 107, 55, 118, 102, 80, 100, 114, 118, 115, 119, 99, 80, 99, 48, 74, 121, 67, 122, 57, 101, 85, 89, 111, 51, 90, 52, 90, 71, 103, 117, 88, 101, 107, 104, 54, 65, 109, 71, 89, 100, 102, 114, 77, 68, 117, 98, 48, 115, 115, 65, 84, 121, 81, 99, 98, 102, 114, 50, 76, 57, 66, 57, 122, 110, 69, 55, 98, 57, 121, 106, 55, 109, 111, 71, 107, 107, 54, 118, 101, 99, 89, 50, 49, 89, 116, 51, 117, 116, 72, 90, 106, 72, 75, 118, 67, 78, 65, 48, 101, 121, 103, 121, 57, 85, 116, 81, 76, 76, 86, 86, 71, 43, 120, 107, 122, 47, 99, 73, 77, 74, 66, 107, 116, 90, 47, 76, 104, 109, 90, 71, 119, 86, 100, 121, 87, 70, 47, 53, 112, 71, 116, 71, 100, 72, 87, 99, 112, 98, 81, 53, 48, 72, 104, 82, 97, 114, 43, 108, 52, 98, 102, 80, 105, 51, 114, 108, 105, 114, 77, 108, 104, 114, 77, 120, 110, 73, 101, 79, 74, 51, 79, 97, 99, 80, 102, 55, 56, 48, 87, 120, 116, 53, 65, 103, 122, 100, 43, 85, 86, 81, 97, 88, 69, 71, 85, 117, 89, 109, 48, 103, 48, 104, 121, 101, 112, 54, 70, 120, 114, 54, 68, 56, 119, 116, 76, 100, 90, 77, 114, 119, 79, 69, 71, 122, 118, 98, 122, 71, 79, 117, 111, 114, 105, 52, 121, 119, 104, 115, 105, 103, 110, 72, 104, 56, 108, 71, 108, 66, 73, 86, 102, 115, 70, 79, 52, 88, 115, 99, 51, 50, 88, 120, 72, 80, 87, 69, 54, 53, 116, 73, 50, 73, 112, 82, 90, 109, 43, 74, 112, 85, 80, 116, 76, 109, 101, 52, 115, 48, 111, 67, 87, 104, 72, 55, 77, 105, 105, 122, 78, 90, 51, 99, 114, 108, 69, 118, 47, 85, 103, 52, 108, 66, 99, 73, 88, 98, 120, 82, 81, 122, 104, 111, 77, 70, 88, 55, 106, 100, 54, 104, 104, 72, 108, 73, 110, 107, 48, 75, 81, 54, 54, 75, 105, 82, 85, 119, 83, 81, 61, 61])
    
    # Extract data from image before decryption
    res_data_str = img.decrypt_text_in_image("encryptions/Image01_encrypted.png")


    # Reconstructing the original data
    res_data_str = res_data_str.replace('[', '').replace(']', '')
 

    # Convert the retrieved strings to lists of integers
    cipher_text_encoded = list(map(int, res_data_str.split(',')))


    # Convert the list of integers back to bytes
    reconstructed_bytes = bytes(cipher_text_encoded)


    cipher_text_decoded = ''.join(chr(code) for code in reconstructed_bytes)

    decrypted_message = img.aes_decrypt(cipher_text_decoded, img.e)

    # Convert the decrypted message to a list of lists
    decoded_message_values = decrypted_message.strip('[]').split(',')
    decoded_message_pairs = [(int(decoded_message_values[i]), int(decoded_message_values[i+1])) for i in range(0, len(decoded_message_values), 2)]

    # Convert the decrypted message to a numpy array
    decoded_array = np.array(decoded_message_pairs)

    # Convert the integer to a string to determine its length
    number_str = str(img.key)
    length = len(number_str)

    # Determine the lengths of each part
    part1_len = length // 4
    part2_len = (length // 4) + (length % 4 > 0)  # Adjust for the remainder
    part3_len = (length // 4) + (length % 4 > 1)  # Adjust for the remainder
    part4_len = length - part1_len - part2_len - part3_len

    # Extract each part
    part1 = int(number_str[:part1_len])
    part2 = int(number_str[part1_len:part1_len + part2_len])
    part3 = int(number_str[part1_len + part2_len:part1_len + part2_len + part3_len])
    part4 = int(number_str[part1_len + part2_len + part3_len:])

    # Define the inverse of the 2x2 matrix used for encoding
    inverse_matrix = np.linalg.inv([[part1, part2], [part3, part4]])

    decoded_array = np.matmul(decoded_array, inverse_matrix)

    # Round the elements of the decoded array to integers
    decoded_array = np.rint(decoded_array).astype(int)

    # Convert the decoded array back to a list
    decoded_list = decoded_array.flatten().tolist()

    # Convert the decoded list back to a string
    decrypted_text = ''.join(chr(m) for m in decoded_list)

    end_time = time.time()

    processing_time = end_time - start_time

    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu_usage}%")

        # # Get memory usage statistics
    memory_info = psutil.virtual_memory()
    print(f"Memory Usage: {memory_info.percent}%")
    print("Processing Time:", processing_time, "seconds")
    print('Decoded Message:', decrypted_text)
if __name__ == "__main__":
    hybridSys()

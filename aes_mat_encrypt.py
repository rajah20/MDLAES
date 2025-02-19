from base64 import b64encode, b64decode
from AesSteg import AesSteg
import numpy as np
import time
import psutil
from memory_profiler import profile
img = AesSteg()
@profile
def hybridSys():

    start_time = time.time()
    # Encrypt the message using AES
    message_encoded = [ord(c) for c in img.message]

    # Convert the decrypted message to a list of integers
    input_array = np.array(message_encoded)

    num_columns = 2

    num_rows = (len(input_array) + num_columns - 1) // num_columns

    num_elements_needed = num_rows * num_columns

    input_array = np.pad(input_array, (0, num_elements_needed - len(input_array)), constant_values=32)
    input_array = input_array.reshape((num_rows, num_columns))

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
    
    matrix = np.array([[part1, part2], [part3, part4]])

    result_array = np.matmul(input_array, matrix)

    # print('result_array', result_array)
    result_list = str(result_array.flatten().astype(int).tolist())

    cipher_text = img.aes_encrypt(result_list, img.e)
    cipher_text_decoded = cipher_text.decode('utf-8')

    # print('cipher_text_decoded', cipher_text_decoded)

    cipher_text_encoded = [ord(c) for c in cipher_text_decoded]
    # print('cipher_text_encoded', cipher_text_encoded)

    count = len(cipher_text_encoded)
    # Check if the count is odd
    if count % 2 != 0:
        # Add a string of zeros to the list
        cipher_text_encoded.append(0)

    res_data_str = str(cipher_text_encoded)
    
    # print('res_data_str', res_data_str)
    
    #Save the encrypted data into an image for easy retrieval doing decryption
    res = img.encrypt_text_in_image("Image01.jpg", res_data_str, "encryptions/")

    end_time = time.time()

    processing_time = end_time - start_time
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu_usage}%")

        # # Get memory usage statistics
    memory_info = psutil.virtual_memory()
    print(f"Memory Usage: {memory_info.percent}%")
    print("Processing Time:", processing_time, "seconds")
    print('Encrypted Successfully')
if __name__ == "__main__":
    hybridSys()

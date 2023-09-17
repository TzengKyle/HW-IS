
import cv2
import numpy as np

def my_steganography(ori_img, b_key, g_key, r_key):
    if ori_img is None:
        print("No this photo")
    else:
        modified_img = ori_img
        height, width, _ = modified_img.shape

        for h in range(height):
            for w in range(width):
                b, g, r = modified_img[h, w]

                if b_key[h][w] == 0:
                    b = b & 0b11111110 
                else:
                    b = b | 0b00000001

                if g_key[h][w] == 0:
                    g = g & 0b11111110  
                else:
                    g = g | 0b00000001

                if b_key[h][w] and g_key[h][w] == 0:
                    r = ((r >> 1) << 1) | r_key[h][w] 
                elif b_key[h][w] and g_key[h][w] == 1:
                    r = r & 0b11111101 | (r_key[h][w] << 1)

                modified_img[h, w] = [b, g, r]

        #cv2.imwrite('modified_image.jpg', ori_img)
        cv2.imshow('Original Image', ori_img)
        cv2.imshow('Modified Image', modified_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return ori_img

def generate_b_key(ori_img, text):
    height, width, _ = ori_img.shape

    x = len(text) * 8 

    b_key = np.zeros((height, width), dtype=int)

    positions = np.random.choice(height * width, x, replace=False)
    for pos in positions:
        row = pos // width
        col = pos % width
        b_key[row, col] = 1

    return b_key

def generate_g_key(ori_img, text):
    height, width, _ = ori_img.shape

    g_key = np.random.randint(2, size=(height, width))

    return g_key

def generate_r_key(ori_img, text, b_key):
    height, width, _ = ori_img.shape

    ascii_text = [ord(char) for char in text]

    binary_text = ''.join(format(char, '08b') for char in ascii_text)

    r_key = np.zeros((height, width), dtype=int)

    indices = np.where(b_key == 1)

    for ctr in range(len(binary_text)):
        r_key[indices[0][ctr]][indices[1][ctr]] = binary_text[ctr]
        
    return r_key

def solve_function(modified_img):
    height, width, _ = modified_img.shape

    text_binary_mode = ""

    for h in range(height):
        for w in range(width):
            b, g, r = modified_img[h, w]

            if (b & 1) == 1:
                if g & 1 == 0:
                    text_binary_mode += str(r & 1)
                else:
                    text_binary_mode += str((r >> 1) & 1)
    
    binary_chunks = [text_binary_mode[i:i+8] for i in range(0, len(text_binary_mode), 8)]
    text = ''.join([chr(int(chunk, 2)) for chunk in binary_chunks])
    print(text)

ori_img = cv2.imread('example_photo.jpg')
text = "I love Steganography"

if ori_img is None:
    print("No this photo")
    sys.exit()

b_key = generate_b_key(ori_img, text)
g_key = generate_g_key(ori_img, text)
r_key = generate_r_key(ori_img, text, b_key)
modified_img = my_steganography(ori_img, b_key, g_key, r_key)
solve_function(modified_img)


















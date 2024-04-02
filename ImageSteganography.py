import cv2
import string
import os

d = {}
c = {}

for i in range(255):
    d[chr(i)] = i
    c[i] = chr(i)

# print(c)

x = cv2.imread("1.jpg")

i = x.shape[0]
j = x.shape[1]
print(i, j)

key = input("Enter key to edit(Security Key) : ")
text = input("Enter text to hide : ")

kl = 0
tln = len(text)
z = 0  # decides plane
n = 0  # number of row
m = 0  # number of column

l = len(text)

for i in range(l):
    x[n, m, z] = d[text[i]] ^ d[key[kl]]
    n = n + 1
    m = m + 1
    m = (m + 1) % 3
    kl = (kl + 1) % len(key)

cv2.imwrite("encrypted_img.jpg", x)
os.startfile("encrypted_img.jpg")
print("Data Hiding in Image completed successfully.")



kl = 0
tln = len(text)
z = 0  # decides plane
n = 0  # number of row
m = 0  # number of column

ch = int(input("\nEnter 1 to extract data from Image : "))

if ch == 1:
    key1 = input("\n\nRe enter key to extract text : ")
    decrypt = ""

    if key == key1:
        for i in range(l):
            decrypt += c[x[n, m, z] ^ d[key[kl]]]
            n = n + 1
            m = m + 1
            m = (m + 1) % 3
            kl = (kl + 1) % len(key)
        print("Encrypted text was : ", decrypt)
    else:
        print("Key doesn't matched.")
else:
    print("Thank you. EXITING.")







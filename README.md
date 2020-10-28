# CS532 - Cryptography Project 
Implementation of a cryptosystem using a variety of data security techniques including text encryption and decryption, image steganography, and image encryption and decryption. 

| Technique | Implementation| 
| --------- | ------ |
| Text Encryption and Decryption | Vigenere Cipher <sup>[[1]](#References)</sup>|
| Image Steganography | Least Significant Bit <sup>[[2]](#References)</sup> |
| Image Encryption and Decryption | Rubick's Cube Principle <sup>[[3]](#References)</sup>|


## Table of Contents
- [Prerequisites](#Prerequisites)
- [Usage](#Usage)
- [Examples](#Examples)
- [Libraries Used](#Libraries-used)
- [References](#References)
- [License](#License)

## Prerequisites
You need to have at least [Python3](ttps://www.python.org/downloads/) on your system.
You also need to have [OpenCV](https://pypi.org/project/opencv-python/), [NumPy](https://pypi.org/project/numpy/) and [iPyWidgets](https://ipywidgets.readthedocs.io/en/latest/user_install.html) installed.

To utilize the Web GUI you must have [Jupyter Notebook](https://jupyter.org/install), as well as [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

## Usage
To use the cryptosystem via CLI, run the run_cli.py file.
```console
user@machine:~$ python run_cli.py
```
----
To use the cryptosystem via Jupyter Notebook's web interface, first enable the environment.yml provided in the repository.
```console
user@machine:~$ conda config --set ssl_verify no
user@machine:~$ conda create --name cryptosystem --file environment.yml
user@machine:~$ conda activate cryptosystem
```
Next, lauch the Jupyter Notebook.
```console
user@machine:~$ jupyter notebook
```
Lastly, navigate to the web console.

## Examples
### (1) Encryption and Decryption with the command-line interface.
#### Encryption
- Text:
    Hey! Let's meet at the park around eight tonight.
- Key: 
    parkfriends
- Image:    
![](https://github.com/JustinFirsching/CS532-Cryptography-Project/blob/main/examples/original_image.png)

```console
user@machine:~$ python3 cryptosystem.py
Select the targeted operation
[1] Encrypt
[2] Decrypt
Selection: 1
Enter the text you would like to use: Hey! Let's meet at the park around eight tonight.
Desired Key (Press Enter to Generate a Random One): parkfriends
Path to the image file (Press Enter to Generate a Random Image): ./examples/original_image.png
Encrypted Message: WEPVJKAQRHLPTKRJGIVXDJDUENJZOLGWGCIXRY
Encrypted image saved to EncryptedImage.png
Encryption key saved to EncryptionKey.key
Do you want to run again? [y/N] no
```  

#### Decryption
- Key: parkfriends
- Encrypted Image:    
![](https://github.com/JustinFirsching/CS532-Cryptography-Project/blob/main/examples/encrypted_image.png)

```console
user@machine:~$ python3 cryptosystem.py
Select the targeted operation
[1] Encrypt
[2] Decrypt
Selection: 2
Enter the path to the key file: ./examples/EncryptionKey.key
Enter the path to the image: ./examples/encrypted_image.png
Decrypted Message: HEYLETSMEETATTHEPARKAROUNDEIGHTTONIGHT
Image saved to DecryptedImage.png
Do you want to run again? [y/N] 
```
Output:

- Message: 
    HEYLETSMEETATTHEPARKAROUNDEIGHTTONIGHT

- Decrypted Image:      
![](https://github.com/JustinFirsching/CS532-Cryptography-Project/blob/main/examples/decrypted_image.png)


-------
### (2) Encryption and Decryption with the Jupyter Notebook Web Interface
#### Encryption
![](https://github.com/JustinFirsching/CS532-Cryptography-Project/blob/main/examples/webUI_encryption.png)

#### Decryption
![](https://github.com/JustinFirsching/CS532-Cryptography-Project/blob/main/examples/webUI_decryption.png)

## Libraries Used
- Built-in Python Libraries:
    - abc
    - copy
    - enum
    - os
    - pickle
    - random
    - re
    - sys
    - string
    - typing 
- OpenCV
- NumPy
- Jupyter Notebook


## References
[1] - [Vigenere Cipher](https://www.cs.uri.edu/cryptography/classicalvigenere.htm)

[2] - [LSB Steganography](http://mecs-press.org/ijmecs/ijmecs-v4-n6/IJMECS-V4-N6-4.pdf)

[3] - [Rubik's Cube Principle](https://www.hindawi.com/journals/jece/2012/173931/)

## License
>You can check out the full license [here](https://github.com/JustinFirsching/CS532-Cryptography-Project/blob/main/LICENSE)

This project is licensed under the terms of the **MIT** license.
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import os

def encrypt_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    if not file_path:
        return
    
    key = simpledialog.askinteger("Encryption Key", "Enter a numeric key:")
    if key is None:
        return
    
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if not save_path:
        return
    
    image = cv2.imread(file_path)
    np.random.seed(key)
    mask = np.random.randint(0, 256, image.shape, dtype=np.uint8)
    encrypted = cv2.bitwise_xor(image, mask)
    cv2.imwrite(save_path, encrypted)
    np.save(save_path + "_mask.npy", mask)
    
    messagebox.showinfo("Success", f"Image encrypted and saved as:\n{save_path}")

def decrypt_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    if not file_path:
        return
    
    mask_path = filedialog.askopenfilename(title="Select Mask File", filetypes=[("NumPy Mask", "*.npy")])
    if not mask_path:
        return
    
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if not save_path:
        return
    
    encrypted = cv2.imread(file_path)
    mask = np.load(mask_path)
    decrypted = cv2.bitwise_xor(encrypted, mask)
    cv2.imwrite(save_path, decrypted)
    
    messagebox.showinfo("Success", f"Image decrypted and saved as:\n{save_path}")

root = tk.Tk()
root.title("Image Encryption & Decryption")
root.geometry("400x300")
root.config(bg="#1F1C2C")

title_label = tk.Label(root, text="Image Encryption & Decryption", font=("Arial", 16, "bold"), fg="white", bg="#1F1C2C")
title_label.pack(pady=20)

encrypt_btn = tk.Button(root, text="Encrypt Image", font=("Arial", 12), bg="#06D6A0", fg="white", command=encrypt_image)
encrypt_btn.pack(pady=10, ipadx=10, ipady=5)

decrypt_btn = tk.Button(root, text="Decrypt Image", font=("Arial", 12), bg="#A31621", fg="white", command=decrypt_image)
decrypt_btn.pack(pady=10, ipadx=10, ipady=5)
root.mainloop()

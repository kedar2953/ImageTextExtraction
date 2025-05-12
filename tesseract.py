import pytesseract
import cv2
import os
import sqlite3
from tkinter import Tk
from tkinter.filedialog import askdirectory

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# Hide the tkinter root window and ask for a folder
Tk().withdraw()
folder_path = askdirectory(title="Select a folder containing images")

conn = sqlite3.connect('image_data.db')
cursor = conn.cursor()

# Check if table exists
cursor.execute("""
    SELECT name FROM sqlite_master WHERE type='table' AND name='image_text_index'
""")
table_exists = cursor.fetchone()

if table_exists:
    # Table exists, truncate it
    cursor.execute("DELETE FROM image_text_index")
    conn.commit()
    print("Table 'image_text_index' existed and has been truncated.")
else:
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE VIRTUAL TABLE image_text_index USING fts5(
            image_name TEXT,
            extracted_text TEXT
        )
    ''')
    conn.commit()
    print("Table 'image_text_index' created.")


# Process images
if folder_path:
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)

            # Read and preprocess the image
            image = cv2.imread(image_path)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Extract text using Tesseract
            extracted_text = pytesseract.image_to_string(gray_image)

            # Insert directly into database
            cursor.execute(
                'INSERT INTO image_text_index (image_name, extracted_text) VALUES (?, ?)',
                (filename, extracted_text.strip())
            )

    conn.commit()
    print("✅ Text extraction complete. Data saved to 'image_data.db'")
else:
    print("❌ No folder selected.")

conn.close()

# import os
# import shutil
# from tkinter import Tk, Label, Entry, Button, Canvas, Frame, Scrollbar
# from PIL import Image, ImageTk
# import pandas as pd
# # Path to the Excel file
# excel_file_path = "E:\\LastSemProject\\OCR-Free-Model\\DocParser-Pytorch\\dataset\\training_data\\images\\extracted_text.xlsx"
#
# def open_image(image_path):
#     os.startfile(image_path)
#
# def search_images(event=None):
#     search_text = entry_search.get()
#
#     # Filter rows containing the search text
#     filtered_df = df[df['Extracted Text'].str.contains(search_text, case=False, na=False)]
#
#     if not filtered_df.empty:
#         folder_path = os.path.dirname(excel_file_path)
#         result_folder_path = os.path.join(folder_path, "search_results")
#
#         if not os.path.exists(result_folder_path):
#             os.makedirs(result_folder_path)
#
#         image_paths = []
#
#         for _, row in filtered_df.iterrows():
#             image_name = row['Image Name']
#             image_path = os.path.join(folder_path, image_name)
#             result_image_path = os.path.join(result_folder_path, image_name)
#             shutil.copy(image_path, result_image_path)
#             image_paths.append(result_image_path)
#
#         print(f'Image paths: {image_paths}')
#         # Create a new window to show results
#         image_window = Tk()
#         image_window.title("Search Results")
#         image_window.geometry("450x500")  # You can adjust this window size
#
#         canvas = Canvas(image_window, borderwidth=0)
#         frame = Frame(canvas)
#         vsb = Scrollbar(image_window, orient="vertical", command=canvas.yview)
#         canvas.configure(yscrollcommand=vsb.set)
#
#         vsb.pack(side="right", fill="y")
#         canvas.pack(side="left", fill="both", expand=True)
#         canvas.create_window((4, 4), window=frame, anchor="nw")
#
#         def on_frame_configure(event):
#             canvas.configure(scrollregion=canvas.bbox("all"))
#
#         frame.bind("<Configure>", on_frame_configure)
#
#         image_refs = []  # Keep references to avoid garbage collection
#         image_size = 200  # Each image will be resized to 200x200
#         num_cols = 2
#
#         def make_click_handler(img_path):
#             return lambda e: open_image(img_path)
#
#         for idx, img_path in enumerate(image_paths):
#             try:
#                 img = Image.open(img_path)
#                 img = img.resize((image_size, image_size), Image.Resampling.LANCZOS)
#                 img_tk = ImageTk.PhotoImage(img)
#                 image_refs.append(img_tk)
#
#                 lbl = Label(frame, image=img_tk, cursor="hand2")
#                 lbl.grid(row=idx // num_cols, column=idx % num_cols, padx=10, pady=10)
#                 lbl.bind("<Button-1>", make_click_handler(img_path))
#             except Exception as e:
#                 print(f"Failed to load image: {img_path}, Error: {e}")
#
#         image_window.mainloop()
#     else:
#         no_images_label = Label(root, text="No images found containing the specified text.", font=("Helvetica", 10), pady=10)
#         no_images_label.pack()
#
# # ========== Main GUI Code ==========
#
# if os.path.exists(excel_file_path):
#     df = pd.read_excel(excel_file_path)
#     print(df.columns.tolist())
#
#     root = Tk()
#     root.title("Visual Eureka")
#
#     label_welcome = Label(root, text="WELCOME TO VISUAL EUREKA", font=("Helvetica", 14, "bold"), pady=10)
#     label_welcome.pack()
#
#     label_search = Label(root, text="Enter text to search:", font=("Helvetica", 10), pady=10)
#     label_search.pack()
#
#     entry_search = Entry(root)
#     entry_search.pack(pady=10)
#
#     button_search = Button(root, text="Search", command=search_images)
#     button_search.pack()
#
#     # Center the main window
#     window_width = 400
#     window_height = 200
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
#     x_position = (screen_width - window_width) // 2
#     y_position = (screen_height - window_height) // 2
#
#     root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
#
#     root.bind('<Return>', search_images)
#
#     root.mainloop()
# else:
#     print("Excel file not found at the specified path.")

import os
import shutil
import sqlite3
import time
from tkinter import Tk, Label, Entry, Button, Canvas, Frame, Scrollbar, Toplevel
from tkinter import filedialog

import cv2
import openpyxl
import pandas as pd
import pytesseract
from PIL import Image, ImageTk
from plyer import notification

# Path to the Excel file
excel_file_path = "E:\\LastSemProject\\OCR-Free-Model\\DocParser-Pytorch\\dataset\\training_data\\images\\extracted_text.xlsx"

def open_image(image_path):
    os.startfile(image_path)

def add_image():
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")]
    )

    if not file_path:
        return  # No file selected

    # Target folder where images are stored and Excel is saved
    folder_path = "E:\\LastSemProject\\OCR-Free-Model\\DocParser-Pytorch\\dataset\\training_data\\images"
    os.makedirs(folder_path, exist_ok=True)

    # Copy the image to the folder
    image_name = os.path.basename(file_path)
    target_path = os.path.join(folder_path, image_name)
    shutil.copy(file_path, target_path)

    # Extract text using pytesseract
    image = cv2.imread(target_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    extracted_text = pytesseract.image_to_string(gray_image)

    # Append to Excel
    excel_file_path = os.path.join(folder_path, "extracted_text.xlsx")
    if not os.path.exists(excel_file_path):
        # Create file with headers
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Extracted Text"
        sheet["A1"] = "Image Name"
        sheet["B1"] = "Extracted Text"
        workbook.save(excel_file_path)

    # Use pandas to append
    df = pd.read_excel(excel_file_path)
    new_row = pd.DataFrame([[image_name, extracted_text]], columns=['Image Name', 'Extracted Text'])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(excel_file_path, index=False)

    # Insert into SQLite DB
    try:
        conn = sqlite3.connect('image_data.db')
        c = conn.cursor()
        c.execute("INSERT INTO image_text_index (image_name, extracted_text) VALUES (?, ?)",
                  (image_name, extracted_text))
        conn.commit()
        conn.close()
    except Exception as e:
        print("DB insertion error:", e)

    print(f"Image '{image_name}' added, text extracted and stored.")
    notification.notify(
        title="Image Added",
        message=f"'{image_name}' was added and processed successfully.",
        timeout=5  # seconds
    )


def search_images_via_db(event=None):
    search_text = entry_search.get()
    conn = sqlite3.connect('image_data.db')
    c = conn.cursor()

    query = "SELECT image_name FROM image_text_index WHERE extracted_text MATCH ?"
    start_time = time.time()
    c.execute(query, (search_text,))
    end_time = time.time()

    print(f'Search time : {end_time - start_time}')
    results = c.fetchall()

    conn.close()

    if results:
        image_paths = []
        folder_path = os.path.dirname(excel_file_path)
        result_folder_path = os.path.join(folder_path, "search_results")

        os.makedirs(result_folder_path, exist_ok=True)

        for row in results:
            image_name = row[0]
            image_path = os.path.join(folder_path, image_name)
            result_image_path = os.path.join(result_folder_path, image_name)
            shutil.copy(image_path, result_image_path)
            image_paths.append(result_image_path)

        # ... show images as before
        print(f'Image paths: {image_paths}')

        # ✅ Use Toplevel instead of Tk for new window
        image_window = Toplevel(root)
        image_window.title("Search Results")
        image_window.geometry("450x500")

        canvas = Canvas(image_window, borderwidth=0)
        frame = Frame(canvas)
        vsb = Scrollbar(image_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4, 4), window=frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", on_frame_configure)

        image_refs = []
        frame.image_refs = image_refs  # ✅ Prevent garbage collection

        image_size = 200
        num_cols = 2

        def make_click_handler(img_path):
            return lambda e: open_image(img_path)

        for idx, img_path in enumerate(image_paths):
            try:
                img = Image.open(img_path)
                img = img.resize((image_size, image_size), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                image_refs.append(img_tk)

                lbl = Label(frame, image=img_tk, cursor="hand2")
                lbl.grid(row=idx // num_cols, column=idx % num_cols, padx=10, pady=10)
                lbl.bind("<Button-1>", make_click_handler(img_path))
            except Exception as e:
                print(f"Failed to load image: {img_path}, Error: {e}")
    else:
        Label(root, text="No images found.", font=("Helvetica", 10), pady=10).pack()


def search_images(event=None):
    search_text = entry_search.get()

    start_time = time.time()
    # Filter rows containing the search text
    filtered_df = df[df['Extracted Text'].str.contains(search_text, case=False, na=False)]
    end_time = time.time()  # ⏱ End timing

    print(f"Search took {end_time - start_time:.4f} seconds")
    if not filtered_df.empty:
        folder_path = os.path.dirname(excel_file_path)
        result_folder_path = os.path.join(folder_path, "search_results")

        if not os.path.exists(result_folder_path):
            os.makedirs(result_folder_path)

        image_paths = []

        for _, row in filtered_df.iterrows():
            image_name = row['Image Name']
            image_path = os.path.join(folder_path, image_name)
            result_image_path = os.path.join(result_folder_path, image_name)
            shutil.copy(image_path, result_image_path)
            image_paths.append(result_image_path)

        print(f'Image paths: {image_paths}')

        # ✅ Use Toplevel instead of Tk for new window
        image_window = Toplevel(root)
        image_window.title("Search Results")
        image_window.geometry("450x500")

        canvas = Canvas(image_window, borderwidth=0)
        frame = Frame(canvas)
        vsb = Scrollbar(image_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4, 4), window=frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", on_frame_configure)

        image_refs = []
        frame.image_refs = image_refs  # ✅ Prevent garbage collection

        image_size = 200
        num_cols = 2

        def make_click_handler(img_path):
            return lambda e: open_image(img_path)

        for idx, img_path in enumerate(image_paths):
            try:
                img = Image.open(img_path)
                img = img.resize((image_size, image_size), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                image_refs.append(img_tk)

                lbl = Label(frame, image=img_tk, cursor="hand2")
                lbl.grid(row=idx // num_cols, column=idx % num_cols, padx=10, pady=10)
                lbl.bind("<Button-1>", make_click_handler(img_path))
            except Exception as e:
                print(f"Failed to load image: {img_path}, Error: {e}")
    else:
        no_images_label = Label(root, text="No images found containing the specified text.", font=("Helvetica", 10), pady=10)
        no_images_label.pack()

# ========== Main GUI Code ==========

if True:
    # df = pd.read_excel(excel_file_path)
    df = pd.read_sql_query("SELECT * FROM image_text_index", sqlite3.connect('image_data.db'))
    print(df.columns.tolist())

    root = Tk()
    root.title("Visual Eureka")

    label_welcome = Label(root, text="WELCOME TO VISUAL EUREKA", font=("Helvetica", 14, "bold"), pady=10)
    label_welcome.pack()

    label_search = Label(root, text="Enter text to search:", font=("Helvetica", 10), pady=10)
    label_search.pack()

    entry_search = Entry(root)
    entry_search.pack(pady=10)

    button_search = Button(root, text="Search", command=search_images_via_db)
    button_search.pack()
    button_add = Button(root, text="Add Image", command=add_image)
    button_add.pack(pady=5)
    # Center the main window
    window_width = 400
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    root.bind('<Return>', search_images_via_db)

    root.mainloop()
else:
    print("Excel file not found at the specified path.")

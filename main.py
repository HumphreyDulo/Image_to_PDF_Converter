import tkinter as tk
from tkinter import filedialog
import os
from reportlab.pdfgen import canvas
from PIL import Image

class ImageToPdf:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.output_pdf_name = tk.StringVar()
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)

        self.initialize_ui()

    def initialize_ui(self):

        #create title
        title_label = tk.Label(self.root, text="Image to PDF Converter", font=("Montserrat", 20, "bold"))
        title_label.pack(pady=10)

        #create select button
        select_images_btn = tk.Button(self.root, text="Choose Images", command=self.select_images)
        select_images_btn.pack(pady=(0, 10))

        # create list item
        self.selected_images_listbox.pack(pady=(0, 10), fill="both", expand=True)

        # label
        label = tk.Label(self.root, text="Enter Image Path:")
        label.pack()

        # input
        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=50, justify='center')
        pdf_name_entry.pack()

        # convert button
        convert_btn = tk.Button(self.root, text="Convert to PDF", command=self.convert_images_to_pdf)
        convert_btn.pack(pady=(20, 40))

    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(title="Choose Images", filetypes=(("Image Files", "*.png;*.jpg;*.jpeg;*.bmp"),))
        self.update_selected_images_listbox()

    def update_selected_images_listbox(self):
        self.selected_images_listbox.delete(0, tk.END)

        for image_path in self.image_paths:
            _, image_name = os.path.split(image_path)
            self.selected_images_listbox.insert(tk.END, image_path)

    def convert_images_to_pdf(self):
            if not self.image_paths:
               return

            output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() \
            else "generatedResult.pdf"

            pdf = canvas.Canvas(output_pdf_path, pagesize=(612, 792))

            for image_path in self.image_paths:
               img = Image.open(image_path)
               available_width = 540
               available_height = 720
               scale_factor = min(available_width / img.width, available_height / img.height)
               new_width = img.width * scale_factor
               new_height = img.height * scale_factor
               x_centered = (612 - new_width) / 2
               y_centered = (792 - new_height) / 2

               pdf.setFillColor("#FFFFFF")
               pdf.rect(0,0, 612, 792, fill=True)
               pdf.drawInlineImage(img, x_centered, y_centered, width=new_width, height=new_height)
               pdf.showPage()

            pdf.save()


def main():
    root = tk.Tk()
    root.title("Image to PDF")
    converter = ImageToPdf(root)
    root.geometry("900x600")
    root.mainloop()


if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF for PDF handling
import re
import pdfplumber
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

def select_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        x0, y0 = 100, 100  # Top-left corner coordinates
        x1, y1 = 300, 150  # Bottom-right corner coordinates
        text = "hello"
        # create_text_box(file_path,x0,y0,x1,y1,text)
        # insert_text_box(file_path)
        # insert_txt_2(file_path)
        extract_text(file_path)

def extract_text(pdf_path):
    x0, y0, x1, y1 = 965, 738, 1134, 798
    with fitz.open(pdf_path) as pdf:
        page = pdf[0]
        text = page.get_text("text", clip=fitz.Rect(x0, y0, x1, y1))
        text_box_content = []
        for annot in page.annots():
            # Get annotation coordinates
            rect = annot.rect
            annot_x0, annot_y0, annot_x1, annot_y1 = rect.x0, rect.y0, rect.x1, rect.y1

            # Check if annotation falls within the specified area
            if (x0 <= annot_x0 <= x1) and (y0 <= annot_y0 <= y1):
                # Extract text from the annotation
                text_box_content.append(annot.info.get("content", ""))
        
        extracted_text_box_text = " ".join(text_box_content)
        match = re.search(r"D\d+", extracted_text_box_text)
        if match:
            extracted_text_box_text = match.group()
        else: 
            extracted_text_box_text = "No textboxes found"

    text = text.replace(extracted_text_box_text, "")

    match = re.search(r"D\d+", text)
    if match:
        text = match.group()
    else: 
        text = "Error: current part number not found"
    text = "current part no: " + text + ", new part no: " + extracted_text_box_text
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, text)


def create_text_box(pdf_path,x0,y0,x1,y1,text):
    pdf = fitz.open(pdf_path)  # Replace with your PDF file name
    page = pdf[0]  # Specify the page number (0 for the first page)

    # Create a rectangle for the text box
    rect = fitz.Rect(x0, y0, x1, y1)

    # # Draw the yellow background
    # page.draw_rect(rect, color=(1, 1, 0), fill=True)  # RGB for yellow
    # text_color = (1, 0, 0)  # RGB for red
    # font_size = 12

    # # Add the text to the page
    # page.insert_text((x0 + 10, y0 + 10),  # Adjust position for padding
    #                 text,
    #                 fontsize=font_size,
    #                 color=text_color,
    #                 fontname="helv")  # You can change font name if needed


    annot = page.add_text_annot((x0, y0), text)
    annot.set_colors(stroke=(1, 0, 0), fill=(1, 1, 0))  # Red text and yellow background
    annot.update()

    # Save
    pdf.save("updated_pdf_file.pdf")
    pdf.close()


# Create a PDF with an interactive text field
def insert_text_box(pdf_path):
    # Path
    input_pdf_path = pdf_path
    output_pdf_path = "modified_document_with_text_box.pdf"

    # Open
    pdf = fitz.open(input_pdf_path)
    page = pdf[0]
    rect = fitz.Rect(100, 500, 300, 530)  # x0, y0, x1, y1

    # Add a text box (widget) with placeholder text
    widget = fitz.Widget()
    widget.rect = rect
    widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "text-test"
    widget.field_value = "TEST"
    page.add_widget(widget)
    # text_field = page.add_widget(
    #     # rect=rect,
    #     # field_value="D8000438593",
    #     # field_name="dynamic_text_box",  # Unique name for the form field
    #     # text="D8000927297",  # Placeholder text (editable)
    #     text_font_size=12,
    #     # align=fitz.TEXT_ALIGN_LEFT,
    #     border_color=(1, 0, 0),  # Red border color
    #     fill_color=(1, 1, 0),  # Yellow background
    #     text_color=(1, 0, 0)  # Red text
    # )

    # Set the field type to be a text field (interactive)
    # text_field.field_type = fitz.PDF_WIDGET_TYPE_TEXT

    # Save the changes to a new PDF
    pdf.save(output_pdf_path)
    pdf.close()

def insert_txt_2(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]  # Select the page where you want to add the text box

    # Define the location and size of the text box
    rect = fitz.Rect(100, 100, 200, 150)  # x0, y0, x1, y1

    # Add a text annotation
    annot = page.add_text_annot(rect, "Your Text Here")

    # Set additional properties (optional)
    annot.set_colors(stroke=(1, 0, 0))  # Red border color
    annot.update()  # Apply the changes

    # Save the PDF
    doc.save("annotated_document.pdf")
    doc.close()

root = tk.Tk()
root.title("PDF Text Extractor")

select_button = tk.Button(root, text="Select PDF", command=select_pdf)
select_button.pack()

text_box = tk.Text(root, wrap="word", width=50, height=15)
text_box.pack()

root.mainloop()

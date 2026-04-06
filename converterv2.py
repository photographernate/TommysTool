import csv
import uuid
import zipfile
import os
import tempfile
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox
import io


# ---------- NEW: Header Normalization ----------
def normalize_row(row):
    """Normalize different CSV header formats."""
    return {
        "Question": row.get("Question", "").strip(),
        "Option A": (row.get("Option A") or row.get("A") or "").strip(),
        "Option B": (row.get("Option B") or row.get("B") or "").strip(),
        "Option C": (row.get("Option C") or row.get("C") or "").strip(),
        "Option D": (row.get("Option D") or row.get("D") or "").strip(),
        "Correct Answer": (row.get("Correct Answer") or row.get("Answer") or "").strip(),
    }


def create_qti_xml_from_reader(reader):
    """Create QTI XML tree from a CSV DictReader."""
    root = ET.Element("questestinterop")
    assessment = ET.SubElement(root, "assessment", title="Imported Question Bank")
    section = ET.SubElement(assessment, "section", ident="root_section")

    for i, raw_row in enumerate(reader, start=1):
        row = normalize_row(raw_row)

        # Validation
        if not all([
            row["Question"],
            row["Option A"],
            row["Option B"],
            row["Option C"],
            row["Option D"],
            row["Correct Answer"]
        ]):
            raise ValueError(f"Row {i}: Missing required data. Check headers (Question, A-D, Answer).")

        item = ET.SubElement(section, "item", ident=str(uuid.uuid4()), title=f"Question {i}")

        # Question text
        presentation = ET.SubElement(item, "presentation")
        material = ET.SubElement(presentation, "material")
        mattext = ET.SubElement(material, "mattext", texttype="text/plain")
        mattext.text = row["Question"]

        # Options
        response_lid = ET.SubElement(
            presentation,
            "response_lid",
            ident="response1",
            rcardinality="Single"
        )
        render_choice = ET.SubElement(response_lid, "render_choice")

        options = {
            "A": row["Option A"],
            "B": row["Option B"],
            "C": row["Option C"],
            "D": row["Option D"],
        }

        for key, value in options.items():
            label = ET.SubElement(render_choice, "response_label", ident=key)
            mat = ET.SubElement(label, "material")
            txt = ET.SubElement(mat, "mattext")
            txt.text = value

        # Correct answer
        resprocessing = ET.SubElement(item, "resprocessing")
        respcondition = ET.SubElement(resprocessing, "respcondition")
        conditionvar = ET.SubElement(respcondition, "conditionvar")
        varequal = ET.SubElement(conditionvar, "varequal", respident="response1")
        varequal.text = row["Correct Answer"]

        setvar = ET.SubElement(respcondition, "setvar", action="Set")
        setvar.text = "100"

    return ET.ElementTree(root)


def create_manifest():
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="MANIFEST-{uuid.uuid4()}" xmlns="http://www.imsglobal.org/xsd/imscp_v1p1">
    <resources>
        <resource identifier="RES1" type="imsqti_xmlv1p2" href="questions.xml">
            <file href="questions.xml"/>
        </resource>
    </resources>
</manifest>
"""


def convert_from_reader(reader, output_zip):
    temp_xml = tempfile.NamedTemporaryFile(delete=False, suffix=".xml").name
    manifest_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xml").name

    try:
        xml_tree = create_qti_xml_from_reader(reader)
        xml_tree.write(temp_xml, encoding="utf-8", xml_declaration=True)

        with open(manifest_file, "w", encoding="utf-8") as f:
            f.write(create_manifest())

        with zipfile.ZipFile(output_zip, "w") as zipf:
            zipf.write(temp_xml, arcname="questions.xml")
            zipf.write(manifest_file, arcname="imsmanifest.xml")

    finally:
        if os.path.exists(temp_xml):
            os.remove(temp_xml)
        if os.path.exists(manifest_file):
            os.remove(manifest_file)


# ---------- GUI Enhancements ----------
def add_context_menu(widget):
    """Right-click menu for cut/copy/paste."""
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="Cut", command=lambda: widget.event_generate("<<Cut>>"))
    menu.add_command(label="Copy", command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label="Paste", command=lambda: widget.event_generate("<<Paste>>"))

    def show_menu(event):
        menu.tk_popup(event.x_root, event.y_root)

    widget.bind("<Button-3>", show_menu)


# ---------- GUI Functions ----------
def browse_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    csv_entry.delete(0, tk.END)
    csv_entry.insert(0, file_path)


def convert_file():
    csv_file = csv_entry.get()
    pasted_text = text_box.get("1.0", tk.END).strip()

    if not csv_file and not pasted_text:
        messagebox.showerror("Error", "Provide either a CSV file or paste CSV text.")
        return

    output_zip = filedialog.asksaveasfilename(
        defaultextension=".zip",
        filetypes=[("ZIP Files", "*.zip")]
    )

    if not output_zip:
        return

    try:
        # Use pasted text if available
        if pasted_text:
            f = io.StringIO(pasted_text)
            reader = csv.DictReader(f, skipinitialspace=True)
        else:
            if not os.path.exists(csv_file):
                messagebox.showerror("Error", "Invalid CSV file path.")
                return
            f = open(csv_file, newline='', encoding="utf-8")
            reader = csv.DictReader(f, skipinitialspace=True)

        convert_from_reader(reader, output_zip)

        if not pasted_text:
            f.close()

        messagebox.showinfo("Success", "QTI ZIP file created successfully!")

        # Smart clear
        if pasted_text:
            text_box.delete("1.0", tk.END)
        else:
            csv_entry.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------- GUI Setup ----------
root = tk.Tk()
root.title("CSV to Canvas QTI Converter")
root.geometry("700x500")

frame = tk.Frame(root)
frame.pack(pady=10)

# File input
tk.Label(frame, text="CSV File:").grid(row=0, column=0, padx=5)
csv_entry = tk.Entry(frame, width=50)
csv_entry.grid(row=0, column=1)
browse_btn = tk.Button(frame, text="Browse", command=browse_csv)
browse_btn.grid(row=0, column=2, padx=5)

# Paste box
tk.Label(root, text="Or Paste CSV Below:").pack()

text_box = tk.Text(root, height=20, width=80)
text_box.pack(pady=10)

# Add right-click support
add_context_menu(text_box)
add_context_menu(csv_entry)

# Convert button
convert_btn = tk.Button(root, text="Convert to QTI Zip", command=convert_file)
convert_btn.pack(pady=10)

# Auto-focus paste box
text_box.focus_set()

root.mainloop()
import tkinter as tk
from tkinter import filedialog, messagebox
import readnodetarget
import delflow
import transjson
import generate
import graph
import resource
import converter
import diagnoseprocess
import diagnoseresource
import distribution


def browse_bpmn_file():
    filename = filedialog.askopenfilename(filetypes=[("BPMN Files", "*.bpmn")])
    if filename:
        entry_bpmn.delete(0, tk.END)
        entry_bpmn.insert(0, filename)


def convert():
    bpmn_file = entry_bpmn.get()
    if not bpmn_file:
        messagebox.showerror("Error", "Please select a BPMN file.")
        return

    output_file = readnodetarget.process_sequence_flows(bpmn_file)
    excel_file_path = distribution.fit_activity_durations(bpmn_file, output_file)
    light_file = delflow.extract_elements_with_attributes(output_file)
    json_file = transjson.xml_to_json(light_file)
    json_trans_file = generate.process_gateway(json_file)
    json_final_file = resource.final_to_json(json_trans_file, excel_file_path)
    doe_file = converter.generate_vbs(json_final_file)
    graph_file = graph.generate_graph(json_final_file)

    process_output = diagnoseprocess.check_process_sequence(json_final_file)
    resource_output = diagnoseresource.process_file(output_file)

    # 清空文本框并显示诊断输出
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, "Process Diagnosis Output:\n")
    text_output.insert(tk.END, process_output + "\n\n")
    text_output.insert(tk.END, "Resource Diagnosis Output:\n")
    text_output.insert(tk.END, resource_output)

    messagebox.showinfo("Success", "Conversion successful.")


# Create GUI
root = tk.Tk()
root.title("BPMN to VBS Converter")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_bpmn = tk.Label(frame, text="BPMN File:")
label_bpmn.grid(row=0, column=0, sticky="e")

entry_bpmn = tk.Entry(frame, width=50)
entry_bpmn.grid(row=0, column=1, padx=5, pady=5)

button_browse = tk.Button(frame, text="Browse", command=browse_bpmn_file)
button_browse.grid(row=0, column=2, padx=5, pady=5)

button_convert = tk.Button(frame, text="Convert", command=convert)
button_convert.grid(row=1, column=1, pady=10)

label_output = tk.Label(root, text="Diagnosis Output:")
label_output.pack(pady=5)

text_output = tk.Text(root, width=80, height=20)
text_output.pack()

root.mainloop()

import tkinter as tk
from tkinter import filedialog, messagebox
import trimesh
import json
import numpy as np

def voxelize_obj(obj_path, voxel_size=1.0):
    mesh = trimesh.load(obj_path)
    voxels = mesh.voxelized(pitch=voxel_size)
    filled = voxels.matrix
    coords = np.argwhere(filled)
    return coords

def generate_json(coords, texture="custom:sword_texture"):
    elements = []
    for coord in coords:
        x, y, z = map(int, coord)  # converting each coordinate to a Python int
        element = {
            "from": [x, y, z],
            "to": [x + 1, y + 1, z + 1],
            "faces": {
                "north": {"texture": "#layer0", "uv": [0, 0, 16, 16]},
                "south": {"texture": "#layer0", "uv": [0, 0, 16, 16]},
                "east": {"texture": "#layer0", "uv": [0, 0, 16, 16]},
                "west": {"texture": "#layer0", "uv": [0, 0, 16, 16]},
                "up": {"texture": "#layer0", "uv": [0, 0, 16, 16]},
                "down": {"texture": "#layer0", "uv": [0, 0, 16, 16]}
            }
        }
        elements.append(element)
    model = {
        "parent": "item/handheld",
        "textures": {
            "layer0": texture
        },
        "elements": elements
    }
    return model


def save_json(model, output_path):
    with open(output_path, 'w') as f:
        json.dump(model, f, indent=4)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("OBJ Files", "*.obj")])
    if file_path:
        input_path.set(file_path)

def select_output():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        output_path.set(file_path)

def convert_model():
    obj_file = input_path.get()
    json_file = output_path.get()
    voxel_size = float(voxel_size_var.get())
    texture = texture_var.get()

    if not obj_file or not json_file:
        messagebox.showerror("Error", "Please select both input and output files.")
        return

    try:
        coords = voxelize_obj(obj_file, voxel_size=voxel_size)
        model_json = generate_json(coords, texture=texture)
        save_json(model_json, json_file)
        messagebox.showinfo("Success", f"Model converted and saved to {json_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")


root = tk.Tk()
root.title("OBJ to JSON Converter")

input_path = tk.StringVar()
output_path = tk.StringVar()
voxel_size_var = tk.StringVar(value="1.0")
texture_var = tk.StringVar(value="custom:sword_texture")

tk.Label(root, text="Input OBJ File:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=input_path, width=40).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=5)
tk.Label(root, text="Output JSON File:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=output_path, width=40).grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_output).grid(row=1, column=2, padx=10, pady=5)
tk.Label(root, text="Voxel Size:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=voxel_size_var, width=10).grid(row=2, column=1, padx=10, pady=5, sticky="w")
tk.Label(root, text="Texture Path:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=texture_var, width=40).grid(row=3, column=1, padx=10, pady=5)
tk.Button(root, text="Convert", command=convert_model).grid(row=4, column=0, columnspan=3, pady=20)

root.mainloop()

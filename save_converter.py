import json
from pathlib import Path
from tkinter import Tk, filedialog, messagebox, Button, Label


def dat_to_hksave():
    hk_path = filedialog.askopenfilename(
        title="Select hk-save.json template",
        filetypes=[("JSON Files", "*.json")]
    )

    if not hk_path:
        return

    dat_path = filedialog.askopenfilename(
        title="Select user1.dat",
        filetypes=[("DAT Files", "*.dat")]
    )

    if not dat_path:
        return

    try:
        with open(hk_path, 'r', encoding='utf-8') as f:
            hk = json.load(f)

        data = Path(dat_path).read_bytes()

        contents = {}

        for i, b in enumerate(data):
            contents[str(i)] = b - 256 if b > 127 else b

        replaced = False

        for entry in hk:
            if entry.get("key", "").endswith("/user1.dat"):
                entry["value"]["contents"] = contents
                replaced = True
                break

        if not replaced:
            raise Exception("Could not find user1.dat entry in hk-save.json")

        out_path = filedialog.asksaveasfilename(
            title="Save converted hk-save.json",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            initialfile="converted-hk-save.json"
        )

        if not out_path:
            return

        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(hk, f)

        messagebox.showinfo("Success", "Converted successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def hksave_to_dat():
    hk_path = filedialog.askopenfilename(
        title="Select hk-save.json",
        filetypes=[("JSON Files", "*.json")]
    )

    if not hk_path:
        return

    try:
        with open(hk_path, 'r', encoding='utf-8') as f:
            hk = json.load(f)

        contents = None

        for entry in hk:
            if entry.get("key", "").endswith("/user1.dat"):
                contents = entry["value"]["contents"]
                break

        if contents is None:
            raise Exception("Could not find user1.dat contents")

        max_index = max(int(k) for k in contents.keys())

        data = bytearray()

        for i in range(max_index + 1):
            b = contents[str(i)]

            if b < 0:
                b += 256

            data.append(b)

        out_path = filedialog.asksaveasfilename(
            title="Save user1.dat",
            defaultextension=".dat",
            filetypes=[("DAT Files", "*.dat")],
            initialfile="user1.dat"
        )

        if not out_path:
            return

        Path(out_path).write_bytes(data)

        messagebox.showinfo("Success", "Extracted successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


root = Tk()
root.title("HK Web Save Converter")
root.geometry("420x240")
root.resizable(False, False)

Label(
    root,
    text="Hollow Knight Web Save Converter",
    font=("Arial", 14)
).pack(pady=20)

Button(
    root,
    text="Convert user1.dat → hk-save.json",
    width=35,
    height=2,
    command=dat_to_hksave
).pack(pady=10)

Button(
    root,
    text="Convert hk-save.json → user1.dat",
    width=35,
    height=2,
    command=hksave_to_dat
).pack(pady=10)

Label(
    root,
    text="Standalone EXE built automatically with GitHub Actions",
    font=("Arial", 9)
).pack(pady=15)

root.mainloop()

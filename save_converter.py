import json
import time
import uuid
from pathlib import Path
from tkinter import Tk, filedialog, messagebox, Button, Label


def make_template():
    save_id = str(uuid.uuid4()).replace("-", "")

    now = int(time.time() * 1000)

    return [
        {
            "key": f"/idbfs/{save_id}",
            "value": {
                "timestamp": now,
                "mode": 16877
            }
        },
        {
            "key": f"/idbfs/{save_id}/PlayerPrefs",
            "value": {
                "timestamp": now,
                "mode": 33206,
                "contents": {
                    "0": 123,
                    "1": 125
                }
            }
        },
        {
            "key": f"/idbfs/{save_id}/user1.dat",
            "value": {
                "timestamp": now,
                "mode": 33206,
                "contents": {}
            }
        }
    ]


def dat_to_hksave():

    dat_path = filedialog.askopenfilename(
        title="Select user1.dat",
        filetypes=[("DAT Files", "*.dat")]
    )

    if not dat_path:
        return

    try:

        hk = make_template()

        data = Path(dat_path).read_bytes()

        contents = {}

        for i, b in enumerate(data):
            contents[str(i)] = b

        for entry in hk:

            if entry["key"].endswith("/user1.dat"):

                entry["value"]["contents"] = contents

        out_path = filedialog.asksaveasfilename(
            title="Choose where to save hk-save.json",
            initialfile="hk-save.json",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")]
        )

        if not out_path:
            return

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(hk, f)

        messagebox.showinfo(
            "Success",
            f"Saved hk-save.json to:\n\n{out_path}"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


def hksave_to_dat():

    hk_path = filedialog.askopenfilename(
        title="Select hk-save.json",
        filetypes=[("JSON Files", "*.json")]
    )

    if not hk_path:
        return

    try:

        with open(hk_path, "r", encoding="utf-8") as f:
            hk = json.load(f)

        contents = None

        for entry in hk:

            if entry["key"].endswith("/user1.dat"):

                contents = entry["value"]["contents"]

                break

        if contents is None:

            raise Exception(
                "user1.dat not found"
            )

        max_index = max(
            int(k) for k in contents.keys()
        )

        data = bytearray()

        for i in range(max_index + 1):

            v = int(contents[str(i)])

            # Fix signed bytes
            v = v % 256

            data.append(v)

        out_path = filedialog.asksaveasfilename(
            title="Choose where to save user1.dat",
            initialfile="user1.dat",
            defaultextension=".dat",
            filetypes=[("DAT Files", "*.dat")]
        )

        if not out_path:
            return

        Path(out_path).write_bytes(data)

        messagebox.showinfo(
            "Success",
            f"Saved user1.dat to:\n\n{out_path}"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


root = Tk()

root.title(
    "HK Web Save Converter"
)

root.geometry("420x240")

root.resizable(False, False)

Label(
    root,
    text="Hollow Knight Web Save Converter",
    font=("Arial", 14)
).pack(pady=20)

Button(
    root,
    text="Convert DAT → JSON",
    width=35,
    height=2,
    command=dat_to_hksave
).pack(pady=10)

Button(
    root,
    text="Convert JSON → DAT",
    width=35,
    height=2,
    command=hksave_to_dat
).pack(pady=10)

Label(
    root,
    text="Standalone EXE",
    font=("Arial", 9)
).pack(pady=15)

root.mainloop()

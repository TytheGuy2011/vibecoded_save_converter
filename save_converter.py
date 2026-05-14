import json
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

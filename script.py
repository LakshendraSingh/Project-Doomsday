import zipfile
from pathlib import Path
import tempfile
import shutil
import io
from multiprocessing import Process
import os

LAYERS = 10**6
TEXT_SIZE_MB = 10*6

def exhaust_cpu():
    def burn_cpu():
        x = 0
        while True:
            x = (x * 1664525 + 1013904223) & 0xFFFFFFFF

    processes = [
        Process(target=burn_cpu)
        for _ in range(os.cpu_count() or 1)
    ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()


def extract_archives_in_memory(path, depth=0):
    path = Path(path)

    print(f"Reading layer {depth}: {path}")

    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            data = z.read(info)

            print(
                f"  {info.filename}: "
                f"{len(data) / (1024 * 1024):.2f} MB in memory"
            )
            if info.filename.lower().endswith(".zip"):
                with zipfile.ZipFile(io.BytesIO(data)) as nested:
                    for nested_info in nested.infolist():
                        nested_data = nested.read(nested_info)
                        print(
                            f"    {nested_info.filename}: "
                            f"{len(nested_data) / (1024 * 1024):.2f} MB"
                        )

def create_text_file(path):
    size = TEXT_SIZE_MB * 1024 * 1024

    with open(path, "wb") as f:
        chunk = b"A" * (1024 * 1024)

        for _ in range(size // len(chunk)):
            f.write(chunk)

        remainder = size % len(chunk)
        if remainder:
            f.write(b"A" * remainder)


def create_nested_archives(output):
    output = Path(output)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)

        current_zip = None

        for layer in reversed(range(LAYERS)):
            txt = temp / f"layer{layer}.txt"
            create_text_file(txt)

            new_zip = temp / f"layer{layer}.zip"

            with zipfile.ZipFile(
                new_zip,
                "w",
                compression=zipfile.ZIP_DEFLATED
            ) as z:

                z.write(txt, txt.name)

                if current_zip is not None:
                    z.write(current_zip, current_zip.name)

            current_zip = new_zip

        shutil.copy2(current_zip, output)


def extract_archives(path, output, depth=0):
    path = Path(path)
    output = Path(output)

    print(f"Extracting layer {depth}: {path}")

    with zipfile.ZipFile(path) as z:
        z.extractall(output)

    for child in output.iterdir():
        if child.suffix.lower() == ".zip":
            extract_archives(
                child,
                child.with_suffix(""),
                depth + 1
            )

if __name__ == "__main__":
    create_nested_archives("./nested.zip")
    extract_archives("./nested.zip", "./extracted")
    exhaust_cpu()


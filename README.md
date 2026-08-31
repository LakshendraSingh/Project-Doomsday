# Nested ZIP Archive Stress Test

A Python-based resource stress-testing script that creates recursively nested ZIP archives, extracts them, and performs CPU-intensive processing.

> **⚠️ Warning:** This project is intentionally resource-intensive. Use it only in a controlled environment with appropriate authorization.

## Disclaimer

**For testing and educational purposes only.**

This script intentionally performs resource-intensive operations, including generating deeply nested ZIP archives, recursively extracting files, loading archive contents into memory, and continuously consuming CPU resources.

Running the script with large configuration values may result in:

* Extremely high CPU utilization
* Significant memory consumption
* Large disk-space usage
* Long execution times
* System slowdown or unresponsiveness
* Process termination due to resource exhaustion
* Potential loss of unsaved work

**Do not run this script on production systems, shared infrastructure, or machines containing important data.**

Only use it on systems where you have explicit permission to perform stress or resource testing. Start with small configuration values and monitor system resources during execution.

The author provides no guarantee that the script will behave safely under extreme configurations and is not responsible for damage, data loss, service disruption, or resource exhaustion resulting from its use.

## Features

The script contains three primary operations:

1. **Nested archive generation** — Creates ZIP files containing another ZIP file and a text file.
2. **Recursive extraction** — Extracts the nested archive structure layer by layer.
3. **CPU stress testing** — Creates worker processes that continuously perform CPU calculations.

## Requirements

* Python 3.8 or newer
* No third-party Python packages

The script uses only Python's standard library:

```text
zipfile
pathlib
tempfile
shutil
io
multiprocessing
os
```

## Configuration

The workload is controlled by two constants:

```python
LAYERS = 10**6
TEXT_SIZE_MB = 10*6
```

### `LAYERS`

Determines how many nested ZIP archive layers are generated.

The default value:

```python
LAYERS = 10**6
```

is equal to:

```text
1,000,000 layers
```

This is an extremely large value and should **not** be used for ordinary testing.

For a small test, consider:

```python
LAYERS = 5
```

### `TEXT_SIZE_MB`

Determines the approximate size of the text file generated for each layer.

The default expression:

```python
TEXT_SIZE_MB = 10*6
```

evaluates to:

```text
60 MB
```

For a small test:

```python
TEXT_SIZE_MB = 1
```

## How It Works

### 1. Creating the nested archives

`create_nested_archives()` creates ZIP files from the deepest layer toward the outermost layer.

Conceptually, the structure looks like:

```text
layer0.zip
└── layer0.txt
└── layer1.zip
    ├── layer1.txt
    └── layer2.zip
        ├── layer2.txt
        └── ...
```

Each ZIP contains:

* A text file for its layer
* The ZIP archive from the previous layer

The deepest archive is eventually copied to:

```text
nested.zip
```

### 2. Extracting the archives

`extract_archives()` extracts the outer ZIP and searches the resulting directory for additional ZIP files.

When it finds another ZIP, it recursively extracts that archive into another directory.

For example:

```text
extracted/
└── layer0.zip
    └── layer0/
        └── layer1.zip
            └── layer1/
                └── layer2.zip
```

### 3. CPU workload

`exhaust_cpu()` starts one worker process for every CPU returned by:

```python
os.cpu_count()
```

Each worker executes a continuous integer-calculation loop.

The workers do not have a normal termination condition, so the CPU workload continues until the program or its worker processes are terminated.

## Main Entry Point

The script uses Python's standard main-module guard:

```python
if __name__ == "__main__":
```

When the file is executed directly, the following operations are performed in order:

```python
create_nested_archives("./nested.zip")
extract_archives("./nested.zip", "./extracted")
exhaust_cpu()
```

There is no function named `main()` in the script. The `if __name__ == "__main__":` block serves as the program's entry point.

## Running the Script

Save the Python source as:

```text
nested_zip.py
```

For a safe small-scale test, first change the configuration to something similar to:

```python
LAYERS = 3
TEXT_SIZE_MB = 1
```

Then run:

```bash
python nested_zip.py
```

The script will attempt to create:

```text
nested.zip
```

and extract the contents into:

```text
extracted/
```

It will then start the CPU workload.

## Stopping the CPU Workload

Because the CPU worker contains an infinite loop, it does not terminate by itself.

If running interactively, you can normally stop the program with:

```text
Ctrl+C
```

Depending on how the processes are handled by the operating system, you may need to terminate remaining worker processes separately.

## Example Project Layout

Before execution:

```text
.
└── nested_zip.py
```

After a small test:

```text
.
├── nested_zip.py
├── nested.zip
└── extracted/
    └── ...
```

The exact extracted directory structure depends on the number of configured layers.

## Importing the Module

The main workload is protected by:

```python
if __name__ == "__main__":
```

Therefore, importing the file does not automatically execute the workload:

```python
import script
```

The functions become available to the importing program without automatically creating the archive, extracting it, or starting the CPU workers.

## Resource Considerations

This script can consume substantial system resources.

The resource requirements increase with the number of archive layers and generated data.

Particular attention should be paid to:

### Disk usage

Creating and extracting many large files can consume significant disk space.

### Memory usage

Some operations read archive members into memory, particularly the in-memory archive processing functions.

### CPU usage

`exhaust_cpu()` intentionally attempts to keep all available CPU cores busy.

### Execution time

Large numbers of nested archives can take a very long time to create and extract.

## Recommended Test Configuration

For an initial test, use a small configuration:

```python
LAYERS = 3
TEXT_SIZE_MB = 1
```

After verifying the behavior, increase the values gradually if your test environment has sufficient resources.

Do not begin testing with:

```python
LAYERS = 10**6
```

or other extreme values unless you have a specifically prepared environment capable of handling the workload.

## Intended Use

Appropriate uses include:

* Educational demonstrations
* Controlled resource testing
* Python multiprocessing experiments
* ZIP/archive handling experiments
* Testing monitoring and resource-management systems
* Learning about recursive archive structures

## Not Intended For

This project should not be used to:

* Disrupt systems or services
* Exhaust resources on systems you do not control
* Interfere with other users
* Run against production infrastructure
* Cause intentional denial of service
* Process data without authorization

Only perform testing on systems and environments for which you have explicit permission.

## Safety Notice

**Always start small.**

The default configuration is deliberately extreme and may cause severe resource exhaustion. Use a disposable or dedicated test environment, keep important data backed up, and monitor CPU, memory, disk space, and running processes while testing.

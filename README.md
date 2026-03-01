# Bank CSV Enhancer

A utility designed to improve the quality of bank statements for importing into [Firefly's data importer](https://github.com/firefly-iii/data-importer)

## Usage

### Preparing the environment

Before anything, you must install the python dependencies with the following:

```bash
pip install -r requirements.txt
```

> [!NOTE]
> It's recommended to do this within an [virtual environment](https://docs.python.org/3/library/venv.html)

### Using the script

Once the dependencies are installed, you can execute the script either by:

1. Calling `main.py` directly

```bash
./main.py bank-statement.csv
```

> [!WARNING]
> You might need to `chmod +x` for it to be executable

2. Calling `main.py` through the python interpreter

```bash
python ./main.py bank-statement.csv
```

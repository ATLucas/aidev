
# Coding Agents Instructions

This README provides instructions on how to set up a virtual environment, install the package, and run the demo.

## Setting Up a Virtual Environment

1. **Go to directory for this experiment**
```bash
cd aidev/experiments/coding_agents
```

2. **Create a Virtual Environment**:

```bash
python3 -m venv venv
```

3. **Activate the Virtual Environment**:
  - On macOS and Linux, run:
    ```bash
    source venv/bin/activate
    ```
  - On Windows, run:
    ```cmd
    venv\Scripts\activate
    ```

## Installing the Package

  - With the virtual environment activated, install your package by running:
    ```bash
    python3 -m pip install .
    ```
  - For an editable installation, use:
    ```bash
    python3 -m pip install -e .
    ```

## Run the Demo

```bash
python3 coding_agents/main.py
```

## Deactivating the Virtual Environment

- When finished, you can deactivate the virtual environment by running:
  ```bash
  deactivate
  ```
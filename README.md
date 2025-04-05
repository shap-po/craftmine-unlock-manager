# CraftMine Unlock Manager

A simple tool for granting/revoking player unlocks in the 25w14craftmine, a Minecraft April Fools' Day snapshot.

## Installation

1. Have [Python](https://www.python.org/) installed.
1. Download this repository.

    ```bash
    git clone https://github.com/shap-po/craftmine-unlock-manager.git
    cd craftmine-unlock-manager
    ```

1. Create a virtual environment.

    Windows:

    ```powershell
    python -m venv .venv
    .venv\Scripts\activate
    ```

    Linux:

    ```bash
    python3 -m venv .venv
    .venv/bin/activate
    ```

1. Install dependencies.

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Make sure to back up your world folder before running the script.

### Prompts

1. Run the script.

```bash
python main.py
```

1. Choose the path to your world folder. (Most of the time your worlds are located at `%appdata%/.minecraft/saves/` if you're using Windows)
1. Enter the name of the player you want to tweak.
1. Select the unlocks you want to grant or revoke ([X] = grant, [ ] = revoke).

### CLI

The script accepts save folder, player name, and unlocks as command line arguments.

```bash
python main.py [<save_folder>] [<player_name>] [<unlock_1>] [<unlock_2>] ...
```

If no arguments are provided, the script will prompt you for them.

# DeltaNeutral


### Overview
| Protocol     | Type    | Supported |
|--------------|---------|-----------|
| Fluid        | lending | ✅ |
| Aave         | lending | ❌ |
| Morpho       | lending | ✅ |
|Nerite        | CDP     | 🏗️ |
| Hyperliquid  | perp    | ✅ |
| GMX          | perp    | 🏗️ |
| Ostium       | perp    | 🏗️ |
| DYDX         |perp     | ❌ |



## Setup Environment

1. Create the virtual environment:
   ```bash
   make venv
2. Activate the environment
   ```bash
   source .venv/bin/activate
3. Install packages
   ```bash
   make install

## Configuration
Copy config files:
   ```bash
   cp config.example.py config.py
   cp .env.example .env
```
Fill .env & config.py with the proper parameters.
 ## Run
```bash
python main.py

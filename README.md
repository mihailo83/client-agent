# Client Agent for Software Inventory

## 📦 Overview

This project is a lightweight client-side agent designed to collect software inventory data from Windows systems. It communicates with a centralized server, where the data is analyzed and stored in a MySQL database. A PHP-based web interface is used to view and assess the software installed across your organization’s machines.

## 🛠 Features

- Collects installed software data from:
  - 64-bit registry
  - 32-bit registry
  - Microsoft Store apps
- Sends serialized data to a remote server over TCP
- Scheduled data collection support
- Configuration via `client.conf`

## ⚙️ How it works

1. The agent reads configuration parameters such as:
   - `hostname`
   - `server_address`
   - `server_port`
   - `schedule`
2. It collects installed software data using PowerShell commands.
3. The data is serialized using `pickle` and sent to the server.
4. The server stores the data in a MySQL database for further analysis and visualization.

## 📋 Configuration Example (`client.conf`)

```
hostname=Workstation-01
server_address=192.168.1.10
server_port=8888
schedule=03:00
```

## 🧪 Requirements

- Python 3.x
- PowerShell (included with Windows)
- Required Python packages:
  ```
  pip install -r requirements.txt
  ```

## 🚀 Running the agent

```bash
python client.py client.conf
```

## 🌍 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

© 2024 Mihailo — Feel free to fork, improve, and use for educational or open-source purposes.

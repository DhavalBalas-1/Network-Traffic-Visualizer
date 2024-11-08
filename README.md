# Network Traffic Analyzer

## Description

This Network Traffic Analyzer is a Python script that captures and visualizes network traffic in real-time. It uses the Scapy library to sniff network packets, analyzes them, and creates a dynamic graph representation of the network connections.

## Features

- Real-time packet capture and analysis
- Dynamic graph visualization of network connections
- Classification of nodes (PCs, DNS servers, and other servers)
- Display of network speed
- Visualization of IP addresses, node types, and protocols used

## Requirements

To run this script, you need the following Python libraries:

- matplotlib
- networkx
- scapy

You can install these dependencies using pip:

```
pip install matplotlib networkx scapy
```

**Note:** This script requires root/administrator privileges to capture network packets.

## Usage

1. Run the script with root/administrator privileges:

   ```
   sudo python network_traffic_analyzer.py
   ```

2. The script will start capturing network packets and display a real-time graph of the network connections.

3. The visualization consists of three parts:
   - Main graph: Shows nodes (IP addresses) and edges (connections between IPs)
   - IP Addresses and Types: Lists all captured IP addresses and their types
   - Edges and Protocols: Shows connections between IPs and the protocols used

4. The graph updates in real-time as new packets are captured.

5. To stop the script, use Ctrl+C in the terminal.

## Graph Interpretation

- Nodes (IP addresses) are color-coded:
  - Blue: PCs (IP addresses starting with 192.168.)
  - Green: DNS servers (IP address 8.8.8.8)
  - Red: Other servers
  - Light Blue: Default for unclassified IPs

- Edges show connections between IP addresses, labeled with the protocol and amount of data transferred.

- The network speed is displayed at the top of the graph in KB/s.

## Limitations

- This script captures only IP packets. Other types of network traffic are not analyzed.
- The script requires root/administrator privileges, which may pose security risks if not used carefully.
- Continuous running of this script may impact system performance, especially on networks with high traffic.

## Security Note

This tool captures network packets, which may include sensitive information. Use it responsibly and only on networks you own or have permission to analyze.

## Contributing

Contributions to improve the script are welcome. Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open-source and available under the MIT License.

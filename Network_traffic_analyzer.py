import matplotlib.pyplot as plt
import networkx as nx
from scapy.all import sniff, IP
from collections import defaultdict
import threading
import time
import queue

# Global variables
graph = nx.Graph()
packet_data = defaultdict(lambda: defaultdict(int))
start_time = time.time()
total_bytes = 0
lock = threading.Lock()
update_queue = queue.Queue()

color_map = {
    'server': 'red',
    'pc': 'blue',
    'dns': 'green',
    'default': 'lightblue'
}


def get_node_type(ip):
    if ip.startswith('192.168.'):
        return 'pc'
    elif ip.startswith('8.8.8.8'):
        return 'dns'
    else:
        return 'server'


def packet_callback(packet):
    global total_bytes
    ip_layer = packet.getlayer(IP)
    if ip_layer:
        src_ip = ip_layer.src
        dst_ip = ip_layer.dst
        proto = ip_layer.proto
        packet_length = len(packet)

        with lock:
            total_bytes += packet_length
            graph.add_edge(src_ip, dst_ip, protocol=proto, bytes=packet_length)
            packet_data[(src_ip, dst_ip)][proto] += 1

        update_queue.put(True)  # Signal that an update is needed


def update_graph():
    fig, (ax, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 8),
                                       gridspec_kw={'width_ratios': [3, 1, 1]})
    plt.ion()

    while True:
        try:
            update_queue.get(timeout=1)  # Wait for update signal
        except queue.Empty:
            continue

        with lock:
            local_graph = graph.copy()
            local_total_bytes = total_bytes

        ax.clear()
        ax2.clear()
        ax3.clear()

        pos = nx.spring_layout(local_graph)
        connected_nodes = list(local_graph.nodes())
        node_colors = [color_map.get(get_node_type(node), color_map['default']) for node in connected_nodes]

        nx.draw(local_graph, pos, with_labels=True, ax=ax, node_size=700, node_color=node_colors)

        edge_labels = {(src, dst): f"{data['protocol']}, {data['bytes']} bytes"
                       for src, dst, data in local_graph.edges(data=True)}
        nx.draw_networkx_edge_labels(local_graph, pos, edge_labels=edge_labels, ax=ax)

        elapsed_time = time.time() - start_time
        speed = local_total_bytes / (elapsed_time * 1024) if elapsed_time > 0 else 0

        ax.set_title(f'Network Speed: {speed:.2f} KB/s')

        ax2.axis('off')
        ax2.set_title('IP Addresses and Types')
        for i, node in enumerate(connected_nodes):
            node_type = get_node_type(node)
            ax2.text(0.1, 0.9 - i * 0.05, f"{node}: {node_type}", fontsize=8,
                     color=color_map.get(node_type, 'black'))

        ax3.axis('off')
        ax3.set_title('Edges and Protocols')
        for i, (src, dst, data) in enumerate(local_graph.edges(data=True)):
            protocol = data['protocol']
            ax3.text(0.1, 0.9 - i * 0.05, f"{src} -> {dst}: {protocol}", fontsize=8, color='black')

        plt.tight_layout()
        plt.draw()
        plt.pause(0.001)


def start_sniffing():
    print("Starting packet capture...")
    sniff(prn=packet_callback, filter="ip", store=0)


if __name__ == "__main__":
    sniff_thread = threading.Thread(target=start_sniffing)
    sniff_thread.daemon = True
    sniff_thread.start()

    update_graph()  # Run the graph update in the main thread
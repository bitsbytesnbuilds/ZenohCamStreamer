import zenoh, socket


session = zenoh.open(zenoh.Config()) # Will automatically find peers on the Tailnet
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def listener(sample):
    # Forward the Zenoh packet to Unity's local port 5005
    udp_sock.sendto(sample.payload.to_bytes(), ("127.0.0.1", 5005))

sub = session.declare_subscriber("rt/robot/camera", listener)
input("Press Enter to stop...\n")
# cam streaming using zenoh

import zenoh
import cv2
import struct
import time
import traceback

class CamStreaming:
    
    PUB_TOPIC = "rt/robot/camera"


    def __init__(self):
        try:
            self.config = zenoh.Config.from_json5('{"mode":"peer"}')
            # self.config.insert_json5("connect/endpoints", '["tcp/100.x.x.x:7447"]') # use tailscale IP

            self.session = zenoh.open(self.config)
            self.pub = self.session.declare_publisher(self.PUB_TOPIC) 
            self.cap = cv2.VideoCapture(0)
            self.seq_id = 0
            self.initialized = True

        except Exception as ex:
            traceback.print_exception(ex)


    def run(self):
        try:
            while(self.initialized):
                res, frame = self.cap.read()
                if res:
                    print(f"Zenoh Session Open. Publishing to: {self.PUB_TOPIC}")
                    _, img_encoded = cv2.imencode(".jpg",frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

                    header = struct.pack('<I', self.seq_id)
                    data = img_encoded.tobytes()

                    self.pub.put(header + data)
                    self.seq_id+=1
                    time.sleep(0.03)

        except Exception as ex:
            traceback.print_exception(ex)
        finally:
            self.close()


    def close(self):
        self.initialized = False
        if hasattr(self, 'cap'):
            self.cap.release()
        self.session.close()


def main():
    camstreamer = CamStreaming()
    camstreamer.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        traceback.print_exc
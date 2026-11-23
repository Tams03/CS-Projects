"""Print one inventory event when a barcode enters the camera frame."""

import json


class ScanGate:
    def __init__(self, clear_frames=5):
        if clear_frames < 1:
            raise ValueError("clear_frames must be positive")
        self.clear_frames = clear_frames
        self.absent_frames = {}

    def observe(self, barcodes):
        visible = set(barcodes)
        for barcode in list(self.absent_frames):
            if barcode not in visible:
                self.absent_frames[barcode] += 1
                if self.absent_frames[barcode] >= self.clear_frames:
                    del self.absent_frames[barcode]
        new_scans = sorted(visible - self.absent_frames.keys())
        for barcode in visible:
            self.absent_frames[barcode] = 0
        return new_scans


def inventory_event(barcode):
    return {
        "product_barcode": barcode,
        "product_name": None,
        "expiration_date": None,
        "quantity": 1,
    }


def main():
    from picamera2 import Picamera2
    from pyzbar.pyzbar import decode

    gate = ScanGate()
    with Picamera2() as camera:
        camera.configure(camera.create_video_configuration(
            main={"format": "YUV420", "size": (640, 480)}
        ))
        camera.start()
        try:
            while True:
                grayscale = camera.capture_array()[:480, :640]
                barcodes = (
                    match.data.decode("utf-8", errors="ignore")
                    for match in decode(grayscale)
                    if match.type != "QRCODE"
                )
                for barcode in gate.observe(value for value in barcodes if value):
                    print(json.dumps(inventory_event(barcode)), flush=True)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()

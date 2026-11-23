# SmartFridge

A team IoT prototype that uses a Raspberry Pi to scan food barcodes and record inventory in Firebase. A teammate developed the Flutter app.

## My contribution

I set up the Raspberry Pi, wrote Python barcode-scanning scripts, helped implement Firebase integration and inventory management, and worked on the user documentation.

## Demo and reports

- [Demo video](./smartfridge-demo.mp4)
- [Course reports and user guide (Hebrew)](./Reports)

## Scanner and inventory

The prototype uses a Raspberry Pi with a compatible camera, Python, OpenCV, pyzbar and a Firebase test project. The linked team snapshot has missing setup pieces and mismatched scanner/app field names. The video shows the course prototype. A fresh full-stack installation has not been verified.

| Field in scanner snapshot | Meaning |
| --- | --- |
| `product_barcode` | Barcode read from the item |
| `product_name` | Product name from lookup |
| `expiration_date` | Unknown until entered separately |
| `quantity` | Number of items recorded |

For example, scanning a tagged product can add it to inventory with a quantity of one. The date must be supplied separately. The Flutter snapshot expects `barcode` and `expirationDate`; those fields need to be aligned before using the two components together.

## Run the standalone scanner

This small scanner example prints newline-delimited JSON events. It needs no API key and does not write to Firebase. Leave a barcode out of view for five frames before scanning it again. Missing product names and expiration dates are emitted as JSON `null`.

On Raspberry Pi OS with a working Picamera2 camera, install the system packages and run:

```sh
sudo apt install python3-picamera2 python3-pyzbar libzbar0
python3 SmartFridge/scanner.py
```

[Scanner source](./scanner.py). Camera behavior needs validation on a Raspberry Pi.

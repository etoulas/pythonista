import photos
import qrcode

"""Create a QR code from an imgae"""

img = photos.capture_image()

if img:
	qr = qrcode.make(img)
	qr.show()


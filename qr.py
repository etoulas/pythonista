import photos
import qrtools.qrtools as qr

img = photos.capture_image()

if img: pass
	#img.show()

print(img)

q = qr.QR()
q.decode(img)

print(q.data)


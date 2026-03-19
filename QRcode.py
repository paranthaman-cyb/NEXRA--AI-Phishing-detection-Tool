import qrcode
url = input("enter the url:")
file_path="C:\\python_learning\\QRimage.png"

qr=qrcode.QRCode()
qr.add_data(url)

img=qr.make_image()
img.save(file_path)

print("qr code was generated")
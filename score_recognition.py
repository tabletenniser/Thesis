try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import os

IMAGE='testing/images/frame_00001.png'
output_image='testing/images/frame_cropped.png'
output_image2='testing/images/frame_cropped_clean.png'

# im = Image.open(IMAGE)
im = Image.open(IMAGE).convert('L')
im = im.crop((362, 590, 362+35, 590+28))
# im = im.crop((362, 590, 362+100, 590+100))
im.save(output_image)
cmd = "./textcleaner "+output_image+" "+output_image2
os.system(cmd)
im = Image.open(output_image2).convert('L')

print(pytesseract.image_to_string(im, boxes=True, config='-psm 10 digits'))
# print(pytesseract.image_to_string(im, config='psm=10 digits'))
print(pytesseract.image_to_string(im, config='-psm 10 digits'))

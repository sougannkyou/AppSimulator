from PIL import Image as myImage
import pytesseract


def ocr_to_text(img_path):
    ret = ''
    try:
        img = myImage.open(img_path)
        img.load()
        ret = pytesseract.image_to_string(img, lang='chi_sm').decode('utf8').replace(' ', '')
    except Exception as e:
        print(e)

    return ret


if __name__ == '__main__':
    ocr_to_text('dianping1.png')

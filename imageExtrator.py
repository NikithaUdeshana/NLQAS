import fitz
import base64

from opticalCharacterRecognizer import ocr, ocr_word_count

def image_extractor(filename):
    doc = fitz.open("test files/" + filename)
    image_count = 0
    json_images_list = list()

    for i in range(1, len(doc)):
        image_list = doc.getPageImageList(i)
        page = doc.loadPage(i)
        text = page.getText(output = "text")
        if(text):
            for img in image_list:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                image_count += 1
                image_name = "images/" + filename + "-p" + str(i) + "-" + str(xref) + ".png"
                if pix.colorspace.n < 4:
                    pix.writePNG(image_name)
                    # binary_image = pix.getPNGData()
                else:
                    pix0 = fitz.Pixmap(fitz.csRGB, pix)
                    pix0.writePNG(image_name)
                    # binary_image = pix0.getPNGData()
                # binary_encoded_image = base64.b64encode(binary_image)
                ocr_text = ocr(image_name)
                word_count = ocr_word_count(ocr_text)
                if(word_count>10):
                    json_image = image_to_json(image_name,i, text, ocr_text, word_count)
                    json_images_list.append(json_image)
    print("extracted images", image_count)
    return json_images_list

def image_to_json(image_path, page_num, text, ocr, ocr_word_count):
    image = {
        "image_path": image_path,
        "page_number": page_num,
        "text": text,
        "ocr": ocr,
        "ocr_word_count": ocr_word_count
    }
    return image
from google.cloud import vision

def detect_document(path):
    """Detects document features in an image."""

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    text = ""
    for page in response.full_text_annotation.pages:
        page_text = ""
        for block in page.blocks:
            #print(f"\nBlock confidence: {block.confidence}\n")
            bloc_text = ""
            #print(block)
            for paragraph in block.paragraphs:
                para_text=""
                #print("Paragraph confidence: {}".format(paragraph.confidence))
                
                for word in paragraph.words:
                    word_text = "".join([symbol.text for symbol in word.symbols])
                    para_text+=word_text+" "
                    
                bloc_text+=para_text
            page_text+=bloc_text
        
        text+=page_text
    
    
            

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    
    if text:
        return text

# path = "/home/k/Documents/high.jpeg"
# detect_document(path)
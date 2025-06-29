import aspose.words as aw

doc = aw.Document()
builder = aw.DocumentBuilder(doc)

shape = builder.insert_image("colored_contours5.jpg")
shape.get_shape_renderer().save("output.svg", aw.saving.ImageSaveOptions(aw.SaveFormat.SVG))
# import svgwrite

# def web_font_embedded(name):
#     dwg = svgwrite.Drawing(name+'.svg', (200, 200), debug=False)
#     # font data downloaded from google fonts
#     dwg.embed_google_web_font(name=name, uri='https://fonts.googleapis.com/css2?family=Press+Start+2P')
#     dwg.embed_stylesheet(f"""
#     .customFont {{
#         font-family: "{name}";
#         font-size: 14px;
#     }}
#     """)
#     # This should work stand alone and embedded in a website!
#     paragraph = dwg.add(dwg.g(class_="customFont"))
#     paragraph.add(dwg.text("hello world", insert=(100, 100), text_anchor="middle"))
#     dwg.save()

# # web_font_embedded("Press Start 2P")


# def web_font_lightweight_svg(filename="hello_world"):
#     font_name = "Press Start 2P"
#     font_url = "https://fonts.googleapis.com/css2?family=Press+Start+2P"

#     dwg = svgwrite.Drawing(filename + '.svg', size=("200", "200"), profile="full")

#     # Add style tag with Google Fonts @import (no base64)
#     css = f"""
#     @import url('{font_url}');
#     .customFont {{
#         font-family: '{font_name}';
#         font-size: 14px;
#     }}
#     """
#     dwg.defs.add(dwg.style(css))

#     # Add the text with the style class
#     text_group = dwg.add(dwg.g(class_="customFont"))
#     text_group.add(dwg.text("hello world", insert=("100", "100"), text_anchor="middle"))

#     dwg.save()

# web_font_lightweight_svg()


import subprocess
import svgwrite

# Step 1: Make the text SVG
dwg = svgwrite.Drawing("hello_temp.svg", size=("200", "200"))
dwg.add(dwg.text("Hello World", insert=("100", "100"), font_size=14, text_anchor="middle"))
dwg.save()

# Step 2: Convert to path
subprocess.run([
    "inkscape", "hello_temp.svg",
    "--export-text-to-path",
    "--export-plain-svg=hello_final.svg"
])


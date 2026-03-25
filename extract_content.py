
import zipfile
import xml.etree.ElementTree as ET
import os

def get_text_from_node(node):
    text = ""
    if node.text:
        text += node.text
    for child in node:
        text += get_text_from_node(child)
    if node.tail:
        text += node.tail
    return text

def extract_content(zip_path, folder, file_prefix):
    results = []
    with zipfile.ZipFile(zip_path, 'r') as z:
        files = [f for f in z.namelist() if f.startswith(f"{folder}/{file_prefix}") and f.endswith('.xml')]
        # Sort files
        files.sort()
        for f in files:
            try:
                content = z.read(f)
                root = ET.fromstring(content)
                # Find all tags that might contain text
                # In docx it's <w:t>, in pptx it's <a:t>
                text_elements = root.findall('.//{*}t')
                texts = [el.text for el in text_elements if el.text]
                if texts:
                    results.append(f"--- {f} ---\n" + "\n".join(texts))
            except Exception as e:
                results.append(f"Error reading {f}: {e}")
    return "\n\n".join(results)

print("DOCX CONTENT:")
print(extract_content('Specialized CV_Template (1).docx', 'word', 'document'))
print("\n" + "="*50 + "\n")
print("PPTX CONTENT:")
print(extract_content('Portfolio Creation Lecture 2.pptx', 'ppt/slides', 'slide'))

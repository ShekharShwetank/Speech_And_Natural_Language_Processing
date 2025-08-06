import nbconvert
import os

# Define the notebook file path
notebook_path = r"C:\Users\shwet\OneDrive\Desktop\NLP\BoW_and_N-gram_language.ipynb"

# Create an HTML exporter instance
exporter = nbconvert.HTMLExporter()

# Read the notebook content
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook_content = f.read()

# Process the notebook content
output, resources = exporter.from_filename(notebook_path)

# Define the output file path
output_path = "BoW_and_N-gram_language.html"

# Write the output to the HTML file
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(output)

print(f"Notebook converted to HTML: {output_path}")
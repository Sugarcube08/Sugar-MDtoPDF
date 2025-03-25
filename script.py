import markdown
import os
import pdfkit
import shutil
def convert_md_to_html(md_content):
    """
    Convert Markdown content to HTML.
    
    Args:
        md_content (str): The Markdown content to convert.
        
    Returns:
        str: The converted HTML content.
    """
    html_content = markdown.markdown(md_content, extensions = [
        'fenced_code',
        'tables',
        'toc',
        'codehilite',
        'extra',
        'sane_lists',
        'smarty',
        'meta',
        'nl2br',
        'admonition'
    ])
    return html_content

def template(css_content, html_output):
   return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Converted Markdown</title>
        <style>
        {css_content}
        </style>
    </head>
    <body>
        {html_output}
    </body>
    </html>
    """

def openfile(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        return content

def out_file(content, output_path):
    with open(output_path, "w") as file:
        file.write(content)

def single_file_mode():
    md_text = input("Enter File Path: ")
    md_content = openfile(md_text)
    print("Markdown content read from file:")
    print(md_content)  
        
    html_output = convert_md_to_html(md_content)
    print("Converted HTML content:")
    print(html_output)  
 
    css_content = openfile("styles.css")
    
    html_template = template(css_content, html_output)
    
    temp_dir = "./temp"
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    else:
        temp_dir = "./temp"
    html_path = os.path.join(temp_dir, "output.html")
    
    out_file(html_template, html_path)
    print(f"HTML file created at: {html_path}")
    
    pdf_path = os.path.join(os.path.dirname(md_text), "output.pdf")
    pdfkit.from_file(html_path, pdf_path)
    print(f"PDF file created at: {pdf_path}")
    
    shutil.rmtree(temp_dir)
    print(f"Temporary directory {temp_dir} removed")

def bulk_file_mode():
    folder_path = input("Enter Folder Path: ")
    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            md_file_path = os.path.join(folder_path, filename)
            md_content = openfile(md_file_path)
            print(f"Markdown content read from file: {md_file_path}")
            print(md_content)
            
            html_output = convert_md_to_html(md_content)
            print("Converted HTML content:")
            print(html_output)
            
            css_content = openfile("styles.css")    
            
            html_template = template(css_content, html_output)
            
            temp_dir = "./temp"
            if not os.path.exists(temp_dir):
                os.mkdir(temp_dir)
            html_path = os.path.join(temp_dir, f"{filename[:-3]}.html")  
                        
            out_file(html_template, html_path)
            print(f"HTML file created at: {html_path}")
            
            pdf_path = os.path.join(folder_path, f"{filename[:-3]}.pdf")  
            pdfkit.from_file(html_path, pdf_path)
            print(f"PDF file created at: {pdf_path}")
    
    shutil.rmtree(temp_dir)
    print(f"Temporary directory {temp_dir} removed")

if __name__ == "__main__":
    print("Welcome to the SugarCube's Markdown to PDF converter\n")
    print("1. Single File Mode")
    print("2. Bulk File Mode")
    print("0. Exit")
    choice = input("Enter your choice (1 or 2): ")
    while True:
        if choice == "1":
            single_file_mode()
            break
        elif choice == "2":
            bulk_file_mode()
            break
        else:
            print("Exiting...")
            break 

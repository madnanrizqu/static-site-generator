from markdown_to_blocks import markdown_to_html_node
import os

def extract_title(markdown: str) -> str:
    if "# " not in markdown:
        raise Exception("h1 does not exist in the markdown")

    line_of_h_one = ""
    count = 0
    for line in markdown.split("\n"):
        if line.startswith("# ") and count == 0:
            line_of_h_one = line
            count += 1
        elif line.startswith("# ") and count > 0:
            raise Exception("multiple h1 not allowed")

    return line_of_h_one.lstrip("# ").strip()


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_content = ""
    with open(from_path, "r") as file:
        from_content = file.read()

    content = ""
    with open(template_path, "r") as file:
        content = file.read()

    html_string = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)

    content = content.replace("{{ Title }}", title)
    content = content.replace("{{ Content }}", html_string)
    
    with open(dest_path.replace(".md", ".html"), "w") as file:
        file.write(content)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    for child in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, child)
        dest_path = os.path.join(dest_dir_path, child)

        if os.path.isdir(from_path):
            print("[generate_pages_recursive] detected a dir, calling function for: ", from_path)
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            generate_pages_recursive(from_path, template_path, dest_path)
        else:
            print("[generate_pages_recursive] detected a file, generating page for: ", from_path)
            generate_page(from_path, template_path, dest_path)
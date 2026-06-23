from markdown_to_blocks import markdown_to_html_node


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

    with open(dest_path, "w") as file:
        file.write(content)

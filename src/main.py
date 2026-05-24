import textnode as tn


def main():
    node = tn.TextNode(
        "This is some anchor text", tn.TextType.LINK, "https://www.boot.dev"
    )
    print(node)


if __name__ == "__main__":
    main()

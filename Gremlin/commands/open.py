import webbrowser
import sys

def open_url_in_browser():
    # Split the command-line arguments into parts
    parts = sys.argv[1:]

    # Process each part to replace 'dot' with '.', and assume 'com' if no TLD is found
    url_parts = []
    for part in parts:
        if part == "dot":
            url_parts.append(".")
        else:
            url_parts.append(part)

    # Join the parts to form the raw URL
    raw_url = "".join(url_parts)

    # Check if a top-level domain is present; if not, append '.com'
    if "." not in raw_url:
        raw_url += ".com"

    # Add 'http://' if no protocol is specified
    if not raw_url.startswith(("http://", "https://")):
        raw_url = "http://" + raw_url

    # Open the URL in the default browser
    webbrowser.open(raw_url)
    print(f"Opening {raw_url}")

if __name__ == "__main__":
    open_url_in_browser()

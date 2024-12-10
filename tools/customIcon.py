
# https://stackoverflow.com/questions/70520191/how-to-add-the-google-analytics-tag-to-website-developed-with-streamlit/78992559#78992559
# Customize the built-in index.html page in the Streamlite app
import os
import streamlit
import logging
from sys import stdout

logging.basicConfig(level=logging.DEBUG, stream=stdout)
log = logging.getLogger(__name__)  # setup a logger for some sanity

# Get the path to the streamlit package
streamlit_package_dir = os.path.dirname(streamlit.__file__)

log.debug(f"streamlit package dir: {streamlit_package_dir}")

index_path = os.path.join(streamlit_package_dir, "static", "index.html")

# head content file in the same directory as this script
head_content_path = os.path.join(os.path.dirname(__file__), "head.html")


def _customize_index_html():
    with open(index_path, "r") as f:
        index_html = f.read()

    with open(head_content_path, "r") as f:
        head_content = f.read()

    # Add the custom content to the head
    index_html = index_html.replace("</head>", f"{head_content}</head>")

    # Replace the <title> tag
    index_html = index_html.replace(
        "<title>Streamlit</title>", "<title>Savantly is cool</title>"
    )

    with open(index_path, "w") as f:
        f.write(index_html)

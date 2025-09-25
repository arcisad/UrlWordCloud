# This is a sample Python script.

import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_gradient_magnitude
import configargparse

parser = configargparse.Parser()
parser.add("--url", type=str, required=True, help="Path to url")
parser.add("--image-file", type=str, required=True, help="Path to image file")
parser.add("--output-file", type=str, required=True, help="Path to output file")
parser.add(
    "--max-words",
    type=int,
    required=False,
    help="Maximum number of words in the word cloud",
    default=500,
)
parser.add(
    "--max-font-size",
    type=int,
    required=False,
    help="Maximum font size for the word cloud",
    default=40,
)

if __name__ == "__main__":
    args = parser.parse_args()
    url = args.url
    image_file = args.image_file
    output_file = args.output_file
    max_words = args.max_words
    max_font_size = args.max_font_size

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "1800",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    }

    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, "lxml")

    text = " ".join(soup.get_text().split())

    color = np.array(Image.open(image_file))

    # create mask  white is "masked out"
    mask = color.copy()
    mask[mask.sum(axis=2) == 0] = 255

    # some finesse: we enforce boundaries between colors so they get less washed out.
    # For that we do some edge detection in the image
    edges = np.mean(
        [gaussian_gradient_magnitude(color[:, :, i] / 255.0, 2) for i in range(3)],
        axis=0,
    )
    mask[edges > 0.08] = 255

    # create word-cloud. A bit sluggish, you can subsample more strongly for quicker rendering
    # relative_scaling=0 means the frequencies in the data are reflected less
    # accurately but it makes a better picture
    wc = WordCloud(
        max_words=max_words,
        mask=mask,
        max_font_size=max_font_size,
        random_state=42,
        relative_scaling=0,
    )

    # generate word cloud
    wc.generate(text)

    # create coloring from image
    image_colors = ImageColorGenerator(color)
    wc.recolor(color_func=image_colors)
    wc.to_file(output_file)

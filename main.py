# This is a sample Python script.

import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud,  ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_gradient_magnitude
import configargparse

parser = configargparse.Parser()
parser.add(
    "--url",
    type=str,
    required=True,
    help="Path to url"
)
parser.add(
    "--image-file",
    type=str,
    required=True,
    help="Path to image file"
)

if __name__ == '__main__':
    args = parser.parse_args()
    url = args.url
    image_file = args.image_file

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'lxml')

    text = " ".join(soup.get_text().split())

    color = np.array(Image.open(image_file))
    color = color[::3, ::3]

    # create mask  white is "masked out"
    mask = color.copy()
    mask[mask.sum(axis=2) == 0] = 255

    # some finesse: we enforce boundaries between colors so they get less washed out.
    # For that we do some edge detection in the image
    edges = np.mean([gaussian_gradient_magnitude(color[:, :, i] / 255., 2) for i in range(3)], axis=0)
    mask[edges > .08] = 255

    # create word-cloud. A bit sluggish, you can subsample more strongly for quicker rendering
    # relative_scaling=0 means the frequencies in the data are reflected less
    # accurately but it makes a better picture
    wc = WordCloud(max_words=2000, mask=mask, max_font_size=40, random_state=42, relative_scaling=0)

    # generate word cloud
    wc.generate(text)
    plt.imshow(wc)

    # create coloring from image
    image_colors = ImageColorGenerator(color)
    wc.recolor(color_func=image_colors)
    plt.figure(figsize=(10, 10))
    plt.imshow(wc, interpolation="bilinear")
    wc.to_file("fugro.png")

    plt.axis("off")
    plt.show()

    # for link in soup.find_all('a'):
    #     print(link.get('href'))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

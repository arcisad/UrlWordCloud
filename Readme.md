This is a small code that scrapes a website at given url and 
creates a word cloud using its contents and an input image as a template.

**Input Args:**

`--url`: url to website

`--image-file`: image to be used as template for the word cloud

`--output-file`: path to the generated output word cloud file

`--max-words`: maximum number of words uses in the word cloud, default = 500

`--max-font-size`: maximum font size used in the word cloud, default = 40


## Prerequisites

Clone the repo by running `git clone https://github.com/arcisad/UrlWordCloud.git`. Open terminal and cd the local downloaded directory. 

run `pip install -r requirements.txt` to install the required package.

Use the provided usage line below to run the code.


## usage

```python main.py --url <url> --image-file <path_to_image_file> --output-file <path_to_output_file> --max-words <max_num_words> --max-font-size <max_font_size>```

#### Example

```python main.py --url <antarctic_related_url> --image-file test_input/antarctica.jpg --output-file an_wordcloud.jpg --max-words 100 --max-font-size 50```


**Note:** The output wordcloud image will have the same resolution of the input image.

**Note:** **YOU** are responsible for any copyright, protection, access, licencing, etc... attached to the used urls as your inputs to this code and their contents.


## Generating tweets programmatically

This document implements a python program to generate conjoint
image-based tweets programatically and at scale. The code is inspired in
two main sources with similar implementation.

-   This medium post
    [here](https://medium.com/analytics-vidhya/how-to-create-twitter-screenshots-with-python-c142ef71fda7)
    describing how to generate tweets’ screenshots in Python.

-   And Alessandro Vecchiato
    [implementation](https://github.com/avecchiato/Introducing_Visual_Conjoints)
    of visual conjoints for Twitter profiles.

This is a work in progress and part of my ongoing collaboration with
Kevin Munger (Penn State), Katherine McCabe (Rutger University) and
Keng-Chi Chang (UCSD). Keng-Chi Chang made invaluable contributtions to
this code.

## Setup

## Calling packages

``` python
# import packages
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
import os
import re
import datetime
from numpy import asarray
```

## Python function to write the tweets and quote tweets

We wrote a python function that allows researcher to create tweets and
quote tweets given a set of inputs. The function has the following
parameters:

-   `CreateTweet()`: Create tweet using parameters.
-   Parameters:
    -   `author_avatar` (str): avatar of author
    -   `author_name` (str): name of author
    -   `author_tag` (str): twitter username/handle of author
    -   `text` (str): main text of tweet
    -   `reactions_retweet` (str): number of reactions of tweet
    -   `reactions_quote` (str): number of quotes of tweet
    -   `reactions_like` (str): number of likes of tweet
    -   `time` (str/NULL/None): time of tweet in format “2022-07-05
        14:34”; if None use current time
    -   `quote` (TRUE/FALSE): whether or not to print quoted tweet
    -   `quote_author_avatar` (str): avatar of author of quoted tweet
    -   `quote_author_name` (str): name of author of quoted tweet
    -   `quote_author_tag` (str): twitter username/handle of author of
        quoted tweet
    -   `quote_text` (str): text of quoted tweet
-   Returns:
    -   image: Twitter image in PIL Image format

You can get access to the function on this repository. The logic of the
function is to split the tweet in many parts, and combine their
positions at the end. These components can all be rotated in a conjoint
experiment.

## CreateTweet

A simple example using the CreateTweet.

``` python
from conjoint_tweets import CreateTweet
tweet = CreateTweet()
print(tweet)
```

    ## <PIL.Image.Image image mode=RGB size=1050x475 at 0x7FB0C0914190>


    ## QuoteTweet

    To generate a quote tweet, you just need to add quote=true


    ```python
    qt = CreateTweet(quote=True)
    print(qt)

    ## <PIL.Image.Image image mode=RGB size=1050x645 at 0x7FB0C0914760>

<!-- ## Rotating to generate the conjoints

Finally, we just need to write a nested loop to iterate over several parameters-->
<!-- See an example below -->
<!-- Done! From here you just need to upload those in your survey and run the experiments. In future iterations of this code, I hope to show how to easily connect these images with Qualtrics -->
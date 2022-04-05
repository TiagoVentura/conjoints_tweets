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
Keng-Chi Chang (UCSD)

## Setup

To run this code, you need to have two main files. First, a background
to build the tweets and images saved in a local folder. Some examples
are provided in this repository.

## Calling packages

``` python
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
import os
import re
```

## Python function to write the tweets

``` python
def create_tweet(empty_background, avatar, name, tag, text, reactions,output):

  #Generating empty Twitter profile.
  img = Image.open(empty_background).convert('RGB')
  # Image
  # solution: pass all profile umage through twitter, and get all with the dimensions
  avatar = Image.open(avatar) 
  avatar = avatar.resize((140, 120))
  img.paste(avatar, (25, 30))
  # name
  draw = ImageDraw.Draw(img)
  draw.text(author_name_position,name,(0,0,0),font=font_name)
  #tag
  draw.text(author_tag_position,tag,font=font_tag, fill = "#667786")
  # text
  x, y = text_position
  text_string_lines = wrap(text, 52)
  for index, line in enumerate(text_string_lines): # get the index and the text
      draw.text((x, y), line, font=font_text, fill=(0, 0, 0)) 
      y +=  50
  # reactions
  # draw
  draw.text(rt_pos, reactions[0], font=font_react, fill=(0, 0, 0)) 
  draw.text(qt_pos, reactions[1], font=font_react, fill=(0, 0, 0)) 
  draw.text(rp_pos, reactions[2], font=font_react, fill=(0, 0, 0)) 
  img.save(output, quality=95)
```

## Define basic parameters

This is the core of the code. To find those positions it is a bit of a
guessing game. So I downloaded a background tweet and went on testing
the correct positions

``` python
# BASIC PARAMETERS
# positions  
author_name_position = (150, 40)
author_tag_position = (150, 95)
text_position = (60, 160)
reactions_pos = (110, 600)

# reactions 3 dig
rt_pos = (65, 510) # 3 dig
qt_pos = (270, 512) # 3 dig
rp_pos = (580, 512) # 3 dig

# reaction 1 dig
#rt_pos = (100, 510) # 3 dig
#qt_pos = (300, 512) # 3 dig
#rp_pos = (590, 512) # 3 dig
  
# fonts
font_name = ImageFont.truetype("HelveticaNeue.ttc", size=35, index = 1)
font_tag = ImageFont.truetype("HelveticaNeue.ttc", size=25, index=1)
font_text = ImageFont.truetype("HelveticaNeue.ttc", size=38, index=0)
font_react = ImageFont.truetype("HelveticaNeue.ttc", size=30, index=1)
rt_pos = (65, 510) # 3 dig
qt_pos = (265, 512) # 3 dig
rp_pos = (550, 512) # 3 dig
```

Finally, we just need to write a nesterd loop to iterate over several
parameters

``` python
empty_background= ["empty_tweet.png"]
avatars = ["woman_clean.png", "woman2_clean.png", "woman3_clean.png"]
names = ["Tiago", "Katie", "KC", "Katie"]
tags = ["@Tiago", "@Katie", "@KC", "@Katie"]
texts = ["This is just a long and random tweet to test the code to generate conjoints tweets on the fly. This is gonna be great! It looks better longer the text is", 
"This is just a SECOND long and random tweet to test the code to generate conjoints tweets on the fly. This is gonna be great! It looks better longer the text is"]
reactions = [["100","300", "20k"],["    1", "     5", "     6"]]


for a, back in enumerate(empty_background):
  for b, avatar in enumerate(avatars):
    for c, name in enumerate(names):
      for d, tag in enumerate(tags):
        for e, text in enumerate(texts):
          for f, reaction in enumerate(reactions):
            # create name to save
            output= "a_" + str(a) + "_" + "b_" + str(b) + "_" + "c_" + str(c) + "_" + "d_" + \
            str(d) + "_" + "e_" + str(e) + "_" + "f_" + str(f)
            output_to_save = "output/" + str(output) + ".png"
            #gen the tweet
            create_tweet(empty_background=back, 
                         avatar=avatar, 
                         name=name, 
                         tag=tag, 
                         text=text, 
                         reactions=reaction, 
                         output=output_to_save)                         
            
```

See an example below

``` r
knitr::include_graphics("output/a_0_b_2_c_0_d_3_e_0_f_1.png")
```

<img src="output/a_0_b_2_c_0_d_3_e_0_f_1.png" width="1050" />

Done! From here you just need to upload those in your survey and run the
experiments. In future iterations of this code, I hope to show how to
easily connect these images with Qualtrics
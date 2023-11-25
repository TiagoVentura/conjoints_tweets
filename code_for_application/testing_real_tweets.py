# generate tweets for experiment
import pandas as pd
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
import os
import re
import datetime
from numpy import asarray
import numpy as np
from conjoint_tweets import *
pd.set_option('display.max_columns', 0) # Display any number of columns

# text Feature --------------------------------------------------------------------------------------------------------------------------
texts = pd.read_csv("input/text.csv", index_col=None)


# Reaction feature ------------------------------------------------------------------------------------------------------------------------------------------------

types = ["low", "low", "low", "medium", "medium", "medium", "high", "high", "high"]

# retweet
reactions_retweet = np.concatenate((np.random.randint(0, 5, size=3), 
                                    np.random.randint(50,99, size=3),  
                                    np.random.randint(100,1200, size=3))).astype(str)
reactions_retweet = pd.DataFrame(list(zip(reactions_retweet, types)),columns=['retweet', 'type'])

# quote
reactions_quote = np.concatenate((np.random.randint(0, 5, size=3), np.random.randint(20,50, size=3),  np.random.randint(150,300, size=3))).astype(str)
reactions_quote = pd.DataFrame(list(zip(reactions_quote, types)),columns=['quotes', 'type'])

# likes
reactions_like = np.concatenate((np.random.randint(10, 50, size=3), np.random.randint(100,300, size=3),  np.random.randint(2532,3500, size=3))).astype(str)
reactions_like = pd.DataFrame(list(zip(reactions_like, types)),columns=['likes', 'type'])



# merge all.
reactions = reactions_retweet.merge(reactions_like, how="left").merge(reactions_quote, how="left")[["retweet", "likes", "quotes", "type"]]

# Images  --------------------------------------------------------------------------------------------
import glob
all_files = glob.glob("input/dalle/unprof/*/*", recursive=True)

# capture names
files_list = [file for file in all_files if not os.path.isdir(file)]

# sort
files_list.sort()

# separate
profiles_rows =[f.split("/") for f in files_list]

# list images
list_images = [element for p in profiles_rows for element in p if "png" in element]

# clean
import re
result = [re.sub(r'-image_\d+.png', '', el).split("-") for el in list_images]

# convert to dataframe
dprof = pd.DataFrame(result, columns=["gender", "race"])
dprof["att"] = "unprof"
dprof["path"]= files_list

# prof
all_files = glob.glob("input/dalle/prof/*/*", recursive=True)

files_list = [file for file in all_files if not os.path.isdir(file)]

# sort
files_list.sort()

# separate
profiles_rows =[f.split("/") for f in files_list]

# list images
list_images = [element for p in profiles_rows for element in p if "png" in element]

# clean
import re
result = [re.sub(r'-image_\d+.png', '', el).split("-") for el in list_images]
# convert to datafram
dprof_ = pd.DataFrame(result, columns=["gender", "race"])
dprof_["att"] = "prof"
dprof_["path"]= files_list

# combine list
dprof = pd.concat([dprof, dprof_])

# Convert race and gender to lowercase
dprof['race'] = dprof['race'].str.lower()
dprof['gender'] = dprof['gender'].str.lower()

# Profiles ------------------------------------------------------------------------

# Select columns and remove 'attractiveness'
profiles = pd.read_csv("input/profiles.csv")

# remove
profiles = profiles.drop('professionalism', axis=1)

# Remove duplicates
profiles = profiles.drop_duplicates()

# Pivot longer
profiles = pd.melt(profiles, id_vars=['gender', 'race'], var_name='profile_type', value_name='names')

# Convert race to lowercase
profiles['race'] = profiles['race'].str.lower()

# Add tag column
profiles['tag'] = profiles['names'].str.replace(" ", "").apply(lambda x: '@' + x)

# fix text issue
texts["issue"] = texts['Issue'].str.replace(' ', '_', regex=True)

# rename lean
texts["lean"] = texts['Ideological Lean']
texts["revised_text"] = texts["Revised Text"]

# function to generate a dataframe with all the combination ------------------------------------------------------------------------

def create_df_profiles(df_profile,author_profile,  df_text, df_reactions):  
  """
  function to generate a data frame with the profiles
    :param
      df_profile: a dataframe with the profile and names of the authros
      gender: a string with the corresponding gender to build the tweets
      race: a string with the corresponding race to build the tweets
      author_profile: dataframe with the corresponding attractiveness and the avatar for each profile
      df_text: dataframe with the texts of the tweet, and the categories for issue, salience, and political leaning
      df_reactions: a dataframe with the reactions
  """
  # create a list of profiles
  list_profiles=[]

  # iteration
  
  # start with gender and race grouped 
  for name, group in df_profile.groupby(['gender', 'race']):
    # get corresponding author's gender and race
    gender, race = name
    att_df_temp = author_profile[(author_profile["gender"]==gender) & (author_profile["race"]==race)]
    # iterate over the attractiveness feature
    for av_, row in att_df_temp.groupby("att"):
      #save attributed
      att =av_
      print("iteration over ",  att)
      for profile_type, df_profile_type in group.groupby("profile_type"):
        # save profile_type
        profile=profile_type
        print("iterating over", profile)
        for b, text in df_text.groupby(["issue", "lean"]):
          # save issue
          issue = b[0]
          #save political leaning
          lean=b[1]
          print("iterating over", issue, lean)
          for c, reaction in df_reactions.groupby("type"):
            reaction_type=c
            
            # get path image
            profile_sample= row[["path"]].sample(n=1)
            path_= profile_sample["path"].to_list()[0]
 
            
            # get a sample for names
            name_sample= df_profile_type[["names", "tag"]].sample(n=1)
            name = name_sample["names"].to_list()[0]
            tag = name_sample["tag"].to_list()[0]


            # get a sample of the text
            text_sample= text[["revised_text"]].sample(n=1)
            text_ = text_sample["revised_text"].to_list()[0]
            #issue = text_sample["issue"].to_list()[0]
              
            # grab a random row of the reactions dataset
            reaction_ = reaction.sample(n=1)

            retweet_= reaction_["retweet"].to_list()[0]

            quote_ = reaction_["quotes"].to_list()[0]

            like_ = reaction_["likes"].to_list()[0]

            # to save
            id_tweet = [gender, 
                    race, 
                    profile,
                    att, 
                    issue, 
                    lean,
                    "reaction" + reaction_type]
                
            output= '_'.join(id_tweet) + ".png"
                  
            # dictionary
            profile_dict = {"p_gender":gender,
                                "p_race":race, 
                                "p_att":att,
                                "path": path_,
                                "p_profile":profile, 
                                "author_name":name, 
                                "author_tag":tag, 
                                "text":text_,
                                "p_issue":issue, 
                                "p_lean":lean,
                                "p_retweet":reaction_type,
                                "retweet":retweet_,
                                "quote":quote_,
                                "like":like_,
                                "p_output":output,
                                "time":"2022-07-05 14:34"}
                  
            # Append
            list_profiles.append(profile_dict)
  
  return(list_profiles)


# rotate over profiles
df_profiles = create_df_profiles(profiles, dprof, texts,reactions)

# generate df
df = pd.DataFrame(df_profiles)

# save
df.to_csv("output/profiles_conjoints.csv")


# retrive unique
len(df[df.columns[0]].unique()) # 2 gender
len(df[df.columns[1]].unique()) # 4 race
len(df[df.columns[2]].unique()) # 2 attrac
len(df[df.columns[4]].unique()) # 4 profile
len(df[df.columns[8]].unique()) # 8 issue
len(df[df.columns[9]].unique()) # 2 lean
len(df[df.columns[10]].unique()) # 3 reactios

df[df.columns[4]].unique()

# total combinations
2*4*2*4*8*2*3==df.shape[0]

#unique images
df["p_output"].value_counts()

# generate the tweets
df["tweet"] = df.apply(lambda row: CreateTweet(author_avatar=row["path"], 
                   author_name=row["author_name"],
                   author_tag=row["author_tag"],
                   text=row["text"],
                   reactions_retweet=str(row["retweet"]),
                   reactions_quote=str(row["quote"]),
                   reactions_like=str(row["like"]),
                   time="2023-07-05 14:34"),
                   axis=1)


df["p_output"]

# save
df.apply(lambda row: SaveTweet(row["tweet"], 
                          "./output/images_to_github/" + row["p_output"], quality=95), 
                          axis=1)

# covert to send for the api
df['p_issue'] = df['p_issue'].str.lower()

df["p_issue"].unique()

# Using replace function to replace certain values
df['p_issue'] = df['p_issue'].replace({
    "ban_birthright_citizenship_for_children_of_illegal_immigrants": "ban_imm",
    "mandating_child_vaccinations": "child_vax",
    "privatize_social_security": "social_sec"
})

# writing csv
df[["p_issue", "p_output"]].to_csv("list_images.csv", index=False)


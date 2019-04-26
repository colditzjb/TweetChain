# TweetChain

A quick Python script that takes longform text and breaks it into a chain of tweet-size text (i.e., >280 characters). It optimizes to preserve sentences within individual tweets and maintains links or hashtags with the preceeding text content. There is a built-in counter (i.e., 1 of _n_ tweets) that is aware of the total number of tweets in the chain. Hashtags can also be set to be included for each tweet the overall tweet chain.

Use: Change "dirin" and "textin" variables to point to a plaintext file. Output is printed to terminal, so if you're running in BASH, you can `>` the output wherever you like. This is primarily intended as base code for basic automation purposes (e.g., Twitter bots creating tweet chains), but the larger code framework would need to be aware of resulting Tweet IDs and respond to those tweets in a chain if the output is intended to look like a "natural" (i.e., Twitter native) tweet chain. 

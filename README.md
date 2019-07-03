# A beer recommendation system

As anyone who hasn't been living under a rock has realized, there has been a
tremendous proliferation of craft beers recently. But, who has the time (or
money) to try these beers and find ones that you like?

Well, don't worry. This application will help you find beers that you should try!

# The basic idea

If you know a beer that you like (or even a description of the kind of beer you like),
you can submit that information. The app will analyze the text you've given it and
recommend a few beers that are similar to what you've described!

# But how does it work?

## Latent Semantic Analysis

This project depends on the [semantic hypothesis](https://en.wikipedia.org/wiki/Distributional_semantics),
which states (roughly) that the meaning of a word can be determined by analyzing the statistical
patterns of that word's usage.

So, given some statistical information about the words used to describe beer, this application
can group beers into categories--like the way we already group beers into styles--based on the words
used to describe those beers.

## What statistical patterns?

For this project, I chose to use TF-IDF
([Term Frequency-Inverse Document Frequency](https://en.wikipedia.org/wiki/Tf%E2%80%93idf))
to transform raw text into a format that a computer can analyze. TF-IDF is simply a number
that increases as a word is used in a document and decreases as the word appears in a larger portion of documents.

I chose this metric because it retains information about the importance of a word to a particular document--measured
by the term frequency--while reducing the value when a word is too common to give us much information.

## But what documents?

I scraped about 700,000 beer reviews for about 9,000 beers.

## And you turned them into numbers, right?

Yep! Recall that I have to transform all of the reviews into a format that a computer can process. For that purpose,
I've chosen to use TF-IDF. So, I transform all the documents into a list of TF-IDF numbers and stack each of these
lists on top of one another to form a matrix. It might look something like this:

[0, 1, 4, 8, 7]
[7, 5, 8, 9, 5]
[9, 5, 0, 1, 1]

Here each row represents one of the reviews, and each column represents the TF-IDF value associated with a single word.

## What do you do with that matrix?

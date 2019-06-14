# Proposals for Capstone #2

## Golf Performance Prediction

### The project
Build a model that predicts a golfer's score relative to par at some course.

### My approach
I will attempt to build a simple model first which will attempt to predict a
golfer's score using only a few features. I will start by using average
driving distance and the total length of a course. I will test the following:

> $H_A$: Average Driving Distance / Total Yardage positively affects scoring.

That is to say, as a golfer hits their drives further relative to the total
course distance, his or her score decreases (and, thus, improves).

Once this basic model is complete, I will attempt improve the model by
engineering and adding more features to the model. Further, currently,
I consider this a problem of regression. However, it may be more useful to
think of the output as a qualitative response. For example, does a golfer finish
in the top 10 of a tournament?

### User interaction
I will build a website using Flask where users can input characteristics of a
golfer and characteristics about a course, and the website will return a
prediction of that golfers score.

### Data sources
I will use the yearly data collected from the PGA Tour's
[website](https://www.pgatour.com/stats.html).

I need to find a website that has detailed course data for various PGA events,
along with the players' performance.

## Social Media and Sports Prediction

### The project
Build a model that predicts a whether a team will win or lose based on the
social media activity about the teams.

### My approach
I will start by attempting a very simple model which takes in the volume
social media activity about the teams and attempts to predict which team
will be victorious. So, testing the following hypothesis will be useful:

> $H_A$: The probability that a team wins given difference between the number
> of tweets about it and it's opponent is different than the probability of
> that team winning.

In other words, if we know something about the social media activity about a
team, we can better estimate its probability of winning.

In order to make this project manageable, I'll use the data about the San
Diego Padres and the Los Angeles Dodgers for the last five years.

From there, I'll attempt to improve the model through intelligent feature
engineering.

### User interaction
I'm not sure what the best model for user interaction will be at this point.

### Data sources
I will gather data using the Twitter API to represent social media activity.
I will gather statistics on competitions using the data from a major sports
association.

## Beer Rating and Trading

### The project
Build a model using data from [Beeradvocate](https://www.beeradvocate.com/)
that is infers the characteristics of a beer that affect its rating. Further,
attempt to develop a recommender system for craft beers.

### My approach

### User interaction

### Data sources
[Beeradvocate](https://www.beeradvocate.com/) has a large number of data on
craft beers.

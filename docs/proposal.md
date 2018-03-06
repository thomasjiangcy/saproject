# Proposal

## SG Travel Planner

This project aims to use data retrieved from Foursquare's API to build and recommend travel itineraries based on user preferences

## Overview

The user will be required to provide several details as input to the recommendation engine:

* Number of days in Singapore (1 day = 16 hours)
* Preferences (Min. 5, the more the better)
* Instead of preferences, we could also ask the user to type a few words to describe what they are looking for instead.
* Where they will be staying (the closest Venue to the accomodation will be selected as the starting point)

The engine will sieve out places of interest and F&B outlets (collectively known as Venues) based on various metrics such as a sentiment analysis of comments, as well as proximity between locations (Shortest Path Problem between each location).


## Proposed Steps

1. Use LDA model to retrieve a list of Venues
2. Sort the Venues based on their sentiment (retrieved from comments)
3. Determine a starting point by choosing the Venue from the shortlist in step 3, that is closest to the user's accomodation
4. Construct possible combinations and find the combination with the most balanced mix of topics. Construction should factor in sentiment, duration spent at each place and traveling time.

Note: We will be setting an arbitrary constant to both duration spent at each place and the traveling speed of the user.

## Data

The tables below represent the essential data we will be working with:

1. Venue

| Unique ID                | Name         | Description         | Rating | Lat               | Long               | Thumbnail             |
| ------------------------ | ------------ | ------------------- | ------ | ----------------- | ------------------ | --------------------- |
| 412d2800f964a520df0c1fe3 | Central Park | Some description... | 9.8    | 40.78408342593807 | -73.96485328674316 | someurl/thumbnail.jpg |

2. Tip (Comments)

| ID                        | Venue ID                 | Tip     |
| ------------------------- | -------------------------| ------- |
| 55a1d6c9498e0dac817317cf  | 412d2800f964a520df0c1fe3 | A true lower east side spectacle with a retractable rooftop and dance floor in the basement. Come here for the nights you won't remember with the friends you won't forget! |

3. Sentiment Analysis

| ID | Tip ID                   | Compound Score | Positive | Neutral | Negative |
| -- | ------------------------ | -------------- | -------- | ------- | -------- |
| 1  | 55a1d6c9498e0dac817317cf | 0.983112       | 0.999999 | 0.6523  | 0.100232 |


## Methodology

The following section describes the pre-processing required to allow for each step.

**1. LDA Model**

Use LDA to model the topics (we will set `n` as the arbitrary number of topics) and the composition of topics of each Venue. Topics here refer to meaningful labels/tags of each Venue.

Analyze topics and give them appropriate labels.

Each document will be a compilation of the Venue's name, description and tips.

When a user provides Preferences, we can take the preferences as a single document and classify it with the LDA model.

The LDA model can be saved with Python's `pickle` module and reused when necessary.

Retrieve all Venues that fall into the topics of which the Preferences document consists of.

**2. Sort By Popularity**

Sort by compound sentiment score in descending order

**3. Determine Starting Point**

Out of the sorted list, find the Venue that is closest to the user's starting point and set that as the root node. Distances will be calculated using the [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula).

**3. Find Shortest Paths**

Shortest path from point to point. Path weights can be determined by using the [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula), taking into account sentiment, time spent at each location and traveling speed.

Construct various combinations of paths from the root node and find the combination with the best mix of topics.
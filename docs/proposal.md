# Proposal

## SG Travel Planner

This project aims to use data retrieved from Foursquare's API to build and recommend travel itineraries based on user preferences

## Overview

The user will be required to provide several details as input to the recommendation engine:

* Number of days in Singapore (1 day = 16 hours)
* Preferences (Min. 5, the more the better)
* Instead of preferences, we could also ask the user to type a few words to describe what they are looking for instead?
* Where they will be staying (the closest Venue to the accomodation will be selected as the starting point)

The engine will sieve out places of interest and F&B outlets (collectively known as Venues) based on various metrics such as ratings, sentiment analysis of comments, as well as proximity between locations (Shortest Path Problem between each location).


## Proposed Steps

1. Use LDA model to retrieve a list of Venues
2. Sort the Venues based on their ratings/sentiment (retrieved from comments)
3. Construct a list of Venues based on geographical proximity
4. Check mix of topics - rerun step 3 if necessary (up to `x` amount of retries)

## Data

The tables below represent the essential data we will be working with:

1. Venues

| Unique ID                | Venue        | Description         | Rating | Lat               | Long               |
| ------------------------ | ------------ | ------------------- | ------ | ----------------- | ------------------ |
| 412d2800f964a520df0c1fe3 | Central Park | Some description... | 9.8    | 40.78408342593807 | -73.96485328674316 |

2. Tips

| Venue ID                 | Tip     |
| -------------------------| ------- |
| 412d2800f964a520df0c1fe3 | A true lower east side spectacle with a retractable rooftop and dance floor in the basement. Come here for the nights you won't remember with the friends you won't forget! |

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

**3. Find Shortest Paths**

Shortest path from point to point. Path weights can be determined by using the [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula) for lat/long coordinates. We must also factor in the time taken to travel as well as the time spent at each Venue.

We will set these as arbitrary constants sufficient for this demonstration.
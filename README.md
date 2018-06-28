# Rocket-League-Scraping

This file captures proposed trades from the Rocket League trading forum for research and speculation purposes.

There are two main files: ScrapeWantsHaves and ScrapeTrades.

ScrapeWantsHaves tracks the count of requests for each item and offers including each item. This data is taken at time intervals and stored in a csv as a time series.
There is also a price tracker in this file, which pulls from a notable price website. Since this is a barter economy, pricing is an interesting science, and I find the absence of methods by this website dubious. I would like to estimate their accuracy some day.

ScrapteTrades creates a time series of all proposed trades as they are posted. One file tracks each offer's "wants," and the other file tracks the respective "haves."

Problems:
The trades posted are often not accurate to the actual desires. For example, the "Have" might be a black market decal, and the "Want" might be seven separate items of equal value, where an additional comment by the poster clarifies he only wants any one of the seven items for his black market decal. This limits the accuracy of the scraped data.

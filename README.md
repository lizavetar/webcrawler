# webcrawler
Data scrapping from internet services providers aggregation website.
Search_automation go over the list of zip codes for the region (in example code it's for a U.S. state) and generates a link with search results, at the last step duplicated results are removed and written to the pandas dataframe.
Crawler takes the list of links, open it one-by-one, scroll through the page (load more buttom) and extract info about each option available. Resuls are saved in a dataframe and extracted as csv.

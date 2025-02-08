In addition to the work provided in the take home assessment, please note that I worked for Fetch via a Data Analytics internship with Loeb.nyc from September 2018 - December 2019, where I worked on the development and maintenance of the Trial & Repeat, Campaign Analysis, Company Scorecard, and Cross Shop dashboards

First: explore the data

See attached .py file for introductory data analysis in python. 

In the products data, over 25% of the rows missing brand and manufacturer information. This information is critical since points are offered to users based on the brands being purchased. Additionally, as you move deeper into the category hierarchy, there are more missing values, but this may not be as concerning as it appears on the surface as certain categories likely do not utilize the full hierarchy. There are also 215 duplicated rows.

In the transaction data, 11% of products are missing a barcode, which will create issues when joining with the products table for deeper analysis. In addition, the analysis of the data reveals that there are rows with a zero or null value for sale amount, which complicates analyses driven by transaction amount. This table also has issues with referential integrity, with 49k invalid foreign keys when compared to the users table, and 19k invalid foreign keys against the products table.

In the user data, missing demographic data for users can complicate data analysis, although the fields are likely optional upon registration.

Second: provide SQL queries

See attached .py file for queries, along with assumptions made.

Third: communicate with stakeholders

Hello,

I am working on an exploratory data analysis on a subset of product, user, and transaction data. The initial review reveals significant issues with referential integrity, wherein the tables cannot be properly joined for analysis due to mismatched or missing key values. Without resolving this issue, over 99% of transactions do not have access to user data, and 38% of barcodes are not mapping to valid products. While certain columns within each dataset have room for improvement in terms of data quality, this particular issue should be seen as a showstopper and the data extraction system should be reviewed. Please work with the scrum master to prioritize this data quality research, as the scope of the impact cannot be understated. I am happy to answer any follow-up questions you may have.

Thanks,
Samantha

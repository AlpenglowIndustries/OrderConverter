# OrderConverter
Python scripts that convert Tindie and Digi-Key Marketplace csv files to Shippo csv files

Incoming csv files from Tindie or DK Marketplace should be called "orders.csv"
Outgoing csv file to Shippo is called "shippoOrders.csv"
CSV files are IGNORED in the git repo, so that I don't accidentally upload order info.

You will need to create a csv file called ProductShippingInfo to map Model Number / SKUs to weights.
  - there is a xlsx file with an example for this file
  - only "lb" is supported right now, weight unit is not used
  - HTS codes are not used right now either, as there is no way to import them through Shippo's csv importer

Total order weight is calculated by:
  - summing item weights for all line items in a single orders
  - adding 1 oz (assumes light bubble packaging)

Other stuff it does:
  - Changes Tindie's "United States of America" to a Shippo-friendly "USA"
  - Concatenates First and Last names from both marketplaces into a Shippo-friendly "Recipient Name"

This is the first quick version, so there's ample opportunity for improvements.  Collaborations welcome!

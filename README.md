# OrderConverter
Python scripts that convert Tindie, Weebly, and Digi-Key Marketplace csv files to Shippo csv files
NEW!  There's now One Script To Rule Them All called OrderReader.py, but the original individual
scripts are still available in the "individual platform scripts" folder.

Input csv files should all start with "orders" and end with "csv" (this is export default).
The script will process all such files in the folder and create a single output file.
Output csv file to Shippo is called "shippoOrders.csv" and is compatible with their default import template.
Orders file platform origin is automatically detected and processed accordingly.
Orders files are moved into a "processed" folder at the end of the script.
CSV files are IGNORED in the git repo, so that I don't accidentally upload order info.

You will need to create a csv file called ProductShippingInfo to map Model Number / SKUs to weights.
  - there is a xlsx file with an example for this file
  - only "lb" is supported right now, weight unit is not used
  - HTS codes are not used right now either, as there is no way to import them through Shippo's csv importer

Total order weight is calculated by:
  - summing item weights for all line items in a single orders
  - adding 1 oz (assumes light bubble packaging)

Other stuff it does:
  Tindie:
    - Changes Tindie's "United States of America" to a Shippo-friendly "USA"
    - Adds a column for a second address line which other platforms use
  Digi-Key:
    - Adds columns for item title, item options, and email
    - Generates an item title by using the description in the ProductShippingInfo csv
  Weebly:
    - Adds a column for Company
    - Merges the first and second lines of each order so the file has one shipped item per row
  Everyone:
    - Concatenates First and Last names from both marketplaces into a Shippo-friendly "Recipient Name"
    - Concatenates Item Title and Option so we can identify exactly what was shipped


There's still ample opportunity for improvements.  Collaborations welcome!

# Takes a csv file downloaded from Alpenglow Industries Weebly site and creates a csv file ready for Shippo upload
# Preparation: from Tindie, export "Unshipped Orders" as "CSV" format
# Rename file as "orders.csv"
# Put in same folder as this .py file

import csv

def getWeight(itemNum):
    infoFile = open('ProductShippingInfo.csv', 'r')
    shipInfo = csv.DictReader(infoFile)
    for row in shipInfo:
        if (row['Product SKU'] == itemNum):
            return row['Weight']
#    return 0.063  # if nothing matches condition - needs testing

# opens orders file downloaded from Tindie and reads into an array,
#   with header names as the first row
inputFile = open('orders.csv')
orders = csv.DictReader(inputFile)
#shipInfo = pandas.read_csv('ProductShippingInfo.csv')


# opens or creates a file to pull into Shippo, with header names
outputFile = open('shippoOrders.csv', "w")
shippoHeader =  ["Order Number", "Order Date", "Recipient Name", "Email", "Phone",
                "Company", "Street Line 1", "Street Line 2", "City", "State/Province", "Zip/Postal Code",
                "Country", "Item Title", "SKU", "Quantity", "Item Price", "Item Weight", "Item Weight Unit",
                "Order Amount", "Order Currency", "Order Weight", "Order Weight Unit"]
shippoOrders = csv.DictWriter(outputFile, fieldnames = shippoHeader, lineterminator = '\n')
shippoOrders.writeheader()

# i = 0
# fOrderRow = 0
# for row in orders:
#     if (row['Order #'] != (row+1)['Order #']):
#         fOrderRow['Product SKU'] = row['Product SKU']
#
#         fOrderRow = row+1



# only grabs individual weight data and adds to a matrix
weightCount = []
for row in orders:
    itemWeight = getWeight(row['Product SKU'])
    if itemWeight is None:
        itemWeight = 0.063
    weightCount.append([row['Order #'], int(row['Product Quantity']), float(itemWeight), " "])

# goes through weight data and calculates overall order weight
# adds 1 oz to all orders to account for bubble packaging
i = 0
orderWeight = 0
while (i < len(weightCount)) :
    begIndex = i
    orderWeight = weightCount[i][1] * weightCount[i][2]   # order weight is the total weight of first line of items
    if i+1 < len(weightCount):
        while (weightCount[i][0] == weightCount[i+1][0]):
            orderWeight += (weightCount[i+1][1] * weightCount[i+1][2])
            if i+2 == len(weightCount):
                break
            else: i += 1
    orderWeight += 0.063
    weightCount[begIndex][3] = orderWeight
    i += 1

# final data adjustments
# writes out to Shippo-readable csv
rowNum = 0
inputFile.seek(0)
orders = csv.DictReader(inputFile)
for row in orders:

    # makes our great country readable to Shippo
#    if "United States of America" in row['Country']:
#        row['Country'] = "USA"

    # writes out all final values to shippoOrders.csv
    # concatenates first and last names into single recipient name
    # concatenates Product Name and Option into a single Item Title
    shippoOrders.writerow({'Order Number': row['Order #'], 'Order Date': row['Date'], 'Email': row['Shipping Email'],
        'Company': '','Phone': row['Phone'], 'Street Line 1': row['Shipping Address'], 'Street Line 2': row['Shipping Address 2'], 'City': row['Shipping City'],
        'State/Province': row['Shipping Region'],'Zip/Postal Code': row['Shipping Postal Code'], 'Country': row['Shipping Country'],
        'Recipient Name': row['Shipping First Name'] + " " + row['Shipping Last Name'], 'Item Title': row['Product Name'] + " " + row['Product Options'],
        'SKU': row['Product SKU'], 'Quantity': row['Product Quantity'], 'Item Price': row['Product Price'], 'Item Weight': weightCount[rowNum][2],
        'Item Weight Unit': 'lb', 'Order Currency': 'USD', 'Order Weight': weightCount[rowNum][3], 'Order Weight Unit': 'lb',
        'Order Amount': row['Total']})
    rowNum += 1

# confirmation in terminal window
print("Done generating shippoOrders.csv")

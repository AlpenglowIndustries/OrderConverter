# Takes a csv file downloaded from Alpenglow Industries Weebly site and creates a csv file ready for Shippo upload
# Preparation: from Weebly, export unshipped orders
# Rename file as "orders.csv"
# Put in same folder as this .py file

import csv, os

def getWeight(itemNum):
    infoFile = open('ProductShippingInfo.csv', 'r')
    shipInfo = csv.DictReader(infoFile)
    for row in shipInfo:
        if (row['Item'] == itemNum):
            return row['Weight']
#    return 0.063  # if nothing matches condition - needs testing

def getDesc(itemNum):
    infoFile = open('ProductShippingInfo.csv', 'r')
    shipInfo = csv.DictReader(infoFile)
    for row in shipInfo:
        if (row['Item'] == itemNum):
            return row['Description']

# creates a file to pull into Shippo, with header names
outputFile = open('shippoOrders.csv', "w")
shippoHeader =  ["Order Number", "Order Date", "Recipient Name", "Email", "Phone",
                "Company", "Street Line 1", "Street Line 2", "City", "State/Province", "Zip/Postal Code",
                "Country", "Item Title", "SKU", "Quantity", "Item Price", "Item Weight", "Item Weight Unit",
                "Order Amount", "Order Currency", "Order Weight", "Order Weight Unit"]
shippoOrders = csv.DictWriter(outputFile, fieldnames = shippoHeader, lineterminator = '\n')
shippoOrders.writeheader()
outputFile.close()

# Creates a list of all "orders" files in the directory
orderFiles = []
i = 0
for file in os.listdir():
    if file.startswith('orders') and file.endswith('csv'):
        orderFiles.append(file)
        print(file)

orderPlatform = 'none'
for file in orderFiles:

    # Weebly does not put item info in the first line, a single item order will have 2 lines with
    # the first line being all info common to the order, and second (and following lines) product info
    # Therefore, before reading it as a dictionary, must merge 1st and 2nd lines of each order.

    inputFile = open(file)
    ordersCSV = csv.reader(inputFile)
    ordersRaw = list(ordersCSV)
    inputFile.close()

    fields = ordersRaw[0]

    # identifies the platform the orders originate with
    if fields[0] == 'Order #':
        orderPlatform = 'Weebly'
        hON = 'Order #'
        hOD = 'Date'
        hFN = 'Shipping First Name'
        hLN = 'Shipping Last Name'
        hEm = 'Shipping Email'
        hPh = 'Shipping Phone'
        hCo = 'Shipping Company'
        hSL1 = 'Shipping Address'
        hSL2 = 'Shipping Address 2'
        hCi = 'Shipping City'
        hSt = 'Shipping Region'
        hZp = 'Shipping Postal Code'
        hCn = 'Shipping Country'
        hIT = 'Product Name'
        hIO = 'Product Options'
        hSKU = 'Product SKU'
        hQty = 'Product Quantity'
        hIP = 'Product Price'
        hOA = 'Total'
    elif fields[0] == 'Order ID':
        orderPlatform = 'Tindie'
        hON = 'Order ID'
        hOD = 'Order Date'
        hFN = 'First Name'
        hLN = 'Last Name'
        hEm = 'Email'
        hPh = 'Phone'
        hCo = 'Company'
        hSL1 = 'Street'
        hSL2 = 'Street2'
        hCi = 'City'
        hSt = 'State/Province'
        hZp = 'Postal/Zip Code'
        hCn = 'Country'
        hIT = 'Product Title'
        hIO = 'Option Summary'
        hSKU = 'Model Number'
        hQty = 'Quantity'
        hIP = 'Unit Price'
        hOA = 'Order Total'
    else:
        orderPlatform = 'DigiKey'
        hON = 'Order number'
        hOD = 'Date created'
        hFN = 'Shipping address first name'
        hLN = 'Shipping address last name'
        hEm = 'Email'
        hPh = 'Shipping address phone'
        hCo = 'Shipping address company'
        hSL1 = 'Shipping address street 1'
        hSL2 = 'Shipping address street 2'
        hCi = 'Shipping address city'
        hSt = 'Shipping address state'
        hZp = 'Shipping address zip'
        hCn = 'Shipping address country'
        hIT = 'Item Name'
        hIO = 'Item Option'
        hSKU = 'Offer SKU'
        hQty = 'Quantity'
        hIP = 'Unit price'
        hOA = 'Total order amount incl. VAT (including shipping charges)'

    print(file + ' is from ' + orderPlatform)

    if orderPlatform == 'Weebly':
        # The following formats a Weebly file into an orders.csv file that's properly
        # organized for turning into a dictionary.  One order item per row, with the
        # first row of an order containing whole-order info (shipping, billing, total cost, etc)

        orderCol = fields.index(hON)
        productCol = fields.index(hIT)

        i = 1
        j = 0
        while i < len(ordersRaw) - 1 :
            if (ordersRaw[i][orderCol] == ordersRaw[i+1][orderCol] and ordersRaw[i][productCol] == '') :  # identifies start of new order by blank product name
                for j in range(len(ordersRaw[0])) :         # looks for blank cells, copies content from record below
                    if ordersRaw[i][j] == '' :
                        ordersRaw[i][j] = ordersRaw[i+1][j]
                del ordersRaw[i+1]                          # deletes now duplicate second order line
            i+=1

        # # for debuggging
        # i = 0
        # for i in range(len(ordersRaw)) :
        #     print(ordersRaw[i])

        # writes out well-formatted orders to orders.csv
        missingCol = 0;
        if hCo not in fields:
            missingCol = 1

        outputFile = open(file, 'w', newline='')  # newline needed to prevent double-spacing
        ordersCSV = csv.writer(outputFile)
        i = 0
        for i in range(len(ordersRaw)) :
            if missingCol:                        # adds a field for Company
                if i == 0:
                    ordersRaw[i].append(hCo)
                else:
                    ordersRaw[i].append('')
            ordersCSV.writerow(ordersRaw[i])
        outputFile.close()

    if orderPlatform == 'Tindie':
        # adds a blank "Street2" column

        missingCol = 0;
        if hSL2 not in fields:
            missingCol = 1

        outputFile = open(file, 'w', newline='')  # newline needed to prevent double-spacing
        ordersCSV = csv.writer(outputFile)
        i = 0
        for i in range(len(ordersRaw)) :
            if missingCol:
                if i == 0:
                    ordersRaw[i].append(hSL2)
                else:
                    ordersRaw[i].append('')
            ordersCSV.writerow(ordersRaw[i])
        outputFile.close()

    if orderPlatform == 'DigiKey':
        # adds blank columns for email, item title, and item option

        missingCol = 0;
        if hEm not in fields:
            missingCol = 1

        outputFile = open(file, 'w', newline='')  # newline needed to prevent double-spacing
        ordersCSV = csv.writer(outputFile)
        i = 0
        for i in range(len(ordersRaw)) :
            if missingCol:
                if i == 0:
                    ordersRaw[i].append(hEm)
                    ordersRaw[i].append(hIT)
                    ordersRaw[i].append(hIO)
                else:
                    ordersRaw[i].append('')
                    ordersRaw[i].append('')
                    ordersRaw[i].append('')
            ordersCSV.writerow(ordersRaw[i])
        outputFile.close()


    # opens properly formatted orders file and reads into a "dictionary" which is more like a database
    #   than an array/list.  No concept of order or ability to operate on previous/next rows.
    #   The first row is translated to header names/labels/keys.
    inputFile = open(file)
    orders = csv.DictReader(inputFile)

    # only grabs individual weight data and adds to a matrix
    weightCount = []
    for row in orders:
        itemWeight = getWeight(row[hSKU])
        if itemWeight is None:
            itemWeight = 0.063
        itemDesc = getDesc(row[hSKU])  # mainly for DigiKey orders that don't have an Item Title, gets it from ProductShippingInfo.csv
        weightCount.append([row[hON], int(row[hQty]), float(itemWeight), " ", itemDesc])

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

    outputFile = open('shippoOrders.csv', "a")
    shippoOrders = csv.DictWriter(outputFile, fieldnames = shippoHeader, lineterminator = '\n')

    for row in orders:

        # makes our great country readable to Shippo, Tindie orders
        if "United States of America" in row[hCn]:
            row[hCn] = "USA"

        if row[hIT] == '':
            row[hIT] = weightCount[rowNum][4]

        # writes out all final values to shippoOrders.csv
        # concatenates first and last names into single recipient name
        # concatenates Product Name and Option into a single Item Title
        shippoOrders.writerow({'Order Number': row[hON], 'Order Date': row[hOD], 'Email': row[hEm],
            'Company': row[hCo],'Phone': row[hPh], 'Street Line 1': row[hSL1], 'Street Line 2': row[hSL2], 'City': row[hCi],
            'State/Province': row[hSt],'Zip/Postal Code': row[hZp], 'Country': row[hCn],
            'Recipient Name': row[hFN] + " " + row[hLN], 'Item Title': row[hIT] + " " + row[hIO],
            'SKU': row[hSKU], 'Quantity': row[hQty], 'Item Price': row[hIP], 'Item Weight': weightCount[rowNum][2],
            'Item Weight Unit': 'lb', 'Order Currency': 'USD', 'Order Weight': weightCount[rowNum][3], 'Order Weight Unit': 'lb',
            'Order Amount': row[hOA]})
        rowNum += 1

    inputFile.close()
    outputFile.close()
    # confirmation in terminal window
    print("Done processing " + file)

print('Done generating shippoOrders.csv')

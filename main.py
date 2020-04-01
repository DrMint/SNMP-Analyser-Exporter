import myLib
from pysnmp import hlapi

# Let's enter all this necessary credentials
myOidTable = myLib.OidTable()
myOidTable.oid =            "1.3.6.1.4.1.11256.1.2.1.1"
myOidTable.snmp.ip =        "192.168.17.254"
myOidTable.snmp.community = "COMMUPAVIPREV"

# Finds the number of rows in this table
myOidTable.numRow = myOidTable.getNumRow()

# oidColumn are the column where the information is located
# Usage: oidColumn(Displayed name, column in the oidTable)
myOidTable.addColumn(myLib.OidColumn(displayedName = "IP", oidColumn = 1))
myOidTable.addColumn(myLib.OidColumn(displayedName = "TTL", oidColumn = 2))
myOidTable.addColumn(myLib.OidColumn(displayedName = "Name", oidColumn = 3))

# We can directly export the file like this
myOidTable.exportTableToCSV("ip.csv")

# Or keep the array for further analysis
# We can use getColumnsValue() or getRowsValue()
myTable = myOidTable.getColumnsValue()

# Let's create a list of Counter
myCounters = myLib.Counters()

# And add new counters.
# We need to indicate its name, which column to analyse and what to look for.
myCounters.addCounter(
    myLib.Counter(
        displayedName = "IP en 10.30",
        predicate = myLib.Predicate(
            columnIndex = myOidTable.getColumnIndex("IP"),
            value = "10.30")
        )
    )

myCounters.addCounter(
    myLib.Counter(
        displayedName = "IP en 10.61",
        predicate = myLib.Predicate(
            columnIndex = myOidTable.getColumnIndex("IP"),
            value = "10.61")
        )
    )

myCounters.addCounter(
    myLib.Counter(
        displayedName = "IP en 192.168.17",
        predicate = myLib.Predicate(
            columnIndex = myOidTable.getColumnIndex("IP"),
            value = "192.168.17")
        )
    )

myCounters.addCounter(
    myLib.Counter(
        displayedName = "IP en 192.168.40",
        predicate = myLib.Predicate(
            columnIndex = myOidTable.getColumnIndex("IP"),
            value = "192.168.40")
        )
    )

# Let's export this analysis in a CSV file
myCounters.exportCountersCountToCSV("stats.csv", myTable)









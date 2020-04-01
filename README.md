# SNMP-Export-Analyse
An easy way to make SNMP query, analyse data, and export tables

This project uses [Quick SNMP (quicksnmp)](https://github.com/alessandromaggio/quicksnmp) by [alessandromaggio](https://github.com/alessandromaggio)


The following exemple connects to a SNMP Manager, selects a specific table OID and export column 1, 2, and 3 in a CSV file.

```python
import myLib

# Let's enter all this necessary credentials
myOidTable = myLib.OidTable()
myOidTable.oid =            "1.3.6.1.4.1.XXXXX.X.X.X.X"
myOidTable.snmp.ip =        "192.168.XX.XXX"
myOidTable.snmp.community = "COMMUNITY_NAME"

# Finds the number of rows in this table
myOidTable.numRow = myOidTable.getNumRow()

# oidColumn are the column where the information is located
# Usage: oidColumn(Displayed name, column in the oidTable)
myOidTable.addColumn(myLib.OidColumn(displayedName = "IP", oidColumn = 1))
myOidTable.addColumn(myLib.OidColumn(displayedName = "TTL", oidColumn = 2))
myOidTable.addColumn(myLib.OidColumn(displayedName = "Name", oidColumn = 3))

# We can directly export the file like this
myOidTable.exportTableToCSV("ip.csv")
```

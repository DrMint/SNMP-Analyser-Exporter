import quicksnmp



# SNMP, acquiring values, exporting

class SnmpServer(object):
    """The credentials used to connect to a snmp server."""
    
    def __init__(self, ip = None, community = None):
        self.ip = ip
        self.community = community

class OidColumn(object):
    """Represents a column used in oidTable."""
    
    def __init__(self, displayedName, oidColumn):
        self.displayedName = displayedName
        self.index = oidColumn

class OidTable(object):
    """ An oidTable is an object used to connect to a snmp server,
        retrieve and export data."""
    
    def __init__(self, snmp = SnmpServer(), oid = None):
        self.oid = oid
        self.snmp = snmp
        self.oidColumns = []
        self.numRow = None
        if snmp.ip != None and oid != None:
            self.numRow = self.getNumRow()        

    def addColumn(self, oidColumn):
        self.oidColumns += [oidColumn]

    def getColumn(self, name):
        for column in self.oidColumns:
            if column.displayedName == name: return column
        return None

    def getColumnIndex(self, name):
        for index, column in enumerate(self.oidColumns):
            if column.displayedName == name: return index
        return None

    def getNumRow(self):
        """Gets the number of rows in the oid."""
        
        column = 1
        row = 0
        while row < 10000:
            tmpOid = self.oid + '.' + str(column) + '.' + str(row)
            if self.getValue(tmpOid) == "":
                return row
            else:
                row += 1        

    def getColumnsValue(self):
        """Gets all the values in all the columns."""
        
        result = []
        for oidColumn in self.oidColumns:
            result += [self.getColumnValue(oidColumn)]
        return result

    def getColumnValue(self, oidColumn):
        """Gets all the values in the column given in parameter."""
        
        result = []
        for row in range(0, self.numRow):
            tmpOid = self.oid + '.' + str(oidColumn.index) + '.' + str(row)
            result += [self.getValue(tmpOid)]
        return result
    
    def getRowsValue(self):
        """Gets all the values in all the rows."""
        
        result = []
        for row in range(0, self.numRow):
            result += [self.getRowValue(row)]
        return result
            
    def getRowValue(self, row):
        """Gets all the values in the row given in parameter."""
        
        result = []
        for oidColumn in self.oidColumns:
            tmpOid = self.oid + '.' + str(oidColumn.index) + '.' + str(row)
            result += [self.getValue(tmpOid)]
        return result

    def getValue(self, oid):
        """Gets one value at one oid coordinates."""
        return quicksnmp.getSimplified(self.snmp.ip, oid, self.snmp.community)

    def exportTableToCSV(self, filePath = "export.csv"):
        """Create a CSV file and fill it with the table"""

        # Create the file if it doesn't exist and overwrite otherwise.
        file = open(filePath, "w")
        self.writeCSV(file, self.getRowsValue())
        file.close()

    def writeCSV(self, file, data):
        """Writes inside a CSV file given in parameters. Contains a header."""
        
        # Write the headers
        for oidColumn in self.oidColumns:
            file.write(oidColumn.displayedName + ";")
        file.write("\n")

        # Write all the data
        for row in data:
            for column in row:
                file.write(str(column) + ";")
            file.write("\n")
        




# Analysing the data

class Counter(object):
    """Give the number of rows that verify a predicate"""
    
    def __init__(self, displayedName, predicate = None):
        self.displayedName = displayedName
        self.predicate = predicate

    def getVerifiedRows(self, data):
        return [row for row in data[self.predicate.columnIndex] if row[:self.predicate.lenght] == self.predicate.value]

    def getCountVerified(self, data):
        return len(self.getVerifiedRows(data))
    
class Counters(object):
    """A list of counters"""
    
    def __init__(self):
        self.list = []

    def addCounter(self, counter):
        self.list += [counter]

    def allCountVerified(self, data):
        result = []
        for counter in self.list:
            result += [counter.countVerified(data)]
        return result

    def exportCountersCountToCSV(self, filePath, data):
        """Create a CSV file and fill it with the counters' number of verified rows"""
        
        file = open(filePath, "w")
        self.writeCSV(file, data)
        file.close()

    def writeCSV(self, file, data):
        """Writes inside a CSV file given in parameters. Contains a header."""
        
        # Write the headers
        for counter in self.list:
            file.write(counter.displayedName + ";")
        file.write("\n")

        # Write all the data
        for counter in self.list:
            file.write(str(counter.getCountVerified(data)) + ";")


class Predicate(object):
    """A predicate is used to know if a row should be considered 'verified'."""
    
    def __init__(self, columnIndex, value):
        self.columnIndex = columnIndex
        self.value = value
        self.lenght = len(value)
        
        
        




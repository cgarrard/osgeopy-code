# Function to get unique values from an attribute field.
def get_unique(datasource, layer_name, field_name):
    sql = 'SELECT DISTINCT {0} FROM {1}'.format(field_name, layer_name)
    lyr = datasource.ExecuteSQL(sql)
    values = []
    for row in lyr:
        values.append(row.GetField(field_name))
    datasource.ReleaseResultSet(lyr)
    return values

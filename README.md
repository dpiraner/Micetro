# Micetro
Mouse measurement tracking and plotting

Point the folder at the directory containing mouse measurements in xls/xlsx format

Excel sheet specifications: 

Row 1: Tumor names only
Row 2: Data headers
Row 3: Data start

Columns without data headers (row 2) are ignored.
Columns containing data headers (row 2) starting with * are ignored

Tumors: Axis1 and Axis2 can be in any order; volumes are computed according to min/max
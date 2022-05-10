# Micetro
Mouse measurement tracking and plotting

Point the folder at the directory containing mouse measurements in xls/xlsx format

Excel sheet specifications: 

Name must start with date in YYYY MM DD format. Other spreadsheets with names not conforming to this format will be ignored.

Row 1: Tumor names and misc. commentary
Row 2: Data headers
Row 3: Data start

Columns without data headers (row 2) are ignored.
Columns containing data headers (row 2) starting with * are ignored
Columns don't have to be in the same place in each spreadsheet; they are matched spreadsheet-by-spreadsheet. Columns can therefore be added/removed between spreadsheets.

Tumors: 
Axis1 and Axis2 can be in any order; volumes are computed according to min/max
For multi-nodal tumors, each node can be recorded by adding additional "+ Axis 1" and "+ Axis 2" column headers (with the same tumor name in Row 1); total volume is the sum of all nodes. There is no limit to the number of nodes, and no requirement that # nodes remains the same between time points.

Data folder can also contain a micetro.txt file containing the following info to accelerate repeat plotting:

"tumor": date of tumor challenge in YYYY MM DD format
"treatment": date of treatment in YYYY MM DD format
"start from": The date set to the 0 time point in the output. Can be "tumor" or "treatment"
"GroupAlias": renames groups (for unblinding).
- Example: "GroupAlias: 1: Tamoxifen" will rename Group "1" in the input spreadsheet to "Tamoxifen" in the output.
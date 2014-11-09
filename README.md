Standardization, is the process to maximize the compatibility between data.

This python code is addressed to company names standardization. This is normally the first step before a linkage or deduplication records process.

It deals with company suffixes (Corp, Ltd, and so on), parenthesis issues, replacement chars or short names (&, 'n) in order to maximize matching.

The output is a CSV file which first column is the original name (set as ID) and the second column is a standardized name. Be aware the standardized name is sorted, and it may look pretty confusing, but during the linkage or deduplication process of two standardized sets the results will be better.

Download / clone
----------------

$ git clone https://github.com/graguirre/company-standard.git

Execute
-------

$ python2 pre-process.py -i <input-col-file> -o <output-file>

if you prefer instead the system I/O

$ cat <input-file> | python2 pre-process.py -i /dev/stdin -o /dev/stdout


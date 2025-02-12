'''
Enrollment analysis:  Summary report of majors enrolled in a class.
CS 210 project, Fall 2022.
Author:  Alexia Crawford
Credits: Worked with Sam
'''
import doctest
import csv

def read_csv_column(path: str, field: str) -> list[str]:
    '''
    Read one column from a CSV file with headers into a list of strings.

    >>> read_csv_column("test_roster.csv", "Major")
    ['DSCI', 'CIS', 'BADM', 'BIC', 'CIS', 'GSS']
    '''
    li = []
    with open(path, "r", newline="") as column:
        reader = csv.DictReader(column)
        for item in reader:
            li.append(item[field])
    return li
                
def counts(column: list[str]) -> dict[str, int]:
    '''
    Returns a dict with counts of elements in column.

    >>> counts(["dog", "cat", "cat", "rabbit", "dog"])
    {'dog': 2, 'cat': 2, 'rabbit': 1}
    '''
    el_counts = {}
    for item in column:
        if item not in el_counts:
            el_counts[item] = 1
        else:
            el_counts[item] += 1
    return el_counts


def read_csv_dict(path: str, key_field: str, value_field: str) -> dict[str, dict]: 
    '''
    Read a CSV with column headers into a dict with selected
    key and value fields.

    >>> read_csv_dict("data/test_programs.csv", key_field="Code", value_field="Program Name")
    {'ABAO': 'Applied Behavior Analysis', 'ACTG': 'Accounting', 'ADBR': 'Advertising and Brand Responsibility'}
    '''
    table = {}
    with open(path, "r", newline="") as column:
        reader = csv.DictReader(column)
        for item in reader:
            key  = item[key_field]
            value = item[value_field]
            table[key] = value
    return table
    
def items_v_k(counts_by_major): 
    '''
    It returns a list of (value, key) pairs for any dict
    >>> items_v_k({'CS': 77, 'EXPL': 15, 'MSCI': 4})
    [(77, 'CS'), (15, 'EXPL'), (4, 'MSCI')]
    '''
    by_count = []
    for code, count in counts_by_major.items():
        pair = (count, code)
        by_count.append(pair)
    return by_count

def main():
    doctest.testmod()
    majors = read_csv_column("data/roster_selected.csv", "Major")
    counts_by_major = counts(majors)
    program_names = read_csv_dict("data/programs.csv", "Code", "Program Name")
    by_count = items_v_k(counts_by_major)
    by_count.sort(reverse=True)  # From largest to smallest
    for count, code in by_count:
        program = program_names[code]
        print(count, program)

if __name__ == "__main__":
    doctest.testmod()
    main()


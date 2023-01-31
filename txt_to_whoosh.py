#After the Top Part Completes, Update with new Log File Name 

import os
from whoosh.index import create_in, open_dir
from whoosh.fields import *

# Define the schema for the Whoosh index
schema = Schema(title=TEXT(stored=True), author=TEXT(stored=True), date=DATETIME(stored=True), 
                url=ID(stored=True), abstract=TEXT(stored=True))

# Create a Whoosh index
index_dir = "indexdir"
if not os.path.exists(index_dir):
    os.mkdir(index_dir)
ix = create_in(index_dir, schema)

# Open the text file and index its contents
with open("/Users/bradboldt/Desktop/EverythingNeurodiversity/researchchatbot/LOGS/LOG_2023-01-30_21_13_neurodiversity_AND_hiring/Abstract_Database_2023-01-30_21_13.txt", "r") as f:
    lines = f.readlines()
    writer = ix.writer()
    for line in lines:
        # Check if the line starts with "Title:"
        if line.startswith("Title:"):
            title = line[7:].strip()
        elif line.startswith("Author:"):
            author = line[8:].strip()
        elif line.startswith("Date:"):
            date = line[6:].strip()
        elif line.startswith("URL:"):
            url = line[5:].strip()
        elif line.startswith("Abstract:"):
            abstract = line[10:].strip()
            # Add the abstract to the index
            writer.add_document(title=title, author=author, date=date, url=url, abstract=abstract)
    writer.commit()

# Open the index for searching
ix = open_dir(index_dir)

# Perform a search
from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
    query = QueryParser("abstract", ix.schema).parse("Autism bias")
    results = searcher.search(query)
    print(f"Found {len(results)} results:")
    for result in results:
        print(result)

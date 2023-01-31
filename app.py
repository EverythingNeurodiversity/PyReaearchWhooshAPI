from flask import Flask, request
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser

app = Flask(__name__)
ix = open_dir("indexdir")

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    with ix.searcher() as searcher:
        query = QueryParser("abstract", ix.schema).parse(query)
        results = searcher.search(query)
        results_list = [{"abstract": result["abstract"], "title": result["title"], "url": result["url"]} for result in results]
        return {"results": results_list}

if __name__ == "__main__":
    app.run(port=8003)

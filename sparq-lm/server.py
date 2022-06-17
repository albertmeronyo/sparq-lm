from flask import Flask, request
from rdflib import URIRef, Graph
from rdflib.plugins.sparql.parser import Query, UpdateUnit
from rdflib.plugins.sparql.processor import translateQuery
import logging
import json
import requests


app = Flask(__name__)

slogger = logging.getLogger("slogger")
slogger.setLevel(logging.DEBUG)

API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"


@app.route("/")
def hello_world():
    query_text = request.args.get('query')
    print(query_text)

    textQuery_uri = URIRef("https://example.org/slm/queryText")
    parsed_query = translateQuery(Query.parseString(query_text, parseAll=True))
    print(parsed_query.algebra)
    print()

    bgp_triples = parsed_query.algebra['p']['p']['triples']
    print(bgp_triples)
    bgp_graph = Graph()

    # Process triples in GBP
    lm_text = ""
    for s,p,o in bgp_triples:
        if p == textQuery_uri:
            lm_text = o
            print(lm_text)

    
    data = query(
        {
            "inputs": lm_text,
            "parameters": {"do_sample": False},
        }
    )

    print(data)

    return "<p>Hello, World!</p>"


def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))
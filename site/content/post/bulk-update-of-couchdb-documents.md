
+++
date = "2014-07-30"
draft = false
title = "Bulk update of CouchDB documents"
slug = "bulk-update-of-couchdb-documents"
tags = ['couchdb', 'update handler', 'bulk update']
banner = ""
aliases = ['/bulk-update-of-couchdb-documents/']
+++

Sometimes you need to apply a change on all of your CouchDB documents. I actually needed to remove an old and unused property from all of them.

CouchDB conceptually doesn't allow you to update a document without knowing its revision, so you would end up reading all your documents, modify them and update them one by one. Sounds nice, eh?

###update handlers
There's a better way, though. CouchDB has a concept of [Document Update Handlers](http://wiki.apache.org/couchdb/Document_Update_Handlers), which are saved in the database's design document and are accessible through the HTTP API. The update handler takes a document id and can perform any modification on the referenced document. On success, the changes will be saved as an updated (or newly created) document.

So, in my case, I created an updated handler function `removeProperty` like this:
```
{
   "_id": "_design/myDatabase",
   "_rev": "2-316a27933f7ab3ab72ab537b9651c267",
   "views": { ... }
   },
   "updates": {
       "removeProperty": "function(doc, req) {delete doc[\"myProperty\"];return [doc, toJSON(doc)];}"
   }
}
```

As you see, I only need two instructions:

- delete doc.myProperty
- return the updated document as first element in the array, to tell CouchDB that it has to save my changes.

What's missing is how to call the update handler for every document in the database.

###iterating over all document ids

First, I got all documents by GETing the `/_all_docs` resource on the database. The response contains an array of all documents with the ids and revisions. I needed to extract the document ids, so the very convenient [jq JSON processor](http://stedolan.github.io/jq/) came into my mind. It allows you to filter any JSON and is very handy when using it in scripts or on the command line. Applying it to the `/_all_docs` response looked like this:
```
$ curl -X GET "http://couchdb.dev:5984/database/_all_docs" | ./jq '.rows | .[].id'

... lots of ids here...
"29888e1753601f9c96c757d5429aa1eb"
"29888e1753601f9c96c757d5429ab10d"
"29888e1753601f9c96c757d5429ac061"
"29888e1753601f9c96c757d5429acb02"
"29888e1753601f9c96c757d5429ad587"
"29888e1753601f9c96c757d5429ae3ec"
"_design/myDatabase"

```

Now I only needed to strip the quotes `"` and remove the design document from the list and call my update handler for each entry. The resulting one liner looks a bit long, but does it's job:
```
$ curl -X GET "http://couchdb.dev:5984/database/_all_docs" | ./jq '.rows | .[].id' | sed -e 's/"//g' | sed -e 's/_design.*//g' | xargs -I id curl -X PUT "http://couchdb.dev:5984/database/_design/myDatabase/_update/removeProperty/id"
```

Using xargs with the option `-I <anything>` allows you to replace `<anything>` on your command with the current argument, in this case the document id.

Since I implemented the update handler to return the document as JSON, all updated documents had been returned as a response. The complete update results in many requests to the CouchDB, but I didn't notice any problems or performance issues.

###Couchtato

My colleagues at [Hypoport](http://blog-it.hypoport.de/) showed me an alternative tool named [Couchtato](https://github.com/cliffano/couchtato). It'll sadly need a bit more setup as only the usual command line tools, but it makes the update look a bit more beautiful than the long and cryptic command line above. I won't go into detail here, everything is explained in the official [readme](https://github.com/cliffano/couchtato/blob/master/README.md).


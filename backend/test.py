# import pymongo
# import sys
# import datetime



# client = pymongo.MongoClient("mongodb://TripDesigner:ShakedKing@tripdesigner-shard-00-00.i9pia.mongodb.net:27017,tripdesigner-shard-00-01.i9pia.mongodb.net:27017,tripdesigner-shard-00-02.i9pia.mongodb.net:27017/Users?ssl=true&replicaSet=atlas-517ql2-shard-0&authSource=admin&retryWrites=true&w=majority")
# db = client.test

# posts = db.posts

# post = {"author": "Mike",
#         "text": "My first blog post!",
#         "tags": ["mongodb", "python", "pymongo"],
#         "date": datetime.datetime.utcnow()}
# post_id = posts.insert_one(post).inserted_id = 1
# print(post_id)





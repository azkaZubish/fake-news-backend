from db import predictions_collection

predictions = list(predictions_collection.find({}, {"_id": 0}))
print(predictions)
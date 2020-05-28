import sys, argparse, pymongo
from bson.objectid import ObjectId
from datetime import date

# Constants
DB_PATH = "mongodb://localhost:27017/"
DATABASE = "amazon"
COLLECTION = "reviews"

CREATE_REVIEW = "create-review"
READ_CUSTOMER = "read-customer"
UPDATE_REVIEW = "update-review"
DELETE_REVIEW = "delete-review"
DELETE_CUSTOMER = "delete-customer"
READ_PRODUCT = "read-product"
TOP_RATED = "top-rated"
TOP_VERIFIED = "top-verified"
RECENTLY_REVIEWED = "recently-reviewed"
HELPFUL_VOTES = "helpful-votes"
CUSTOMER_REVIEWS = "customer-reviews"
MOST_REVIEWS = "most-reviews"
HIGHEST_RATINGS = "highest-ratings"
LOWEST_RATINGS = "lowest-ratings"
REVIEW_HELPFUL = "review-helpful"
CHOICES = [
    CREATE_REVIEW,
    READ_CUSTOMER,
    UPDATE_REVIEW,
    DELETE_REVIEW,
    DELETE_CUSTOMER,
    READ_PRODUCT,
    TOP_RATED,
    TOP_VERIFIED,
    RECENTLY_REVIEWED,
    HELPFUL_VOTES,
    CUSTOMER_REVIEWS,
    MOST_REVIEWS,
    HIGHEST_RATINGS,
    LOWEST_RATINGS,
    REVIEW_HELPFUL
]

# Our application's entry point
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=CHOICES, help="Specify action type")
    args = parser.parse_args()

    if args.action == CREATE_REVIEW:
        create_review()
    elif args.action == READ_CUSTOMER:
        read_customer()
    elif args.action == UPDATE_REVIEW:
        update_review()
    elif args.action == DELETE_REVIEW:
        delete_review()
    elif args.action == DELETE_CUSTOMER:
        delete_customer()
    elif args.action == READ_PRODUCT:
        read_product()
    elif args.action == TOP_RATED:
        top_rated()
    elif args.action == TOP_VERIFIED:
        top_verified()
    elif args.action == RECENTLY_REVIEWED:
        recently_reviewed()
    elif args.action == HELPFUL_VOTES:
        helpful_votes()
    elif args.action == CUSTOMER_REVIEWS:
        customer_reviews()
    elif args.action == MOST_REVIEWS:
        most_reviews()
    elif args.action == HIGHEST_RATINGS:
        highest_ratings()
    elif args.action == LOWEST_RATINGS:
        lowest_ratings()
    elif args.action == REVIEW_HELPFUL:
        review_helpful()

def create_review():
    customer_id = input("Please enter the customer id: ")
    product_title = input("Please enter the product name: ")
    product_category = input("Please enter the product category: ")
    star_rating = input("Please enter the star rating: ")
    review_headline = input("Please enter the review title: ")
    review_body = input("Please enter the review body: ")

    review = {
        "marketplace": "US",
        "customer_id": int(customer_id),
        "review_id": "",
        "product_id": "",
        "product_parent": 0,
        "product_title": str(product_title),
        "product_category": str(product_category),
        "star_rating": int(star_rating),
        "helpful_votes": 0,
        "total_votes": 0,
        "vine": "N",
        "verified_purchase": "N",
        "review_headline": str(review_headline),
        "review_body": str(review_body),
        "review_date": str(date.today())
    }

    collection = get_collection()
    result = collection.insert_one(review)

    if result is not None:
        print("Successfully inserted a new review record with insert id: " + str(result.inserted_id))
    else:
        print("Error: Unable to insert new review record")

def read_customer():
    customer_id = input("Please enter the customer id: ")
    customer_id = int(customer_id)

    collection = get_collection()

    for review in collection.find({"customer_id": customer_id}):
        print(review)

def update_review():
    review_id = input("Please enter the review id: ")

    query = {"_id": ObjectId(review_id)}
    collection = get_collection()
    count = collection.count_documents(query)

    if count < 1:
        print("Error: The specified review does not exist")
        sys.exit()

    star_rating = input("Please enter the new star rating: ")
    review_headline = input("Please enter the new review title: ")
    review_body = input("Please enter the new review body: ")

    update = {"$set": {
        "star_rating": int(star_rating),
        "review_headline": str(review_headline),
        "review_body": str(review_body)
    }}
    result = collection.update_one(query, update)

    if result is not None:
        print("Successfully updated " + str(result.modified_count) + " review record")
    else:
        print("Error: Unable to update review record")

def delete_review():
    review_id = input("Please enter the review id: ")

    query = {"_id": ObjectId(review_id)}
    collection = get_collection()
    result = collection.delete_one(query)

    if result is not None:
        print("Successfully deleted " + str(result.deleted_count) + " review record")
    else:
        print("Error: Unable to delete review record")

def delete_customer():
    customer_id = input("Please enter the customer id: ")
    customer_id = int(customer_id)

    query = {"customer_id": customer_id}
    collection = get_collection()
    result = collection.delete_many(query)

    if result is not None:
        print("Successfully deleted " + str(result.deleted_count) + " review record")
    else:
        print("Error: Unable to delete all customer record")

def read_product():
    product_id = input("Please enter the product id: ")

    collection = get_collection()

    for review in collection.find({"product_id": product_id}):
        print(review)

def top_rated():
    product_category = input("Please enter the product category: ")
    query = {"product_category": product_category}

    collection = get_collection()

    agr = [ { '$match': { "product_category": product_category } }, {'$group': {'_id': '$product_id', "marketplace":{'$first':'$marketplace'}, "product_parent":{'$first':'$product_parent'}, "product_title":{'$first':'$product_title'}, "product_category":{'$first':'$product_category'}, "average_star_rating": { '$avg': '$star_rating' } } }, { '$sort': {'average_star_rating': -1}}, { '$limit': 10} ]
    val = list(collection.aggregate(agr, allowDiskUse= True))
    
    for review in val:
        print(review)

def top_verified():
    product_category = input("Please enter the product category: ")
    query = {"product_category": product_category}

    collection = get_collection()

    agr = [ { '$match': {'$and':[{ "product_category": product_category }, {"verified_purchase":"Y"}]} }, {'$group': {'_id': '$product_id', "marketplace":{'$first':'$marketplace'}, "product_parent":{'$first':'$product_parent'}, "product_title":{'$first':'$product_title'}, "product_category":{'$first':'$product_category'}, "average_star_rating": { '$avg': '$star_rating' }, "verified_purchase":{'$first':'$verified_purchase'} } }, { '$sort': {'average_star_rating': -1}}, { '$limit': 10} ]
    val = list(collection.aggregate(agr, allowDiskUse= True))
    
    for review in val:
        print(review)

def recently_reviewed():
    product_category = input("Please enter the product category: ")

    collection = get_collection()

    for review in collection.find({"product_category": product_category}).sort("review_date", -1).limit(10):
        print(review)

def helpful_votes():
    product_id = input("Please enter the product id: ")

    collection = get_collection()

    for review in collection.find({"product_id": product_id}).sort("helpful_votes", -1).limit(10):
        print(review)

def customer_reviews():
    collection = get_collection()
    
    agr = [ {'$group': {'_id': '$customer_id', "reviews_count": { '$sum': 1 } } }, { '$sort': {'reviews_count': -1}}, { '$limit': 10} ]
    val = list(collection.aggregate(agr))
    
    for review in val:
        print(review)

def most_reviews():
    collection = get_collection()

    agr = [ {'$group': {'_id': '$product_id', "marketplace":{'$first':'$marketplace'}, "product_parent":{'$first':'$product_parent'}, "product_title":{'$first':'$product_title'}, "product_category":{'$first':'$product_category'}, "reviews_count": { '$sum': 1 } } }, { '$sort': {'reviews_count': -1}}, { '$limit': 10} ]
    val = list(collection.aggregate(agr))
    
    for review in val:
        print(review)

def highest_ratings():
    collection = get_collection()

    agr = [ {'$group': {'_id': '$customer_id', "average_star_rating": { '$avg': '$star_rating' } } }, { '$sort': {'average_star_rating': -1}}, { '$limit': 10} ]
    val = list(collection.aggregate(agr))
    
    for review in val:
        print(review)

def lowest_ratings():
    collection = get_collection()

    agr = [ {'$group': {'_id': '$customer_id', "average_star_rating": { '$avg': '$star_rating' } } }, { '$sort': {'average_star_rating': 1}}, { '$limit': 10} ]
    val = list(collection.aggregate(agr))
    
    for review in val:
        print(review)

def review_helpful():
    review_id = input("Please enter the review id: ")

    query = {"review_id": review_id}
    collection = get_collection()
    count = collection.count_documents(query)

    if count < 1:
        print("Error: The specified review does not exist")
        sys.exit()

    previous = collection.find(query).next()['helpful_votes']

    update = {"$set": {
        "helpful_votes": previous+1,
    }}
    result = collection.update_many(query, update)

    if result is not None:
        print("Successfully submitted " + str(result.modified_count) + " helpful vote")
    else:
        print("Error: Unable to submit helpful vote")

def get_collection(db=DATABASE, collection=COLLECTION):
    client = pymongo.MongoClient(DB_PATH)
    db = client[DATABASE]
    collection = db[COLLECTION]
    return collection

# If this script is invoked via the command line
if __name__ == "__main__":
    main()

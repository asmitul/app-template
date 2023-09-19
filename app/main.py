import logging
import os
from dotenv import load_dotenv
load_dotenv()

LOGS_LOCATE = os.getenv("LOGS_LOCATE","LOCAL")

if LOGS_LOCATE == "LOCAL":
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")

    logging.basicConfig(
        filename=f"./app/logs/{current_date}.log",
        format="%(asctime)s %(levelname)s %(message)s",
        level=os.getenv("LOGGING_LEVEL")
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)

if LOGS_LOCATE == "REMOTE":
    from pymongo import MongoClient
    client = MongoClient(f'mongodb://{os.getenv("MONGODB_USER")}:{os.getenv("MONGODB_PASSWORD")}@{os.getenv("MONGODB_HOST")}:{os.getenv("MONGODB_PORT")}/?authMechanism=DEFAULT')
    db_logs = client[os.getenv("APP_NAME")+os.getenv("MONGODB_LOGS_DATABASE_NAME")]
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")
    collection_logs = db_logs["log_"+current_date]

    logger = logging.getLogger(__name__)
    logger.setLevel(os.getenv("LOGGING_LEVEL"))

    class MongoDBhandler(logging.Handler):
        def emit(self, record):
            from datetime import datetime
            record.created = datetime.now().isoformat()
            collection_logs.insert_one(record.__dict__)

    logger.addHandler(MongoDBhandler())

def main():
    logger.debug(" level debug : debug message!")
    logger.info(" level info : like start end message etc.!")
    logger.warning(" level warn : warning message but dont terminate issue!")
    logger.error(" level error : error message!")
    logger.critical("level critical : will be terminated!")


    # main database
    if LOGS_LOCATE == "REMOTE":
        from pymongo import MongoClient
        client = MongoClient(f'mongodb://{os.getenv("MONGODB_USER")}:{os.getenv("MONGODB_PASSWORD")}@{os.getenv("MONGODB_HOST")}:{os.getenv("MONGODB_PORT")}/?authMechanism=DEFAULT')
        db = client[os.getenv("APP_NAME")+os.getenv("MONGODB_DATABASE_NAME")]
        collection = db["collection"]

        # insert data
        collection.insert_one({
            "id": 1,
            "name": "test"
        })

if __name__ == "__main__":
    main()
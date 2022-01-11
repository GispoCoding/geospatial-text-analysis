conf = {
    "settings": {
        "analysis": {
            "analyzer": {
                "default": {
                    "tokenizer": "finnish",
                    "filter": ["lowercase", "stopFilter", "raudikkoFilter"],
                }
            },
            "filter": {
                "stopFilter": {"type": "stop", "stopwords": "_finnish_"},
                "raudikkoFilter": {"type": "raudikko"},
            },
        }
    },
    "mappings": {
        "properties": {
            "service_request_id": {"type": "keyword"},
            "service_code": {"type": "integer"},
            "description": {
                "type": "text",
                "analyzer": "default",
            },
            "requested_datetime": {"type": "date"},
            "updated_datetime": {"type": "date"},
            "status": {"type": "keyword"},
            "status_notes": {
                "type": "text",
                "analyzer": "default",
            },
            "agency_responsible": {"type": "keyword"},
            "service_name": {"type": "keyword"},
            "address": {
                "type": "text",
                "analyzer": "default",
            },
            "address_id": {"type": "keyword"},
            "zip_code": {"type": "keyword"},
            "location": {"type": "geo_point"},
        },
    },
}

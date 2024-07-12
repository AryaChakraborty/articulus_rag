from marshmallow import Schema, fields, ValidationError
import bleach

# Define Schemas for validation
class RankRequestSchema(Schema):
    search_keywords = fields.List(fields.Str(), required=True)

class KeywordExtractorSchema(Schema):
    body = fields.Str(required=True)

class AIRequestSchema(Schema):
    path = fields.Str(required=True)
    type = fields.Str(required=True)
    question = fields.Str(required=True)

def validate_and_sanitize_rank(data):
    try:
        schema = RankRequestSchema()
        result = schema.load(data)
        sanitized_keywords = [bleach.clean(keyword) for keyword in result['search_keywords']]
        return {"sanitized_keywords": sanitized_keywords}
    except ValidationError as err:
        return {"error": err.messages}

def validate_and_sanitize_keyword_extractor(data):
    try:
        schema = KeywordExtractorSchema()
        result = schema.load(data)
        sanitized_body = bleach.clean(result['body'])
        return {"sanitized_body": sanitized_body}
    except ValidationError as err:
        return {"error": err.messages}

def validate_and_sanitize_ai(data):
    try:
        schema = AIRequestSchema()
        result = schema.load(data)
        sanitized_path = bleach.clean(result['path'])
        sanitized_type = bleach.clean(result['type'])
        sanitized_question = bleach.clean(result['question'])
        return {
            "sanitized_path": sanitized_path,
            "sanitized_type": sanitized_type,
            "sanitized_question": sanitized_question
        }
    except ValidationError as err:
        return {"error": err.messages}

# Test data
test_rank_data = {"search_keywords": ["<script>alert('xss')</script>", "news"]}
test_keyword_extractor_data = {"body": "<img src='invalid' onerror='alert(\"xss\")'>"}
test_ai_data = {"path": "<script>alert('xss')</script>", "type": "url", "question": "What is <b>AI</b>?"}

# Run validations and sanitizations
print("Testing /rank endpoint:")
print(validate_and_sanitize_rank(test_rank_data))

print("\nTesting /keyword_extractor endpoint:")
print(validate_and_sanitize_keyword_extractor(test_keyword_extractor_data))

print("\nTesting /ai endpoint:")
print(validate_and_sanitize_ai(test_ai_data))

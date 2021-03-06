import utils.api_requests_utils as api_requests_utils
import utils.json_schema_utils as json_schema_utils
from behave import when, then
from jsonschema import validate
from utils.file_utils import get_json_file

@when(u'a {method} request is sent to "{endpoint}" with body')
def step_impl(context, method, endpoint):
    api_requests_utils.call_rest_api(context=context, method=method, endpoint=endpoint, body=context.text)

@then(u'the response should have the code "{expected_status_code:d}"')
def step_impl(context, expected_status_code):
    assert expected_status_code == context.api_response_status_code, 'Status code not expected: %s not equal to %s' % (expected_status_code, context.api_response_status_code)

@then(u'the response body should have "{response_path}" equals to "{expected_response_value}"')
def step_impl(context, response_path, expected_response_value):
    found_value = api_requests_utils.get_response_value(context.api_response_body, response_path)
    
    assert found_value != False, 'Response value was not found in response: %s' % context.api_response_body
    assert str(found_value) == expected_response_value, 'Response value not expected: %s not equal to %s' % (expected_response_value, found_value)

@then(u'the repsonse body should be valid based on "{json_schema_name}" schema')
def step_impl(context, json_schema_name):
    json_schema = get_json_file(context.config.userdata['json_schemas'] + json_schema_name + '.json')
    validation_result = json_schema_utils.validate_response(context.api_response_body, json_schema, context.json_schema_resolver)
    
    assert validation_result['result'] == True, 'Response does not match expected schema: %s' % validation_result['message']

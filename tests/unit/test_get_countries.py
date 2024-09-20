from lambda_functions.get_countries.app import handler

def test_handler():
    # Mock event and context
    event = {}
    context = {}

    # Call the handler function
    response = handler(event, context)

    # Assert he expected output
    assert response == "Hello World!", "Unexpected output"

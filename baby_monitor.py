def is_something(parameters):
    
    [api_key,image_filepath,string_list,threshold] = parameters
    

    # Instantiate a new Clarifai app by passing in your API key.
    app = ClarifaiApp(api_key=api_key)

    # Choose one of the public models.
    model = app.public_models.general_model

    # Predict the contents of an image by passing in a URL.
    response = model.predict_by_filename(image_filepath, max_concepts=200)

    #Interate through response to find baby or child percentage
    relevant = []

    for result in response['outputs'][0]['data']['concepts']:
        if result['name'] in string_list and result['value'] > threshold:
                relevant.append(result['name'])

    return relevant

danger_low_list = ['toy','stand']
danger_high_list = ['knife','drink','fire']
missing_list = ['child','baby']

general = lambda x: is_something(x)
isBaby = general([my_key, image, missing_list,0.9])
detectLowDanger = general([my_key, image, danger_low_list,0])
detectHighDanger = general([my_key, image,danger_high_list,0.1])


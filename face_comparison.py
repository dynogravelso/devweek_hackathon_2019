#final workflow cell
from clarifai.rest import ClarifaiApp
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle

#intantiate important objects
app = ClarifaiApp(api_key='d9610a6498934cf1bd90e8e26684a2c2')
is_face_model = app.public_models.face_detection_model
model = app.public_models.face_embedding_model
filename = "ENTER FILENAME HERE"
reference_vectors = pickle.load(open('reference_vectors.pkl', 'rb'))

#check to see if there is a face
is_face_data = is_face_model.predict_by_filename(filename)
is_face = is_face_data['outputs'][0]['data']

#if there is a face, see who it is
if is_face:
    test_vector = model.predict_by_filename(filename)
    tv = np.array(test_vector['outputs'][0]['data']['regions'][0]['data']['embeddings'][0]['vector'])
    sims = cosine_similarity(reference_vectors, [tv])
    names = ['Aaron', 'Ben', 'Danny', 'Steve']

    for i, val in enumerate(sims):
        if val > 0.7:
            print(names[i])
            break
        if i == 3:
            print("No Matches")
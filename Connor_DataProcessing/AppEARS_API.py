import json
import requests
import geojson
import os
from multiprocessing import Pool

response = requests.post('https://appeears.earthdatacloud.nasa.gov/api/login', auth=('cwang104', 'TacoMonki168'))
token_response = response.json()

# submit the task request
token = token_response['token']
task_id = '57b0adce-8009-4d99-8e25-fc9fbe8376ce' 
response = requests.get(
    'https://appeears.earthdatacloud.nasa.gov/api/bundle/{0}'.format(task_id),  
    headers={'Authorization': 'Bearer {0}'.format(token)}
)
bundle_response = response.json()

dest_dir = 'C:/Users/Connor/Desktop/Data/AppEARS_LST/'

    
def download(file):
        
    file_id = file["file_id"]
    filename = file["file_name"]
    response = requests.get( 
        'https://appeears.earthdatacloud.nasa.gov/api/bundle/{0}/{1}'.format(task_id,file_id),  
        headers={'Authorization': 'Bearer {0}'.format(token)}, 
        allow_redirects=True,
        stream=True
    ) 

    filepath = os.path.join(dest_dir, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # write the file to the destination directory
    with open(filepath, 'wb') as f:
        for data in response.iter_content(chunk_size=8192):
            f.write(data)




if __name__ == '__main__':

    print("Beginning download ໒(⊙ᴗ⊙)७✎▤")

    files = []
    for file in bundle_response["files"]:
        files.append(file)

    pool = Pool()
    pool.map(download, files)
    print("Download finished! (づ ◕‿◕ )づ")

# Cloudvis Python API

## Usage

### Retrieving and Responding
The following code snippet demonstrates retrieving information from a request and responding:
```python
from cloudvis import CloudVis

PORT = 9999

def callback(request, response, data):
    value0 = request.getValue('input_number0')    # No default value
    value1 = request.getValue('input_number1', 0) # With default value

    '''
    If no default value is supplied an error will automatically be generated and dispatched 
    to the user to notify them that they have failed to supply required information
    '''
    
    # Typecast and increment both values
    value0 = int(value0) + 1
    value1 = int(value1) + 1

    response.addValue('output_number0', value0)
    response.addValue('output_number1', value1)

if __name__ == '__main__':
    cloudvis = CloudVis(
        PORT,
        secure=True,
        server_key_file=key_file_path
    )
    cloudvis.run(callback)
```

#### Retrieving and Responding with Images
You can also retrieve ***images*** from a request and send ***images*** in a response:
```python
import cv2
from cloudvis import CloudVis

PORT = 9999 

def callback(request, response, data):
    img = request.getImage('input_image_id')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    response.addImage('out_img_id', gray)

if __name__ == '__main__':
    cloudvis = CloudVis(
        PORT,
        secure=True,
        server_key_file=key_file_path
    )
    cloudvis.run(callback)
```

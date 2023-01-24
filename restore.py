import json
import os
import base64
import requests

def restore(image_url):
    
    restore_input = {"img": image_url, "version": "v1.4", "scale": 2}
    model_version = "9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3"
    token = "1ae32685285182311b70c29704b5ed649a368154"
        
        

    # Start the image restoration generation process
    start_response = requests.post(
        "https://api.replicate.com/v1/predictions",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Token " + token
        },
        data=json.dumps({
            "version": model_version,
            "input": restore_input
        })
    )


    # Get the endpoint URL from the start response
    endpoint_url = start_response.json()["urls"]["get"]

    # Poll the endpoint until the image restoration is complete
    restored_image = None
    while not restored_image:
        # Make a GET request to the endpoint
        final_response = requests.get(
            endpoint_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Token " + token
            }
        )
        json_final_response = final_response.json()

        # Check the status of the image restoration
        if json_final_response["status"] == "succeeded":
            restored_image = json_final_response["output"]
        elif json_final_response["status"] == "failed":
            print("Image restoration failed")
            break
        else:
            import time
            time.sleep(1)

    # Display the restored image
    return restored_image


if __name__ == "__main__":
    restore()
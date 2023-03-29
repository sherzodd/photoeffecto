import json
import requests

def restore(image_url):
    
    restore_input = {"img": image_url, "version": "v1.4", "scale": 2}
    model_version = "9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3"
    token = "YOUR TOKEN"
        
        
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


    endpoint_url = start_response.json()["urls"]["get"]

    restored_image = None
    while not restored_image:
        final_response = requests.get(
            endpoint_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Token " + token
            }
        )
        json_final_response = final_response.json()

        if json_final_response["status"] == "succeeded":
            restored_image = json_final_response["output"]
        elif json_final_response["status"] == "failed":
            print("Image restoration failed")
            break
        else:
            import time
            time.sleep(1)

    return restored_image


if __name__ == "__main__":
    restore()
# Write a  function to flatten the object


flattened = {}
def flatten_json(un_flattened_input, key_input=None):
    for key, value in un_flattened_input.items():
        final_key = key_input+"."+key if key_input else key
        if not isinstance(value, dict):
            flattened[final_key] = value
        else:
            flatten_json(value, final_key)
    return flattened



if __name__ == "__main__":
    un_flattened = {
        "fullName": "Rohit Sharma",
        "age": 29,
        "address": {
            "street": "MG Road",
            "city": "Bengaluru",
            "location": {
            "lat": 12.9716,
            "lng": 77.5946
            }
        }
        }
    print(flatten_json(un_flattened))
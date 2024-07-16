# Python program to write JSON
# to a file
 
 
import json
 
# Data to be written
dictionary = {
    "name": "Jiu",
    "gpa": 8.6,
    "phonenumber": "9976770500"
}
 
# with open("sample.json", "w") as outfile:
#     json.dump({"1":dictionary}, outfile)

with open('sample.json', 'r') as openfile:
 
    # Reading from json file
    json_object = json.load(openfile)
print(json_object)

with open("sample.json", "w") as outfile:
    json_object["2"] = dictionary
    json.dump(json_object, outfile)

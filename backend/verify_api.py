import http.client

conn = http.client.HTTPSConnection("jsearch.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "e8eda8476dmsh64111d702293581p174763jsne7a9ae9e8ef1",
    'x-rapidapi-host': "jsearch.p.rapidapi.com"
}

conn.request("GET", "/search?query=Python%20developer%20in%20Texas%2C%20USA&page=1&num_pages=1", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

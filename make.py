import requests

def send_link(room_link:str, emails:list):
    data={
        "emails":emails,
        "room_link":room_link
    }
    response=requests.request("POST",url="https://hook.eu2.make.com/t9emuqvbx9ewsgx5l4ib7nl2kdk14n9a",data=data)
    try:
        if response.status_code==200:
            print("Successfully sent the meet link")
    except Exception as e:
        print(f"Some error occured {e}" )

    return response

if __name__=="__main__":
    send_link("www.example.com",['anjaneyparasar14@gmail.com','123lutherwinston@gmail.com'])

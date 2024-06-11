import asyncio
import os
from sydney import SydneyClient
import io
import cv2
import pathlib
import json
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
import piexif
import glob

os.environ["BING_COOKIES"] = "_gcl_au=1.1.1448956925.1714043638; MC1=GUID=ccf20e3da5934cfa85b6c500681c34cb&HASH=ccf2&LV=202404&V=4&LU=1714128332126; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=A0C130DE030946A692CA0AEA4122C147&dmnchg=1; MUIDB=0A6CBF02E6E46BD623ABAB69E7B26ADF; MUID=0A6CBF02E6E46BD623ABAB69E7B26ADF; GI_FRE_COOKIE=gi_prompt=1; MMCASM=ID=09134B9309324591A818D72281E4DD89; _clck=1ohef47%7C2%7Cfmd%7C1%7C1612; display-culture=en-US; _C_Auth=; _EDGE_S=SID=12263DCB899E6F221193295188B06EAC; ak_bmsc=0085903C817CB6943230C1EB9F8687CA~000000000000000000000000000000~YAAQ0kvWF3ejHQGQAQAA59+HAhjxs/vWHUp82oqT0yj0U3xNwQCM9BQSViallhO6vZoGa2WVqwyY01vXI++8YZib0/uLc985ZnrN3Drk2S/L1KeeaxwnOQFjNyKI4gNGE4cqmK7Fouwrpxvjz2gm5Qh7wiQkH9GPNBNyRbHZGdJCucUcjlNUwGs6D3Kp0Kg2aoGjjfLtopbkDJvEjXjlHImL4yNNUEJx/8fSTnp/h/7+Di1foZQgIZgV/m2tsv/QkX2Bwo5JggiQk+hdKo+xKebmPNO/wNVD79OG6c1IzzXYf91OkCVVvYk8AIWnF0KQ2eGhxr+BCJrjG41qfKhaaYkJiSk8F/7TRv2+PaYKNx5cZj/s4s3my1O+HeouGV2Q/vQSSc5aeZOsY6Lk; _Rwho=u=d&ts=2024-06-10; CSRFCookie=68c732c7-f4fc-4e1e-a4e5-ce4a044b8386; SRCHUSR=DOB=20240531&T=1718029377000&TPC=1717181014000&POEX=W; ANON=A=4471D23256EDD83420F283AEFFFFFFFF&E=1dd9&W=2; NAP=V=1.9&E=1d7f&C=tXX2eYCAhh0Mq5bJSOSHOT9C2EQKfr5iALlW1a8coZbns1utDf9Eyg&W=2; PPLState=1; KievRPSSecAuth=FAByBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACJK9N6X1m6JCMARGasoCYmb8Ay3+9fu1HijB9juwakF5q4TdVZBfxoyq4psBLA6P5OJ9hReSF3Sh3ft3tdhGn9IOhrMzGw9gFvXwheT0UIvy4mGMu4+sQH1G/6YV66an3N3UAtqa+9tow0lmC47TWVmG2Zu0BDPJJONUveC6Ru/J2hO5rDB2ZuUyzHrLipO28vOumwUxWnwpuu6nyOYe8yXKGwQAsQCQUVm1R8u06uAPvo4tCJAEq7LeRB5aCh2c7xqZ/cmpI87JjJzZpjEfcuWGopA/LwWUzVKGeOmeEGgIHYkmpAxtkGPwM2iCszzvKYPVf21hYKmpFRhN/csa3g2ts5oGlWtiipPIGZrhzgRRt78HKC3cOfNmgJzY2UcWtS50nOW9/tqmg4pY0eonTNZCMc/hTDK80QroDR76a7ySqNiWC9t99s9q0YcX5bpD3jGPniUvHU9O3sr/95UfCFyNmZVUly5k2FBVmwDoCNHW2+wzgVPil2ZlXumWXrAd9jwetcb46XJTN3iT8CuB92oFPvxhB5bfAOpnkzYyhvpciH8PUE69s5rH/pFndhmt25Irg4xje4Es5JAyCEJY6+fPaPxckmFPGk/lmev2Qzs1k7TqqI+Bx8GMQpPRBJpff9l7CH/5jA7LJp4nRgUIAzvIwk1kYWEdr6Qn4N7r6LFgkPxUG1iRL87CZUoi0miNnGyph2rrDKG896ji0XaSfvpWTszYptF+1NxKYt4PtpJpnslGEOyia1OygAhfWRLutDnaUHGECQbsXKBws4a7mEqa3nELyA3N9y5GSyF+Lxj1ATG26gVnuQrW1uFB62XlqQQka0DWTw9A6uKzlzxrw/U4RATy75dilaj48x0CYnQzsegcCDIg/QXlp/hbxWSb7rUaA3ftDFBARkpNsixTcaxJjCis2mHqNZ0msy74FxWp6mn1YaKSy/bvUjN6EbK1sRxGJ0Z5wmEh+DFR8wABpVf4Xz+egPfP8kQ4ITAiZfC7Hb3az5BED97gcGiu/idqCXab/Byjby01hmt8hp8PEw1Pyio/sIc0s1F9W9WCuhXCgVFvizSr9DNq/cTEB7vCBK7Jqe/oncQRkRf0wjrcfEUZI4NBByXIOgXqtEB8v6ktOqJym4Dp+l/3qXdu5uUaKmX9538U3btLSPji+0XFZyfad4vxBN2fh/w2yUAf88zwFU7YEQYXPWeGcGlzTs3RLls+HZ2FJTkvnNHVumVdX0hF+mfEYg10EbBCrnoFpWHm2rCDWFFiyKQEO/46X3xpNgo5esCRfGI7Soh4uWEDHscgwQrgjjEKeUQ04ovZffAH1qJX9lBQGSCQCccfr21RH32qC8UBG+mNq8/aB4HfAs+uYzShcPuJwm/x2qt0I7CBg7h4peZWGxRa9zExbetutszwsYEq7JP0tPllCsdJEc5RhZtKx5IWtJ3/FABs2MJY2ZBTVLvMNSOTlq37wpkhQw==; _U=17yfTuavwDYTExIiWqZH50xNb4sFsPZM2-48PDi9zqspJIUPZW8UnZYLyAqSx3MzSmFoenOrC1DiVb9IwfJ4ayohNG572sAOHbyz40cuWn10xCXBarJc5pzxiEDnGPHT1G9ZGMzUgOwIraJwlAfMySw2xTFsyC02xxKaGAQKahfM6QM5URH6M6vFYCGQxAQ4ywbS8gTfk6C17TWOuF5kBpQ; WLS=C=811b24f74e5b363a&N=dicky; WLID=efdNk5zAq/w3XUv23OgoMtuILsTPHyVI6UFhvS/9j7VndTp8/9RKcXMVihzUrXv3VzH8S/SC3aAUsC0H8HF6KIWtY75MCC0nYe6EzgRHiOk=; _uetsid=f45c51a0273411efbf628b4d90ebde1a; _uetvid=d9973ff01f7711ef8d04474592cd34d6; _SS=SID=12263DCB899E6F221193295188B06EAC&R=134&RB=134&GB=0&RG=0&RP=134; _RwBf=r=0&ilt=1&ihpd=1&ispd=0&rc=134&rb=134&gb=0&rg=0&pc=134&mtu=0&rbb=0&g=0&cid=&clo=0&v=3&l=2024-06-10T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&ard=0001-01-01T00:00:00.0000000&rwdbt=0001-01-01T16:00:00.0000000-08:00&rwflt=0001-01-01T16:00:00.0000000-08:00&o=0&p=BINGCOPILOTWAITLIST&c=MR000T&t=4512&s=2023-03-23T18:24:13.4192833+00:00&ts=2024-06-10T14:28:11.1057333+00:00&rwred=0&wls=2&wlb=0&wle=0&ccp=2&cpt=0&lka=0&lkt=0&aad=0&TH=&mta=0&e=RVQJLT4danL1E2f_vWwxoJKZONP8G7TnnLzI_mfY3fBq3H4-mduQUpS4zGaHMRi-Po_DdKpn3vYrW0xywOYdYQ&A=4471D23256EDD83420F283AEFFFFFFFF; _C_ETH=1; bm_sv=89485DA510FACCF564B12D9D68F33A25~YAAQzUvWFzW4BgGQAQAAsMuMAhh1BQ/HPG3TRWqrnIficD6lu1Wqce/7MnqLhfNLWZBhCawBW/7K+S7i2+ChqzFrFzJ9ttqzu74WqbVkaMTMZf5B0JFLo7XiQPTe72hgMzFZTKQHv8jWIUTejoB5aZa82XBZKenWY/nthYVerVdRUFnZLanmW1AW/sG9JCQdvs411FhHuCsA6WtW5Ei57vfPZlJEMviHQzCq4W3ZYN7ngERIih6Cgg7dnqfWP2iqr6IeSg==~1; SRCHHPGUSR=SRCHLANG=id&BRW=HTP&BRH=T&CW=983&CH=1305&SCW=983&SCH=796&DPR=1.0&UTC=420&DM=1&PV=15.0.0&WTS=63853626177&HV=1718029692&PRVCW=2560&PRVCH=1305&CIBV=1.1766.0&cdxtone=Balanced&cdxtoneopts=galileo,flxvoice";

def edit_tag_metadata(image_path, new_tags,title):
    if "example" in image_path : 
        return
    else:
        try:
            # Open the image
            img = Image.open(image_path)

            # Extract existing EXIF data
            exif_dict = piexif.load(img.info['exif'])

            # Convert new_tags list to a UTF-16 encoded string for EXIF
            new_tags_str = "; ".join(new_tags).encode('utf-16le')
        
            # Add or update the UserComment tag
            exif_dict["0th"][piexif.ImageIFD.XPKeywords] = new_tags_str
            exif_dict["0th"][piexif.ImageIFD.ImageDescription] = title
            print(exif_dict)
            exif_bytes = piexif.dump(exif_dict)
            img.save(image_path, exif=exif_bytes)

            print(f"Tag metadata added for image at '{image_path}': {new_tags}")
        except Exception as e:
            print(f"Error adding tag metadata for image at '{image_path}': {e}")

def get_jpg_images(folder_path):
    # Get all .jpg files in the folder
    jpg_files = glob.glob(os.path.join(folder_path, '*.jpg')) + glob.glob(os.path.join(folder_path, '*.jpeg'))
    return jpg_files

def reset_gambar(image_path):
    folder_name = 'default\\default.jpg'
    root_path = os.path.dirname(os.path.abspath(__file__))
    print(f"root path '{root_path}'")
    folder_path = os.path.join(root_path, folder_name)
    source_exif_dict = piexif.load(folder_path)
    piexif.transplant(folder_path, image_path)
    piexif.insert(piexif.dump(source_exif_dict), image_path)
    print(source_exif_dict)

def rename_file(current_name, new_name):
    """Renames a file from current_name to new_name."""
    try:
        os.rename(current_name, new_name)
        print(f"File renamed from '{current_name}' to '{new_name}'")
    except FileNotFoundError:
        print(f"The file '{current_name}' does not exist.")
    except PermissionError:
        print(f"Permission denied. Cannot rename '{current_name}' to '{new_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

async def reset_chat():
    async with SydneyClient() as sydney:
        await sydney.reset_conversation()

async def main(image_path) -> None:
    async with SydneyClient() as sydney:
        response = await sydney.ask("give json format for title without special character or symbol just alphabet, description, and give tags as you can list all tag for this image", attachment=image_path)
        new_title = response.partition("title:")
        start_index = response.find("{")
        end_index = response.rfind("}")

        # Extract the substring between the first "{" and the last "}"
        json_content = response[start_index:end_index+1]
        if json_content.strip():
            try:
                data = json.loads(json_content)
                title = data["title"]
                tags = data["tags"]
                directory, file_name = os.path.split(image_path)
                newPath = os.path.join(directory,f"{title}")
                print(f"newpath = {newPath}")
                print(f"tags = {tags}")
                rename_file(image_path,f"{newPath}.jpg")
                edit_tag_metadata(f"{newPath}.jpg",tags,title)
                print(data)
            except json.decoder.JSONDecodeError as e:
                print("Error decoding JSON:", e)
            except KeyError as e:
                print("Error accessing title:", e)
        else:
            print(f"JSON string is empty '{json_content}'")
if __name__ == "__main__":
    # rubah dengan folder kalian setiap \ tambahkan \
    # example : C:\\Users\\sethep\\Downloads\\shutterstock
    default_path = "images" 
    root_path = os.path.dirname(os.path.abspath(__file__))
    folder_path = root_path + default_path
    jpg_files = get_jpg_images(folder_path)
    while True:
        prompt = input("pilih 1 untuk reset dan pilih 2 ketika sudah reset: ")
        if prompt == "1":
            for file in jpg_files:
                reset_gambar(file)
            continue
        elif prompt == "2":
            for file in jpg_files:
                asyncio.run(main(file))
            break
        elif prompt == "0":
            asyncio.run(reset_chat())
            break
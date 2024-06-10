import asyncio
import os
from sydney import SydneyClient
import io
import pathlib
import json
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
import piexif
import glob

os.environ["BING_COOKIES"] = "C_Auth=; _C_Auth=; _gcl_au=1.1.1448956925.1714043638; MC1=GUID=ccf20e3da5934cfa85b6c500681c34cb&HASH=ccf2&LV=202404&V=4&LU=1714128332126; _C_Auth=; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=A0C130DE030946A692CA0AEA4122C147&dmnchg=1; MUIDB=0A6CBF02E6E46BD623ABAB69E7B26ADF; ak_bmsc=5EBE66527E4DC472826F619773A5D865~000000000000000000000000000000~YAAQzUvWF8GowrGPAQAAvuPPzxd/5WMIcDUdkpK02tvm6SUXioVZETzPdMFv5gX540l94ZIrBGCnnSkGiGPzBQAUfV/RRIvLHMYbNZUgg51eyzpnP/CSskxmZBTCn9Pxt6f6WHMSwGKEOZYtgmHeh+AqViIJY9BMUYARlcLk+eN2xbmpBG8wGMicMlMTybqjybwm3IfC9mbqELOvAHFhqq9AT0m4oS6hLBn6hY4G3ONgD1oGbhwtxiwJNP+XtmU02/1HGxz2IygqGV8EiFP+XjWVpuKRfOyShxQwnp3voOfuil+8OOrbNCnpfoSYiCiXeD4kOp6Vq1JrhJyvNX2XsLHQuVB6WUP4VuAzfoYw0JjcwD/csk1r+bgssmjyfXvD0vJVdA274vhCzSYRKA==; MUID=0A6CBF02E6E46BD623ABAB69E7B26ADF; _Rwho=u=d&ts=2024-05-31; CSRFCookie=e169ba50-ee9f-422e-8ae5-867066fb57dc; ANON=A=9C06A6CAF043C0C8959B599CFFFFFFFF&E=1dd4&W=1; NAP=V=1.9&E=1d7a&C=vVqTKECtaSlsT4Q1dVjYcQaVYuzI0jnRrJjJbH49yssAS26AlV_xQQ&W=1; PPLState=1; KievRPSSecAuth=FACSBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACEeMawjvzkbXUAQ+9jbipcQbPPEffpdMsYQoDHysppocfsEIFVXcbf6mvYaVotEcwMRZNiXBiDY6joMESnfcFu/7ZRpU6+3qx8nb/gh7evTx+rff34upObEoJhe41tHhEzEzTv1qhWlj5nUFyY8z1ZGXFL8jWw72r9+1ZKCFHNSV8QZenbjz030kNZAF/YNdbpaVvC+bg4ZrTM692E50TTQWHEDajqdNrFpoZcMvIqnmXSiY+CZAVQRmzl7oTprYARjsbBU+tKVYBOarMv9GVc4sgOI/AhfKSsZfuV/TUPvyDNl59jD+88TWYNSjSe0ulUb1h9Fg1+dRwHB4YgiuL2ThaTlemrCKFDsPjHjfu4cGd18DooQpqPI9AXMAGz4BuatLZtV3RtllLSDZtf4vlylQVYRSOKAhrw0hnPe/GFVa1LIEauDU2PY9GaIAy68lCtZqU2wEdZwE87qXbknmYKNMqbIhVLZiNngDdEhxt8j+gbsxlE9NIfwdL363J9Ptvvj9Ug4h5mxZv7rLbXoHGxPHSlYGX3WnDU5q50SRd+cL7oRuBCH3Ww8Kl72Ok7r5s44x/+GlazT+bGPry0o+UASpoJy4WF9K0JoNaxj/MokwfQxmPi7g6yqXMNrK9JVXMQNYdT18bdBUpIBkM3Pm5K/RR1lIBZthW1bIILw3WmUA7Eh6mQhk3RM+JE8UJg8JqIEilteBRTKEBZvi76iKOHjIkOdOKBUB5PIiWHdzkvAbw8/4geHxrO6Uu8e7ySu5d0ZcDtCN3LqSn/N91dWv1IwEW0qmF71LsDYJ6AtTORHL6dBfYsRaOnka0t++yRMVNQOSV/DxEDYcFsHZn1SZtIhs/G5EeicQQWHV8SmIsL75650uoOBMZPPBabzh9HM8QqzhElqZh2NwadWjzdKqUCEyLLIf4O3EZwQYiq0aOWf6rKuB3alU6ikKrJV/m95Tb4Uw1mH6d0gLOa+nmA75KDfZWN/LKAivYbLqfYol1FbKLfCUbSQhyI+8eYIYXytGcALU+dIWeul0GLq1jwO0v77DBtKUF4oa1cmwsycr2RITLOV4mlCDfMYqrHDFRSPJldDuAkgmbeyQH81B2oxjhI4joFYVFxiHv71mugAGkltdT3F99vRwC/0+1qL8PcJspHOUaG2qjoLV4ecFsgGoLQUgNL2f7OWmaOUlPur5Bb/j08sxuqh1c1XEXoGuUhy+plHmXh02u22NpsaMG5arddFapr6jW8VnUZNoVeh8uRb1aqXQ9PPOnGmFurMFufGMVau5lsAw+GpsjdgRo5/KKBfC6t02Q/l4btAV19edpy+a8/pCvsizG3p7hjjCrCAlG93eWD41Iap4h78kcCqCXYI39cCdboFDuBx0IlDLePhnkkNX6ynjaoaqo5ZwTIVylDLmr+VJunw3H10rTnPDWrf1FP/ZSHF0cvVKYGLVusf413qwFdXDH1/z5kspQDv4LFObE8ISJhuahbkUAIMaZeatKS35yt8tRadltcbKVwJe; _U=1GvuXQtTzNFVLGmbFk3AttDDpfJf8MjFB3LegHXQ358wk9HBFDklKlc8IRSN7yz1y8ySGU1Fs6IxndADyI1fCgto5Hg8WlACn_VKcQ9lTJKUr9jYCjAhO4eNG19pooQSz7x43DLXVvsK3SdE8nAxtrvKzVwBv1-vv_P1BY_IDixMCJUgPsn-FPtocL0u2ugrWZWoKOAoJwIdtb-oBiiO4n2FfrObw-whE4_yMVw2hbaE; WLS=C=7e77e0bb03e4825b&N=dickysuryo; WLID=IJTlXlD3MEaBW4EmITiuklTaLdqjU6Zbu1iAtXY7HWNWPOW/uGSd0GYtAsh5lgJXpsgCT/jtlBeNJdiYROt1dbOs1jXCjMg1/qUTWqm5TZQ=; _SS=SID=27D06F46CDC7663A28E77BD6CCA86701&R=0&RB=0&GB=0&RG=0&RP=0; GI_FRE_COOKIE=gi_prompt=1; _clck=1ohef47%7C2%7Cfm8%7C0%7C1612; _clsk=1p2eo0m%7C1717181010727%7C4%7C1%7Ct.clarity.ms%2Fcollect; MMCASM=ID=09134B9309324591A818D72281E4DD89; SRCHUSR=DOB=20240531&T=1717178459000&POEX=W&TPC=1717181014000; _EDGE_S=SID=27D06F46CDC7663A28E77BD6CCA86701&mkt=en-id&ui=id-id; _RwBf=r=0&ilt=1&ihpd=1&ispd=0&rc=0&rb=0&gb=0&rg=0&pc=0&mtu=0&rbb=0&g=0&cid=&clo=0&v=4&l=2024-05-31T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&ard=0001-01-01T00:00:00.0000000&rwdbt=0001-01-01T16:00:00.0000000-08:00&rwflt=0001-01-01T16:00:00.0000000-08:00&o=0&p=MSAAUTOENROLL&c=MR000T&t=1876&s=2024-05-31T18:01:52.3522066+00:00&ts=2024-05-31T18:50:29.0469535+00:00&rwred=0&wls=2&wlb=0&wle=0&ccp=2&cpt=0&lka=0&lkt=0&aad=0&TH=&mta=0&e=ZHVaGCmlHDZTvXkKCYSS6bg1zt8--lndJGJgqqxuKfXu8o_sFj3Lyc5jRmbFXTqUpxfVV0YR3w80D1s7fwyp_w&A=9C06A6CAF043C0C8959B599CFFFFFFFF; _uetsid=d99723801f7711efaa44c9a3d3cbe829; _uetvid=d9973ff01f7711ef8d04474592cd34d6; _C_ETH=1; bm_sv=17C06BCA569EC3154FA9AB891BB72EEC~YAAQlu84F0cwLaWPAQAAM2v9zxfrea5bWcXrTfxrIttX+Cjll7H7DbwzLd3FSM116lKbhutgWTvL7rmiTW7V8yPZt1AVfn2zTdPbDdkRcXD1ael20dk30Jv5vm6N0ZkMzVx/3vlqbTuCZ5OzEdU1D0vVQATE11lqkwQLqbr6MOI0+2EAaNC4ifit6ZakUOXzDIp2KejU0iMYygbCneNJ2gFKzbOFqubOU2sU5sIh3fnRoF+ih2cwB5jfUFyBbphObO9pHQ==~1; SRCHHPGUSR=SRCHLANG=id&BRW=XW&BRH=T&CW=1701&CH=1305&SCW=1701&SCH=796&DPR=1.0&UTC=420&DM=1&PV=15.0.0&WTS=63852775259&HV=1717181426&PRVCW=2560&PRVCH=1305&CIBV=1.1764.0&cdxtone=Balanced&cdxtoneopts=galileo,flxvoice"

def edit_tag_metadata(image_path, new_tags,title):
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
    jpg_files = glob.glob(os.path.join(folder_path, '*.jpg'))
    return jpg_files


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

async def main(image_path) -> None:
    async with SydneyClient() as sydney:
        response = await sydney.ask("Give title for this image , and description , and tags, with format json", attachment=image_path)
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
            print("JSON string is empty")
if __name__ == "__main__":
    # rubah dengan folder kalian setiap \ tambahkan \
    # example : C:\\Users\\sethep\\Downloads\\shutterstock
    folder_path = "C:\\Users\\sethep\\Downloads\\shutterstock" 
    jpg_files = get_jpg_images(folder_path)
    for file in jpg_files:
        asyncio.run(main(file))
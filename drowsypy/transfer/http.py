import os
import tempfile
import shutil
import requests
from urllib.parse import urljoin
import urllib.request as urllib
import ssl
from bs4 import BeautifulSoup


class HTTPClient:
    def __init__(self) -> None:
        pass
    
    def check_url(self, url:str=None) -> bool:
        """
        Check if the URL is valid.

        Args:
            url : str
                URL to check.
        
        Returns:
            bool
                True : URL is valid.
                False : URL is invalid.
        """
        if url == None :
            message = "check_url() : URL missing"
            print(message)
            return False

        try :
            response = requests.head(url, verify=False)
            response.raise_for_status()
        except requests.HTTPError as e:
            message = f"{url} : {e}"
            print(message)
            return False
        except requests.RequestException as e:
            message = f"Error during requests to {url} : {str(e)}"
            print(message)
            return False
        
    def search(self, base_url, ext):
        if base_url[-1] != '/':
            base_url += '/'
        response = requests.get(base_url, verify=False)
        if response.status_code == 200:
            urls = []
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and (href.endswith(f".{ext.lower()}") or href.endswith(f".{ext.upper()}")):
                    urls.append(urljoin(base_url, href))
            print(f"Found {len(urls)} data files {base_url}")
            return urls
        elif response.status_code == 404:
            print(f"Error: {base_url} not found")
            return []
        else :
            print(f"Error: {base_url} status code {response.status_code}")
            return []


    def download_url(self, source:str=None, destination:str=None, overwrite:bool=False) -> bool:
        context = ssl._create_unverified_context()
        fp = urllib.urlopen(source, timeout=30, context=context)
        content = fp.read()
        destination = open(destination, "wb")
        destination.write(content)
        fp.close()
        destination.close()


    def download_file(self, source:str=None, destination:str=None, overwrite:bool=False) -> bool:
        """
        Download file from HTTP.

        Args:
            remote_path : str
                Remote file path.
            local_path : str
                Local file path.
        
        Returns:
            bool
                True : Success to download file.
                False : Fail to download file.
        """
        if source == None or destination == None :
            message = "download() : source or destination missing"
            print(message)
            return False

        if os.path.exists(destination) and not overwrite:
            message = f"download() : {destination} is already existed"
            print(message)
            return False


        with tempfile.NamedTemporaryFile() as f:
            temporary = f.name

        try :
            with requests.get(source, stream=True, verify=False) as response:
                response.raise_for_status()
                with open(temporary, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
            shutil.move(temporary, destination)
            message = f"download() : Downloaded {source} to {destination}"
            print(message)
        except requests.HTTPError as e:
            message = f"{source} : {e}"
            return False
        except requests.RequestException as e:
            message = f"Error during requests to {source} : {str(e)}"
            print(message)
            return False
        return True

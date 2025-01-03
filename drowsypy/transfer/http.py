import os
import tempfile
import shutil
import requests


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

    def download(self, source:str=None, destination:str=None, overwrite:bool=False) -> bool:
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

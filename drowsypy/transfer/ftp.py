import os
import tempfile
import shutil
import ftplib


class FTPClient:
    def __init__(self, address:str=None, port:int=None, username:str=None, password:str=None) -> None:
        
        # Validate server info
        if (address == "") or (address == None) :
            message = "Address missing"
            raise Exception(message)
        if ":" in address :
            address, port = address.split(":")
            port = int(port)
        self.host = address
        self.port = port

        # Validate login info
        if (username != None and password == None) or (username == None and password != None) :
            message = "Username or password missing"
            raise Exception(message)
        self.user = username
        self.passwd = password

        self.session = None

    def connect(self) -> bool:
        """
        Connect to FTP.

        Args:
            None
        
        Returns:
            bool
                True : Success to connect FTP.
                False : Fail to connect FTP.
        """
        # Connect to FTP
        try :
            ftp = ftplib.FTP(timeout=30)
            ftp.connect(self.host, self.port)
            message = f"connect() : Connect ftp\t{self.host}:{self.port}"
            print(message)
        except Exception as e :
            message = f"connect() : Fail to connect ftp.\t{e}"
            print(message)
            return False

        # Login
        try :
            # anonymous
            if(self.user == None and self.passwd == None) :
                ftp.login()
                message = f"connect() : Login ftp as anonymous"
            # login with username and password
            else :
                ftp.login(user=self.user, passwd=self.passwd)
                message = f"connect() : Login ftp\t{self.user}"
            print(message)
        except Exception as e :
            message = f"connect() : Fail to login ftp.\t{e}"
            print(message)
            return False
        self.session = ftp
        return True

    def check_connection(self) -> bool :
        """
        Check FTP connection.

        Args:
            None

        Returns:
            bool
                True : FTP is connected.
                False : FTP is not connected
        """
        session = self.session
        if(session == None):
            message = "check_connection() : There is no session."
            print(message)
            return False
        try:
            session.voidcmd("NOOP")
            message = "check_connection() : Success to check connection."
            print(message)
        except Exception as e:
            message = f"check_connection() : Fail to check connection.\t{e}"
            print(message)
            return False
        return True

    def disconnect(self) -> bool :
        """
        Disconnect FTP.

        Args:
            None

        Returns:
            bool
                True : Success to disconnect FTP.
                False : Fail to disconnect FTP.
        """
        if(self.session == None):
            message = "disconnect() : There is no FTP session to close."
            print(message)
            return False
        # self.session.close()
        self.session.quit()
        self.session = None
        message = "disconnect() : FTP is disconnected"
        print(message)
        return True

    def check_directory(self, directory:str) -> bool :
        """
        Check directory in FTP.

        Args:
            directory : str
                Directory path.
        
        Returns:
            bool
                True : Directory is existed.
                False : Directory is not existed.
        """
        ftp = self.session
        if not self.check_connection() :
            return False
        try :
            ftp.cwd(directory)
            message = f"check_directory() : Directory is existed.\t{directory}"
            print(message)
        except Exception as e:
            if "550" in str(e):
                message = f"check_directory() : Directory is not existed or can't access.\t{directory}"
                print(message)
                return False
            else :
                message = f"check_directory() : Fail to check directory.\t{e}"
                print(message)
        return True

    def check_file_path(self, file_path:str) -> bool :
        """
        Check file path in FTP.

        Args:
            file_path : str
                File path.

        Returns:
            bool
                True : File path is existed.
                False : File path is not existed.
        """
        ftp = self.session
        if not self.check_connection() :
            return False
        try :
            ftp.size(file_path)
            message = f"check_file_path() : File path is existed.\t{file_path}"
            print(message)
        except Exception as e:
            if "550" in str(e):
                message = f"check_file_path() : File path is not existed or can't access.\t{file_path}"
                print(message)
                return False
            else :
                message = f"check_file_path() : Fail to check file path.\t{e}"
                print(message)
        return True
    
    def get_file_list_in_directory(self, directory:str=None) -> list :
        """
        Get file list in directory of FTP.

        Args:
            directory : str
                Directory path.
            pattern : str
                File name pattern.

        Returns:
            file_list : list
                File list.
        """
        file_list = []
        if directory == None :
            message = "get_file_list_in_directory() : directory missing"
            print(message)
            return file_list
        
        if not self.check_connection() :
            return False
        ftp = self.session

        try :
            file_list = ftp.nlst(directory)
            message = f"get_file_list_in_directory() : Get file list in {directory}"
            print(message)
        except Exception as e :
            message = f"get_file_list_in_directory() : Fail to get file list in {directory}\t{e}"
            print(message)
        return file_list

        # directory_step = directory.split("/")
        # ftp.cwd("/")
        # for step in directory_step :
        #     try :
        #         ftp.cwd(step)
        #     except Exception as e :
        #         self.logger.error(f"ftp_get_file_list_in_directory() : Fail to change directory\t{e}")
        #         return None
        # file_list = ftp.nlst()
        # if pattern is not None :
        #     file_list = [file_name for file_name in file_list if re.match(pattern, file_name)]
        # return file_list

    def download(self, source:str=None, destination:str=None, overwrite:bool=False) -> bool :
        """
        Download file from FTP.

        Args:
            source : str
                Source file path.
            destination : str
                Destination file path.
            overwrite : bool
                Overwrite flag.
        
        Returns:
            bool
                True : Success to download file.
                False : Fail to download file.        
        """
        if source == None or destination == None :
            message = "download() : source or destination missing"
            print(message)
            return False

        if not self.check_connection() :
            return False
        ftp = self.session
        
        if os.path.exists(destination) and not overwrite:
            message = f"download() : {destination} is already existed"
            print(message)
            return False

        with tempfile.NamedTemporaryFile() as f:
            temporary = f.name

        try :
            with open(temporary, "wb") as t :
                ftp.retrbinary(f"RETR {source}", t.write)
            shutil.move(temporary, destination)
            message = f"download() : Downloaded {source} to {destination}"
            print(message)
        except Exception as e :
            message = f"download() : Fail to download {source} to {destination}\t{e}"
            print(message)
            return False
        return True

    def upload(self, source:str, destination:str, overwrite:bool=False) -> bool :
        """
        Upload file to FTP.

        Args:
            source : str
                Source file path.
            destination : str
                Destination file path.
            overwrite : bool
                Overwrite flag.

        Returns:
            bool
                True : Success to upload file.
                False : Fail to upload file.
        """
        if source == None or destination == None :
            message = "download() : source or destination missing"
            print(message)
            return False

        if not self.check_connection() :
            return False
        ftp = self.session

        if self.check_file_path(destination) and not overwrite :
            message = f"upload() : {destination} is already existed"
            print(message)
            return False
        
        try :
            with open(source, "rb") as src_path :
                ftp.storbinary(f"STOR {destination}", src_path)
            message = f"upload() : Uploaded {source} to {destination}"
            print(message)
        except Exception as e :
            message = f"upload() : Fail to upload {source} to {destination}\t{e}"
            print(message)
            return False
        
        return True

import os
import tempfile
import ftplib
import shutil


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


        




class FTP:
    def __init__(self, address:str="", port:int=21, username:str="", password:str="") -> None:
        """
        Initialize FTP.

        Args:
            address : str
                FTP address.
            port : int
                FTP port.
            username : str
                FTP username.
            password : str
                FTP password.

        Returns:
            None
        """
        self.address = address
        self.port = port
        self.username = username
        self.password = password
        self.session = None
        self.logger = None

    def connect(self):
        """
        Connect to FTP.

        Args:
            None

        Returns:
            bool
                True : Success to connect FTP.
                False : Fail to connect FTP.
        """
        #
        # Get host and port.
        #
        if (self.address == "") or (self.address == None) :
            message = "connect() : address missing"
            print(message)
            if self.logger != None :
                self.logger.error(message)
            return False

        if ":" in self.address :
            host, port = self.address.split(":")
            port = int(port)
        else :
            host, port = self.address, self.port

        if (self.username != None and self.password == None) or (self.username == None and self.password != None) :
            message = "connect() : id or pw missing"
            print(message)
            if self.logger != None :
                self.logger.error(message)
            return False

        #
        # Connect Ftp.
        #
        try :
            ftp = ftplib.FTP(timeout=30)
            ftp.connect(host, port)
            message = f"connect() : Connect ftp\t{host}:{port}"
            print(message)
            if self.logger != None :
                self.logger.info(message)
        except Exception as e :
            message = f"connect() : Fail to connect ftp.\t{e}"
            print(message)
            if self.logger != None :
                self.logger.error(message)
            return False

        #
        # Login.
        #
        try :
            # anonymous
            if(self.username == None and self.password == None) :
                ftp.login()
            else :
                ftp.login(user=self.username, passwd=self.password)
            message = f"connect() : Login ftp\t{host}:{port}"
            if self.logger != None :
                self.logger.info(message)
            print(message)
        except Exception as e :
            message = f"connect() : Fail to login ftp.\t{e}"
            print(message)
            if self.logger != None :
                self.logger.error(message)
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
            if self.logger != None :
                self.logger.error(message)
            return False
        try:
            session.voidcmd("NOOP")
            message = "check_connection() : Success to check connection."
            print(message)
            if self.logger != None :
                self.logger.info(message)
        except Exception as e:
            message = f"check_connection() : Fail to check connection.\t{e}"
            print(message)
            if self.logger != None :
                self.logger.error(message)
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
            if self.logger != None :
                self.logger.error(message)
            return False
        self.session.close()
        self.session = None
        message = "disconnect() : FTP is disconnected"
        print(message)
        if self.logger != None :
            self.logger.info(message)
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

    def download(self, source:str, destination:str, overwrite:bool=False) -> bool :
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
        if not self.check_connection() :
            return False

        with tempfile.TemporaryDirectory() as temp_dir :
            temporary = os.path.join(temp_dir, os.path.basename(destination))
            if not os.path.exists(destination) :
                try :
                    with open(temporary, "wb") as t :
                        self.ftp_session.retrbinary(f"RETR {source}", t.write)
                    shutil.move(temporary, destination)
                except Exception as e :
                    self.logger.error(f"ftp_download() : Fail to download {source} to {destination}\t{e}")
                    return False
                self.logger.info(f"ftp_download() : Downloaded {source} to {destination}")
            else :
                if overwrite :
                    try :
                        with open(temporary, "wb") as t :
                            self.ftp_session.retrbinary(f"RETR {source}", t.write)
                        shutil.move(temporary, destination)
                    except Exception as e :
                        self.logger.error(f"ftp_download() : Fail to download {source} to {destination}\t{e}")
                        return False
                    self.logger.info(f"ftp_download() : Downloaded {source} to {destination}")
                else :
                    self.logger.info(f"ftp_download() : {destination} is already existed")        
        return True
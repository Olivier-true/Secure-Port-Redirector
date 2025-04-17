import os, uuid, http.client, json
from hashlib import sha512, sha1
from base64 import b64decode, b64encode
from time import time

class requests:

    class get:
        def __init__(self, url, headers = {}, stream = False):
            self.headers = headers
            self.stream = stream
            proto, host = url.split("://")
            hostUri = host.split("/")
            host = hostUri[0]
            uri = "/" + "/".join(hostUri[1:])
            print(proto, host, uri)
            self.conn = http.client.HTTPSConnection(host)
            self.headers["Host"] = host
            self.conn.request("GET", uri, headers=self.headers)
            self.response = self.conn.getresponse()
            self.status_code = f"<Response {self.response.status} {self.response.reason}>"
            self.headers = self.response.headers

            if self.stream:
                self.raw = self.response
                self.content = b""
                self.text = ""
            else:
                self.content = self.response.read(int(self.response.headers["Content-Length"]))
                self.raw = self.response
                try:
                    self.text = self.content.decode()
                except:
                    pass

        

def getDotnet():
    if not(os.path.exists("dotnet.zip")) and not(os.path.exists("dotnet")):
        r = requests.get("https://builds.dotnet.microsoft.com/dotnet/Sdk/8.0.408/dotnet-sdk-8.0.408-win-x64.zip", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3"
        }, stream=True)
        length = int(r.headers.get("Content-Length"))
        print(length)
        sha = sha512()
        with open("dotnet.zip", "wb") as f:
            sz = 0
            for i in range(0, length, 262144):
                data = r.raw.read(262144)
                sha.update(data)
                sz += len(data)
                #print(sz)
                f.write(data)
            if sz < length:
                data = r.raw.read(length - sz)
                sha.update(data)
                f.write(data)
                f.close()
        print("valid checksum =", sha.hexdigest() == "49ff4363663d28b8f55b7af4cad4cb469cf9ff1bc6e826117b2381180a7c5e7c8d5aaefd02c7b5ae06c87609816858bbf554c68a8308ac6260d3d5b432123272")
    else:
        print("[i] dotnet already installed.")

def get7zr():
    if not(os.path.exists("7zr.exe")):
        data7zr = requests.get("https://www.7-zip.org/a/7zr.exe", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3"}
        ).content

        open("7zr.exe", "wb").write(data7zr)
        print("[+] 7zr.exe installed.")
    else:
        print("[i] 7zr already install.")

def get7za():
    if not(os.path.exists("7za.exe")):
        data7za = requests.get("https://www.7-zip.org/a/7z2409-extra.7z", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3"}
        ).content
        open("7za.7z", "wb").write(data7za)

        os.system("7zr.exe x 7za.7z -y -o7zax")
        for f in os.listdir("./7zax/x64"):
            try:
                os.rename(f"./7zax/x64/{f}", f)
            except:
                pass
        
        print("[+] 7za.exe installed.")
    else:
        print("[i] 7za already install.")

def unzipDotnet():
    if not(os.path.exists("dotnet")):
        os.system("7za.exe x dotnet.zip -y -odotnet")
        print("[+] dotnet is installed.")
    else:
        print("[i] dotnet already installed.")

def getOpenSSL() -> str:
    if not(os.path.exists("openssl.zip")):
        OPENSSLZip = requests.get("https://wiki.overbyte.eu/arch/openssl-3.5.0-win64.zip", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3"}
        ).content
        open("openssl.zip", "wb").write(OPENSSLZip)

        os.system("7za.exe x openssl.zip -y -oOpenSSL")
        open("./OpenSSL/openssl.cnf", "wb").write(requests.get("https://raw.githubusercontent.com/openssl/openssl/refs/heads/master/apps/openssl.cnf", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3"}
        ).content)

    else:
        print("[i] OpenSSL is already installed.")
    return "./OpenSSL/openssl.exe"

class Dotnet:

    def __init__(self, binary = "./dotnet/dotnet.exe"):
        self.binary = binary
    
    def call(self, cmds: list):
        cmd = self.binary + " " + " ".join(cmds)
        b64CmdLine = b64encode(cmd.encode("utf-16le")).decode()

        os.system(f"powershell.exe -e {b64CmdLine}")
    
    def run(self, projPath: str, args = []):
        self.call(["run", f"'{projPath}'"] + args)
    
    def build(self, projPath: str, args = []):
        self.call(["build", f"'{projPath}'"] + args)
    
    def publish(self, projPath: str, args = []):
        self.call(["publish", f"'{projPath}'"] + args)
    
class OpenSSL:

    def __init__(self, binary: str):
        self.binary = binary
        self.expiration = 7300 # 20 years
        self.domain = "paris.fr"
        self.customer = "paris"
        self.COUNTRY = "FR"
        self.state = "France"
        self.city = "Paris"
        
    
    def run(self, cmdLine: str):
        cmdLine = self.binary + " " + cmdLine
        b64CmdLine = b64encode(cmdLine.encode("utf-16le")).decode()

        os.system(f"powershell.exe -e {b64CmdLine}")
    
    def generateKeys(self, pubKeyPath: str, privKeyPath: str):
        pass

    def generatePfx(self, pubKeyPath: str, privKeyPath: str, password: str) -> bytes:
        return b""
    
    def generatePfx(self, password: str) -> tuple[str, bytes]:
        keyPem = f"key{str(uuid.uuid4()).split('-')[0]}.pem"
        certPem = f"cert{str(uuid.uuid4()).split('-')[1]}.pem"
        self.run(f'req -x509 -newkey rsa:4096 -keyout {keyPem} -out {certPem} -sha256 -days {self.expiration} -nodes -subj "/C={self.COUNTRY}/ST={self.state}/L={self.city}/O={self.customer}/OU={self.customer}/CN={self.domain}" -config "./OpenSSL/openssl.cnf"')#

        pfxPath = f"domain{str(uuid.uuid4()).split('-')[2]}.pfx"

        self.run(f"pkcs12 -inkey {keyPem} -in {certPem} -export -out {pfxPath} -passout pass:{password}")
        b64Cert = open(certPem, "rb").read().decode().replace("\n", "").replace("-----BEGIN CERTIFICATE-----", "").replace("-----END CERTIFICATE-----", "")
        certHash = sha1(b64decode(b64Cert)).hexdigest().upper()
        
        os.remove(keyPem)
        os.remove(certPem)
        pfxBytes = open(pfxPath, "rb").read()
        os.remove(pfxPath)
        return (certHash, pfxBytes)
get7zr()
getDotnet()
get7za()
unzipDotnet()

openssl = OpenSSL(getOpenSSL())
clientPFXPasswd = sha512(str(uuid.uuid4()).encode("utf-16") + str(uuid.uuid1()).encode("utf-32") + str(time() * 42424.2333333333).encode("utf-16")).hexdigest()
ClientPFX = openssl.generatePfx(clientPFXPasswd)
print(ClientPFX)


serverPFXPasswd = sha512(sha1(str(uuid.uuid4()).encode("utf-32")).digest() + str(uuid.uuid1()).encode("utf-16") + str(time() * 1245733.66666666666).encode("utf-32")).hexdigest()
ServerPFX = openssl.generatePfx(serverPFXPasswd)
print(ServerPFX)
conf = json.loads(open("conf.json", 'r').read())
CLIENT_RemoteIP = conf["client"]["RemoteIP"]
CLIENT_RemotePort = str(conf["client"]["RemotePort"])
CLIENT_ListenPort = str(conf["client"]["ListenPort"])
CLIENT_CertHash = ClientPFX[0]
CLIENT_PFXRAW = str(list(ClientPFX[1]))[1:-1]

CLIENT_PFXPasswd = clientPFXPasswd

CLIENT_Program = open("./CLIENT_Program.cs", "rb").read()
CLIENT_Program = CLIENT_Program.replace(b'private static string remoteIP = "127.0.0.1";', f'private static string remoteIP = "{CLIENT_RemoteIP}";'.encode())
CLIENT_Program = CLIENT_Program.replace(b'private static int port = 50000;', f'private static int port = {CLIENT_RemotePort};'.encode())
CLIENT_Program = CLIENT_Program.replace(b'private static int listenPort = 443;', f'private static int listenPort = {CLIENT_ListenPort};'.encode())
CLIENT_Program = CLIENT_Program.replace(b'private static byte[] rawClientCert = new byte[] {/*ClientPFX*/};', ('private static byte[] rawClientCert = new byte[] {' + CLIENT_PFXRAW + '};').encode())
CLIENT_Program = CLIENT_Program.replace(b'=======ClientPFXPasswd========', CLIENT_PFXPasswd.encode())

open("./client/Program.cs", "wb").write(CLIENT_Program)



SERVER_DstIP = conf["server"]["DestinationIP"]
SERVER_DstPort = str(conf["server"]["DestinationPort"])
SERVER_ListenPort = str(conf["server"]["ListenPort"])
SERVER_CertHash = ClientPFX[0] # Prend le Hash de la cle publique du Client
SERVER_PFXRAW = str(list(ServerPFX[1]))[1:-1]
SERVER_PFXPasswd = serverPFXPasswd

SERVER_Program = open("./SERVER_Program.cs", "rb").read()
SERVER_Program = SERVER_Program.replace(b'static string dstIP = "---dstIP---";', f'static string dstIP = "{SERVER_DstIP}";'.encode())
SERVER_Program = SERVER_Program.replace(b'static int dstPort = 445;', f'static int dstPort = {SERVER_DstPort};'.encode())
SERVER_Program = SERVER_Program.replace(b'static int port = 50000;', f'static int port = {SERVER_ListenPort};'.encode())
SERVER_Program = SERVER_Program.replace(b'/*ServerPFX*/', SERVER_PFXRAW.encode())
SERVER_Program = SERVER_Program.replace(b'=======ServerPFXPasswd========', SERVER_PFXPasswd.encode())
SERVER_Program = SERVER_Program.replace(b'---ClientCertHash---', CLIENT_CertHash.encode())

open("./server/Program.cs", "wb").write(SERVER_Program)


dotnet = Dotnet()
dotnet.publish("./client/client.csproj")
dotnet.publish("./server/server.csproj")
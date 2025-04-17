---

# 🔐 Secure Port Redirector (via SSLStream)

This project is a secure stream redirector developed in C#. It only redirects traffic from a port if the client is authenticated using an SSL certificate. It uses `SSLStream` to ensure secure communication between the client and the server.

## ✨ Features

- 🔁 Network stream redirection between client and server  
- 🛡️ Strong authentication via SSL certificates  
- ⚙️ Automatic certificate generation and configuration  
- 💼 Windows compatible (with .NET 8.0)  
- 🧪 Automated build & publish using `dotnet`  
- 📦 Embedded client  

---

## 🚀 Installation

> 💡 This project has only been tested on **Windows**. However, it's possible to host the server on Linux by replacing `<RuntimeIdentifier>win-x64</RuntimeIdentifier>` with `<RuntimeIdentifier>linux-x64</RuntimeIdentifier>` in `server/server.csproj`.

### Prerequisites

- A Windows machine (7, 8.1, 10, 11, Server, etc.) to generate executables with `compile.bat` and host the server  
- PowerShell  
- Internet access for downloading dependencies  

### Automatic Installation Steps

The provided Python script will automatically:
- Install .NET 8.0 SDK  
- Install 7-Zip (CLI version: `7zr.exe` / `7za.exe`)  
- Install precompiled OpenSSL for Windows  
- Generate client/server certificates  
- Modify `Program.cs` files with correct parameters  
- Build and publish both the client and server projects  

### Running the Script

## Edit the **`conf.json`** file and specify your IP addresses and corresponding ports:

```json
{
  "client": {
    "RemoteIP": "127.0.0.1", // IP of the redirector server exposed on the internet
    "RemotePort": 50000,     // Port exposed on the internet
    "ListenPort": 443        // Port where the stream will be duplicated and where you should connect (e.g., localhost:443)
  },
  "server": {
    "DestinationIP": "127.0.0.1", // IP of the machine that should receive the request (e.g., localhost:445 for a service listening on port 445 of the local machine; this can be a device on the same network like a NAS)
    "DestinationPort": 445,       // Port where the destination service is listening
    "ListenPort": 50000           // Port the redirector listens on → must be open to the internet!
  }
}
```

## After editing the configuration, run: `compile.bat`

### > The redirector server is located at: `./server/bin/Release/net8.0/server.exe`  
### > The client is located at: `./client/bin/Release/net8.0/client.exe`

## 🧪 Example Usage

### Once the binaries are compiled:

### 1. Launch the server on the machine where the redirector port is exposed:
```bash
./server/bin/Release/net8.0-windows/server.exe
```

### 2. Launch the client on any Windows machine:
```bash
./client/bin/Release/net8.0-windows/client.exe
```

## You can now access your service via `localhost:<ListenPort>` on the client machine from anywhere.

## 📝 License

### This project is licensed under the MIT License. See the LICENSE file for more details.

## 🤝 Contributions

#### Contributions are welcome! Feel free to open an issue or a pull request to improve the project or add new features.
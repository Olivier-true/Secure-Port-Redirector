// See https://aka.ms/new-console-template for more information
using System;
using System.Collections;
using System.Net;
using System.Net.Sockets;
using System.Net.Security;
using System.Security.Authentication;
using System.Text;
using System.Security.Cryptography.X509Certificates;
using System.IO;

public sealed class SslTcpServer
{
    static X509Certificate2 serverCertificate2 = null;
    static int port = 50000;
    static string dstIP = "---dstIP---";
    static int dstPort = 445;

    static bool App_CertificateValidation(Object sender, X509Certificate certificate, X509Chain chain, SslPolicyErrors sslPolicyErrors) {
        if (sslPolicyErrors == SslPolicyErrors.None) { return true; }
        if (sslPolicyErrors == SslPolicyErrors.RemoteCertificateChainErrors) { return true; }
        return true;
    }
    public static void RunServer(byte[] certificate)
    {
        serverCertificate2 = new X509Certificate2(certificate, "=======ServerPFXPasswd========");

        TcpListener listener = new TcpListener(IPAddress.Any, port);
        listener.Start();
        while (true)
        {
            Console.WriteLine("Waiting for a client to connect...");
            TcpClient client = listener.AcceptTcpClient();
            Task.Run(() => ProcessClient(client));
        }
    }
    static void ProcessClient (TcpClient client)
    {
        SslStream sslStream = new SslStream(
            client.GetStream(), false,
            App_CertificateValidation);

        try
        {
            sslStream.AuthenticateAsServer(serverCertificate2, clientCertificateRequired: true, SslProtocols.Tls13, checkCertificateRevocation: false);
            

            DisplaySecurityLevel(sslStream);
            DisplaySecurityServices(sslStream);
            DisplayCertificateInformation(sslStream);
            DisplayStreamProperties(sslStream);

            X509Certificate? clientCert = sslStream.RemoteCertificate;
            if(clientCert != null) {
                string clientCertHashString = clientCert.GetCertHashString();
                Console.WriteLine("Remote certificate: " + clientCertHashString);
                if(clientCertHashString == "---ClientCertHash---") {
                    RedirectSslStream2Ns(sslStream);
                } else {
                    Console.WriteLine("[-] bad Remote Certificate: " + clientCertHashString);
                }
            } else {
                sslStream.Close();
                client.Close();
            }
            
            
        }
        catch (AuthenticationException e)
        {
            Console.WriteLine("Exception: {0}", e.Message);
            if (e.InnerException != null)
            {
                Console.WriteLine("Inner exception: {0}", e.InnerException.Message);
            }
            Console.WriteLine ("Authentication failed - closing the connection.");
            sslStream.Close();
            client.Close();
            return;
        }
        finally
        {
            sslStream.Close();
            client.Close();
        }
    }
    static void RedirectSslStream2Ns(SslStream sslStream) {
        TcpClient client = new TcpClient();
        client.Connect(dstIP, dstPort);
        NetworkStream ns = client.GetStream();
        Console.WriteLine("[i] Connect To " + dstIP);
        Task.Run(() => {
            sslStream.CopyTo(ns);
        });

        Task.Run(() => {
            ns.CopyTo(sslStream);
        }).Wait();

    }
        static void DisplaySecurityLevel(SslStream stream)
        {
        Console.WriteLine("Cipher: {0} strength {1}", stream.CipherAlgorithm, stream.CipherStrength);
        Console.WriteLine("Hash: {0} strength {1}", stream.HashAlgorithm, stream.HashStrength);
        Console.WriteLine("Key exchange: {0} strength {1}", stream.KeyExchangeAlgorithm, stream.KeyExchangeStrength);
        Console.WriteLine("Protocol: {0}", stream.SslProtocol);
        }
        static void DisplaySecurityServices(SslStream stream)
        {
        Console.WriteLine("Is authenticated: {0} as server? {1}", stream.IsAuthenticated, stream.IsServer);
        Console.WriteLine("IsSigned: {0}", stream.IsSigned);
        Console.WriteLine("Is Encrypted: {0}", stream.IsEncrypted);
        }
        static void DisplayStreamProperties(SslStream stream)
        {
        Console.WriteLine("Can read: {0}, write {1}", stream.CanRead, stream.CanWrite);
        Console.WriteLine("Can timeout: {0}", stream.CanTimeout);
        }
    static void DisplayCertificateInformation(SslStream stream)
    {
        Console.WriteLine("Certificate revocation list checked: {0}", stream.CheckCertRevocationStatus);
        X509Certificate localCertificate = stream.LocalCertificate;
        if (stream.LocalCertificate != null)
        {
            Console.WriteLine("Local cert was issued to {0} and is valid from {1} until {2}.",
                localCertificate.Subject,
                localCertificate.GetEffectiveDateString(),
                localCertificate.GetExpirationDateString());
            } else
        {
            Console.WriteLine("Local certificate is null.");
        }
        // Display the properties of the client's certificate.
        X509Certificate remoteCertificate = stream.RemoteCertificate;
        if (stream.RemoteCertificate != null)
        {
        Console.WriteLine("Remote cert was issued to {0} and is valid from {1} until {2}.",
            remoteCertificate.Subject,
            remoteCertificate.GetEffectiveDateString(),
            remoteCertificate.GetExpirationDateString());
        } else
        {
            Console.WriteLine("Remote certificate is null.");
        }
    }
    private static void DisplayUsage()
    {
        Console.WriteLine("To start the server specify:");
        Console.WriteLine("serverSync certificateFile.cer");
        Environment.Exit(1);
    }
    public static int Main(string[] args)
    {
        string certificate = "domain.pfx";
        SslTcpServer.RunServer (new byte[] {/*ServerPFX*/});
        return 0;
    }
}
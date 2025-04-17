// See https://aka.ms/new-console-template for more information
using System;
using System.Collections;
using System.Net;
using System.Net.Security;
using System.Net.Sockets;
using System.Security.Authentication;
using System.Text;
using System.Security.Cryptography.X509Certificates;
using System.IO;


public class SslTcpClient
{
    private static string remoteIP = "127.0.0.1";
    private static int port = 50000;
    private static int listenPort = 443;
    private static byte[] rawClientCert = new byte[] {/*ClientPFX*/};
    static bool App_CertificateValidation(Object sender, X509Certificate certificate, X509Chain chain, SslPolicyErrors sslPolicyErrors) {
        if (sslPolicyErrors == SslPolicyErrors.None) { return true; }
        if (sslPolicyErrors == SslPolicyErrors.RemoteCertificateChainErrors) { return true; } //we don't have a proper certificate tree
        return true;
    }
    public static void RunClient(string ipAddress, TcpClient RClient)
    {            
        TcpClient client = new TcpClient(ipAddress, port);
        Console.WriteLine("Client connected.");
        SslStream sslStream = new SslStream(
            client.GetStream(),
            false,
            App_CertificateValidation
            );

        X509Certificate2 clientCert = new X509Certificate2(rawClientCert, "=======ClientPFXPasswd========");
        var clientCertificateCollection = new X509CertificateCollection(new X509Certificate[] { clientCert });
        try
        {
            NetworkStream ns = RClient.GetStream();
            sslStream.AuthenticateAsClient(ipAddress, clientCertificateCollection, SslProtocols.Tls13, false);

            Task.Run(() => {
            sslStream.CopyTo(ns);
        });

        Task.Run(() => {
            ns.CopyTo(sslStream);
        });
        }
        catch (AuthenticationException e)
        {
            Console.WriteLine("Exception: {0}", e.Message);
            if (e.InnerException != null)
            {
                Console.WriteLine("Inner exception: {0}", e.InnerException.Message);
            }
            Console.WriteLine ("Authentication failed - closing the connection.");
            client.Close();
            return;
        }
    }
    private static void DisplayUsage()
    {
        Console.WriteLine("To start the client specify:");
        Console.WriteLine("clientSync machineName [serverName]");
        Environment.Exit(1);
    }
    public static int Main(string[] args)
    {
        string machineName = remoteIP;
        TcpListener listener = new TcpListener(IPAddress.Any, listenPort);
        bool _ = true;
        listener.Start();
        while(_) {
            TcpClient client = listener.AcceptTcpClient();
            try {
                Task.Run(() => SslTcpClient.RunClient (machineName, client));
            } catch(Exception e) {
                Console.WriteLine(e.Message);
            }
        }
        
        return 0;
    }
}
#!/usr/bin/python

import SOAPpy, base64, re
from datetime import datetime

class myHTTPTransport(SOAPpy.HTTPTransport):
        username = None
        passwd = None

        @classmethod
        def setAuthentication(cls,u,p):
                cls.username = getAuth('vsscreds.txt')['username']
                cls.passwd = getAuth('vsscreds.txt')['password']

        def call(self, addr, data, namespace, soapaction=None, encoding=None, http_proxy=None, config=SOAPpy.Config, timeout=None):

            if not isinstance(addr, SOAPpy.SOAPAddress):
                addr = SOAPpy.SOAPAddress(addr, config)

            if self.username != None:
                addr.user = self.username+":"+self.passwd
            
            return SOAPpy.HTTPTransport.call(self, addr, data, namespace, soapaction, encoding, http_proxy, config)

def getAuth(fName):
    f = open(fName)
    creds = {}

    for line in f:
        creds.update( dict(re.findall(r'(\S+)=(".*?"|\S+)', line)))
    f.close()
    return creds

if __name__ == '__main__':



    # Getting the instance of Server
    input = datetime.now()
    creds = getAuth('vsscreds.txt')
    #myHTTPTransport.setAuthentication(creds['username'],creds['password'])
    namespace = "http://indlpscm1/"
    wsdlFile = 'http://indlpscm1/SourceSafe/VssService.asmx?WSDL'
    wsdlFile = 'http://'+creds['username']+':'+creds['password']+'@indlpscm1/SourceSafe/VssService.asmx?WSDL'
    try:
        
    #    server = SOAPpy.WSDL.Proxy(wsdlFile, transport=myHTTPTransport)
        proxy = SOAPpy.SOAPProxy(wsdlFile, namespace)
        proxy.config.debug = 1
        proxy.GetCursOnDate(input)
    except Exception as inst:
        print type(inst)
        exit(-1)
        

    #f = open('vsswsdl.xml')
    #wsdlFile = f.read()
    #server= SOAPpy.WSDL.Proxy(wsdlFile)



    #server.methods.keys()
    #for method in server.methods.keys():
    #    print(method)

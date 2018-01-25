import hashlib
import base64
import urllib
import urllib2
import mimetypes
import json

def file_get_contents(filename, use_include_path = 0, context = None, offset = -1, maxlen = -1):
    if (filename.find('://') > 0):
        ret = urllib2.urlopen(filename).read()
        if (offset > 0):
            ret = ret[offset:]
        if (maxlen > 0):
            ret = ret[:maxlen]
        return ret
    else:
        fp = open(filename,'rb')
        try:
            if (offset > 0):
                fp.seek(offset)
            ret = fp.read(maxlen)
            return ret
        finally:
            fp.close( )

class docsmit(object):
    def __init__(self,username,password,softwareid,sandbox=True):
        self.username = username
        self.password = hashlib.sha512(password).hexdigest()
        self.softwareid = softwareid
        if sandbox:
            self.url = "secure.tracksmit.com/api/v1"
        else:
            self.url = "secure.docsmit.com/api/v1"
        self._token = ""

        #generate token on init
        self._getToken()

    def __del__(self,*args):
        """
        run the delete token in class destructor
        """
        self._deleteToken()

    #Authentication Tokens

    def _getToken(self):
        """
        POST /token
        generate a token by authenticating username / password and softwareid
        """
        function = "token"
        result = self._sendRequest({"function":function,"method":"POST","email":self.username,"password":self.password,"softwareID":self.softwareid})
        print result
        if "token" in result:
            self._token = base64.b64encode(result["token"]+":")
        else:
            return False
        return True

    def _deleteToken(self):
        """
        DELETE /token/
        Deletes the token, revoking its ability to authenticate
        """
        function = "token"
        result = self._sendRequest({"function":function,"method":"DELETE","email":self.username,"password":self.password,"softwareID":self.softwareid})
        if "Token deleted." in result:
            return True
        else:
            raise GeneratorExit("Error deleting token")

    #Messages - Before Sending

    def newMessage(self):
        """
        POST /messages/new 
        new message
        """
        function = "messages"

    def uploadFile(self,messageID,filename):
        """
        POST /messages/{messageID}/upload 
        upload a file
        """
        mimetypes.init()
        print mimetypes.guess_type(filename)
        fileData = file_get_contents(filename)
        function = "messages"

    def sendMessage(self,messageID):
        """
        POST /messages/{messageID}/send 
        send message
        """
        function = "messages"

    def addParty(self,messageID):
        """
        POST /messages/{messageID}/party 
        add party
        """
        function = "messages"

    def deleteParty(self,messageID,partyID):
        """
        DELETE /messages/{messageID}/party/{partyID} 
        delete party
        """
        function = "messages"

    def updateParty(self,messageID,partyID):
        """
        PUT /messages/{messageID}/party/{partyID} 
        update party
        """
        function = "messages"

    def priceCheck(self,messageID):
        """
        GET /messages/{messageID}/priceCheck 
        get the price and the details
        """
        function = "messages"

    #Messages - After Sending

    def getMessage(self,messageID):
        """
        GET /messages/{messageID}
        get a message
        """
        function = "messages"

    def signFor(self,messageID):
        """
        PUT /messages/{messageID}/signFor
        sign for message
        """
        function = "messages"

    def getCertification(self,messageID):
        """
        GET /messages/{messageID}/documentation
        get certification
        """
        function = "messages"
        raise NotImplementedError("getCertification")

    def getParties(self,messageID):
        """
        GET /messages/{messageID}/parties
        get recipients and their statuses - parties
        """
        function = "messages"
        raise NotImplementedError("getParties")

    def getAttachmentsList(self,messageID):
        """
        GET /messages/{messageID}/attachments
        get attachments list
        """
        function = "messages"
        raise NotImplementedError("getAttachementsList")

    def getHistory(self,messageID):
        """
        GET /messages/{messageID}/transactions
        message transaction history 
        """
        function = "messages"
        raise NotImplementedError("getHistory")

    def downloadAttachment(self,fileID):
        """
        GET /messages/{messageID}/download/{fileID}
        download file attachment
        """
        function = "messages"
        raise NotImplementedError("downloadAttachment")

    def downloadZipAttachment(self,messageID,zipID):
        """
        GET /messages/{messageID}/download/{ZipID}
        download zip attachment
        """
        function = "messages"
        raise NotImplementedError("downloadZipAttachment")

    def generateTrackingID(self):
        """
        POST /messages/{messageID}/trackingID
        generate tracking id (DONT USE RIGHT NOW)
        """
        function = "messages"
        raise NotImplementedError("generateTrackingID")

    #Account functions

    def sentList(self):
        """
        GET /messages/sent/
        sent list
        """
        function = "messages"

    def inboxList(self):
        """
        GET /messages/inbox
        inbox list
        """
        function = "messages"

    def draftList(self):
        """
        GET /messages/draft
        draft list
        """
        function = "messages"

    def accountInfo(self):
        """
        GET /account/info
        user account information
        """
        function = "account"

    #Miscellaneous

    def cassCheck(self):
        """
        GET /utils/multiCASS
        CASS validate and correct an address
        """
        function = "utils"

    #Packet and connection handling

    def _checkResult(self,result):
        """
        Verify the results of the API Call to give back the correct error message on failure
        """
        if "errors" in result:raise Exception(result["errors"])
    
    def _sendRequest(self,request):
        """
        Send the request to the socket and check the result.  Then pass the result baack to the API function call
        """
        function = request["function"]
        method = "POST"
        if "method" in request:method = request["method"]
        del request["function"]
        del request["method"]
        if request!={}:
            reqdat = json.dumps(request)
        else:
            reqdat = ""

        res = self._sendHttpRestRequest(reqdat,function,method)
        try:
            resdat = json.loads(res)
            self._checkResult(resdat)
        except:
            self._checkResult(str(res))
            resdat = str(res)
        return resdat

    def _sendHttpRestRequest(self,request_data,add_path="",method="POST"):
        """
        Send the socket data and return the result
        """
        self.httpError = ""
        if add_path!="":
            add_path="/"+add_path
        url = "https://%s" % self.url
        handler = urllib2.HTTPHandler()
        urlOpener = urllib2.build_opener(handler,urllib2.HTTPHandler(debuglevel=2))
        add_headers={'User-Agent':'Python' ,'Content-Type':'application/json', 'Accept':'application/json', 'Content-Length':str(len(request_data))}
        if self._token!="":add_headers["Authorization"] = "Basic "+self._token

        try:
            req = urllib2.Request(url+add_path,data=request_data)
            for key,value in add_headers.items():
                req.add_header(key,value)
            req.get_method = lambda: method
            res = urlOpener.open(req)
        except urllib2.HTTPError as e:
            res = e
            self.httpError = str(e.code) + " "

        result=res.read()
        return result



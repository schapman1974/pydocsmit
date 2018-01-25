import hashlib

class docsmit(object):
    def __init__(self,username,password,softwareid,sandbox=True):
        self.username = ""
        self.password = hashlib.sha512(password).hexdigest()
        self.softwareid = softwareid
        if sandbox:
            self.url = "secure.tracksmit.com/api/v1"
        else:
            self.url = "secure.docsmit.com/api/v1"

    #Authentication Tokens

    def _getToken(self):
        """
        POST /token
        generate a token by authenticating username / password and softwareid
        """
        function = "token"

    def _deleteToken(self):
        """
        DELETE /token/
        Deletes the token, revoking its ability to authenticate
        """
        function = "token"

    #Messages - Before Sending

    def newMessage(self):
        """
        POST /messages/new 
        new message
        """
        function = "messages"

    def uploadFile(self):
        """
        POST /messages/{messageID}/upload 
        upload a file
        """
        function = "messages"

    def sendMessage(self):
        """
        POST /messages/{messageID}/send 
        send message
        """
        function = "messages"

    def addParty(self):
        """
        POST /messages/{messageID}/party 
        add party
        """
        function = "messages"

    def deleteParty(self):
        """
        DELETE /messages/{messageID}/party/{partyID} 
        delete party
        """
        function = "messages"

    def updateParty(self):
        """
        PUT /messages/{messageID}/party/{partyID} 
        update party
        """
        function = "messages"

    def priceCheck(self):
        """
        GET /messages/{messageID}/priceCheck 
        get the price and the details
        """
        function = "messages"

    #Messages - After Sending

    def getMessage(self):
        """
        GET /messages/{messageID}
        get a message
        """
        function = "messages"

    def signFor(self):
        """
        PUT /messages/{messageID}/signFor
        sign for message
        """
        function = "messages"

    def getCertification(self):
        """
        GET /messages/{messageID}/documentation
        get certification
        """
        function = "messages"

    def getParties(self):
        """
        GET /messages/{messageId}/parties
        get recipients and their statuses - parties
        """
        function = "messages"

    def getAttachmentsList(self):
        """
        GET /messages/{messageID}/attachments
        get attachments list
        """
        function = "messages"

    def getHistory(self):
        """
        GET /messages/{messageID}/transactions
        message transaction history 
        """
        function = "messages"

    def downloadAttachment(self):
        """
        GET /messages/{messageId}/download/{fileId}
        download file attachment
        """
        function = "messages"

    def downloadZipAttachment(self):
        """
        GET /messages/{messageID}/download/{ZipID}
        download zip attachment
        """
        function = "messages"

    def generateTrackingID(self):
        """
        POST /messages/{messageID}/trackingID
        generate tracking id (DONT USE RIGHT NOW)
        """
        function = "messages"

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
    
    def _sendRequest(self,request):
        """
        Send the request to the socket and check the result.  Then pass the result baack to the API function call
        """
        function = request["function"]
        del request["function"]
        reqdat = urllib.urlencode(request)

        res = self._sendHttpRestRequest(reqdat,function)
        resdat = json.loads(res)
        self._checkResult(resdat)
        return resdat

    def _sendHttpRestRequest(self,request_data,command="POST",add_path=""):
        """
        Send the socket data and return the result
        """
        self.httpError = ""
        if add_path!="":
            add_path="/"+add_path
        url = "https://%s" % self.url
        handler = urllib2.HTTPHandler()
        urlOpener = urllib2.build_opener(handler,urllib2.HTTPHandler(debuglevel=2))
        add_headers={'User-Agent':'Pace Software' ,'Content-Type':'application/json', 'Accept':'application/json', 'Content-Length':str(len(request_data))}
        if self.access_token!="":add_headers["Authorization"] = "Bearer "+str(self.access_token)

        try:
            req = urllib2.Request(url+self.path+add_path,data=request_data)
            for key,value in add_headers.items():
                req.add_header(key,value)
            res = urlOpener.open(req)
        except urllib2.HTTPError as e:
            res = e
            self.httpError = str(e.code) + " "

        result=res.read()
        return result


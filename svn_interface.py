import pysvn
from datetime import datetime

repo_path = 'http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/branches/FCUBS_12.0.2.0.0SCOBAN_R1'


class svn_exception(Exception):
    def __init__(self, Exception):
        self.value = Exception

    def __str__(self):
        return repr(self.value)

class svn_interface_tools:
    ''' Gives tools and methods to communicate with the svn repository'''
    log_msg = None
    username = ""
    password = ""

 # INIT
    def __init__(self, path):
        try:
            self.client = pysvn.Client()
            self.path = path
        except pysvn.ClientError, e:
            raise svn_exception('Cannot initialize SVN client')
        
# TODO GET SVN PATH

# GET ITEMS
    def getItems(self, path, recurse=False):
        ''' Returns list of tuple of information for each files in the given path'''
        try:
            entries = pysvn.Client().list(path, recurse=recurse)
            # remove parent directory from the list
            del entries[0]
            self.formatItems(entries)
        except pysvn.ClientError, e:
            raise svn_exception('Cannot retrieve the information from path: +path')
        return

# FORMAT ITEMS
    def formatItems(self, entries):
        # formatting display
        print "-" *119
        print "%12s %s %6s %s %30s %s %60s %s" % ("Folder Name", "|", "RevNum", "|", "Author", "|", "Repo Path", "|")
        print "-" *119
        for x in entries:
            full_path = x[0]
            dir_name = full_path["repos_path"].split("/")[-1]
            revision_number =  full_path["created_rev"].number
            last_author = full_path["last_author"]
            repos_path = full_path["repos_path"]
            print "%12s %s %6s %s %30s %s %60s %s" % (dir_name, "|", revision_number, "|", last_author, "|", repos_path, "|")
            # for y in full_path:
                # print y
        print "-" *119

# GET LOGIN
    def __get__login__(self, realm, user, may_save):
        '''Callback method that is used whenever a svn command requires user information. It is called to get a username and password to access a repository. Pysvn expect this method to have 3 ( +self, eventually) parameters.'''
        return True, self.username, self.password, True

    def __set__login__(self, usr, pwd):
        ''' sets the username and password'''
        self.username =  usr
        self.password = pwd

# GET LOG MESSAGE
    def __get_log_message__(self):
        '''Callback method that is used when we want to operate an "svn copy" (tag). It is called when a log message is required. Pysvn expect this method to have 0 ( +self, eventually) parameters.'''
        return True, self.log_msg

# PATH LOG
    def getPathLog(self, path):
        # self.client.callback_get_login = self.__get__login__
        no_of_revisions = 0
        try:
            logfile = self.client.log(path)
            for x in logfile:
                print x["revision"].number, " ", x["author"], " ", x["message"]
                no_of_revisions += 1
            print no_of_revisions
            # TODO GET CHANGE PATH INFORMATION
        except Exception, e:
            raise svn_exception("Cannot retrieve log information for the path")
        return logfile

# GET HEAD REVISION - CURRENT TOP MOST REVISION
    def getHeadRevision(self,path):
        try:
            infofile = self.client.revpropget("revision", url=path)
            print infofile
        except Exception, e:
            raise svn_exception("Cannot retrieve path information")


# GET YOUNGER REVISION OF A PATH
    def getYoungestRevision(self, path):
        revision_numbers = []
        try:
            pathlog = self.client.log(path)
            for x in logfile:
                revision_numbers.append(x["revision"].number)
            print revision_numbers[-1]
        except Exception, e:
            raise svn_exception("Cannot find the youngest revision of the path")


# GET LAST REVISION OF A path


# GENERATE PATHS - BRANCHES PATH, TAG PATH, DOCS PATH, SOFT PATH, USER MANUALS PATH


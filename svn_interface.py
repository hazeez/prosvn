import pysvn
from datetime import datetime

path = 'http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/branches/FCUBS_12.0.2.0.0SCOBAN_R1'


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
            entries = self.client.list(path, recurse=recurse)
            # remove parent directory from the list
            del entries[0]
            #self.formatItems(entries)
        except pysvn.ClientError, e:
            raise svn_exception('Cannot retrieve the information from path: +path')
        return entries

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
                x["revision"].number, " ", x["author"], " ", x["message"]
                no_of_revisions += 1
            # TODO GET CHANGE PATH INFORMATION
        except Exception, e:
            raise svn_exception("Cannot retrieve log information for the path")
        return logfile

# GET HEAD REVISION - CURRENT TOP MOST REVISION
    def getHeadRevision(self,path):
        try:
            infofile = self.client.revpropget("revision", url=path)
        except Exception, e:
            raise svn_exception("Cannot retrieve path information")
        return infofile

# GET YOUNGER REVISION OF A PATH
    def getYoungestRevision(self, path):
        revision_numbers = []
        try:
            pathlog = self.client.log(path)
            # Get youngest revision
            gyr = pathlog[-1]["revision"].number
        except Exception, e:
            raise svn_exception("Cannot find the youngest revision of the path")
        return gyr
# GET LAST REVISION OF A path


# GENERATE PATHS - DOCS PATH, SOFT PATH, USER MANUALS PATH

    def generateDSUMPath(self, path):
        try:
            docs_path = soft_path = um_path = 0
            entries = self.client.list(path)
            # remove parent directory from the list
            del entries[0]            
            for x in entries:
                if x[0]["path"].split("/")[-1].lower() == "docs":
                    docs_path = x[0]["path"]
                if x[0]["path"].split("/")[-1].lower() == "soft":
                    soft_path = x[0]["path"]
                if x[0]["path"].split("/")[-1].lower() == "usermanuals":
                    um_path = x[0]["path"]
        except Exception, e:
            raise svn_exception("Cannot generate the directory paths")
        return docs_path, soft_path, um_path

#GENERATE TAG LIST FROM TAG PATH FOR A RELEASE
    def generateTagList(self, path):
        try:
            base_tag_path = self.generateTagPath(path)
            tags = self.getItems(base_tag_path, False)
            release_name = self.getReleaseName(path)
            tag_list = []
            for x in tags:
                tag_info = x[0]["path"]
                if release_name in tag_info:
                    tag_list.append(tag_info)
            if len(tag_list) > 1:
                tag_list.reverse()
        except Exception, e:
            raise svn_exception("Cannot generate the tag path")
        return tag_list

# GENERATE TAG PATH FROM BRANCHES PATH
    def generateTagPath(self, path):
        tag_path = ""
        branch_path = path
        main_tag_path = branch_path.split("/")[0:-2]
        for x in main_tag_path:
            tag_path += x + "/"
        tag_path += "tags/"
        return tag_path

    def getReleaseName(self, path):
        release_name = path.split("/")[-1]
        return release_name 
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
        try:
            tag_path = ""
            branch_path = path
            main_tag_path = branch_path.split("/")[0:-2]
            for x in main_tag_path:
                tag_path += x + "/"
            tag_path += "tags/"
        except Exception, e:
            raise svn_exception("Cannot generate tag path")
        return tag_path

# GET RELEASE NAME
    def getReleaseName(self, path):
        try:
            release_name = path.split("/")[-1]
        except Exception, e:
            raise svn_exception("Cannot generate release name")
        return release_name 

# FROM TAG LIST GENERATE DSUM PATH FOR TAGS
    def tagDSUMPaths(self, path):
        try:
            tag_fullpath = []
            tag_list = self.generateTagList(path)
            for x in tag_list:
                tag_fullpath.append(self.generateDSUMPath(x))
        except Exception, e:
            raise svn_exception("Cannot generate tag Docs, Soft, User Manuals path")
        return tag_fullpath

# FROM TAG FULL PATH GET THE TOP REVISION
    def getTagTopRevisionList(self, path):
        try:
            top_rev_list = []
            len_tagfullpathlist = 0
            tag_fullpathlist = self.tagDSUMPaths(path)
            len_tagfullpathlist = len(tag_fullpathlist)
            for x in tag_fullpathlist:
                for y in x:
                    top_rev_list.append(y + "/" + str(self.getYoungestRevision(y)))
        except Exception, e:
            raise svn_exception("Cannot generate Tag top revision list")
        return top_rev_list

# FROM BRANCH GET THE BASE REVISION OF EACH BRACNCH DIRECTORIES
    def getBranchYoungestRevisionList(self, path):
        try:
            branch_rev_list=[]
            branch_dir_list = self.generateDSUMPath(path)
            for x in branch_dir_list:
                branch_rev_list.append(x + "/" + str(self.getYoungestRevision(x)))
        except Exception, e:
            raise svn_exception("Cannot get branch's revision list")
        return branch_rev_list
   
# FROM BRANCH REVISON LIST ASSIGN GLOBAL BASE REVISION 
    def branchGlobalBaseRevision(self, path):
        try:
            docs_base_revision = soft_base_revision = um_base_revision = 0
            get_branch_rev_list = self.getBranchYoungestRevisionList(path)
            for x in get_branch_rev_list:
                if x.split("/")[-2].lower() == "docs":
                    docs_base_revision = x.split("/")[-1]
                if x.split("/")[-2].lower() == "soft":
                    soft_base_revision = x.split("/")[-1]
                if x.split("/")[-2].lower() == "usermanuals":
                    um_base_revision = x.split("/")[-1]
        except Exception, e:
            raise svn_exception("Cannot get global base revision number")
        return docs_base_revision, soft_base_revision, um_base_revision

# GET closure REVISION AND END REVISION FROM BRANCH GLOBAL REVISION LIST AND TAG TOP REVISION LIST
    def getPathStartRevEndRev(self, path):
        try:
            itr1_start_list = []
            start_ITR1_base_version = start_ITR2_base_version = closure_ITR2_base_version = closure_IUT_base_version = 0

            label_name_closureIUT = "closure_of_iut"
            label_name_startITR1 = "start_of_itr1"
            label_name_startITR2 = "start_of_itr2"
            label_name_closureITR2 = "closure_of_itr2"
                   
            tagTopRevList = self.getTagTopRevisionList(path)
            for x in tagTopRevList:
                if label_name_startITR1 in x.lower():
                    start_ITR1_base_version = x.split("/")[-1]
                if label_name_startITR2 in x.lower():
                    start_ITR2_base_version = x.split("/")[-1]
                if label_name_closureITR2 in x.lower():
                    closure_ITR2_base_version = x.split("/")[-1]
                if label_name_closureIUT in x.lower():
                    closure_IUT_base_version = x.split("/")[-1]
            return start_ITR1_base_version, start_ITR2_base_version, closure_ITR2_base_version, closure_IUT_base_version
        except Exception, e:
            raise svn_exception("Cannot get start end revison of each tag paths")
        return

# GENERATE FINAL LIST OF PATHS, START AND END REVISION AS A LIST
    def listPathStartRevEndRev(self, path):
        tag_path_list = self.tagDSUMPaths(path)
        tagdir_list = []
        start_itr1_base_version, start_itr2_base_version, closure_itr2_base_version, closure_iut_base_version = self.getPathStartRevEndRev(path)
        docs_base_revision, soft_base_revision, um_base_revision = self.branchGlobalBaseRevision(path)
        for x in tag_path_list:
            for y in x:
                if "start_of_itr1" in y.lower() and "docs" in y.lower():
                    tagdir_list.append(y + "/" + start_itr1_base_version + "/" + docs_base_revision)
                if "start_of_itr1" in y.lower() and "soft" in y.lower():
                    tagdir_list.append(y + "/" + start_itr1_base_version + "/" + soft_base_revision)
                if "start_of_itr1" in y.lower() and "usermanuals" in y.lower():
                    tagdir_list.append(y + "/" + start_itr1_base_version + "/" + um_base_revision)

                if "start_of_itr2" in y.lower() and "docs" in y.lower():
                    tagdir_list.append(y + "/" + start_itr2_base_version + "/" + start_itr1_base_version)
                if "start_of_itr2" in y.lower() and "soft" in y.lower():
                    tagdir_list.append(y + "/" + start_itr2_base_version + "/" + start_itr1_base_version)
                if "start_of_itr2" in y.lower() and "usermanuals" in y.lower():
                    tagdir_list.append(y + "/" + start_itr2_base_version + "/" + start_itr1_base_version)

                if "closure_of_itr2" in y.lower() and "docs" in y.lower():
                    tagdir_list.append(y + "/" + closure_itr2_base_version + "/" + start_itr2_base_version)
                if "closure_of_itr2" in y.lower() and "soft" in y.lower():
                    tagdir_list.append(y + "/" + closure_itr2_base_version + "/" + start_itr2_base_version)
                if "closure_of_itr2" in y.lower() and "usermanuals" in y.lower():
                    tagdir_list.append(y + "/" + closure_itr2_base_version + "/" + start_itr2_base_version)

                if "closure_of_iut" in y.lower() and "docs" in y.lower():
                    tagdir_list.append(y + "/" + closure_iut_base_version + "/" + closure_iut_base_version)
                if "closure_of_iut" in y.lower() and "soft" in y.lower():
                    tagdir_list.append(y + "/" + closure_iut_base_version + "/" + closure_iut_base_version)
                if "closure_of_iut" in y.lower() and "usermanuals" in y.lower():
                    tagdir_list.append(y + "/" + closure_iut_base_version + "/" + closure_iut_base_version)   
        return tagdir_list

# FROM tagdir_list GET THE LOG INFORMATION
    def getLogInfo(self, path):
        list_log_path = self.listPathStartRevEndRev(path)
        start_revision = end_revision = 0
        for x in list_log_path:
            tag_path = ""
            start_revision = x.split("/")[-1]
            end_revision = x.split("/")[-2]
            main_tag_path = x.split("/")[0:-2]
            for y in main_tag_path:
                tag_path += y + "/"
            print tag_path
            #generate log info
            log_message = self.client.log(tag_path, pysvn.Revision( pysvn.opt_revision_kind.number, start_revision ), pysvn.Revision( pysvn.opt_revision_kind.number, end_revision ), False, False, 0)
            for z in log_message:
                print z["revision"].number, z["author"]
            print "------------------------------"

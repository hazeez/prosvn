import svn_interface as svni
import time
# TODO GET SVN PATH

svn_path = 'http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/branches/FCUBS_12.0.2.0.0SCOBAN_R1'

#svn_path = 'http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/tags'

#svn_path = "http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/branches/FCUBS_12.0.2.0.0MELOCAL_R2"

#svn_path = "http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/branches/FCUBS_12.2.0.0USALAL_R1"

#svn_path = "http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/branches/FCUBS_12.0.2.0.0EGYPT_R1"

#svn_path = "http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/branches/FCUBS_12.0.2.0.0AMLAKF_R1"

svni_tools = svni.svn_interface_tools(svn_path)
# print "Path : ", svn_path
# print ""

# GET PATH FROM THE USER
class svn_client:

    def getSVNPath(self):
        print ""
        print "Please enter the svn branch path"
        print "(E.g.) http://ipaddress:port/svn/FCUBS_*.*.0.0.0/branches/release_name"
        svn_path = raw_input("Enter the svn path:")
        return svn_path

    def validateSVNPath(self):
        path = self.getSVNPath()
        if path.lower() == "exit" or path.lower() == 'e':
            print "Quitting the program"
            exit()
        if "branches" not in path.lower():
            if len(path) == 0:
                print "SVN path cannot be empty"
                print "Try again or type e or exit to quit the program."
            else:
                print "Looks like the svn_path provided is incorrect."
                print "Try again or type e or exit to quit the program."
                print ""
            self.validateSVNPath()
        if path.startswith("'") or path.startswith('"'):
            path = path.lstrip("'")
            path = path.lstrip('"')
        if path.endswith("'") or path.endswith('"'):
            path = path.rstrip("'")
            path = path.rstrip('"')
        return path

    def getLogInformation(self):
        svn_path = self.validateSVNPath()
        start_time = time.time()
        svni_tools.getLogInfo(svn_path)
        time_taken = time.time() - start_time
        print "Time taken in seconds:", time_taken

svn_client = svn_client()
#try:
svn_client.getLogInformation()
#except Exception:
#print "Oops, could not generate the report. Try again"
#svni_tools.wait()



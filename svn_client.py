import svn_interface as svni
import sys

# TODO GET SVN PATH

#svn_path = 'http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/branches/FCUBS_12.0.2.0.0SCOBAN_R1'

#svn_path = 'http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/tags'

svn_path = "http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/branches/FCUBS_12.0.2.0.0MELOCAL_R2"

svni_tools = svni.svn_interface_tools(svn_path)
print "Path : ", svn_path
print ""
# print svni_tools.getPathLog(svn_path)
svni_tools.getItems(svn_path, False)
# svni_tools.getHeadRevision(svn_path)
# Get youngest revision

svni_tools.generateDSUMPath(svn_path)

docs_base_revision, soft_base_revision, um_base_revision = svni_tools.branchGlobalBaseRevision(svn_path)

svni_tools.tagDSUMPaths(svn_path)

svni_tools.listPathStartRevEndRev(svn_path)

svni_tools.getLogInfo(svn_path)
svni_tools.wait()





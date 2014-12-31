import svn_interface as svni
import sys

svn_path = 'http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/branches/FCUBS_12.0.2.0.0SCOBAN_R1'

#svn_path = 'http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/tags'

#svn_path = "http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/branches/FCUBS_12.0.2.0.0MELOCAL_R2"

svni_tools = svni.svn_interface_tools(svn_path)
# print svni_tools.getPathLog(svn_path)
svni_tools.getItems(svn_path, False)
# svni_tools.getHeadRevision(svn_path)
# Get youngest revision
svni_tools.getYoungestRevision(svn_path)

svni_tools.generateDSUMPath(svn_path)

print svni_tools.generateTagList(svn_path)




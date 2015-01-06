import svn_interface as svni
import sys

# TODO GET SVN PATH

svn_path = 'http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/branches/FCUBS_12.0.2.0.0SCOBAN_R1'

#svn_path = 'http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/tags'

#svn_path = "http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/branches/FCUBS_12.0.2.0.0MELOCAL_R2"
#NOT WORKING
#svn_path = "http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/branches/FCUBS_12.0.2.0.0USALAL_R1"
#NOT WORKING
#svn_path = "http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/branches/FCUBS_12.0.2.0.0EGYPT_R1"

#svn_path = "http://10.184.152.13:18080/svn/FCUBS_12.0.2.0.0/branches/FCUBS_12.0.2.0.0AMLAKF_R1"

svni_tools = svni.svn_interface_tools(svn_path)
print "Path : ", svn_path
print ""

#print svni_tools.generateDSUMPath(svn_path)
#print ""
#print svni_tools.generateTagList(svn_path)
#print ""

# tag_list = svni_tools.generateTagList(svn_path)
# for b in tag_list:
#     print b
# print ""

# #tag_full_path = svni_tools.tagDSUMPaths(svn_path)
# svni_tools.tagDSUMPaths(svn_path)
# #for a in tag_full_path:
#     #for c in a:
#     #    print c
# print ""

# top_rev_list = svni_tools.getTagTopRevisionList(svn_path)
# for x in top_rev_list:
#     print x

# print ""

# gyr = svni_tools.getBranchYoungestRevisionList(svn_path)
# for y in gyr:
#     print y


# print ""

#tag_dir_list =  svni_tools.listPathStartRevEndRev(svn_path)
#for z in tag_dir_list:
#    print z

print svni_tools.getLogInfo(svn_path)
svni_tools.wait()



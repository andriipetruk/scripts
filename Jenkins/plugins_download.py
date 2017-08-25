import xml.etree.ElementTree as ET
import urllib

# init dict for storing array plugin_name[version] 
plugin_list = {}

# load xml file with plugin and version from jenkins
tree = ET.parse('plugins_list.xml')
root = tree.getroot()

# get plugin name and version and storing in array
for child in root:
   if child.tag == 'shortName':
      plugin_name = child.text
   else: 
      plugin_list[plugin_name] = child.text


# download plugins 
for plugin in plugin_list:
   url  = 'http://updates.jenkins-ci.org/download/plugins/'+plugin+'/'+plugin_list[plugin]+'/'+plugin+'.hpi'
   plugin_file = plugin+'.hpi' 
   urllib.urlretrieve (url, plugin_file)

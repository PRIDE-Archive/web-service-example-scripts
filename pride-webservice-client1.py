import sys
import json
import urllib2

# check the number of input parameters, we need at least one project accession to query with
if len(sys.argv) < 2:
  print('No input parameter specified. You have to provide at least one project accession')
  sys.exit(-1)
 
projects = sys.argv;
# get rid of the first argument, as it is the name of the script itself
projects.pop(0)

# for each of the provided project accessions retrieve the record and print some details
for project in projects:
  try:
    # Set the request URL
    url = 'http://www.ebi.ac.uk/pride/ws/archive/project/' + project
    # Create the request
    req = urllib2.Request(url)
    # Send the request and retrieve the data
    resp = urllib2.urlopen(req).read()
    # Interpret the JSON response 
    project = json.loads(resp.decode('utf8'))
    # Output some project properties 
    print(project['accession'] + ' - ' + project['title'])
    print('\tsubmission date: ' + project['publicationDate'])
    print('\tsubmission type: ' + project['submissionType'])
    print('\tsubmitter email: ' + project['submitter']['email'])
    print('\tnumber of assays: ' + str(project['numAssays']))
  except (Exception):
    print('Error for project: ' + project + ' perhaps this project does not exist?')

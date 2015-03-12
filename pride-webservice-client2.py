import argparse
import sys
import json
import urllib2

# create the argument parser
parser = argparse.ArgumentParser(description='Command-line example.')
# Add optional switches
parser.add_argument('-p', '--page', action='store', dest='page',
                    metavar='PAGE', default=0,
                    help='the result page to retrieve (default=0, the first page)')
parser.add_argument('-s', '--show', action='store', dest='show',
                    metavar='NUM', default=10,
                    help='number of results to retrieve per page (default=10)')
parser.add_argument('-c', '--count', action='store_true', dest='count',
                    help='only count total number of results')
# Allow any number of query terms.
parser.add_argument(nargs='*', action='store', dest='term',
                    help='term(s) to query for')
# parse the provided arguments
args = parser.parse_args()

# join the provided terms into one list of query terms
terms = '%20'.join(args.term)

# create the basic query (which is the same for count and list operations)
query = 'q='+terms

# if we are not counting, we have to take the paging parameters into account
if not args.count:
  query = query + '&page='+str(args.page)+'&show='+str(args.show)

# use different services for counting and listing
if not args.count:
  url = 'http://www.ebi.ac.uk/pride/ws/archive/project/list?' + query
else:
  url = 'http://www.ebi.ac.uk/pride/ws/archive/project/count?' + query

# do the actual request and store the response
request = urllib2.Request(url)
response = urllib2.urlopen(request).read()

# the result is either a count or the full list of projects matching the conditions
result = json.loads(response.decode('utf8'))


# depending on the desired action, either print the count or the list of projects
if args.count:
  print('Number of matching projects: ' + str(result))
else: 
  projects = result['list']
  # for each of the provided project accessions retrieve the record and print some details
  for project in projects:
    try:
      # Output some project properties 
      print(project['accession'] + ' - ' + project['title'])
      print('\tsubmission date: ' + project['publicationDate'])
      print('\tsubmission type: ' + project['submissionType'])
      print('\treported species: ' + ' '.join(project['species']))
      print('\tnumber of assays: ' + str(project['numAssays']))
      print
    except (Exception):
      print('Error for project: ' + project['accession'] + ' perhaps this project does not exist?')

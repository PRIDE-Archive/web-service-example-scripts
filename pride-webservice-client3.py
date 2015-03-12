###############################################################################
# Simple Python script to retrieve identification records across projects     #
# for a given protein accession or peptide sequence                           #
#                                                                             #
# Note: this if for demonstration purpose only, results will be trunkated for #
#       display purposes and the code is not in production ready state.       #
###############################################################################
import argparse
import traceback
import sys
import json
import urllib2

# create the argument parser
parser = argparse.ArgumentParser(description='Command-line example.')
# Add allowed arguments 
parser.add_argument('-t', '--taxid', action='store', dest='taxid',
                    metavar='TAXID',
                    help='restrict query by species (taxonomy id, example: 9606 for human)')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-p', '--protein', action='store', dest='protein',
                    metavar='PROTEIN', 
                    help='the protein accession to search for (example: P38398)')
group.add_argument('-s', '--seqeunce', action='store', dest='sequence',
                    metavar='SEQUENCE',
                    help='the peptide sequence to search for (example: MDPNTIIEALR)')

# parse the provided arguments
args = parser.parse_args()

# create the basic query (which is the same for count and list operations)
if args.protein:
  query = 'query='+args.protein
else: 
  query = 'query='+args.sequence

if args.taxid:
  query = query + '&speciesFilter='+args.taxid

# restrict the result list to 5 projects max
query = query + '&show=5'

# create the url to search for projects reporting the protein/peptide 
projectUrl = 'http://www.ebi.ac.uk/pride/ws/archive/project/list?' + query

# do the actual request and store the response
request = urllib2.Request(projectUrl)
response = urllib2.urlopen(request).read()

# the result will be a list of projects matching the query
projectResult = json.loads(response.decode('utf8'))


# print the list of projects and print some details
projects = projectResult['list']
for project in projects:
  try:
    # Output some project properties 
    print(project['accession'] + ' - ' + project['title'])
    print('\tsubmission date : ' + project['publicationDate'])
    print('\tsubmission type : ' + project['submissionType'])
    print('\treported species: ' + ' '.join(project['species']))
    print('\tnumber of assays: ' + str(project['numAssays']))
    if args.protein:
      proteinUrl = 'http://www.ebi.ac.uk/pride/ws/archive/protein/list/project/' + project['accession'] + '/protein/' + args.protein
      #print('\t\tprotein query URL: ' + proteinUrl)
      request = urllib2.Request(proteinUrl)
      response = urllib2.urlopen(request).read()
      proteinResult = json.loads(response.decode('utf8'))
      proteins = proteinResult['list']
      for prot in proteins:
        print('\t\tprotein : ' + prot['accession'])
        print('\t\t\tassay        : ' + prot['assayAccession'])
        if prot['sequence']:
          print('\t\t\tsequence     : ' + prot['sequence'][:50] + '...')
          print('\t\t\tsequence type: ' + prot.get('sequenceType', ''))
        else:
          print('\t\t\tNo sequence available')
    else:
      peptideUrl = 'http://www.ebi.ac.uk/pride/ws/archive/peptide/list/project/' + project['accession'] + '/sequence/' + args.sequence
      #print('\t\tpeptide query URL: ' + peptideUrl)
      request = urllib2.Request(peptideUrl)
      response = urllib2.urlopen(request).read()
      peptideResult = json.loads(response.decode('utf8'))
      peptides = peptideResult['list']
      for pep in peptides:
        print('\t\tpeptide : ' + pep['id'])
        print('\t\t\tspectrum : ' + pep['spectrumID'])
        print('\t\t\tassay    : ' + pep['assayAccession'])
        print('\t\t\tprotein  : ' + pep['proteinAccession'])
    print
  except TypeError as te:
    print('Unexpected error handling data types')
    execInfo = sys.exc_info()
    traceback.print_exception(*execInfo)
  except:
    print('Error showing results, perhaps no records exist?')
    print(sys.exc_info()[0])
    execInfo = sys.exc_info()
    traceback.print_exception(*execInfo)

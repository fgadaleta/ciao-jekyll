#!/usr/bin/python

import sys, os, getopt
import re
import xmltodict
from datetime import datetime
import html2text
import shutil

def printStuff(msg, arg):
    sys.stdout.write('\r')
    sys.stdout.write(msg % (arg))
    sys.stdout.flush()


def openXml(fname, verbose=False):
    #fname = 'xmldata/worldofpiggy.wordpress.2016-07-31(1).xml'
    
    with open(fname) as fd:
        doc = xmltodict.parse(fd.read())
    posts = doc['rss']['channel']['item']

    if verbose:
        print('Collected %d posts' %len(posts))

    return posts


def process(posts, odir, limit=10, verbose=False):
    if not odir:
        odir = '_posts'
   
    if os.path.exists(odir):
	print('Found old posts. Deleting...')
    	shutil.rmtree(odir)
 
    if not os.path.exists(odir):
        os.makedirs(odir)
        
        
    for i in xrange(min(len(posts),limit)):

        info = {}        # dictionary of post info 
        info['layout']   = 'post'
        info['title']    = posts[i]['title']
        info['status']   = posts[i]['wp:status']
        info['date']     = posts[i]['wp:post_date']
        info['content']  = posts[i]['content:encoded']
        info['category'] = posts[i]['category']
        info['comments'] = 'true'

        # process tags 
        tags = []
        for e in info['category']:
            try:
                if e.items()[0][1] == 'post_tag':
                    tags.append(e.items()[1][1])
            except:
                if verbose:
                    print('No tags found')
                pass
                
        # process content 
        h = html2text.HTML2Text()
        # Ignore converting links from HTML
        h.ignore_links = False
        info['content'] = h.handle(info['content'])
        #info['content'] = html2text.html2text(info['content'])
        info['content'] = info['content'].encode('utf-8')
        
        # TODO consolidate links to local directory

        
        # clean title and filename 
        info['title'] = re.sub('[^A-Za-z0-9]+', '-', info['title'].lower())
        #strip last dash 
        if info['title'][-1] == '-':
            info['title'] = info['title'][:-1]
        # encode ignoring bad stuff
        info['title'] = info['title'].encode('utf-8', 'ignore')
        

        # create jekyll markdown filename from post date
        date_object = datetime.strptime(info['date'], "%Y-%m-%d %H:%M:%S")
        fname = date_object.strftime("%Y-%m-%d")+'-'
        fname += info['title'].lower().replace (" ", "-")+'.md'
        fname = os.path.join(odir, fname)

        # write content to file
        if verbose:
            print('Converting to file %s'%(fname))
        fh = open(fname, "a")
        fh.write("---\n")
        fh.write('layout: %s\n'  %info['layout'])
        fh.write('title: %s\n'   %info['title'])
        fh.write('comments: %s\n'%info['comments'])

        tag_string = str([t.replace("'", "").encode('utf-8') for t in tags]).replace("'", "")

        fh.write('tags: %s\n'%tag_string)
        fh.write("---\n")
        fh.write(info['content']) #.encode('utf-8'))
        fh.close
        printStuff('Processed %d posts', i)
    

def main(argv):
    inputfile = ''
    outputdir = '_posts'
    limit = 42
    verbose = False

    try:
        opts, args = getopt.getopt(argv,"hi:o:n:v",["ifile=","odir=", "nposts="])
    except getopt.GetoptError:
        print 'ciao-jekyll.py -i <inputfile> -o <outputdir> -n <max_num_posts> -v <verbosity>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Usage:\n')
            print('-'*50)
            print('python ciaoJekyll.py -i xmldata/worldofpiggy.wordpress.2016-07-31.xml -n 42')
            print 'ciao-jekyll.py -i <inputfile> -o <outputdir>'
            print('-'*50)
            print 'ciao-jekyll.py -i my_wordpress_export.xml -o _posts'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--odir"):
            outputdir = arg
        elif opt in ("-n", "--nposts"):
            limit = int(arg)
        elif opt in ("-v", "--verbose"):
            verbose = False if arg==0 else True

    if not inputfile:
    	print('No input file provided')
	return
    
    print('Input file is [%s]'%inputfile)
    print('\nProcessed files saved to [%s/]'%outputdir)
     
    data = openXml(inputfile, verbose)
    process(data, outputdir, limit, verbose)
    print('\n')
    print('-'*50)
    print('\nCheck out [%s/] and publish your posts in Markdown format\n'%outputdir) 
    print('Bye!\n')
    
if __name__ == "__main__":
    main(sys.argv[1:])



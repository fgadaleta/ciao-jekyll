# ciao-jekyll

Migrate all posts from Wordpress xml to Jekyll markdown format.

## jekyll md format

  ---
  layout: post
  title: Title of original post 
  tags: [tag1, tag2, tag3]
  comments: true
  type: post
  ---
  
  Content here 
  
## Installation
Requires [html2text](https://github.com/Alir3z4/html2text)

No installation is required. Just export your wordpress site to an xml using the Wordpress Dashboard->Export

### Usage
From console run 

    python ciao-jekyll.py -i wordpress_export.xml -o _posts -n 42
  This will process the first 42 posts from xml (in reverse chronological order) and create one markdown file per post in the _post directory. These files should be ready to be published to your jekyll site.
  

## License

[The MIT License (MIT)](LICENSE.md)

Copyright © 2014-2016 Francesco Gadaleta

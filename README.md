<h1>Which CSS</h1>
<p><a href="http://www.bradleyhamilton.com/projects/Which-CSS/">Go give it a try over here</a></p>
<p>An easy way to figure out which CSS properties from your sites style sheets are being used.</p>
<p>No need to upload the files just:</p>
<ol>
    <li>Type in your sites URL</li>
    <li>(Optional) Specify a specific style sheet if you like</li>
    <li>Click run and wait for the scraping to be done</li>
</ol>
<p>The program is written in python and lives in the direcotry <code>codebase/</code></p>
<h3>Python Dependencies</h3>
<ul>
    <li>Python2.7 or greater</li>
    <li>BeautifulSoup</li>
    <li>tinycss</li>
    <li>soupselect</li>
</ul>
<p>These are included but can be removed if you have them installed or wish to install them instead. They are
all available using <code>pip install packagename</code></p>

</br>
<h3>Running the script</h3>
<h6>Command line</h6>
<code>python codebase/parse.py http://wwww.website.com</code>
<h6>Web interface</h6>
<p>Get the code in a directory your webserver can run on localhost.</p>
<p>Setup a subdomain to point to <code>/path/Which-CSS/</code> with a subdomain <code>whichcss.localhost</code></p>
<p>Install/Enable <code>X-Sendfile</code></p>


<h3>Output</h3>
<p>Ouput lives in the directory <code>codebase/newcss/yoursiteurl.com/</code></p>
<p>Contained in that folder is a file called <code>output.html</code> and all css files found on your site but in
two verisions one prefixed with the name </code>.found</code> for the styles that were found, and one prefixed
<code>.notfound</code> for the styles that weren't found.</p>

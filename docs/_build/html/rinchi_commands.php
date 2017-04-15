<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">


<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    
    <title>RInChI Master Script &mdash; RInChI Extended Toolkit 1.0 documentation</title>
    
    <link rel="stylesheet" href="_static/alabaster.css" type="text/css" />
    <link rel="stylesheet" href="_static/pygments.css" type="text/css" />
    
    <script type="text/javascript">
      var DOCUMENTATION_OPTIONS = {
        URL_ROOT:    './',
        VERSION:     '1.0',
        COLLAPSE_INDEX: false,
        FILE_SUFFIX: '.php',
        HAS_SOURCE:  true
      };
    </script>
    <script type="text/javascript" src="_static/jquery.js"></script>
    <script type="text/javascript" src="_static/underscore.js"></script>
    <script type="text/javascript" src="_static/doctools.js"></script>
    <link rel="top" title="RInChI Extended Toolkit 1.0 documentation" href="index.php" />
    <link rel="prev" title="RInChI Extended Toolkit" href="rinchi_tools.php" />
   
  
  <meta name="viewport" content="width=device-width, initial-scale=0.9, maximum-scale=0.9" />

  </head>
  <body role="document">  

    <div class="document">
      <div class="documentwrapper">
        <div class="bodywrapper">
          <div class="body" role="main">
            
  <span class="target" id="module-rinchi"></span><div class="section" id="rinchi-master-script">
<h1>RInChI Master Script<a class="headerlink" href="#rinchi-master-script" title="Permalink to this headline">¶</a></h1>
<p>Contains all of the action of the RInChI module! Uses a system of subparsers which can be called independently.</p>
<p>Modifications:</p>
<blockquote>
<div><ul class="simple">
<li>D.F. Hampshire 2017</li>
</ul>
</div></blockquote>
</div>
<div class="highlight-python"><div class="highlight"><pre>Usage: rinchi.py [-h] {search,convert,db,changes,addition,stats} ...

RInChI Module Command Line Tools. Can execute each of the other functions, allowing
for a complete command line program navigation.

positional arguments:
  {search,convert,db,changes,addition,stats}
                        Main Function
    search              Search for RInChIs, InChIs &amp; their components or
                        RInChI Keys in a RInChI SQL Database / Flat File
    convert             RInChI Conversion to/from other formats
    db                  RInChI SQL Database Manipulation Tools
    changes             RInChI Changes Analysis
    addition            RInChI Addition
    stats               RInChI Statistical analysis

optional arguments:
  -h, --help            show this help message and exit
</pre></div>
</div>
<span class="target" id="module-rinchi_add"></span><div class="section" id="rinchi-addition-script">
<h1>RInChI Addition Script<a class="headerlink" href="#rinchi-addition-script" title="Permalink to this headline">¶</a></h1>
<p>This script adds together flat files of RInChIs separated by newlines.</p>
<p>Modifications:</p>
<blockquote>
<div><ul>
<li><p class="first">C.H.G. Allen 2012</p>
</li>
<li><p class="first">D.F. Hampshire 2016</p>
<blockquote>
<div><p>Rewritten to use argparse module and Python3</p>
</div></blockquote>
</li>
</ul>
</div></blockquote>
<dl class="function">
<dt id="rinchi_add.add_addition">
<code class="descclassname">rinchi_add.</code><code class="descname">add_addition</code><span class="sig-paren">(</span><em>subparser</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_add.add_addition" title="Permalink to this definition">¶</a></dt>
<dd><p>Adds the arguments for the addition operation to the <code class="docutils literal"><span class="pre">ArgumentParser</span></code> object.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>subparser</strong> &#8211; An <code class="docutils literal"><span class="pre">ArgumentParser</span></code> object</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_add.addition_ops">
<code class="descclassname">rinchi_add.</code><code class="descname">addition_ops</code><span class="sig-paren">(</span><em>args</em>, <em>parser</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_add.addition_ops" title="Permalink to this definition">¶</a></dt>
<dd><p>Executes the addition operations.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first last simple">
<li><strong>args</strong> &#8211; The output of the <code class="docutils literal"><span class="pre">parser.parse_args()</span></code>. The command line arguments.</li>
<li><strong>parser</strong> &#8211; An <code class="docutils literal"><span class="pre">ArgumentParser</span></code> object</li>
</ul>
</td>
</tr>
</tbody>
</table>
</dd></dl>

</div>
<div class="highlight-python"><div class="highlight"><pre>usage: rinchi_add.py [-h] [-o [OUTPUT]] input_path

This script combines seperate RInChIs representing the steps of a multi-step
reaction into a total RInChI representing the overall reaction.

The input RInChI file should contain the RInChIs representing the steps of the
reaction IN ORDER and seperated by line breaks.

positional arguments:
  input_path            Path of file to input

optional arguments:
  -h, --help            show this help message and exit
  -o [OUTPUT], --output [OUTPUT]
                        Output the result to a file. Optionally specify the
                        file output name
</pre></div>
</div>
<span class="target" id="module-rinchi_changes"></span><div class="section" id="rinchi-changes-analysis-script">
<h1>RInChI Changes Analysis Script<a class="headerlink" href="#rinchi-changes-analysis-script" title="Permalink to this headline">¶</a></h1>
<p>This script analyses RInChI(s) for changes in properties.</p>
<p>Modifications:</p>
<blockquote>
<div><ul>
<li><ol class="first upperalpha simple" start="3">
<li>Allen</li>
</ol>
</li>
<li><ol class="first upperalpha simple" start="2">
<li>Hammond 2014</li>
</ol>
</li>
<li><p class="first">D.F. Hampshire 2017</p>
<blockquote>
<div><p>Interface completely rewritten. New features added. Based on prior work.</p>
</div></blockquote>
</li>
</ul>
</div></blockquote>
<dl class="function">
<dt id="rinchi_changes.add_changes">
<code class="descclassname">rinchi_changes.</code><code class="descname">add_changes</code><span class="sig-paren">(</span><em>subparser</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_changes.add_changes" title="Permalink to this definition">¶</a></dt>
<dd><p>Adds the arguments for the changes operation to the <code class="docutils literal"><span class="pre">ArgumentParser</span></code> object.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>subparser</strong> &#8211; An <code class="docutils literal"><span class="pre">ArgumentParser</span></code> object</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_changes.changes_ops">
<code class="descclassname">rinchi_changes.</code><code class="descname">changes_ops</code><span class="sig-paren">(</span><em>args</em>, <em>parser</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_changes.changes_ops" title="Permalink to this definition">¶</a></dt>
<dd><p>Executes the changes operations.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first last simple">
<li><strong>args</strong> &#8211; The output of the <code class="docutils literal"><span class="pre">parser.parse_args()</span></code>. The command line arguments.</li>
<li><strong>parser</strong> &#8211; An <code class="docutils literal"><span class="pre">ArgumentParser</span></code> object</li>
</ul>
</td>
</tr>
</tbody>
</table>
</dd></dl>

</div>
<div class="highlight-python"><div class="highlight"><pre>usage: rinchi_changes.py [-h] (-b | -r | -k) [--list] [--filein] [--ringcount]
                         [--formula] [--valence] [--hybrid]
                         [--ringcountelements] [--ringcountold]
                         [--stereoold [STEREOOLD]]
                         input

RInChI Analysis and Manipulation

positional arguments:
  input                 The file or string containing RInChI(s) or Long Key to
                        be processed

optional arguments:
  -h, --help            show this help message and exit
  -b, --batch           Process multiple RInChIs
  -r, --rinchi          Process a single RInChI
  -k, --key             Process a RInChI key

File options:
  --list                List RInChIs along with results. Otherwise returns
                        count populations
  --filein              Assert that the input is a file

Operation:
  --ringcount           Change in ring populations by size
  --formula             Change in formula across a reaction
  --valence             Change in valence across reaction
  --hybrid              Change in hybridisation of C atoms across reaction
  --ringcountelements   Change in ring populations by ring elements
  --ringcountold        Change in ring populations. Old method
  --stereoold [STEREOOLD]
                        Change stereocentres. Old method. Takes an argument as
                        a dictionary such as
                        {&#39;sp2&#39;:True,&#39;sp3&#39;:False,&#39;wd&#39;:True} for options to 1.
                        Count sp2 centres 2. Count sp3 centre 3. Well defined
                        stereocentres only
</pre></div>
</div>
<span class="target" id="module-rinchi_convert"></span><div class="section" id="rinchi-conversion-script">
<h1>RInChI Conversion Script<a class="headerlink" href="#rinchi-conversion-script" title="Permalink to this headline">¶</a></h1>
<p>Converts RInChIs to and from various chemical reaction file formats.</p>
<p>Modifications:</p>
<blockquote>
<div><ul>
<li><ol class="first upperalpha simple" start="3">
<li>Allen 2012</li>
</ol>
</li>
<li><p class="first">D.F. Hampshire 2016</p>
<blockquote>
<div><p>Code rewritten for Python 3 using the argparse module, and major structural and procedural
changes.</p>
</div></blockquote>
</li>
</ul>
</div></blockquote>
<dl class="function">
<dt id="rinchi_convert.add_convert">
<code class="descclassname">rinchi_convert.</code><code class="descname">add_convert</code><span class="sig-paren">(</span><em>subparser</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_convert.add_convert" title="Permalink to this definition">¶</a></dt>
<dd><p>Adds the arguments for the conversion operation to the <code class="docutils literal"><span class="pre">ArgumentParser</span></code> object.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>subparser</strong> &#8211; An <code class="docutils literal"><span class="pre">ArgumentParser</span></code> object</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_convert.convert_ops">
<code class="descclassname">rinchi_convert.</code><code class="descname">convert_ops</code><span class="sig-paren">(</span><em>args</em>, <em>parser</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_convert.convert_ops" title="Permalink to this definition">¶</a></dt>
<dd><p>Executes the conversion operations.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first last simple">
<li><strong>args</strong> &#8211; The output of the <code class="docutils literal"><span class="pre">parser.parse_args()</span></code>. The command line arguments.</li>
<li><strong>parser</strong> &#8211; An <code class="docutils literal"><span class="pre">ArgumentParser</span></code> object</li>
</ul>
</td>
</tr>
</tbody>
</table>
</dd></dl>

</div>
<div class="highlight-python"><div class="highlight"><pre>usage: rinchi_convert.py [-h]
                         (--rxn2rinchi | --rdf2rinchi | --rinchi2file | --rinchi2key | --rdf2csv | --dir2csv | --svg)
                         [-o [FILEOUT]] [-i] [-e] [-ra] [-l] [-s] [-w] [-r]
                         [-ordf] [-orxn]
                         input

RInChI Conversion tools

positional arguments:
  input                 The path of the file or folder to be converted, or the
                        input string

optional arguments:
  -h, --help            show this help message and exit

Conversion Type:
  --rxn2rinchi          RXN to RInChI conversion
  --rdf2rinchi          RDF to RInChI conversion
  --rinchi2file         RInChI-to-File conversion. Accepts any file containing
                        a rinchi and optionally rauxinfo. The RAuxInfo must
                        immediately follow the RInChI
  --rinchi2key          RInChi to RInChI-Key conversion
  --rdf2csv             Create or append a .csv with an rdfile
  --dir2csv             Convert a directory of rdfiles to a single csv file
  --svg                 Convert a RInChI to a collection of .svg files

All operations:
  -o [FILEOUT], --fileout [FILEOUT]
                        Save the output to disk.
  -i, --filein          Assert that the input is a file

Conversion to RInChI file:
  -e, --equilibrium     Force output to be an equilibrium reaction
  -ra, --rauxinfo       Generate and return RAuxInfo
  -l, --longkey         Generate and return the Long-RInChIKey
  -s, --shortkey        Generate and return the Short-RInChIKey
  -w, --webkey          Generate and return the Web-RInChIKey

Converting RInChIs to Keys:
  -r, --include_rinchi  Include original RInChI in the output

Converting to a RXN/RDF:
  -ordf, --rdfileoutput
                        Output as RDFile. Otherwise RXN file(s) are produced
  -orxn, --rxnfileoutput
                        Output as RXNFile
</pre></div>
</div>
<span class="target" id="module-rinchi_database"></span><div class="section" id="rinchi-databasing-tools-script">
<h1>RInChI Databasing Tools Script<a class="headerlink" href="#rinchi-databasing-tools-script" title="Permalink to this headline">¶</a></h1>
<p>Converts, creates, and removes from SQL databases</p>
<p>Modifications:</p>
<blockquote>
<div><ul>
<li><ol class="first upperalpha simple" start="2">
<li>Hammond 2014</li>
</ol>
</li>
<li><p class="first">D.F. Hampshire 2016</p>
<blockquote>
<div><p>Major features added</p>
</div></blockquote>
</li>
</ul>
</div></blockquote>
<dl class="function">
<dt id="rinchi_database.add_db">
<code class="descclassname">rinchi_database.</code><code class="descname">add_db</code><span class="sig-paren">(</span><em>subparser</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_database.add_db" title="Permalink to this definition">¶</a></dt>
<dd><table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>subparser</strong> &#8211; </td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_database.db_ops">
<code class="descclassname">rinchi_database.</code><code class="descname">db_ops</code><span class="sig-paren">(</span><em>args</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_database.db_ops" title="Permalink to this definition">¶</a></dt>
<dd><p>Executes the database operations.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>args</strong> &#8211; The output of the <code class="docutils literal"><span class="pre">parser.parse_args()</span></code>. The command line arguments.</td>
</tr>
</tbody>
</table>
</dd></dl>

</div>
<div class="highlight-python"><div class="highlight"><pre>usage: rinchi_database.py [-h] [-o [OUTPUT]] [--rdf2db] [--csv2db]
                          [--ufingerprints] [--rfingerprints]
                          [--cfingerprints] [--convert2_to_3]
                          [--generate_rauxinfo] [-k [{L,S,W}]]
                          [database] [input]

Database Tools Module

positional arguments:
  database              The existing database to manipulate, or the name of
                        database to be created
  input                 The name of the input data file or table

optional arguments:
  -h, --help            show this help message and exit
  -o [OUTPUT], --output [OUTPUT]
                        The output table name or something else to output

Adding Data to a database:
  --rdf2db              Convert and add an rdfile to an SQL database
  --csv2db              Add the contents of a rinchi .csv file to an SQL
                        database

Fingerprints:
  --ufingerprints       Adds new entries to the fpts table containing
                        fingerprint data
  --rfingerprints       Returns the fingerprint of a given key
  --cfingerprints       Returns all RInChIs containing the given InChI to
                        STDOUT

Converting operations:
  --convert2_to_3       Creates a new table of v.03 rinchis from a table of
                        v.02 rinchis
  --generate_rauxinfo   Generate RAuxInfos from rinchis within a SQL database
  -k [{L,S,W}], --key [{L,S,W}]
                        Returns the RInChI corresponding to a given key.
                        Optionally accepts an argument denoting the type of
                        key to lookup
</pre></div>
</div>
<span class="target" id="module-rinchi_search"></span><div class="section" id="rinchi-searching-script">
<h1>RInChI Searching Script<a class="headerlink" href="#rinchi-searching-script" title="Permalink to this headline">¶</a></h1>
<p>Searches an SQL database for InChIs.</p>
<p>Modifications:</p>
<blockquote>
<div><ul>
<li><ol class="first upperalpha simple" start="2">
<li>Hammond 2014</li>
</ol>
</li>
<li><p class="first">D.F. Hampshire 2017</p>
<blockquote>
<div><p>Rewrote search function completely</p>
</div></blockquote>
</li>
</ul>
</div></blockquote>
<dl class="function">
<dt id="rinchi_search.add_search">
<code class="descclassname">rinchi_search.</code><code class="descname">add_search</code><span class="sig-paren">(</span><em>subparser</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_search.add_search" title="Permalink to this definition">¶</a></dt>
<dd><p>Adds the arguments for the search operation to the <code class="docutils literal"><span class="pre">ArgumentParser</span></code> object.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>subparser</strong> &#8211; An <code class="docutils literal"><span class="pre">ArgumentParser</span></code> object</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_search.search_ops">
<code class="descclassname">rinchi_search.</code><code class="descname">search_ops</code><span class="sig-paren">(</span><em>args</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_search.search_ops" title="Permalink to this definition">¶</a></dt>
<dd><p>Executes the search operations.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>args</strong> &#8211; The output of the <code class="docutils literal"><span class="pre">parser.parse_args()</span></code></td>
</tr>
</tbody>
</table>
</dd></dl>

</div>
<div class="highlight-python"><div class="highlight"><pre>usage: rinchi_search.py [-h] (-k [{L,S,W,N}] | -i | -l) [-db]
                        [-o {list,file,stats}] [-hb HYBRIDISATION]
                        [-v VALENCE] [-r RINGS] [-f FORMULA] [-re RINGELEMENT]
                        [-iso] [-rct] [-pdt] [-agt] [-n NUMBER]
                        search_term file [table_name]

Search for RInChIs, InChIs &amp; their components or RInChI Keys in a RInChI SQL
Database / Flat File

positional arguments:
  search_term           The search_term to find
  file                  The database or flat file to search
  table_name            The table name for the search to be performed on.
                        Providing this argument asserts that the input file is
                        an SQL database

optional arguments:
  -h, --help            show this help message and exit

Action:
  -k [{L,S,W,N}], --key [{L,S,W,N}]
                        Returns the RInChI corresponding to a given key.
                        Optionally accepts an argument denoting the type of
                        key to lookup
  -i, --inchi           Returns all RInChIs containing the given InChI with
                        filters
  -l, --layer           Search for a component of an InChI in a database

Input / Output Options:
  -db, --is_database    Assert that the input is a database. If the table_name
                        argument is not provided then the default value of
                        &#39;rinchis03&#39; is used
  -o {list,file,stats}, --output_format {list,file,stats}
                        The format of the output - must be one of &#39;list&#39;,
                        &#39;file&#39;, &#39;stats&#39;

Filters - the changes should be of the form &#39;sp2=1,sp3=-1,...&#39;:
  -hb HYBRIDISATION, --hybridisation HYBRIDISATION
                        The changes in hybridisation sought
  -v VALENCE, --valence VALENCE
                        The changes in valence sought
  -r RINGS, --rings RINGS
                        The changes in ring numbers sought by size
  -f FORMULA, --formula FORMULA
                        The changes in the formula sought by element
  -re RINGELEMENT, --ringelement RINGELEMENT
                        Search for reactions containing a certain ring type
  -iso, --isotopic      Search for reactions containing defined isotopic
                        layers
  -rct, --reactant      Search for the InChI in the reactants
  -pdt, --product       Search for the InChI in the products
  -agt, --agent         Search for the InChI in the agents
  -n NUMBER, --number NUMBER
                        Limit the number of initial search results. A value of
                        0 means no limit
</pre></div>
</div>
<span class="target" id="module-rinchi_stats"></span><div class="section" id="rinchi-statictics-script">
<h1>RInChI Statictics Script<a class="headerlink" href="#rinchi-statictics-script" title="Permalink to this headline">¶</a></h1>
<p>Calculates summary statistics for a flat file of RInChIs.</p>
<p>Modifications:</p>
<blockquote>
<div><ul class="simple">
<li>D.F. Hampshire 2017</li>
</ul>
</div></blockquote>
<dl class="function">
<dt id="rinchi_stats.add_stats">
<code class="descclassname">rinchi_stats.</code><code class="descname">add_stats</code><span class="sig-paren">(</span><em>subparser</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_stats.add_stats" title="Permalink to this definition">¶</a></dt>
<dd><p>Adds the arguments for the stats operation to the <code class="docutils literal"><span class="pre">ArgumentParser</span></code> object.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>subparser</strong> &#8211; An <code class="docutils literal"><span class="pre">ArgumentParser</span></code> object</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_stats.stats_ops">
<code class="descclassname">rinchi_stats.</code><code class="descname">stats_ops</code><span class="sig-paren">(</span><em>args</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_stats.stats_ops" title="Permalink to this definition">¶</a></dt>
<dd><p>Executes the statitics operations.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>args</strong> &#8211; The output of the <code class="docutils literal"><span class="pre">parser.parse_args()</span></code>. The command line arguments.</td>
</tr>
</tbody>
</table>
</dd></dl>

</div>
<div class="highlight-python"><div class="highlight"><pre>usage: rinchi_stats.py [-h] [-all] [-r] [-p] [-a] [-d] [-u] [-m [MOSTCOMMON]]
                       input

RInChI Statistical analysis

positional arguments:
  input                 The flat file of rinchis to generate statistics from

optional arguments:
  -h, --help            show this help message and exit
  -all                  return all information
  -r, --reactants       Include information about the reactants
  -p, --products        Include Information about the products
  -a, --agents          Include information about the agents
  -d, --directions      Include information about the directions
  -u, --unknownstructs  Include information about unknown structures
  -m [MOSTCOMMON], --mostcommon [MOSTCOMMON]
                        Only include information about the most commonly
                        occuring items
</pre></div>
</div>


          </div>
        </div>
      </div>
      <div class="sphinxsidebar" role="navigation" aria-label="main navigation">
        <div class="sphinxsidebarwrapper">
  <h3><a href="index.php">Table Of Contents</a></h3>
  <ul>
<li><a class="reference internal" href="#">RInChI Master Script</a></li>
<li><a class="reference internal" href="#rinchi-addition-script">RInChI Addition Script</a></li>
<li><a class="reference internal" href="#rinchi-changes-analysis-script">RInChI Changes Analysis Script</a></li>
<li><a class="reference internal" href="#rinchi-conversion-script">RInChI Conversion Script</a></li>
<li><a class="reference internal" href="#rinchi-databasing-tools-script">RInChI Databasing Tools Script</a></li>
<li><a class="reference internal" href="#rinchi-searching-script">RInChI Searching Script</a></li>
<li><a class="reference internal" href="#rinchi-statictics-script">RInChI Statictics Script</a></li>
</ul>
<div class="relations">
<h3>Related Topics</h3>
<ul>
  <li><a href="index.php">Documentation overview</a><ul>
      <li>Previous: <a href="rinchi_tools.php" title="previous chapter">RInChI Extended Toolkit</a></li>
  </ul></li>
</ul>
</div>
<div id="searchbox" style="display: none" role="search">
  <h3>Quick search</h3>
    <form class="search" action="search.php" method="get">
      <input type="text" name="q" />
      <input type="submit" value="Go" />
      <input type="hidden" name="check_keywords" value="yes" />
      <input type="hidden" name="area" value="default" />
    </form>
    <p class="searchtip" style="font-size: 90%">
    Enter search terms or a module, class or function name.
    </p>
</div>
<script type="text/javascript">$('#searchbox').show(0);</script>
        </div>
      </div>
      <div class="clearer"></div>
    </div>
    <div class="footer">
      &copy;2017, Duncan Hampshire.
      
      |
      <a href="_sources/rinchi_commands.txt"
          rel="nofollow">Page source</a>
    </div>

    

    
  </body>
</html>
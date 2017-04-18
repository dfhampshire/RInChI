<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">


<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    
    <title>RInChI Extended Toolkit &mdash; RInChI Extended Toolkit 1.0 documentation</title>
    
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
    <link rel="next" title="RInChI Master Script" href="rinchi_commands.php" />
    <link rel="prev" title="Welcome to the RInChI Extended Toolkit documentation!" href="index.php" />
   
  
  <meta name="viewport" content="width=device-width, initial-scale=0.9, maximum-scale=0.9" />

  </head>
  <body role="document">  

    <div class="document">
      <div class="documentwrapper">
        <div class="bodywrapper">
          <div class="body" role="main">
            
  <span class="target" id="module-rinchi_tools"></span><div class="section" id="rinchi-extended-toolkit">
<h1>RInChI Extended Toolkit<a class="headerlink" href="#rinchi-extended-toolkit" title="Permalink to this headline">¶</a></h1>
<p>This module contains additional functions from that officially distributed by the InChI trust. It develops a range of
tools and programs to manipulate RInChIs, a concise machine readable reaction identifier.</p>
<hr class="docutils" />
<blockquote>
<div><p>Licensed under the Apache License, Version 2.0 (the &#8220;License&#8221;); you may not use this file except in compliance with
the License. You may obtain a copy of the License at</p>
<p><a class="reference external" href="http://www.apache.org/licenses/LICENSE-2.0">http://www.apache.org/licenses/LICENSE-2.0</a></p>
<p>Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
on an &#8220;AS IS&#8221; BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
the specific language governing permissions and limitations under the License.</p>
</div></blockquote>
<hr class="docutils" />
<p>Authors:</p>
<blockquote>
<div><ul class="simple">
<li>C.H.G. Allen 2012</li>
<li>N.A. Parker 2013</li>
<li><ol class="first upperalpha" start="2">
<li>Hammond 2014</li>
</ol>
</li>
<li>D.F. Hampshire 2016-17</li>
</ul>
</div></blockquote>
</div>
<span class="target" id="module-rinchi_tools.atom"></span><div class="section" id="rinchi-object-orientated-atom-class-module">
<h1>RInChI Object Orientated Atom Class Module<a class="headerlink" href="#rinchi-object-orientated-atom-class-module" title="Permalink to this headline">¶</a></h1>
<p>This module contains the Atom class and associated functions</p>
<p>Modifications:</p>
<blockquote>
<div><ul>
<li><ol class="first upperalpha simple" start="2">
<li>Hammond 2014</li>
</ol>
</li>
<li><ol class="first upperalpha simple" start="4">
<li>Hampshire 2017</li>
</ol>
<blockquote>
<div><p>Restructuring and changes as documented in Project Report</p>
</div></blockquote>
</li>
</ul>
</div></blockquote>
<dl class="class">
<dt id="rinchi_tools.atom.Atom">
<em class="property">class </em><code class="descclassname">rinchi_tools.atom.</code><code class="descname">Atom</code><span class="sig-paren">(</span><em>index=None</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.atom.Atom" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal"><span class="pre">object</span></code></p>
<p>A class containing a brief description of an atom, for use as nodes in a graph describing a molecule</p>
<dl class="method">
<dt id="rinchi_tools.atom.Atom.get_attached_edges">
<code class="descname">get_attached_edges</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.atom.Atom.get_attached_edges" title="Permalink to this definition">¶</a></dt>
<dd><p>Get the edges attached to this atom.</p>
<p>Returns: The edges attached to the molecule.</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.atom.Atom.get_hybridisation">
<code class="descname">get_hybridisation</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.atom.Atom.get_hybridisation" title="Permalink to this definition">¶</a></dt>
<dd><p>Gets the atom hybridisation.  Only defined for C atoms but still useful</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">None or a string signalling the hybridisation e.g.  &#8220;sp2&#8221;</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.atom.Atom.get_valence">
<code class="descname">get_valence</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.atom.Atom.get_valence" title="Permalink to this definition">¶</a></dt>
<dd><p>Get the valence as determined by counting the number of bonds.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">Number of bonds</td>
</tr>
</tbody>
</table>
</dd></dl>

</dd></dl>

</div>
<span class="target" id="module-rinchi_tools.conversion"></span><div class="section" id="rinchi-conversion-module">
<h1>RInChI Conversion Module<a class="headerlink" href="#rinchi-conversion-module" title="Permalink to this headline">¶</a></h1>
<p>This module provides a variety of functions for the interconversion of RInChIS, Molfiles, RXNfiles and more.</p>
<p>Modifications:</p>
<blockquote>
<div><ul>
<li><p class="first">C.H.G. Allen 2012</p>
</li>
<li><p class="first">N.A. Parker 2013</p>
<blockquote>
<div><p>minor additional material added (specifically, .rxn to mol file agent conversion and
subsequent amendments for agents in the .rxn to RInChI converter). added support to the rxn2rinchi function
for non standard .rxn files containing reaction agents specified separately from the reactants and products.</p>
</div></blockquote>
</li>
<li><ol class="first upperalpha simple" start="2">
<li>Hammond 2014</li>
</ol>
<blockquote>
<div><p>extended support for non standard .rxn files to the rdf parsing functions. Modified all .rxn
handling functions to no longer discard reaction data in the $DTYPE/$DATUM  format, instead optionally returns
them.</p>
</div></blockquote>
</li>
<li><p class="first">D.F. Hampshire 2016</p>
<blockquote>
<div><p>Removed functions now included in source v0.03 software (commands that interface with
RInChI).  Similar python functionality can be found from the rinchi_lib.py interfacing file.  Some functions
are now modified to use this rinchi_lib.py interface. Major restructuring across library means functions have
been extensively moved to / from elsewhere.</p>
</div></blockquote>
</li>
</ul>
</div></blockquote>
<dl class="function">
<dt id="rinchi_tools.conversion.create_csv_from_directory">
<code class="descclassname">rinchi_tools.conversion.</code><code class="descname">create_csv_from_directory</code><span class="sig-paren">(</span><em>root_dir</em>, <em>outname</em>, <em>return_rauxinfo=False</em>, <em>return_longkey=False</em>, <em>return_shortkey=False</em>, <em>return_webkey=False</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.conversion.create_csv_from_directory" title="Permalink to this definition">¶</a></dt>
<dd><p>Iterate recursively over all rdf files in the given folder and combine them into a single .csv database.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>root_dir</strong> &#8211; The directory to search</li>
<li><strong>outname</strong> &#8211; Output file name parameter</li>
<li><strong>return_rauxinfo</strong> &#8211; Include RAuxInfo in the result</li>
<li><strong>return_longkey</strong> &#8211; Include Long key in the result</li>
<li><strong>return_shortkey</strong> &#8211; Include the Short key in the result</li>
<li><strong>return_webkey</strong> &#8211; Include the Web key in the result</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Raises:</th><td class="field-body"><p class="first last"><code class="xref py py-exc docutils literal"><span class="pre">IndexError</span></code> &#8211;
File failed to be recognised for importing</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.conversion.rdf_to_csv">
<code class="descclassname">rinchi_tools.conversion.</code><code class="descname">rdf_to_csv</code><span class="sig-paren">(</span><em>rdf</em>, <em>outfile='rinchi'</em>, <em>return_rauxinfo=False</em>, <em>return_longkey=False</em>, <em>return_shortkey=False</em>, <em>return_webkey=False</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.conversion.rdf_to_csv" title="Permalink to this definition">¶</a></dt>
<dd><p>Convert an RD file to a CSV file containing RInChIs and other optional parameters</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>rdf</strong> &#8211; The RD file as a text block</li>
<li><strong>outfile</strong> &#8211; Optional output file name parameter</li>
<li><strong>return_rauxinfo</strong> &#8211; Include RAuxInfo in the result</li>
<li><strong>return_longkey</strong> &#8211; Include Long key in the result</li>
<li><strong>return_shortkey</strong> &#8211; Include the Short key in the result</li>
<li><strong>return_webkey</strong> &#8211; Include the Web key in the result</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">The name of the CSV file created with the requested fields</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.conversion.rdf_to_csv_append">
<code class="descclassname">rinchi_tools.conversion.</code><code class="descname">rdf_to_csv_append</code><span class="sig-paren">(</span><em>rdf</em>, <em>csv_file</em>, <em>existing_keys=None</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.conversion.rdf_to_csv_append" title="Permalink to this definition">¶</a></dt>
<dd><p>Append an existing CSV file with values from an RD file</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first last simple">
<li><strong>rdf</strong> &#8211; The RD file as a text block</li>
<li><strong>csv_file</strong> &#8211; the CSV file path</li>
<li><strong>existing_keys</strong> &#8211; The keys already existing in the CSV file</li>
</ul>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.conversion.rdf_to_rinchis">
<code class="descclassname">rinchi_tools.conversion.</code><code class="descname">rdf_to_rinchis</code><span class="sig-paren">(</span><em>rdf</em>, <em>start=0</em>, <em>stop=0</em>, <em>force_equilibrium=False</em>, <em>return_rauxinfos=False</em>, <em>return_longkeys=False</em>, <em>return_shortkeys=False</em>, <em>return_webkeys=False</em>, <em>return_rinchis=True</em>, <em>columns=None</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.conversion.rdf_to_rinchis" title="Permalink to this definition">¶</a></dt>
<dd><p>Convert an RDFile to a list of RInChIs.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>rdf</strong> &#8211; The contents of an RDFile as a string.</li>
<li><strong>start</strong> &#8211; The index of the RXN entry within the RDFile at which to start converting.  If set at default value (0),
conversion begins from the first RXN entry.</li>
<li><strong>stop</strong> &#8211; The index of the RXN entry within the RDFile at which to stop converting.  If set at default value (0),
conversion does not stop until the end of the file is reached.</li>
<li><strong>force_equilibrium</strong> &#8211; Whether to set the direction flags explicitly to equilibrium</li>
<li><strong>return_rauxinfos</strong> &#8211; If True, generates and returns RAuxInfo each generated RInChI.</li>
<li><strong>return_longkeys</strong> &#8211; If True, generates and returns Long-RInChIKeys for each generated RInChI.</li>
<li><strong>return_shortkeys</strong> &#8211; If True, generates and returns Short-RInChIKeys for each generated RInChI.</li>
<li><strong>return_webkeys</strong> &#8211; If True, generates and returns Web-RInChIKeys for each generated RInChI.</li>
<li><strong>return_rinchis</strong> &#8211; Return the rinchi. Defaults to True</li>
<li><strong>columns</strong> &#8211; the data to return may be given as list of headers instead.</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">List of dicts of reaction data as defined above. The data types are the keys for each dict</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.conversion.rinchi_to_file">
<code class="descclassname">rinchi_tools.conversion.</code><code class="descname">rinchi_to_file</code><span class="sig-paren">(</span><em>data</em>, <em>rxnout=True</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.conversion.rinchi_to_file" title="Permalink to this definition">¶</a></dt>
<dd><p>Takes a file object or a multi-line string and returns a list of output file text blocks (RXN or RDF)</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>data</strong> &#8211; The string of a file input or a file object.</li>
<li><strong>rxnout</strong> &#8211; Return a reaction file. Otherwise, return an RD file</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">A list of RXN of RD file text blocks</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.conversion.rinchis_to_keys">
<code class="descclassname">rinchi_tools.conversion.</code><code class="descname">rinchis_to_keys</code><span class="sig-paren">(</span><em>data</em>, <em>longkey=False</em>, <em>shortkey=False</em>, <em>webkey=False</em>, <em>inc_rinchi=False</em>, <em>inc_rauxinfo=False</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.conversion.rinchis_to_keys" title="Permalink to this definition">¶</a></dt>
<dd><p>Converts a list of rinchis in a flat file into a dictionary of RInChIs and keys</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>inc_rauxinfo</strong> &#8211; Include the RAuxInfo in the result</li>
<li><strong>data</strong> &#8211; The data string or file object to parse</li>
<li><strong>longkey</strong> &#8211; Whether to include the longkey</li>
<li><strong>shortkey</strong> &#8211; Whether to include the shortkey</li>
<li><strong>webkey</strong> &#8211; Whether to include the webkey</li>
<li><strong>inc_rinchi</strong> &#8211; Whether to include the original rinchi</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first"><p>:</p>
<p>{&#8216;rinchi&#8217;: &#8216;[DATA], &#8216;rauxinfo&#8217;: [DATA, ... }</p>
</p>
</td>
</tr>
<tr class="field-odd field"><th class="field-name">Return type:</th><td class="field-body"><p class="first last">list of dictionaries containing the data produced data with the key as the property name like so</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.conversion.rxn_to_rinchi">
<code class="descclassname">rinchi_tools.conversion.</code><code class="descname">rxn_to_rinchi</code><span class="sig-paren">(</span><em>rxn_text</em>, <em>ret_rauxinfo=False</em>, <em>longkey=False</em>, <em>shortkey=False</em>, <em>webkey=False</em>, <em>force_equilibrium=False</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.conversion.rxn_to_rinchi" title="Permalink to this definition">¶</a></dt>
<dd><p>Convert a RXN to a dictionary of calculated data.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>rxn_text</strong> &#8211; The RXN text as a string</li>
<li><strong>ret_rauxinfo</strong> &#8211; Return RAuxInfo</li>
<li><strong>longkey</strong> &#8211; Return the Long Key</li>
<li><strong>shortkey</strong> &#8211; Return the Short Key</li>
<li><strong>webkey</strong> &#8211; Return the Web Key</li>
<li><strong>force_equilibrium</strong> &#8211; Force the output direction to be an equilibrium</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first"><p>:</p>
<p>{&#8216;rinchi&#8217;: &#8216;[DATA], &#8216;rauxinfo&#8217;: [DATA, ... }</p>
</p>
</td>
</tr>
<tr class="field-odd field"><th class="field-name">Return type:</th><td class="field-body"><p class="first last">A dictionary of data with the key as the property name like so</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

</div>
<span class="target" id="module-rinchi_tools.database"></span><div class="section" id="rinchi-database-module">
<h1>RInChI Database Module<a class="headerlink" href="#rinchi-database-module" title="Permalink to this headline">¶</a></h1>
<p>Provides tools for converting, creating, and removing from SQL databases</p>
<p>Modifications:</p>
<blockquote>
<div><ul>
<li><ol class="first upperalpha simple" start="2">
<li>Hammond 2014</li>
</ol>
</li>
<li><ol class="first upperalpha simple" start="4">
<li>Hampshire 2017</li>
</ol>
<blockquote>
<div><p>Python 3 restructuring and new function addition. Significantly modularised the exisiting code</p>
</div></blockquote>
</li>
</ul>
</div></blockquote>
<dl class="function">
<dt id="rinchi_tools.database.compare_fingerprints">
<code class="descclassname">rinchi_tools.database.</code><code class="descname">compare_fingerprints</code><span class="sig-paren">(</span><em>search_term</em>, <em>db_filename</em>, <em>table_name</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.database.compare_fingerprints" title="Permalink to this definition">¶</a></dt>
<dd><p>Search db for top 10 closest matches to a RInChI by fingerprinting method.  Sent to stdout.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first last simple">
<li><strong>search_term</strong> &#8211; A RInChi or Long-RInChIKey to search with</li>
<li><strong>db_filename</strong> &#8211; the db containing the fingerprints</li>
<li><strong>table_name</strong> &#8211; The table containing the RInChI fingerprints</li>
</ul>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.database.convert_v02_v03">
<code class="descclassname">rinchi_tools.database.</code><code class="descname">convert_v02_v03</code><span class="sig-paren">(</span><em>db_filename</em>, <em>table_name</em>, <em>v02_rinchi=False</em>, <em>v02_rauxinfo=False</em>, <em>v03_rinchi=False</em>, <em>v03_rauxinfo=False</em>, <em>v03_longkey=False</em>, <em>v03_shortkey=False</em>, <em>v03_webkey=False</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.database.convert_v02_v03" title="Permalink to this definition">¶</a></dt>
<dd><p>Converts a db of v02 rinchis into a db of v03 rinchis and associated information.  N.B keys for v02
are not required as new keys must be generated for the db.  Because of the nature of this problem,
this is achieved by creating a new db for the processed data and then transferring back to the original</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first last simple">
<li><strong>db_filename</strong> &#8211; The db filename to which the changes should be made.  The new db is added as a table.</li>
<li><strong>table_name</strong> &#8211; the name for the new v03 rinchi table.</li>
<li><strong>v02_rinchi</strong> &#8211; The name of the v02 rinchi column.  Defaults to False (No RInChI in db).</li>
<li><strong>v02_rauxinfo</strong> &#8211; The name of the v02 rauxinfo column.  Defaults to False (No rauxinfos in db).</li>
<li><strong>v03_rinchi</strong> &#8211; The name of the v03 new rinchi column.  Defaults to False (No rinchi column will be created).</li>
<li><strong>v03_rauxinfo</strong> &#8211; The name of the v03 new rinchi column.  Defaults to False (No rauxinfo column will be created).</li>
<li><strong>v03_longkey</strong> &#8211; The name of the v03 new rinchi column.  Defaults to False (No longkey column will be created).</li>
<li><strong>v03_shortkey</strong> &#8211; The name of the v03 new rinchi column.  Defaults to False (No shortkey column will be created).</li>
<li><strong>v03_webkey</strong> &#8211; The name of the v03 new webkey column.  Defaults to False (No webkey column will be created).</li>
</ul>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.database.csv_to_sql">
<code class="descclassname">rinchi_tools.database.</code><code class="descname">csv_to_sql</code><span class="sig-paren">(</span><em>csv_name</em>, <em>db_filename</em>, <em>table_name</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.database.csv_to_sql" title="Permalink to this definition">¶</a></dt>
<dd><p>Creates or appends an SQL db with values from a CSV file</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first last simple">
<li><strong>csv_name</strong> &#8211; The CSV filename</li>
<li><strong>db_filename</strong> &#8211; The SQLite3 db</li>
<li><strong>table_name</strong> &#8211; The name of the table to create or append</li>
</ul>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.database.gen_rauxinfo">
<code class="descclassname">rinchi_tools.database.</code><code class="descname">gen_rauxinfo</code><span class="sig-paren">(</span><em>db_filename</em>, <em>table_name</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.database.gen_rauxinfo" title="Permalink to this definition">¶</a></dt>
<dd><p>Updates a table in a db to give rauxinfos where the column is null</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first last simple">
<li><strong>db_filename</strong> &#8211; Database filename</li>
<li><strong>table_name</strong> &#8211; name of table</li>
</ul>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.database.rdf_to_sql">
<code class="descclassname">rinchi_tools.database.</code><code class="descname">rdf_to_sql</code><span class="sig-paren">(</span><em>rdfile</em>, <em>db_filename</em>, <em>table_name</em>, <em>columns=None</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.database.rdf_to_sql" title="Permalink to this definition">¶</a></dt>
<dd><p>Creates or adds to an SQLite db the contents of a given RDFile.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first last simple">
<li><strong>rdfile</strong> &#8211; The RD file to add to the db</li>
<li><strong>db_filename</strong> &#8211; The file name of the SQLite db</li>
<li><strong>table_name</strong> &#8211; The name of the table to create or append</li>
<li><strong>columns</strong> &#8211; The columns to add.  If None, the default is [rinchi,rauxinfo,longkey,shortkey,webkey]</li>
</ul>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.database.recall_fingerprints">
<code class="descclassname">rinchi_tools.database.</code><code class="descname">recall_fingerprints</code><span class="sig-paren">(</span><em>lkey</em>, <em>db_filename</em>, <em>table_name</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.database.recall_fingerprints" title="Permalink to this definition">¶</a></dt>
<dd><p>Recall a fingerprint from the db</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>lkey</strong> &#8211; The long key to search for</li>
<li><strong>db_filename</strong> &#8211; The db filename</li>
<li><strong>table_name</strong> &#8211; The table name which stores the fingerprints</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">A numpy array the reaction fingerprint as stored in the reaction db</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.database.search_for_roles">
<code class="descclassname">rinchi_tools.database.</code><code class="descname">search_for_roles</code><span class="sig-paren">(</span><em>db</em>, <em>table_name</em>, <em>reactant_subs=None</em>, <em>product_subs=None</em>, <em>agent_subs=None</em>, <em>limit=200</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.database.search_for_roles" title="Permalink to this definition">¶</a></dt>
<dd><p>Searches for reactions in a particular roles</p>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.database.search_for_roles_advanced">
<code class="descclassname">rinchi_tools.database.</code><code class="descname">search_for_roles_advanced</code><span class="sig-paren">(</span><em>db</em>, <em>table_name</em>, <em>reactant_subs=None</em>, <em>product_subs=None</em>, <em>agent_subs=None</em>, <em>changing_subs=None</em>, <em>exclusive=False</em>, <em>unique=True</em>, <em>limit=200</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.database.search_for_roles_advanced" title="Permalink to this definition">¶</a></dt>
<dd><p>Searches for reactions in a particular functionality</p>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.database.search_master">
<code class="descclassname">rinchi_tools.database.</code><code class="descname">search_master</code><span class="sig-paren">(</span><em>search_term</em>, <em>db=None</em>, <em>table_name=None</em>, <em>is_sql_db=False</em>, <em>hyb=None</em>, <em>val=None</em>, <em>rings=None</em>, <em>formula=None</em>, <em>reactant=False</em>, <em>product=False</em>, <em>agent=False</em>, <em>number=1000</em>, <em>keytype=None</em>, <em>ring_type=None</em>, <em>isotopic=None</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.database.search_master" title="Permalink to this definition">¶</a></dt>
<dd><p>Search for an string within a RInChi database. Includes all options.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>ring_type</strong> &#8211; </li>
<li><strong>isotopic</strong> &#8211; </li>
<li><strong>db</strong> &#8211; </li>
<li><strong>is_sql_db</strong> &#8211; </li>
<li><strong>number</strong> &#8211; Maximum number of initial results</li>
<li><strong>search_term</strong> &#8211; The term to search for</li>
<li><strong>table_name</strong> &#8211; the table to search in</li>
<li><strong>reactant</strong> &#8211; Search for InChIs in the products</li>
<li><strong>product</strong> &#8211; Search for InChIs in the reactants</li>
<li><strong>agent</strong> &#8211; Search for InChIs in the agents</li>
<li><strong>keytype</strong> &#8211; The type of key to look for. If not found, then the function will check if the search term is a key,</li>
<li><strong>try to parse the Key regardless. Otherwise, it assumes to look in the RInChIs</strong> (<em>and</em>) &#8211; </li>
<li><strong>args following are dicts of the format {property</strong> (<em>All</em>) &#8211; count,property2:count2,...}</li>
<li><strong>hyb</strong> &#8211; The hybridisation changes(s) desired</li>
<li><strong>val</strong> &#8211; The valence change(s) desired</li>
<li><strong>rings</strong> &#8211; The ring change(s) desired</li>
<li><strong>formula</strong> &#8211; The formula change(s) desired</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">A dictionary of lists where an inchi was found</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.database.search_rinchis">
<code class="descclassname">rinchi_tools.database.</code><code class="descname">search_rinchis</code><span class="sig-paren">(</span><em>search_term</em>, <em>db=None</em>, <em>table_name=None</em>, <em>is_sql_db=False</em>, <em>hyb=None</em>, <em>val=None</em>, <em>rings=None</em>, <em>formula=None</em>, <em>ringelements=None</em>, <em>isotopic=None</em>, <em>reactant=False</em>, <em>product=False</em>, <em>agent=False</em>, <em>number=1000</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.database.search_rinchis" title="Permalink to this definition">¶</a></dt>
<dd><p>Search for an Inchi within a RInChi database. Includes all options</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>db</strong> &#8211; </li>
<li><strong>is_sql_db</strong> &#8211; </li>
<li><strong>number</strong> &#8211; </li>
<li><strong>search_term</strong> &#8211; The term to search for</li>
<li><strong>table_name</strong> &#8211; the table to search in</li>
<li><strong>args following are dicts of the format {property</strong> (<em>All</em>) &#8211; count,property2:count2,...}</li>
<li><strong>hyb</strong> &#8211; The hybridisation changes(s) desired</li>
<li><strong>val</strong> &#8211; The valence change(s) desired</li>
<li><strong>rings</strong> &#8211; The ring change(s) desired</li>
<li><strong>formula</strong> &#8211; The formula change(s) desired</li>
<li><strong>reactant</strong> &#8211; Search for InChIs in the products</li>
<li><strong>product</strong> &#8211; Search for InChIs in the reactants</li>
<li><strong>agent</strong> &#8211; Search for InChIs in the agents</li>
<li><strong>ringelements</strong> &#8211; </li>
<li><strong>isotopic</strong> &#8211; </li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">A dictionary of lists where an inchi was found</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.database.sql_key_to_rinchi">
<code class="descclassname">rinchi_tools.database.</code><code class="descname">sql_key_to_rinchi</code><span class="sig-paren">(</span><em>key</em>, <em>db_filename</em>, <em>table_name</em>, <em>keytype='L'</em>, <em>column=None</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.database.sql_key_to_rinchi" title="Permalink to this definition">¶</a></dt>
<dd><p>Returns the RInChI matching the given Long RInChI key for a given database</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>key</strong> &#8211; The key to search for</li>
<li><strong>db_filename</strong> &#8211; The database in which to search</li>
<li><strong>table_name</strong> &#8211; The table in which to search for the key</li>
<li><strong>keytype</strong> &#8211; The key type to seach for.  Defaults to the long key</li>
<li><strong>column</strong> &#8211; Optional column to look for the key in.</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Raises:</th><td class="field-body"><p class="first"><code class="xref py py-exc docutils literal"><span class="pre">ValueError</span></code> &#8211;
The keytype argument must be one of &#8220;L&#8221; , &#8220;S&#8221; or &#8220;W&#8221;</p>
</td>
</tr>
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">the corresponding RInChI</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.database.update_fingerprints">
<code class="descclassname">rinchi_tools.database.</code><code class="descname">update_fingerprints</code><span class="sig-paren">(</span><em>db_filename</em>, <em>table_name</em>, <em>fingerprint_table_name</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.database.update_fingerprints" title="Permalink to this definition">¶</a></dt>
<dd><p>NOT CURRENTLY WORKING.  NEEDS UPDATING TO USE MULTITHREADING FOR USABLE PERFORMANCE</p>
<p>Calculates the reaction fingerprint as defined in the reaction Reaction class, and stores it in the given
db in a compressed form</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first last simple">
<li><strong>db_filename</strong> &#8211; the db filename to update</li>
<li><strong>table_name</strong> &#8211; The table containing the RInChIs</li>
<li><strong>fingerprint_table_name</strong> &#8211; The table to contain the fingerprint</li>
</ul>
</td>
</tr>
</tbody>
</table>
</dd></dl>

</div>
<span class="target" id="module-rinchi_tools.matcher"></span><div class="section" id="rinchi-substructure-matching-module">
<h1>RInChI Substructure Matching Module<a class="headerlink" href="#rinchi-substructure-matching-module" title="Permalink to this headline">¶</a></h1>
<p>This module contains the matcher for matching molecules.</p>
<p>Modifications:</p>
<blockquote>
<div><ul class="simple">
<li><ol class="first upperalpha" start="4">
<li>Hampshire 2017</li>
</ol>
</li>
</ul>
</div></blockquote>
<dl class="class">
<dt id="rinchi_tools.matcher.Backup">
<em class="property">class </em><code class="descclassname">rinchi_tools.matcher.</code><code class="descname">Backup</code><span class="sig-paren">(</span><em>matcher_object</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Backup" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal"><span class="pre">object</span></code></p>
<p>Stores the backed up mappings</p>
<dl class="method">
<dt id="rinchi_tools.matcher.Backup.backup">
<code class="descname">backup</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Backup.backup" title="Permalink to this definition">¶</a></dt>
<dd><p>Backs up this iteration of the mapping</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.matcher.Backup.depth">
<code class="descname">depth</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Backup.depth" title="Permalink to this definition">¶</a></dt>
<dd><p>The depth of the iterations</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.matcher.Backup.restore">
<code class="descname">restore</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Backup.restore" title="Permalink to this definition">¶</a></dt>
<dd><p>Restores the previous mapping in the event of a failed mapping</p>
</dd></dl>

</dd></dl>

<dl class="class">
<dt id="rinchi_tools.matcher.Matcher">
<em class="property">class </em><code class="descclassname">rinchi_tools.matcher.</code><code class="descname">Matcher</code><span class="sig-paren">(</span><em>sub</em>, <em>master</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Matcher" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal"><span class="pre">object</span></code></p>
<p>Implementation of VF2 algorithm for matching as a subgraph of another.</p>
<p>made using this <a class="reference external" href="http://lalg.fri.uni-lj.si/pub/amalfi/papers/vf-algorithm.pdf">site</a>.</p>
<p>Uses the python set implementation widely for best performance.</p>
<dl class="method">
<dt id="rinchi_tools.matcher.Matcher.bonds_compatible">
<code class="descname">bonds_compatible</code><span class="sig-paren">(</span><em>mapping</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Matcher.bonds_compatible" title="Permalink to this definition">¶</a></dt>
<dd><p>Checks if the bonds to the atoms in the mapping are compatible</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.matcher.Matcher.count_compatable">
<code class="descname">count_compatable</code><span class="sig-paren">(</span><em>mapping</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Matcher.count_compatable" title="Permalink to this definition">¶</a></dt>
<dd><p>Checks that the terminal sets as computed the mapping have the appropriate bond counts.</p>
<p>Also sets terminal sets for next iteration to avoid unnecessary repeated computation.</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.matcher.Matcher.gen_possible_mappings">
<code class="descname">gen_possible_mappings</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Matcher.gen_possible_mappings" title="Permalink to this definition">¶</a></dt>
<dd><p>The function P(s) which generates the mappings to be tested for the particular current mapping M(s)</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.matcher.Matcher.gen_test_state">
<code class="descname">gen_test_state</code><span class="sig-paren">(</span><em>mapping</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Matcher.gen_test_state" title="Permalink to this definition">¶</a></dt>
<dd><p>Generates a test state for testing criteria.</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.matcher.Matcher.get_backup_mappings">
<code class="descname">get_backup_mappings</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Matcher.get_backup_mappings" title="Permalink to this definition">¶</a></dt>
<dd><p>Get the trial mappings of the atoms in the event that no terminal mappings are found.</p>
<p>The inclusion of the min is fundamental to quick execution of the script</p>
</dd></dl>

<dl class="staticmethod">
<dt id="rinchi_tools.matcher.Matcher.get_terminal_atoms">
<em class="property">static </em><code class="descname">get_terminal_atoms</code><span class="sig-paren">(</span><em>atoms_mapped_set</em>, <em>molecule</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Matcher.get_terminal_atoms" title="Permalink to this definition">¶</a></dt>
<dd><p>Gets the set of atoms in a moleculethat are not in the current mapping but are branches of the current mapping</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.matcher.Matcher.get_terminal_mappings">
<code class="descname">get_terminal_mappings</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Matcher.get_terminal_mappings" title="Permalink to this definition">¶</a></dt>
<dd><p>Gets the mappings based on terminal atoms</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.matcher.Matcher.is_compatible">
<code class="descname">is_compatible</code><span class="sig-paren">(</span><em>mapping</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Matcher.is_compatible" title="Permalink to this definition">¶</a></dt>
<dd><dl class="docutils">
<dt>Checks if:</dt>
<dd><ol class="first last arabic simple">
<li>The atom mapping has the correct atom</li>
<li>Checks that other things</li>
</ol>
</dd>
</dl>
<p>Returns a list of compatible atoms.</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.matcher.Matcher.is_covering">
<code class="descname">is_covering</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Matcher.is_covering" title="Permalink to this definition">¶</a></dt>
<dd><p>Checks if all the atoms are mapped from the sublist in the lists</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.matcher.Matcher.is_sub">
<code class="descname">is_sub</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Matcher.is_sub" title="Permalink to this definition">¶</a></dt>
<dd><p>Returns True if a subgraph of G1 is isomorphic to G2.</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.matcher.Matcher.master_to_sub">
<code class="descname">master_to_sub</code><span class="sig-paren">(</span><em>index</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Matcher.master_to_sub" title="Permalink to this definition">¶</a></dt>
<dd><p>Converts a sub graph index to the master index</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.matcher.Matcher.match">
<code class="descname">match</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Matcher.match" title="Permalink to this definition">¶</a></dt>
<dd><p>Extends the isomorphism mapping, and acts as the iterating function in the VF2 algorithm.</p>
<p>This function is called recursively to determine if a complete
isomorphism can be found between sub and master.  It cleans up the class
variables after each recursive call. If an isomorphism is found,
we return the mapping.</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.matcher.Matcher.new_state">
<code class="descname">new_state</code><span class="sig-paren">(</span><em>mapping</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Matcher.new_state" title="Permalink to this definition">¶</a></dt>
<dd><p>Generates an new state from a mapping</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.matcher.Matcher.sub_count">
<code class="descname">sub_count</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Matcher.sub_count" title="Permalink to this definition">¶</a></dt>
<dd><p>The number of unique matches found in the molecule</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.matcher.Matcher.sub_count_unique">
<code class="descname">sub_count_unique</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Matcher.sub_count_unique" title="Permalink to this definition">¶</a></dt>
<dd></dd></dl>

<dl class="method">
<dt id="rinchi_tools.matcher.Matcher.sub_to_master">
<code class="descname">sub_to_master</code><span class="sig-paren">(</span><em>index</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.matcher.Matcher.sub_to_master" title="Permalink to this definition">¶</a></dt>
<dd><p>Converts a sub graph index to the master index</p>
</dd></dl>

</dd></dl>

</div>
<span class="target" id="module-rinchi_tools.molecule"></span><div class="section" id="rinchi-object-orientated-molecule-class-module">
<h1>RInChI Object Orientated Molecule Class Module<a class="headerlink" href="#rinchi-object-orientated-molecule-class-module" title="Permalink to this headline">¶</a></h1>
<p>This module contains the Molecule class and associated functions</p>
<p>Modifications:</p>
<blockquote>
<div><ul>
<li><ol class="first upperalpha simple" start="2">
<li>Hammond 2014</li>
</ol>
</li>
<li><ol class="first upperalpha simple" start="4">
<li>Hampshire 2017</li>
</ol>
<blockquote>
<div><p>Significant restructuring of the class to gain more consistent and less verbose code.</p>
</div></blockquote>
</li>
</ul>
</div></blockquote>
<dl class="class">
<dt id="rinchi_tools.molecule.Molecule">
<em class="property">class </em><code class="descclassname">rinchi_tools.molecule.</code><code class="descname">Molecule</code><span class="sig-paren">(</span><em>inchi</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal"><span class="pre">object</span></code></p>
<p>A class containing a molecule as defined by an inchi.  Contains functions for generating edge lists and node edge
tables describing molecular graphs, and functions that use molecular graphs to calculate information about the
molecules - ring sizes, atom hybridisation, contained functional groups etc.</p>
<dl class="staticmethod">
<dt id="rinchi_tools.molecule.Molecule.breadth_first_search">
<em class="property">static </em><code class="descname">breadth_first_search</code><span class="sig-paren">(</span><em>graph</em>, <em>start</em>, <em>finish</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.breadth_first_search" title="Permalink to this definition">¶</a></dt>
<dd><p>Get the shortest path between the start and finish nodes</p>
<p>Adapted from <a class="reference external" href="http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/">http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/</a>,
accessed 06/11/2014</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>graph</strong> &#8211; an unweighted, undirected vertex-edge graph as a list</li>
<li><strong>start</strong> &#8211; the starting node</li>
<li><strong>finish</strong> &#8211; the finishing node as</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">The shortest path as a list</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.calculate_edges">
<code class="descname">calculate_edges</code><span class="sig-paren">(</span><em>edge_list=None</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.calculate_edges" title="Permalink to this definition">¶</a></dt>
<dd><p>Sets the node-edge graph as a dict.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>edge_list</strong> &#8211; A molecular graph as a list of edges.  If no list is passed, the function sets the atoms for its
own instance.</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.calculate_rings">
<code class="descname">calculate_rings</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.calculate_rings" title="Permalink to this definition">¶</a></dt>
<dd><p>Sets the ring count property which contains the ring sizes in the format { ring size : number of rings
present, ...}</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.calculate_rings_by_atoms">
<code class="descname">calculate_rings_by_atoms</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.calculate_rings_by_atoms" title="Permalink to this definition">¶</a></dt>
<dd><p>Count the rings by atom list eg.  &#8220;CCCCCN&#8221; will return the number of pyridine fragments in the molecule.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">number of rings</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.chemical_formula_to_dict">
<code class="descname">chemical_formula_to_dict</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.chemical_formula_to_dict" title="Permalink to this definition">¶</a></dt>
<dd><p>Get the chemical formula as a dict</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">A dict with elements as keys and number of atoms as value</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="staticmethod">
<dt id="rinchi_tools.molecule.Molecule.composite_to_simple">
<em class="property">static </em><code class="descname">composite_to_simple</code><span class="sig-paren">(</span><em>inchi</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.composite_to_simple" title="Permalink to this definition">¶</a></dt>
<dd><p>Splits an inchi with multiple disconnected components into a list of connected inchis</p>
<p># Modified 2017 D Hampshire to split formula of multiple identical components
# cf. <a class="reference external" href="http://www.inchi-trust.org/technical-faq/#5.6">http://www.inchi-trust.org/technical-faq/#5.6</a></p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>inchi</strong> &#8211; A inchi (usually composite</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">A list of simple inchis within the composite inchi argument</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.count_centres">
<code class="descname">count_centres</code><span class="sig-paren">(</span><em>wd=False</em>, <em>sp2=True</em>, <em>sp3=True</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.count_centres" title="Permalink to this definition">¶</a></dt>
<dd><p>Counts the centres contained within an inchi</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>wd</strong> &#8211; Whether or not the stereocentre must be well-defined to be counted.</li>
<li><strong>sp2</strong> &#8211; Count sp2 centres</li>
<li><strong>sp3</strong> &#8211; Count sp3 centres</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first">The number of stereocentres
stereo_mols: The number of molecules with stereocentres</p>
</td>
</tr>
<tr class="field-odd field"><th class="field-name">Return type:</th><td class="field-body"><p class="first last">stereocentres</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.count_rings">
<code class="descname">count_rings</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.count_rings" title="Permalink to this definition">¶</a></dt>
<dd><p>Count the number of rings in an InChI.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">The number of rings in the InChI.</td>
</tr>
<tr class="field-even field"><th class="field-name">Return type:</th><td class="field-body">ring_count</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.count_sp2">
<code class="descname">count_sp2</code><span class="sig-paren">(</span><em>wd=False</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.count_sp2" title="Permalink to this definition">¶</a></dt>
<dd><p>Count the number of sp2 stereocentres.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>wd</strong> &#8211; Whether or not the stereocentre must be well-defined to be counted.</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">The number of sp2 stereocentres in the structure.</td>
</tr>
<tr class="field-odd field"><th class="field-name">Return type:</th><td class="field-body">sp2_centre_count</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.count_sp3">
<code class="descname">count_sp3</code><span class="sig-paren">(</span><em>wd=False</em>, <em>enantio=False</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.count_sp3" title="Permalink to this definition">¶</a></dt>
<dd><p>Count the number of sp3 stereocentres in a molecule.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>wd</strong> &#8211; Whether or not the stereocentre must be well-defined to be counted.</li>
<li><strong>enantio</strong> &#8211; Whether or not the structure must be enantiopure to be counted.</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">The number of sp3 stereocentres in the structure.</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.depth_first_search">
<code class="descname">depth_first_search</code><span class="sig-paren">(</span><em>start=1</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.depth_first_search" title="Permalink to this definition">¶</a></dt>
<dd><p>Performs a DFS over the molecular graph of a given Molecule object, returning a list of edges that form a
spanning tree (tree edges), and a list of the edges that would cyclise this spanning tree (back edges)</p>
<p>The number of back edges returned is equal to the number of rings that can be described in the molecule</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>start</strong> &#8211; Set which atom should be the starting node</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">A list of tree edges.
back_edges: A list of back edges. The list length is equal to the smallest number of cycles that can
describe the cycle space of the molecular graph</td>
</tr>
<tr class="field-odd field"><th class="field-name">Return type:</th><td class="field-body">tree_edges</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="staticmethod">
<dt id="rinchi_tools.molecule.Molecule.edge_list_to_atoms_spanned">
<em class="property">static </em><code class="descname">edge_list_to_atoms_spanned</code><span class="sig-paren">(</span><em>edge_list</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.edge_list_to_atoms_spanned" title="Permalink to this definition">¶</a></dt>
<dd><p>Takes an edge list and returns a list of atoms spanned</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>edge_list</strong> &#8211; An edge list</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">A list of all the keys for the atoms which are spanned by the edge list.</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.edge_list_to_vector">
<code class="descname">edge_list_to_vector</code><span class="sig-paren">(</span><em>subset</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.edge_list_to_vector" title="Permalink to this definition">¶</a></dt>
<dd><p>Converts an edge list to a vector in the (0, 1)^N vector space spanned by the edges of the molecule</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>subset</strong> &#8211; The vector subset to use</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">The vector stored as a list.</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="staticmethod">
<dt id="rinchi_tools.molecule.Molecule.edges_to_atoms">
<em class="property">static </em><code class="descname">edges_to_atoms</code><span class="sig-paren">(</span><em>ls</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.edges_to_atoms" title="Permalink to this definition">¶</a></dt>
<dd><p>Sets the node-edge graph as a dict.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>ls</strong> &#8211; A molecular graph as a list of edges.  If no list is passed, the function sets the atoms for its
own instance.</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.find_initial_ring_set">
<code class="descname">find_initial_ring_set</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.find_initial_ring_set" title="Permalink to this definition">¶</a></dt>
<dd><p>For every edge in the molecule, find the smallest ring is it a part of, add it to a list
NEEDS REIMPLEMENTATION</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">list of all minimal rings, sorted by the number of edges they contain</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.find_initial_ring_set_trial">
<code class="descname">find_initial_ring_set_trial</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.find_initial_ring_set_trial" title="Permalink to this definition">¶</a></dt>
<dd><p>For every edge in the molecule, find the smallest ring is it a part of, add it to a list
TRIAL REIMPLEMENTATION, NOT YET WORKING</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">list of all minimal rings, sorted by the number of edges they contain</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.find_linearly_independent">
<code class="descname">find_linearly_independent</code><span class="sig-paren">(</span><em>cycles</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.find_linearly_independent" title="Permalink to this definition">¶</a></dt>
<dd><p>Given a list of candidate cycles, sorted by size, this function attempts to find the smallest,
linearly independent basis of cycles that spans the entire cycle space of the molecular graph - the Minimum
Cycle Basis.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>cycles</strong> &#8211; list of candidate cycles sorted by size</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">None</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.find_rings_from_back_edges">
<code class="descname">find_rings_from_back_edges</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.find_rings_from_back_edges" title="Permalink to this definition">¶</a></dt>
<dd><p>Accepts output from the depth_first_search algorithm, returns a list of all rings within the molecule.</p>
<p>Will NOT find a minimum cycle basis, but can be used to find an initial cycle set when performing the Horton
Algorithm (see elsewhere)</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.find_shortest_path">
<code class="descname">find_shortest_path</code><span class="sig-paren">(</span><em>graph</em>, <em>start</em>, <em>end</em>, <em>path=None</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.find_shortest_path" title="Permalink to this definition">¶</a></dt>
<dd><p>Recursively iterates over the entire molecular graph, yielding the shortest path between two points</p>
<p>Adapted from <a class="reference external" href="https://www.python.org/doc/essays/graphs/">https://www.python.org/doc/essays/graphs/</a>, accessed 15/10/2014</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>graph</strong> &#8211; an unweighted, undirected vertex-edge graph as a list</li>
<li><strong>start</strong> &#8211; the starting node as a number</li>
<li><strong>end</strong> &#8211; the finishing node as a number</li>
<li><strong>path</strong> &#8211; latest iteration of the path</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">The shortest path as a list of indices</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.generate_edge_list">
<code class="descname">generate_edge_list</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.generate_edge_list" title="Permalink to this definition">¶</a></dt>
<dd><p>Takes the connective layer of an inchi and returns the molecular graph as an edge list, parsing it directly
using re.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">A list containing the edges of the molecular graph</td>
</tr>
<tr class="field-even field"><th class="field-name">Return type:</th><td class="field-body">edges</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.get_formula">
<code class="descname">get_formula</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.get_formula" title="Permalink to this definition">¶</a></dt>
<dd><p>Get chemical empirical formula</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">Chemical formula stored as a counter</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.get_hybrid_count">
<code class="descname">get_hybrid_count</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.get_hybrid_count" title="Permalink to this definition">¶</a></dt>
<dd><p>Calculate the hybridisation of each atom</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">A Counter object containing the hybridisation of the atoms</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.get_ring_count">
<code class="descname">get_ring_count</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.get_ring_count" title="Permalink to this definition">¶</a></dt>
<dd><p>Get the ring count</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">a Counter object containing the number of rings of each size</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.get_ring_count_inc_elements">
<code class="descname">get_ring_count_inc_elements</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.get_ring_count_inc_elements" title="Permalink to this definition">¶</a></dt>
<dd><p>Count the rings of a molecule.  Result includes the elements of the ring.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">a Counter containing the number of rings of each size and the elements contained by a ring</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.get_valence_count">
<code class="descname">get_valence_count</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.get_valence_count" title="Permalink to this definition">¶</a></dt>
<dd><p>Calculates the valences of each atom in the Molecule</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">A Counter object containing the valences of the atoms</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.has_isotopic_layer">
<code class="descname">has_isotopic_layer</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.has_isotopic_layer" title="Permalink to this definition">¶</a></dt>
<dd><p>Does the molecule inchi have an isotopic layer?</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">A boolean value</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.inchi_to_chemical_formula">
<code class="descname">inchi_to_chemical_formula</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.inchi_to_chemical_formula" title="Permalink to this definition">¶</a></dt>
<dd><p>Converts an Inchi to a Chemical formula</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">The Chemical Formula of the Molecule as a string</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.inchi_to_layer">
<code class="descname">inchi_to_layer</code><span class="sig-paren">(</span><em>l</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.inchi_to_layer" title="Permalink to this definition">¶</a></dt>
<dd><p>Get a particular layer of the InChI</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>l</strong> &#8211; The layer of the InChI to retrieve</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">The InChI layer desired</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.initialize">
<code class="descname">initialize</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.initialize" title="Permalink to this definition">¶</a></dt>
<dd><p>Initialises the molecule</p>
</dd></dl>

<dl class="staticmethod">
<dt id="rinchi_tools.molecule.Molecule.new">
<em class="property">static </em><code class="descname">new</code><span class="sig-paren">(</span><em>inchi</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.new" title="Permalink to this definition">¶</a></dt>
<dd><p>Creates a list of new Molecule objects.  Safer than Molecule() due to composite InChI implications.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>inchi</strong> &#8211; An InChI string</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">list of Molecule objects.</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="staticmethod">
<dt id="rinchi_tools.molecule.Molecule.path_to_cycle_edge_list">
<em class="property">static </em><code class="descname">path_to_cycle_edge_list</code><span class="sig-paren">(</span><em>path</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.path_to_cycle_edge_list" title="Permalink to this definition">¶</a></dt>
<dd><p>Converts a cycle described by an ordered list of nodes to an edge list</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>path</strong> &#8211; The path of the cycle stored as an ordered list</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">The edge list</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.set_atomic_hydrogen">
<code class="descname">set_atomic_hydrogen</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.set_atomic_hydrogen" title="Permalink to this definition">¶</a></dt>
<dd><p>Takes the molecular graph and the inchi, and sets the number of protons attached to each atom.</p>
<p>Requires initialised atoms.</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.set_atoms">
<code class="descname">set_atoms</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.set_atoms" title="Permalink to this definition">¶</a></dt>
<dd><p>Sets the atoms objects with their appropriate indexes and elements for each of the instances of the the Atom
class.</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.molecule.Molecule.vector_to_edge_list">
<code class="descname">vector_to_edge_list</code><span class="sig-paren">(</span><em>vector</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.molecule.Molecule.vector_to_edge_list" title="Permalink to this definition">¶</a></dt>
<dd><p>Takes an edge vector and returns an edge list</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>vector</strong> &#8211; an edge vector stored in an iterable</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">The edge list</td>
</tr>
</tbody>
</table>
</dd></dl>

</dd></dl>

</div>
<span class="target" id="module-rinchi_tools.reaction"></span><div class="section" id="rinchi-object-orientated-reaction-class-module">
<h1>RInChI Object Orientated Reaction Class Module<a class="headerlink" href="#rinchi-object-orientated-reaction-class-module" title="Permalink to this headline">¶</a></h1>
<p>This module contains the Reaction class and associated functions</p>
<p>Modifications:</p>
<blockquote>
<div><ul>
<li><ol class="first upperalpha simple" start="2">
<li>Hammond 2014</li>
</ol>
</li>
<li><ol class="first upperalpha simple" start="4">
<li>Hampshire 2017</li>
</ol>
<blockquote>
<div><p>Significant restructuring of the class to gain more consistent and less verbose code.</p>
</div></blockquote>
</li>
</ul>
</div></blockquote>
<dl class="class">
<dt id="rinchi_tools.reaction.Reaction">
<em class="property">class </em><code class="descclassname">rinchi_tools.reaction.</code><code class="descname">Reaction</code><span class="sig-paren">(</span><em>rinchi</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal"><span class="pre">object</span></code></p>
<p>This class defines a reaction, as defined by a RInChI.  Molecule objects are created from all component InChIs,
and the member functions of the class can be used to analyse various parameters that may be changing across the
reaction</p>
<dl class="method">
<dt id="rinchi_tools.reaction.Reaction.calculate_reaction_fingerprint">
<code class="descname">calculate_reaction_fingerprint</code><span class="sig-paren">(</span><em>fingerprint_size=1024</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction.calculate_reaction_fingerprint" title="Permalink to this definition">¶</a></dt>
<dd><p>Calculates a reaction fingerprint for a given reaction.  Uses a 1024 bit fingerprint by default</p>
<p>Method of Daniel M. Lowe (2015)</p>
<p>This function generates fingerprints for individual molecules using obabel. Could be simply modified to use
other software packages ie.  RDKIT if desired</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>fingerprint_size</strong> &#8211; The length of the fingerprint to be generated.</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.reaction.Reaction.change_across_reaction">
<code class="descname">change_across_reaction</code><span class="sig-paren">(</span><em>func</em>, <em>*args</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction.change_across_reaction" title="Permalink to this definition">¶</a></dt>
<dd><p>Calculates the total change in a parameter across a molecule, Molecule class function and returns a Python
Counter object</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>func</strong> &#8211; The class function to calculate the parameter, which returns a Counter object</li>
<li><strong>args</strong> &#8211; Args if required for the function</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">the change in the parameter</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.reaction.Reaction.detect_reaction">
<code class="descname">detect_reaction</code><span class="sig-paren">(</span><em>hyb_i=None</em>, <em>val_i=None</em>, <em>rings_i=None</em>, <em>formula_i=None</em>, <em>isotopic=False</em>, <em>ring_present=None</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction.detect_reaction" title="Permalink to this definition">¶</a></dt>
<dd><p>Detect if a reaction satisfies certain conditions.  Allows searching for reactions based on ring changes,
valence changes, formula changes, hybridisation of C atom changes.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>args are dicts of the format {property</strong> (<em>All</em>) &#8211; count,property2:count2,...}</li>
<li><strong>hyb_i</strong> &#8211; The hybridisation change(s) desired</li>
<li><strong>val_i</strong> &#8211; The valence change(s) desired</li>
<li><strong>rings_i</strong> &#8211; The ring change(s) desired</li>
<li><strong>formula_i</strong> &#8211; The formula change(s) desired</li>
<li><strong>isotopic</strong> &#8211; Whether to look for reactions involving an isotopic InChI</li>
<li><strong>ring_present</strong> &#8211; Look for a ring in the reaction</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">True if the given reaction satisfies all the conditions, otherwise False.</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.reaction.Reaction.generate_svg_image">
<code class="descname">generate_svg_image</code><span class="sig-paren">(</span><em>outname</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction.generate_svg_image" title="Permalink to this definition">¶</a></dt>
<dd><p>Outputs the reactants, products, and agents as SVG files in the current directory with the given filename</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>outname</strong> &#8211; the name of the file to output the SVG image</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.reaction.Reaction.has_isotopic_inchi">
<code class="descname">has_isotopic_inchi</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction.has_isotopic_inchi" title="Permalink to this definition">¶</a></dt>
<dd></dd></dl>

<dl class="method">
<dt id="rinchi_tools.reaction.Reaction.has_ring">
<code class="descname">has_ring</code><span class="sig-paren">(</span><em>ring</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction.has_ring" title="Permalink to this definition">¶</a></dt>
<dd></dd></dl>

<dl class="method">
<dt id="rinchi_tools.reaction.Reaction.has_substructures">
<code class="descname">has_substructures</code><span class="sig-paren">(</span><em>reactant_subs=None</em>, <em>product_subs=None</em>, <em>agent_subs=None</em>, <em>exclusive=True</em>, <em>rct_disappears=True</em>, <em>pdt_appears=True</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction.has_substructures" title="Permalink to this definition">¶</a></dt>
<dd><p>Detects if the reaction is a substructure</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>reactant_subs</strong> &#8211; Lists of reactant inchis</li>
<li><strong>product_subs</strong> &#8211; List of product inchis</li>
<li><strong>agent_subs</strong> &#8211; List of agent inchis</li>
<li><strong>exclusive</strong> &#8211; Match one functionality per molecule of reactant</li>
<li><strong>rct_disappears</strong> &#8211; Only match if substructures not in products</li>
<li><strong>pdt_appears</strong> &#8211; Only match if substructures not in reactants</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">Boolean, whether the substructures are contained</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.reaction.Reaction.has_substructures_by_populations">
<code class="descname">has_substructures_by_populations</code><span class="sig-paren">(</span><em>reactant_subs=None</em>, <em>product_subs=None</em>, <em>agent_subs=None</em>, <em>changing_subs=None</em>, <em>exclusive=False</em>, <em>unique=True</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction.has_substructures_by_populations" title="Permalink to this definition">¶</a></dt>
<dd><p>Detects if the reaction is a substructure</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>reactant_subs</strong> &#8211; Dictionary of reactant inchis and their populations in the layer</li>
<li><strong>product_subs</strong> &#8211; Dictionary of product inchis and their populations in the layer</li>
<li><strong>agent_subs</strong> &#8211; Dictionary of product inchis and their populations in the layer</li>
<li><strong>changing_subs</strong> &#8211; Dictionary of inchi changes in populations</li>
<li><strong>exclusive</strong> &#8211; Match one functionality per molecule of reactant</li>
<li><strong>unique</strong> &#8211; Prevent matching the same atoms</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">Boolean, whether the substructures are contained</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.reaction.Reaction.is_agent">
<code class="descname">is_agent</code><span class="sig-paren">(</span><em>inchi</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction.is_agent" title="Permalink to this definition">¶</a></dt>
<dd><p>Determine whether the reaction is catalytic in a particular chemical</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>inchi</strong> &#8211; A InChI string specifying a molecule</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">True or False (Boolean)</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.reaction.Reaction.is_balanced">
<code class="descname">is_balanced</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction.is_balanced" title="Permalink to this definition">¶</a></dt>
<dd><p>Determine if a reaction is balanced</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">True if Balanced, False otherwise.</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.reaction.Reaction.longkey">
<code class="descname">longkey</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction.longkey" title="Permalink to this definition">¶</a></dt>
<dd><p>Set longkey if not already set, then return longkey</p>
</dd></dl>

<dl class="staticmethod">
<dt id="rinchi_tools.reaction.Reaction.present_in_layer">
<em class="property">static </em><code class="descname">present_in_layer</code><span class="sig-paren">(</span><em>layer</em>, <em>inchi</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction.present_in_layer" title="Permalink to this definition">¶</a></dt>
<dd><p>Checks if an InChI is is present in a layer</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>layer</strong> &#8211; A reaction layer</li>
<li><strong>inchi</strong> &#8211; an Inchi</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">Returns the RInChI if the inchi is present, otherwise returns None.</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.reaction.Reaction.present_in_reaction">
<code class="descname">present_in_reaction</code><span class="sig-paren">(</span><em>func</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction.present_in_reaction" title="Permalink to this definition">¶</a></dt>
<dd><p>Tests if a molecule is present in the reaction</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>func</strong> &#8211; function of a Molecule object that returns True if a given condition is satisfied</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">If the function returns true for any InChI, the parent RInChI is returned</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.reaction.Reaction.ring_change">
<code class="descname">ring_change</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction.ring_change" title="Permalink to this definition">¶</a></dt>
<dd><p>Determine how the number of rings changes in a reaction. Old method</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">A counter containing the changes across the reaction.</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.reaction.Reaction.shortkey">
<code class="descname">shortkey</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction.shortkey" title="Permalink to this definition">¶</a></dt>
<dd><p>Set shortkey if not already set, then return shortkey</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.reaction.Reaction.stereo_change">
<code class="descname">stereo_change</code><span class="sig-paren">(</span><em>wd=False</em>, <em>sp2=True</em>, <em>sp3=True</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction.stereo_change" title="Permalink to this definition">¶</a></dt>
<dd><p>Determine whether a reaction creates or destroys stereochemistry. Old Methold</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>wd</strong> &#8211; Whether only well-defined stereocentres count.</li>
<li><strong>sp2</strong> &#8211; Whether to count sp2 stereocentres.</li>
<li><strong>sp3</strong> &#8211; Whether to count sp3 stereocentres.</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">The number of stereocentres created by a reaction stored as a value in a dictionary</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.reaction.Reaction.webkey">
<code class="descname">webkey</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.reaction.Reaction.webkey" title="Permalink to this definition">¶</a></dt>
<dd><p>Set webkey if not already set, then return webkey</p>
</dd></dl>

</dd></dl>

</div>
<span class="target" id="module-rinchi_tools.rinchi_lib"></span><div class="section" id="rinchi-c-library-interface-module">
<h1>RInChI C Library Interface Module<a class="headerlink" href="#rinchi-c-library-interface-module" title="Permalink to this headline">¶</a></h1>
<p>This module provides functions defining how RInChIs and RAuxInfos are constructed from InChIs and reaction data.  It
also interfaces with the RInChI v0.03 software as provided by the InChI trust.</p>
<p>This file is based on that provided with the official v0.03 RInChI software release, but with modifications to ensure
Python 3 compatibility.  Documentation was adapted from the official v0.03 release document.</p>
<p>Modifications:</p>
<blockquote>
<div><ul class="simple">
<li><ol class="first upperalpha" start="4">
<li>Hampshire 2017</li>
</ol>
</li>
</ul>
</div></blockquote>
<dl class="class">
<dt id="rinchi_tools.rinchi_lib.RInChI">
<em class="property">class </em><code class="descclassname">rinchi_tools.rinchi_lib.</code><code class="descname">RInChI</code><span class="sig-paren">(</span><em>lib_path='/home/dh493/Documents/rinchi03-extended/rinchi_tools/libs/librinchi.so.1.0.0'</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.rinchi_lib.RInChI" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal"><span class="pre">object</span></code></p>
<p>The RInChI class interfaces the C class in the librinchi library</p>
<dl class="method">
<dt id="rinchi_tools.rinchi_lib.RInChI.file_text_from_rinchi">
<code class="descname">file_text_from_rinchi</code><span class="sig-paren">(</span><em>rinchi_string</em>, <em>rinchi_auxinfo</em>, <em>output_format</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.rinchi_lib.RInChI.file_text_from_rinchi" title="Permalink to this definition">¶</a></dt>
<dd><p>Reconstructs (or attempts to reconstruct) RD or RXN file from RInChI string and RAuxInfo</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>rinchi_string</strong> &#8211; The RInChI string to convert</li>
<li><strong>rinchi_auxinfo</strong> &#8211; The RAuxInfo to convert (optional, recommended)</li>
<li><strong>output_format</strong> &#8211; &#8220;RD&#8221; or &#8220;RXN&#8221;</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">The text block for the file</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.rinchi_lib.RInChI.inchis_from_rinchi">
<code class="descname">inchis_from_rinchi</code><span class="sig-paren">(</span><em>rinchi_string</em>, <em>rinchi_auxinfo=''</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.rinchi_lib.RInChI.inchis_from_rinchi" title="Permalink to this definition">¶</a></dt>
<dd><p>Splits an RInChI string and optional RAuxInfo into components.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>rinchi_string</strong> &#8211; A RInChI string</li>
<li><strong>rinchi_auxinfo</strong> &#8211; RAuxInfo string.  May be blank but may not be NULL.</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Raises:</th><td class="field-body"><p class="first"><code class="xref py py-exc docutils literal"><span class="pre">Exception</span></code> &#8211;
RInChi format related errors</p>
</td>
</tr>
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body"><p class="first"><p>:</p>
<blockquote>
<div><dl class="docutils">
<dt>{&#8216;Direction&#8217;: [direction character],</dt>
<dd><p class="first last">&#8216;No-Structures&#8217;: [list of no-structures],
&#8216;Reactants&#8217;: [list of inchis &amp; auxinfos],
&#8216;Products&#8217;: [list of inchis &amp; auxinfos],
&#8216;Agents&#8217;: [list of inchis] &amp; auxinfos}</p>
</dd>
</dl>
</div></blockquote>
<p>Each Reactant, Product, and Agent list contains a set of (InChI, AuxInfo) tuples. The
No-Structures list contains No-Structure counts for Reactants, Products, and Agents.</p>
</p>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Return type:</th><td class="field-body"><p class="first last">A dictionary of data returned. The structure is as below</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.rinchi_lib.RInChI.rinchi_errorcheck">
<code class="descname">rinchi_errorcheck</code><span class="sig-paren">(</span><em>return_code</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.rinchi_lib.RInChI.rinchi_errorcheck" title="Permalink to this definition">¶</a></dt>
<dd><p>Specifies Python error handling behavior</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>return_code</strong> &#8211; the return code from the C library</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.rinchi_lib.RInChI.rinchi_from_file_text">
<code class="descname">rinchi_from_file_text</code><span class="sig-paren">(</span><em>input_format</em>, <em>rxnfile_data</em>, <em>force_equilibrium=False</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.rinchi_lib.RInChI.rinchi_from_file_text" title="Permalink to this definition">¶</a></dt>
<dd><p>Generates RInChI string and RAuxInfo from supplied RD or RXN file text.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>input_format</strong> &#8211; “AUTO”, &#8220;RD&#8221; or &#8220;RXN&#8221; (with “AUTO” as default value)</li>
<li><strong>rxnfile_data</strong> &#8211; text block of RD or RXN file data</li>
<li><strong>force_equilibrium</strong> (<em>bool</em>) &#8211; Force interpretation of reaction as equilibrium reaction</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">tuple pair of the RInChI and RAuxInfo generated</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.rinchi_lib.RInChI.rinchikey_from_file_text">
<code class="descname">rinchikey_from_file_text</code><span class="sig-paren">(</span><em>input_format</em>, <em>file_text</em>, <em>key_type</em>, <em>force_equilibrium=False</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.rinchi_lib.RInChI.rinchikey_from_file_text" title="Permalink to this definition">¶</a></dt>
<dd><p>Generates RInChI key of supplied RD or RXN file text.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>input_format</strong> &#8211; &#8220;RD&#8221; or &#8220;RXN&#8221;</li>
<li><strong>file_text</strong> &#8211; text block of RD or RXN file data</li>
<li><strong>key_type</strong> &#8211; 1 letter controlling the type of key generated; “L” for Long-RInChIKey, “S” for Short key</li>
<li><strong>“W” for Web key</strong> (<em>(Short-RInChIKey),</em>) &#8211; </li>
<li><strong>force_equilibrium</strong> (<em>bool</em>) &#8211; Force interpretation of reaction as equilibrium reaction</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">a RInChIKey</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.rinchi_lib.RInChI.rinchikey_from_rinchi">
<code class="descname">rinchikey_from_rinchi</code><span class="sig-paren">(</span><em>rinchi_string</em>, <em>key_type</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.rinchi_lib.RInChI.rinchikey_from_rinchi" title="Permalink to this definition">¶</a></dt>
<dd><p>Generates RInChI key of supplied RD or RXN file text.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>rinchi_string</strong> &#8211; A RInChI string</li>
<li><strong>key_type</strong> &#8211; 1 letter controlling the type of key generated with “L” for the Long-RInChIKey, “S” for the Short
key (Short-RInChIKey), “W” for the Web key (Web-RInChIKey)</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">the RInChiKey</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

</dd></dl>

<dl class="class">
<dt id="rinchi_tools.rinchi_lib.StringHandler">
<em class="property">class </em><code class="descclassname">rinchi_tools.rinchi_lib.</code><code class="descname">StringHandler</code><a class="headerlink" href="#rinchi_tools.rinchi_lib.StringHandler" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal"><span class="pre">object</span></code></p>
<p>Enables seamless use with Python 3 by converting to ascii within the argument objects</p>
<dl class="classmethod">
<dt id="rinchi_tools.rinchi_lib.StringHandler.from_param">
<em class="property">classmethod </em><code class="descname">from_param</code><span class="sig-paren">(</span><em>value</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.rinchi_lib.StringHandler.from_param" title="Permalink to this definition">¶</a></dt>
<dd><p>Performs the conversion</p>
</dd></dl>

</dd></dl>

</div>
<span class="target" id="module-rinchi_tools.tools"></span><div class="section" id="rinchi-tools-module">
<h1>RInChI Tools Module<a class="headerlink" href="#rinchi-tools-module" title="Permalink to this headline">¶</a></h1>
<p>This module provides functions defining how RInChIs and RAuxInfos are constructed from InChIs and reaction data.  It
also interfaces with the RInChI v0.03 software as provided by the InChI trust.</p>
<p>Modifications:</p>
<blockquote>
<div><ul class="simple">
<li>C.H.G. Allen 2012</li>
<li>D.F. Hampshire 2016</li>
</ul>
</div></blockquote>
<dl class="function">
<dt id="rinchi_tools.tools.add">
<code class="descclassname">rinchi_tools.tools.</code><code class="descname">add</code><span class="sig-paren">(</span><em>rinchis</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.tools.add" title="Permalink to this definition">¶</a></dt>
<dd><p>Combines a list of RInChIs into one combined RInChI.</p>
<p>N.B.  As stoichiometry is not represented in the input, this is an approximate addition.</p>
<p>Substances from RInChIs are sorted into one of four &#8220;pots&#8221;:</p>
<blockquote>
<div><ul>
<li><p class="first">&#8220;Used&#8221; contains substances which have acted as a reagent, and have not yet been created again as a product.</p>
</li>
<li><p class="first">&#8220;Made&#8221; contains substances which have been created as a product of a step, and have yet to be used again.</p>
</li>
<li><dl class="first docutils">
<dt>&#8220;Present&#8221; contains substance which have been present during a step, but have not yet been used up or</dt>
<dd><p class="first last">substances which have been used as a reagent, and later regenerated as a product.</p>
</dd>
</dl>
</li>
<li><p class="first">&#8220;Intermediates&#8221; contains substances which have been created as a product, and later used as a reagent.</p>
</li>
</ul>
</div></blockquote>
<p>Each RInChI is considered in turn:</p>
<dl class="docutils">
<dt>The reactants are considered:</dt>
<dd><ul class="first last simple">
<li>If novel, add to &#8220;used&#8221;.</li>
<li>If in &#8220;used&#8221;, remain in &#8220;used&#8221;.</li>
<li>If in &#8220;made&#8221;, move to &#8220;intermediates&#8221;.</li>
<li>If in &#8220;present&#8221;, move to &#8220;used&#8221;.</li>
<li>If in &#8220;intermediates&#8221;, remain in &#8220;intermediates&#8221;.</li>
</ul>
</dd>
<dt>The products are considered:</dt>
<dd><ul class="first last simple">
<li>If novel, add to &#8220;made&#8221;.</li>
<li>If in &#8220;used&#8221;, move to &#8220;present&#8221;.</li>
<li>If in &#8220;made&#8221;, remain in &#8220;made&#8221;.</li>
<li>If in &#8220;present&#8221;, remain in &#8220;present&#8221;.</li>
<li>If in &#8220;intermediates&#8221;, move to &#8220;made&#8221;.</li>
</ul>
</dd>
<dt>The extras are considered:</dt>
<dd><ul class="first last simple">
<li>If novel, add to &#8220;present&#8221;.</li>
</ul>
</dd>
<dt>The pots are then emptied into the following output receptacles:</dt>
<dd><ul class="first last simple">
<li>&#8220;Used&#8221; -&gt; LHS InChIs</li>
<li>&#8220;Made&#8221; -&gt; RHS InChIs</li>
<li>&#8220;Present&#8221; -&gt; BHS InChIs</li>
<li>&#8220;Intermediates&#8221; -&gt; discarded</li>
</ul>
</dd>
</dl>
<p>Finally, the RInChI is constructed in the usual way and returned.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>rinchis</strong> &#8211; A list of RInChIs, representing a sequence of reactions making up one overall process.  The order
of this list is important, as each RInChI is interpreted as a step in the overall process.  They must
also have a clearly defined direction.</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">A RInChI representing the overall process.</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.tools.build_rauxinfo">
<code class="descclassname">rinchi_tools.tools.</code><code class="descname">build_rauxinfo</code><span class="sig-paren">(</span><em>l2_auxinfo</em>, <em>l3_auxinfo</em>, <em>l4_auxinfo</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.tools.build_rauxinfo" title="Permalink to this definition">¶</a></dt>
<dd><p>Takes 3 sets of AuxInfos and converts them into a RAuxInfo.  n.b.  The order of Inchis in each list is presumed
to be corresponding to that in the RInChI</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>l2_auxinfo</strong> &#8211; List of layer 2 AuxInfos</li>
<li><strong>l3_auxinfo</strong> &#8211; List of layer 3 AuxInfos</li>
<li><strong>l4_auxinfo</strong> &#8211; List of layer 4 AuxInfos</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">An RAuxInfo</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.tools.build_rinchi">
<code class="descclassname">rinchi_tools.tools.</code><code class="descname">build_rinchi</code><span class="sig-paren">(</span><em>l2_inchis=None</em>, <em>l3_inchis=None</em>, <em>l4_inchis=None</em>, <em>direction=''</em>, <em>u_struct=''</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.tools.build_rinchi" title="Permalink to this definition">¶</a></dt>
<dd><p>Build a RInChI from the specified InChIs and reaction data.</p>
<p>RInChI Builder takes three groups of InChIs, and additional reaction data (currently limited to directionality
information), and returns a RInChI.</p>
<p>The first three arguments are groups of InChIs saved as strings within an iterable (e.g.  a list, set,
tuple). Any or all of these may be omitted.  All InChIs must be of the same version number.  If a chemical
which cannot be described by an InChI is desired within the RInChI, it should be added to the u_struct
argument detailed below.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>l2_inchis</strong> &#8211; Chemicals in the second layer of the RInChI</li>
<li><strong>l3_inchis</strong> &#8211; Chemicals in the third layer of the RInChI</li>
<li><strong>l4_inchis</strong> &#8211; Chemicals in the fourth layer of a RInChI.  It refers to the substances present at the start and
end of the reaction (e.g.  catalysts, solvents), only referred to as &#8220;agents&#8221;.</li>
<li><strong>direction</strong> &#8211; This must be &#8220;+&#8221;, &#8220;-&#8221; or &#8220;=&#8221;.  &#8220;+&#8221; means that l2_inchis_input are the reactants, and the l3_inchis
the products; &#8220;-&#8221; means the opposite; and &#8220;=&#8221; means the l2_inchis and l3_inchis are in equilibrium.</li>
<li><strong>u_struct</strong> &#8211; Defines the number of unknown structures in each layer.  This must be a list of the form [#2,#3,
#4] where #2 is the number of unknown reactants in layer 2, #3 is number in layer 3 etc.</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first">The RinChI made from the input InChIs and reaction data.</p>
</td>
</tr>
<tr class="field-odd field"><th class="field-name">Raises:</th><td class="field-body"><p class="first last"><code class="xref py py-exc docutils literal"><span class="pre">VersionError</span></code> &#8211;
The input InChIs are not of the same version.</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.tools.build_rinchi_rauxinfo">
<code class="descclassname">rinchi_tools.tools.</code><code class="descname">build_rinchi_rauxinfo</code><span class="sig-paren">(</span><em>l2_input=None</em>, <em>l3_input=None</em>, <em>l4_input=None</em>, <em>direction=''</em>, <em>u_struct=''</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.tools.build_rinchi_rauxinfo" title="Permalink to this definition">¶</a></dt>
<dd><p>Build a RInChI and RAuxInfo from the specified InChIs and reaction data.</p>
<p>RInChI Builder takes three groups of InChIs, and additional reaction data, and returns a RInChI.</p>
<p>The first three arguments are tuples of InChI and RAuxInfo pairs within an iterable (e.g.  a list, set,
tuple). Any or all of these may be omitted.  All InChIs must be of the same version number.  If a chemical
which cannot be described by an InChI is desired within the RInChI, it should be added to the u_struct
argument detailed below.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>u_struct</strong> &#8211; Defines the number of unknown structures in each layer.  This must be a list of the form [#2,#3, #4]
where #2 is the number of unknown reactants in layer 2, #3 is number in layer 3 etc.</li>
<li><strong>l2_input</strong> &#8211; Chemicals in the second layer of the RInChI</li>
<li><strong>l3_input</strong> &#8211; Chemicals in the third layer of the RInChI</li>
<li><strong>l4_input</strong> &#8211; Chemicals in the fourth layer of a RInChI.  It refers to the substances present at the start and
end of the reaction (e.g.  catalysts, solvents), only referred to as &#8220;agents&#8221;.</li>
<li><strong>direction</strong> &#8211; This must be &#8220;+&#8221;, &#8220;-&#8221; or &#8220;=&#8221;.  &#8220;+&#8221; means that the LHS are the reactants, and the RHS the products;
&#8220;-&#8221; means the opposite; and &#8220;=&#8221; means the LHS and RHS are in equilibrium.</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first">The RInChI  and RAuxInfo made from the input InChIs and reaction data.</p>
</td>
</tr>
<tr class="field-odd field"><th class="field-name">Raises:</th><td class="field-body"><p class="first last"><code class="xref py py-exc docutils literal"><span class="pre">VersionError</span></code> &#8211;
The input InChIs are not of the same version.</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.tools.dedupe_rinchi">
<code class="descclassname">rinchi_tools.tools.</code><code class="descname">dedupe_rinchi</code><span class="sig-paren">(</span><em>rinchi</em>, <em>rauxinfo=''</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.tools.dedupe_rinchi" title="Permalink to this definition">¶</a></dt>
<dd><p>Removes duplicate InChI entries from the RInChI</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>rinchi</strong> &#8211; A RInChI string</li>
<li><strong>rauxinfo</strong> &#8211; Optional RAuxInfo</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">A RInChI and RAuxInfo tuple</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.tools.generate_rauxinfo">
<code class="descclassname">rinchi_tools.tools.</code><code class="descname">generate_rauxinfo</code><span class="sig-paren">(</span><em>rinchi</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.tools.generate_rauxinfo" title="Permalink to this definition">¶</a></dt>
<dd><p>Create RAuxInfo for a RInChI using the InChI conversion function.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>rinchi</strong> &#8211; The RInChI of which to create the RAuxInfo.</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">The RAuxInfo of the RinChI.</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.tools.inchi_2_auxinfo">
<code class="descclassname">rinchi_tools.tools.</code><code class="descname">inchi_2_auxinfo</code><span class="sig-paren">(</span><em>inchi</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.tools.inchi_2_auxinfo" title="Permalink to this definition">¶</a></dt>
<dd><p>Run the InChI software on an InChI to generate AuxInfo.</p>
<p>The function saves the InChI to a temporary file, and runs the inchi-1 program on this tempfile as a subprocess.
The AuxInfo will not include 2D coordinates, but an AuxInfo of some kind is required for the InChI software to
convert an InChI to an SDFile.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>inchi</strong> &#8211; An InChI from which to generate AuxInfo.</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">The InChI&#8217;s AuxInfo (will not contain 2D coordinates).</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.tools.process_stats">
<code class="descclassname">rinchi_tools.tools.</code><code class="descname">process_stats</code><span class="sig-paren">(</span><em>rinchis</em>, <em>mostcommon=None</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.tools.process_stats" title="Permalink to this definition">¶</a></dt>
<dd><p>Takes an iterable</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>rinchis</strong> &#8211; An iterable of RInChIs</li>
<li><strong>mostcommon</strong> &#8211; Return only the most common items</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">Dictionary of counters containing the information.</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.tools.remove_stereo">
<code class="descclassname">rinchi_tools.tools.</code><code class="descname">remove_stereo</code><span class="sig-paren">(</span><em>inchi</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.tools.remove_stereo" title="Permalink to this definition">¶</a></dt>
<dd><p>Removes stereochemistry from an InChI</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>inchi</strong> &#8211; an InChI as a string</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">an InChI</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.tools.rinchi_to_dict_list">
<code class="descclassname">rinchi_tools.tools.</code><code class="descname">rinchi_to_dict_list</code><span class="sig-paren">(</span><em>data</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.tools.rinchi_to_dict_list" title="Permalink to this definition">¶</a></dt>
<dd><p>Takes a text block or file object and parse a dictionary of RInChI entries</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>data</strong> &#8211; The text block or file object to parse</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">A list of dictionaries containing each dictionary entry</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.tools.split_rinchi">
<code class="descclassname">rinchi_tools.tools.</code><code class="descname">split_rinchi</code><span class="sig-paren">(</span><em>rinchi</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.tools.split_rinchi" title="Permalink to this definition">¶</a></dt>
<dd><p>Returns the inchis without RAuxInfo, each in lists, and the direct and no_structs lists</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>rinchi</strong> &#8211; A RInChI String</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><dl class="docutils">
<dt>rct_inchis:</dt>
<dd>List of reactant inchis</dd>
<dt>pdt_inchis:</dt>
<dd>List of product inchis</dd>
<dt>agt_inchis:</dt>
<dd>List of agent inchis</dd>
<dt>direction:</dt>
<dd>returns the direction character</dd>
<dt>no_structs:</dt>
<dd>returns a list of the numbers of unknown structures in each layer</dd>
</dl>
</td>
</tr>
<tr class="field-odd field"><th class="field-name">Return type:</th><td class="field-body">A tuple containing</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.tools.split_rinchi_inc_auxinfo">
<code class="descclassname">rinchi_tools.tools.</code><code class="descname">split_rinchi_inc_auxinfo</code><span class="sig-paren">(</span><em>rinchi</em>, <em>rinchi_auxinfo</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.tools.split_rinchi_inc_auxinfo" title="Permalink to this definition">¶</a></dt>
<dd><p>Returns the inchi and auxinfo pairs, each in lists, the direction character, and a list of unknown structures.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>rinchi</strong> &#8211; A RInChI String</li>
<li><strong>rinchi_auxinfo</strong> &#8211; The corresponding RAuxInfo</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first"><dl class="docutils">
<dt>rct_inchis:</dt>
<dd><p class="first last">List of reactant inchi and auxinfo pairs</p>
</dd>
<dt>pdt_inchis:</dt>
<dd><p class="first last">List of product inchi and auxinfo pairs</p>
</dd>
<dt>agt_inchis:</dt>
<dd><p class="first last">List of agent inchi and auxinfo pairs</p>
</dd>
<dt>direction:</dt>
<dd><p class="first last">returns the direction character</p>
</dd>
<dt>no_structs:</dt>
<dd><p class="first last">returns a list of the numbers of unknown structures in each layer</p>
</dd>
</dl>
</p>
</td>
</tr>
<tr class="field-odd field"><th class="field-name">Return type:</th><td class="field-body"><p class="first last">A tuple containing</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.tools.split_rinchi_only_auxinfo">
<code class="descclassname">rinchi_tools.tools.</code><code class="descname">split_rinchi_only_auxinfo</code><span class="sig-paren">(</span><em>rinchi</em>, <em>rinchi_auxinfo</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.tools.split_rinchi_only_auxinfo" title="Permalink to this definition">¶</a></dt>
<dd><p>Returns the RAuxInfo</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>rinchi</strong> &#8211; A RInChI String</li>
<li><strong>rinchi_auxinfo</strong> &#8211; The corresponding RAuxInfo</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first"><dl class="docutils">
<dt>rct_inchis_auxinfo:</dt>
<dd><p class="first last">List of reactant AuxInfos</p>
</dd>
<dt>pdt_inchis_auxinfo:</dt>
<dd><p class="first last">List of product AuxInfos</p>
</dd>
<dt>agt_inchis_auxinfo:</dt>
<dd><p class="first last">List of agent AuxInfos</p>
</dd>
</dl>
</p>
</td>
</tr>
<tr class="field-odd field"><th class="field-name">Return type:</th><td class="field-body"><p class="first last">A tuple containing</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

</div>
<span class="target" id="module-rinchi_tools.utils"></span><div class="section" id="rinchi-utilities-module">
<h1>RInChI Utilities Module<a class="headerlink" href="#rinchi-utilities-module" title="Permalink to this headline">¶</a></h1>
<p>This module provides functions that perform various non RInChI specific tasks.</p>
<p>Modifications:</p>
<blockquote>
<div><ul class="simple">
<li>D.F. Hampshire 2016</li>
</ul>
</div></blockquote>
<dl class="class">
<dt id="rinchi_tools.utils.Hashable">
<em class="property">class </em><code class="descclassname">rinchi_tools.utils.</code><code class="descname">Hashable</code><span class="sig-paren">(</span><em>val</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.utils.Hashable" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal"><span class="pre">object</span></code></p>
<p>Make an object hashable for counting. Used to count counters</p>
</dd></dl>

<dl class="class">
<dt id="rinchi_tools.utils.Spinner">
<em class="property">class </em><code class="descclassname">rinchi_tools.utils.</code><code class="descname">Spinner</code><span class="sig-paren">(</span><em>delay=None</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.utils.Spinner" title="Permalink to this definition">¶</a></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal"><span class="pre">object</span></code></p>
<p>A spinner which shows during a long process.</p>
<dl class="attribute">
<dt id="rinchi_tools.utils.Spinner.busy">
<code class="descname">busy</code><em class="property"> = False</em><a class="headerlink" href="#rinchi_tools.utils.Spinner.busy" title="Permalink to this definition">¶</a></dt>
<dd></dd></dl>

<dl class="attribute">
<dt id="rinchi_tools.utils.Spinner.delay">
<code class="descname">delay</code><em class="property"> = 0.1</em><a class="headerlink" href="#rinchi_tools.utils.Spinner.delay" title="Permalink to this definition">¶</a></dt>
<dd></dd></dl>

<dl class="staticmethod">
<dt id="rinchi_tools.utils.Spinner.spinning_cursor">
<em class="property">static </em><code class="descname">spinning_cursor</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.utils.Spinner.spinning_cursor" title="Permalink to this definition">¶</a></dt>
<dd></dd></dl>

<dl class="method">
<dt id="rinchi_tools.utils.Spinner.start">
<code class="descname">start</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.utils.Spinner.start" title="Permalink to this definition">¶</a></dt>
<dd><p>Starts the spinner</p>
</dd></dl>

<dl class="method">
<dt id="rinchi_tools.utils.Spinner.stop">
<code class="descname">stop</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.utils.Spinner.stop" title="Permalink to this definition">¶</a></dt>
<dd><p>Stops the spinner</p>
</dd></dl>

</dd></dl>

<dl class="function">
<dt id="rinchi_tools.utils.call_command">
<code class="descclassname">rinchi_tools.utils.</code><code class="descname">call_command</code><span class="sig-paren">(</span><em>args</em>, <em>debug=False</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.utils.call_command" title="Permalink to this definition">¶</a></dt>
<dd><p>Run a command as a subprocess and return the output</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>args</strong> &#8211; The command to execute as a string</li>
<li><strong>debug</strong> &#8211; Debug the command</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">The output of query and error code</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.utils.consolidate">
<code class="descclassname">rinchi_tools.utils.</code><code class="descname">consolidate</code><span class="sig-paren">(</span><em>items</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.utils.consolidate" title="Permalink to this definition">¶</a></dt>
<dd><p>Check that all non-empty items in an iterable are identical</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>items</strong> &#8211; the iterable</td>
</tr>
<tr class="field-even field"><th class="field-name">Raises:</th><td class="field-body"><code class="xref py py-exc docutils literal"><span class="pre">ValueError</span></code> &#8211;
Items are not all identical</td>
</tr>
<tr class="field-odd field"><th class="field-name">Returns:</th><td class="field-body">the value of all the items in the list</td>
</tr>
<tr class="field-even field"><th class="field-name">Return type:</th><td class="field-body">value</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.utils.construct_output_text">
<code class="descclassname">rinchi_tools.utils.</code><code class="descname">construct_output_text</code><span class="sig-paren">(</span><em>data</em>, <em>header_order=False</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.utils.construct_output_text" title="Permalink to this definition">¶</a></dt>
<dd><p>Turns a variable containing a list of dicts or a dict or dict of lists into a single string of data</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>data</strong> &#8211; The data variable</li>
<li><strong>header_order</strong> &#8211; Optional list of keys for the dictionaries. The list can contain non present keys.</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">The output as a text block</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.utils.counter_to_print_string">
<code class="descclassname">rinchi_tools.utils.</code><code class="descname">counter_to_print_string</code><span class="sig-paren">(</span><em>counter</em>, <em>name</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.utils.counter_to_print_string" title="Permalink to this definition">¶</a></dt>
<dd><p>Formats counter for printing</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first last simple">
<li><strong>counter</strong> &#8211; The <code class="docutils literal"><span class="pre">Counter</span></code> object</li>
<li><strong>name</strong> &#8211; Name of the data stored in the counter</li>
</ul>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.utils.create_output_file">
<code class="descclassname">rinchi_tools.utils.</code><code class="descname">create_output_file</code><span class="sig-paren">(</span><em>output_path</em>, <em>default_extension</em>, <em>create_out_dir=True</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.utils.create_output_file" title="Permalink to this definition">¶</a></dt>
<dd><p>Creates an output file</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>output_path</strong> &#8211; the path of the file to create</li>
<li><strong>default_extension</strong> &#8211; the extension to use for the file</li>
<li><strong>create_out_dir</strong> &#8211; Create an output directory</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">A tuple containing a file object and the path of the file object.</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.utils.output">
<code class="descclassname">rinchi_tools.utils.</code><code class="descname">output</code><span class="sig-paren">(</span><em>text</em>, <em>output_path=False</em>, <em>default_extension=False</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.utils.output" title="Permalink to this definition">¶</a></dt>
<dd><p>Simple output wrapper to print or write outputs.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first last simple">
<li><strong>text</strong> &#8211; text input</li>
<li><strong>output_path</strong> &#8211; Specifies the filename for the output file</li>
<li><strong>default_extension</strong> &#8211; specifies the file extension if none in the outputname</li>
</ul>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.utils.read_input_file">
<code class="descclassname">rinchi_tools.utils.</code><code class="descname">read_input_file</code><span class="sig-paren">(</span><em>input_path</em>, <em>filetype_check=False</em>, <em>return_file_object=False</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.utils.read_input_file" title="Permalink to this definition">¶</a></dt>
<dd><p>Reads an input path into a string</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>input_path</strong> &#8211; The path of the file to open</li>
<li><strong>filetype_check</strong> &#8211; Check type of file</li>
<li><strong>return_file_object</strong> &#8211; Return a file object instead of a string</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">A multi-line string or a file object</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.utils.string_to_dict">
<code class="descclassname">rinchi_tools.utils.</code><code class="descname">string_to_dict</code><span class="sig-paren">(</span><em>string</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.utils.string_to_dict" title="Permalink to this definition">¶</a></dt>
<dd><p>Converts a string of form &#8216;a=1,b=2,c=3&#8217; to a dictionary of form {a:1,b:2,c:3}</p>
</dd></dl>

</div>
<span class="target" id="module-rinchi_tools.v02_rinchi_key"></span><div class="section" id="version-0-02-rinchikey-generation-library-module">
<h1>Version 0.02 RInChIKey Generation Library Module<a class="headerlink" href="#version-0-02-rinchikey-generation-library-module" title="Permalink to this headline">¶</a></h1>
<p>This module provides functions to create Long- and Short-RInChIKeys from RInChIs.</p>
<p>The supplied implementation of the inchi_2_inchikey function uses the InChIKey creation algorithm from OASA,
a free python library for the manipulation of chemical formats, now stored permanently in the v02_inchi_key.py module.</p>
<p>Modifications:</p>
<blockquote>
<div><ul>
<li><p class="first">C.H.G. Allen 2012</p>
</li>
<li><p class="first">D.F. Hampshire 2016</p>
<blockquote>
<div><p>Modified for Python3 compatibility</p>
</div></blockquote>
</li>
</ul>
</div></blockquote>
<dl class="function">
<dt id="rinchi_tools.v02_rinchi_key.rinchi_2_longkey">
<code class="descclassname">rinchi_tools.v02_rinchi_key.</code><code class="descname">rinchi_2_longkey</code><span class="sig-paren">(</span><em>rinchi</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.v02_rinchi_key.rinchi_2_longkey" title="Permalink to this definition">¶</a></dt>
<dd><p>Create Long-RInChIKey from a RInChI.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>rinchi</strong> &#8211; The RInChI of which to create the RAuxInfo.</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">The Long-RInChIKey of the RinChI.</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.v02_rinchi_key.rinchi_2_shortkey">
<code class="descclassname">rinchi_tools.v02_rinchi_key.</code><code class="descname">rinchi_2_shortkey</code><span class="sig-paren">(</span><em>rinchi</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.v02_rinchi_key.rinchi_2_shortkey" title="Permalink to this definition">¶</a></dt>
<dd><p>Create a Short-RInChIKey from a RInChI.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>rinchi</strong> &#8211; The RInChI from which to create the Short-RInChIKey</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">The Short-RInChIKey of the RInChI</td>
</tr>
</tbody>
</table>
</dd></dl>

</div>
<span class="target" id="module-rinchi_tools.v02_tools"></span><div class="section" id="rinchi-v0-02-to-0-03-conversion-module">
<h1>RInChI v0.02 to 0.03 Conversion Module<a class="headerlink" href="#rinchi-v0-02-to-0-03-conversion-module" title="Permalink to this headline">¶</a></h1>
<p>Modifications:</p>
<blockquote>
<div><ul class="simple">
<li>D.F. Hampshire 2016</li>
</ul>
</div></blockquote>
<dl class="function">
<dt id="rinchi_tools.v02_tools.convert_all">
<code class="descclassname">rinchi_tools.v02_tools.</code><code class="descname">convert_all</code><span class="sig-paren">(</span><em>rinchi</em>, <em>rauxinfo</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.v02_tools.convert_all" title="Permalink to this definition">¶</a></dt>
<dd><p>Convert a v0.02 RInChI &amp; RAuxInfo into a v0.03 RInChI &amp; RAuxInfo.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>rinchi</strong> &#8211; A RInChI of version 0.02.</li>
<li><strong>rauxinfo</strong> &#8211; A RAuxInfo of version 0.02.</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first"><dl class="docutils">
<dt>rauxinfo:</dt>
<dd><p class="first last">A RAuxInfo of version 0.03.</p>
</dd>
<dt>rauxinfo:</dt>
<dd><p class="first last">A RAuxInfo of version 0.03.</p>
</dd>
</dl>
</p>
</td>
</tr>
<tr class="field-odd field"><th class="field-name">Return type:</th><td class="field-body"><p class="first last">A tuple containing</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.v02_tools.convert_rauxinfo">
<code class="descclassname">rinchi_tools.v02_tools.</code><code class="descname">convert_rauxinfo</code><span class="sig-paren">(</span><em>rauxinfo</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.v02_tools.convert_rauxinfo" title="Permalink to this definition">¶</a></dt>
<dd><p>Convert a v0.02 RAuxInfo into a v0.03 RAuxInfo.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>rauxinfo</strong> &#8211; A RAuxInfo of version 0.02.</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">A RAuxInfo of version 0.03.</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.v02_tools.convert_rinchi">
<code class="descclassname">rinchi_tools.v02_tools.</code><code class="descname">convert_rinchi</code><span class="sig-paren">(</span><em>rinchi</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.v02_tools.convert_rinchi" title="Permalink to this definition">¶</a></dt>
<dd><p>Convert a v0.02 RInChI into a v0.03 RInChI.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>rinchi</strong> &#8211; A RInChI of version 0.02.</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">A RInChI of version 0.03.</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="rinchi_tools.v02_tools.generate_rauxinfo">
<code class="descclassname">rinchi_tools.v02_tools.</code><code class="descname">generate_rauxinfo</code><span class="sig-paren">(</span><em>rinchi</em><span class="sig-paren">)</span><a class="headerlink" href="#rinchi_tools.v02_tools.generate_rauxinfo" title="Permalink to this definition">¶</a></dt>
<dd><p>Create RAuxInfo for a RInChI using a conversion function.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><strong>rinchi</strong> &#8211; The RInChI of which to create the RAuxInfo.</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body">The RAuxInfo of the RinChI</td>
</tr>
<tr class="field-odd field"><th class="field-name">Raises:</th><td class="field-body"><code class="xref py py-exc docutils literal"><span class="pre">VersionError</span></code> &#8211;
If the generated AuxInfos are not of the same version.</td>
</tr>
</tbody>
</table>
</dd></dl>

</div>


          </div>
        </div>
      </div>
      <div class="sphinxsidebar" role="navigation" aria-label="main navigation">
        <div class="sphinxsidebarwrapper">
  <h3><a href="index.php">Table Of Contents</a></h3>
  <ul>
<li><a class="reference internal" href="#">RInChI Extended Toolkit</a></li>
<li><a class="reference internal" href="#rinchi-object-orientated-atom-class-module">RInChI Object Orientated Atom Class Module</a></li>
<li><a class="reference internal" href="#rinchi-conversion-module">RInChI Conversion Module</a></li>
<li><a class="reference internal" href="#rinchi-database-module">RInChI Database Module</a></li>
<li><a class="reference internal" href="#rinchi-substructure-matching-module">RInChI Substructure Matching Module</a></li>
<li><a class="reference internal" href="#rinchi-object-orientated-molecule-class-module">RInChI Object Orientated Molecule Class Module</a></li>
<li><a class="reference internal" href="#rinchi-object-orientated-reaction-class-module">RInChI Object Orientated Reaction Class Module</a></li>
<li><a class="reference internal" href="#rinchi-c-library-interface-module">RInChI C Library Interface Module</a></li>
<li><a class="reference internal" href="#rinchi-tools-module">RInChI Tools Module</a></li>
<li><a class="reference internal" href="#rinchi-utilities-module">RInChI Utilities Module</a></li>
<li><a class="reference internal" href="#version-0-02-rinchikey-generation-library-module">Version 0.02 RInChIKey Generation Library Module</a></li>
<li><a class="reference internal" href="#rinchi-v0-02-to-0-03-conversion-module">RInChI v0.02 to 0.03 Conversion Module</a></li>
</ul>
<div class="relations">
<h3>Related Topics</h3>
<ul>
  <li><a href="index.php">Documentation overview</a><ul>
      <li>Previous: <a href="index.php" title="previous chapter">Welcome to the RInChI Extended Toolkit documentation!</a></li>
      <li>Next: <a href="rinchi_commands.php" title="next chapter">RInChI Master Script</a></li>
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
      <a href="_sources/rinchi_tools.txt"
          rel="nofollow">Page source</a>
    </div>

    

    
  </body>
</html>
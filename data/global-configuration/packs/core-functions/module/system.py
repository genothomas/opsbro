from opsbro.evaluater import export_evaluater_function
from opsbro.gossip import gossiper
from opsbro.misc.lolcat import lolcat


@export_evaluater_function
def get_os():
    """**get_os()** -> return a string about the os.

<code>
    Example:
        get_os()

    Returns:
        'linux'
</code>
    """
    import platform
    return platform.system().lower()


@export_evaluater_function
def have_group(group):
    """**have_group(group)** -> return True if the node have the group, False otherwise.

 * group: (string) group to check.


<code>
    Example:
        have_group('linux')
    Returns:
        True
</code>
    """
    return gossiper.have_group(group)


try:
    import pwd, grp
    from pwd import getpwnam
    from grp import getgrnam
except ImportError, exp:
    getpwnam = getgrnam = None


@export_evaluater_function
def user_exists(username_or_uid):
    """**user_exists(uname_or_uid)** -> return True if the node username/uid does exists, False otherwise.

 * username_or_uid: (string or int) string of the username or int for the user id.

<code>
    Example:
        user_exists('root')
    Returns:
        True
</code>
    """
    if getpwnam is None:
        raise Exception('This function is not available on this OS')
    
    # is an int or a string?
    try:
        uid = int(username_or_uid)
    except ValueError:
        uid = None
    
    # Maybe we have a uid, maybe a string to search
    if uid is not None:
        try:
            pwd.getpwuid(uid)
            # We can get it's data, he/she does exists
            return True
        except KeyError:
            # ok no such uid
            return False
    # else: is a string
    try:
        getpwnam(username_or_uid)
        return True  # we can get he/she data
    except KeyError:  # no such user sorry
        return False


@export_evaluater_function
def group_exists(groupname_or_gid):
    """**group_exists(groupname_or_gid)** -> return True if the groupname/gid does exists, False otherwise.

 * groupname_or_gid: (string or int) string of the groupname or int for the group id.

<code>
    Example:
        group_exists('www-data')
    Returns:
        True
</code>
    """
    if getgrnam is None:
        raise Exception('This function is not available on this OS')
    
    # is an int or a string?
    try:
        gid = int(groupname_or_gid)
    except ValueError:
        gid = None
    
    # Maybe we have a uid, maybe a string to search
    if gid is not None:
        try:
            grp.getgrgid(gid)
            # We can get it's data, he/she does exists
            return True
        except KeyError:
            # ok no such uid
            return False
    # else: is a string
    try:
        getgrnam(groupname_or_gid)
        return True  # we can get he/she data
    except KeyError:  # no such group sorry
        return False


@export_evaluater_function
def colorize(s, color):
    """**colorize(s, color)** -> return the string s with the color (ainsi)

 * s: (string) string to colorize
 * color: (int between 1 -> 64) ainsi color

<code>
    Example:
        colorize('my string', 55)
    Returns:
        \x1b[55Dmy string\x1b[0m
</code>
    """
    if not isinstance(s, basestring):
        try:
            s = unicode(s)
        except:
            return ''
    return lolcat.get_line(s, color, spread=None)











'''
diskfree
Table of Contents
Prototype: diskfree(path)
Return type: int
Descriptions: Return the free space (in KB) available on the current partition of path.
If path is not found, this function returns 0.
Arguments:
path: string, in the range: "?(/.*)
Example:
body common control
{
      bundlesequence => { "example" };
}

bundle agent example
{
  classes:
      "has_space" expression => isgreaterthan($(free), 0);

  vars:
      "free" int => diskfree("/tmp");

  reports:
    has_space::
      "The filesystem has free space";
    !has_space::
      "The filesystem has NO free space";
}
Output:
R: The filesystem has free space
'''




'''
execresult
Table of Contents
Prototype: execresult(command, shell)
Return type: string
The return value is cached.
Description: Execute command and return output as string.
If the command is not found, the result will be the empty string.
The shell argument decides whether a shell will be used to encapsulate the command. This is necessary in order to combine commands with pipes etc, but remember that each command requires a new process that reads in files beyond CFEngine's control. Thus using a shell is both a performance hog and a potential security issue.
Arguments:
command: string, in the range: .+
shell: one of
noshell
useshell
powershell
Example:
Prepare:
rm -rf /tmp/testhere
mkdir -p /tmp/testhere
touch /tmp/testhere/a
touch /tmp/testhere/b
touch /tmp/testhere/c
touch /tmp/testhere/d
touch /tmp/testhere/e
Run:
body common control
{
      bundlesequence  => { "example" };
}

bundle agent example
{
  vars:
      "my_result" string => execresult("/bin/ls /tmp/testhere","noshell");

  reports:
      "/bin/ls /tmp/testhere returned '$(my_result)'";
}
Output:
R: /bin/ls /tmp/testhere returned 'a
b
c
d
e'
Notes: you should never use this function to execute commands that make changes to the system, or perform lengthy computations. Such an operation is beyond CFEngine's ability to guarantee convergence, and on multiple passes and during syntax verification these function calls are executed, resulting in system changes that are covert. Calls to execresult should be for discovery and information extraction only. Effectively calls to this function will be also repeatedly executed by cf-promises when it does syntax checking, which is highly undesirable if the command is expensive. Consider using commands promises instead, which have locking and are not evaluated by cf-promises.
See also: returnszero().
Change: policy change in CFEngine 3.0.5. Previously newlines were changed for spaces, now newlines are preserved.
'''


'''
findprocesses
Table of Contents
Prototype: findprocesses(regex)
Return type: data
The return value is cached.
Description: Return the list of processes that match the given regular expression regex.
This function searches for the given regular expression in the process table. Use .*sherlock.* to find all the processes that match sherlock. Use .*\bsherlock\b.* to exclude partial matches like sherlock123 (\b matches a word boundary).
Arguments:
regex: regular expression, in the range: .*
The returned data container is a list of key-value maps. Each one is guaranteed to have the key pid with the process ID. The key line will also be available with the raw process table contents.
The process table is usually obtained with something like ps -eo user,pid,ppid,pgid,%cpu,%mem,vsize,ni,rss,stat,nlwp,stime,time,args, and the CMD or COMMAND field (args) is used to match against. However the exact data used may change per platform and per CFEngine release.
Example:
    vars:
      "holmes" data => findprocesses(".*sherlock.*");
Output:
    [ { "pid": "2378", "line": "...the ps output here" }, ... ]
History: Introduced in CFEngine 3.9
See also: processes processexists().
'''



'''
getusers
Table of Contents
Prototype: getusers(exclude_names, exclude_ids)
Return type: slist
Description: Returns a list of all users defined, except those names in exclude_names and uids in exclude_ids
Arguments:
exclude_names: string, in the range: .*
exclude_ids: string, in the range: .*
Example:
body common control
{
      bundlesequence => { "example" };
}

bundle agent example
{
  vars:
      "allusers" slist => getusers("","");
      "root_list" slist => { "root" };
      # this will get just the root users out of the full user list
      "justroot" slist => intersection(allusers, root_list);

  reports:
      "Found just the root user: $(justroot)";
}
Output:
R: Found just the root user: root
Notes: This function is currently only available on Unix-like systems.
History: Was introduced in version 3.1.0b1,Nova 2.0.0b1 (2010).
See also: getuserinfo(), users.
'''


'''
getenv
Table of Contents
Prototype: getenv(variable, maxlength)
Return type: string
Description: Return the environment variable variable, truncated at maxlength characters
Returns an empty string if the environment variable is not defined. maxlength is used to avoid unexpectedly large return values, which could lead to security issues. Choose a reasonable value based on the environment variable you are querying.
Arguments:
variable: string, in the range: [a-zA-Z0-9_$(){}\[\].:]+
maxlength: int, in the range: 0,99999999999
Example:
body common control
{
      bundlesequence => { "example" };
}

bundle agent example
{
  vars:

      "myvar" string => getenv("EXAMPLE","2048");

  classes:

      "isdefined" not => strcmp("$(myvar)","");

  reports:

    isdefined::

      "The EXAMPLE environment variable is $(myvar)";

    !isdefined::

      "The environment variable EXAMPLE does not exist";

}
Output:
R: The EXAMPLE environment variable is getenv.cf
Notes:
History: This function was introduced in CFEngine version 3.0.4 (2010)
'''


'''
getuserinfo
Table of Contents
Prototype: getuserinfo(optional_uidorname)
Return type: data
Description: Return information about the current user or any other, looked up by user ID (UID) or user name.
This function searches for a user known to the system. If the optional_uidorname parameter is omitted, the current user (that is currently running the agent) is retrieved. If optional_uidorname is specified, the user entry is looked up by name or ID, using the standard getpwuid() and getpwnam() POSIX functions (but note that these functions may in turn talk to LDAP, for instance).
On platforms that don't support these POSIX functions, the function simply fails.
Arguments:
optional_uidorname: string, in the range: .*
Example:
body common control
{
      bundlesequence => { "example" };
}

bundle agent example
{
    vars:
      # note the results here will vary depending on your platform
      "me" data => getuserinfo(); # the current user's info
      "root" data => getuserinfo("root"); # the "root" user's info (usually UID 0)
      "uid0" data => getuserinfo(0); # lookup user info for UID 0 (usually "root")

      # sys.user_data has the information for the user that started the agent
      "out" string => format("I am '%s', root shell is '%s', and the agent was started by %S", "$(me[description])", "$(root[shell])", "sys.user_data");

  reports:
      "$(out)";
}
Typical Results:
R: I am 'Mr. Current User', root shell is '/bin/bash', and the agent was started by {"description":"Mr. Current User","gid":1000,"home_dir":"/home/theuser","shell":"/bin/sh","uid":1000,"username":"theuser"}

And variable contents:
  "me": {
    "description": "Mr. Current User",
    "gid": 1000,
    "home_dir": "/home/theuser",
    "shell": "/bin/sh",
    "uid": 1000,
    "username": "theuser"
  }

  "root": {
    "description": "root",
    "gid": 0,
    "home_dir": "/root",
    "shell": "/bin/bash",
    "uid": 0,
    "username": "root"
  }

  "uid0": {
    "description": "root",
    "gid": 0,
    "home_dir": "/root",
    "shell": "/bin/bash",
    "uid": 0,
    "username": "root"
  }
History: Introduced in CFEngine 3.10
See also: getusers(), users.
'''



'''
getuid
Table of Contents
Prototype: getuid(username)
Return type: int
Description: Return the integer user id of the named user on this host
If the named user is not registered the variable will not be defined.
Arguments:
username: string, in the range: .*
Example:
body common control
{
      bundlesequence => { "example" };
}

bundle agent example
{
  vars:

      "uid" int => getuid("root");

  reports:
      "root's uid is $(uid)";
}
Output:
R: root's uid is 0
Notes: On Windows, which does not support user ids, the variable will not be defined.
'''


'''
getgid
Table of Contents
Prototype: getgid(groupname)
Return type: int
Description: Return the integer group id of the group groupname on this host.
If the named group does not exist, the function will fail and the variable will not be defined.
Arguments:
groupname: string, in the range: .*
Example:
body common control
{
      bundlesequence => { "example" };
}

bundle agent example
{
  vars:
    linux|solaris|hpux::
      "gid" int => getgid("root");
    freebsd|darwin|openbsd::
      "gid" int => getgid("wheel");
    aix::
      "gid" int => getgid("system");

  reports:
      "root's gid is $(gid)";
}
Output:
R: root's gid is 0
Notes: On Windows, which does not support group ids, the variable will not be defined.
'''




'''
isplain
Table of Contents
Prototype: isplain(filename)
Return type: boolean
Description: Returns whether the named object filename is a plain/regular file.
Arguments:
filename: string, in the range: "?(/.*)
Example:
body common control
{
      bundlesequence => { "example" };
}

bundle agent example
{
  classes:

      "fileisplain" expression => isplain("/etc/passwd");
      "dirisnotplain" not => isplain("/");

  reports:

    fileisplain::
      "/etc/passwd is plain..";

    dirisnotplain::
      "/ is not plain..";

}
Output:
R: /etc/passwd is plain..
R: / is not plain..
'''




'''
laterthan
Table of Contents
Prototype: laterthan(year, month, day, hour, minute, second)
Return type: boolean
Description: Returns whether the current time is later than the given date and time.
The specified date/time is an absolute date in the local timezone. Note that, unlike some other functions, the month argument is 1-based (i.e. 1 corresponds to January).
Arguments:
year: int, in the range: 0,10000
month: int, in the range: 0,1000
day: int, in the range: 0,1000
hour: int, in the range: 0,1000
minute: int, in the range: 0,1000
second: int, in the range: 0,40000
Example:
bundle agent example
{
    classes:

      "after_deadline" expression => laterthan(2000,1,1,0,0,0);
    reports:
      after_deadline::
        "deadline has passed";
}
See also: on()
'''



'''
packagesmatching
Table of Contents
Prototype: packagesmatching(package_regex, version_regex, arch_regex, method_regex)
Return type: data
Description: Return a data container with the list of installed packages matching the parameters.
This function searches for the anchored regular expressions in the list of currently installed packages.
The return is a data container with a list of package descriptions, looking like this:
[
   {
      "arch":"default",
      "method":"dpkg",
      "name":"zsh-common",
      "version":"5.0.7-5ubuntu1"
   }
]
Arguments:
package_regex: string, in the range: .*
version_regex: string, in the range: .*
arch_regex: string, in the range: .*
method_regex: string, in the range: .*
Argument Descriptions:
package_regex - Regular expression matching packge name
version_regex - Regular expression matching package version
arch_regex - Regular expression matching package architecutre
method_regex - Regular expression matching package method (apt-get, rpm, etc ...)
The following code extracts just the package names, then looks for some desired packages, and finally reports if they are installed.
IMPORTANT: Please note that you need to provide package_inventory attribute in body common control in order to be able to use this function. Also depending on the value(s) of package_inventory only packages from selected package modules will be returned. For more information about package_inventory please read package_inventory section.
body common control

{
      bundlesequence => { "missing_packages" };
}


bundle agent missing_packages
{
  vars:
    # List of desired packages
    "desired" slist => { "mypackage1", "mypackage2" };

    # Get info on all installed packages
    "installed" data => packagesmatching(".*",".*",".*",".*");
    "installed_indices" slist => getindices(installed);

    # Build a simple array of the package names so that we can use
    # getvalues to pull a unified list of package names that are installed.
    "installed_name[$(installed_indices)]"
      string => "$(installed[$(installed_indices)][name])";

    # Get unified list of installed packages
    "installed_names" slist => getvalues("installed_name");

    # Determine packages that are missing my differencing the list of
    # desired packages, against the list of installed packages
    "missing_list" slist => difference(desired,installed_names);

  reports:
    # Report on packages that are missing, installed
    # and what we were looking for
    "Missing packages = $(missing_list)";
    "Installed packages = $(installed_names)";
    "Desired packages = $(desired)";
}
This policy can be found in /var/cfengine/share/doc/examples/packagesmatching.cf and downloaded directly from github.
Example:
      "all_packages" data => packagesmatching(".*", ".*", ".*", ".*");
Refresh rules: * inastalled packages cache used by packagesmatching() is refreshed at the end of each agent run in accordance with constraints defined in the relevant package module body. * installed packages cache is refreshed after installing or removing a package. * installed packages cache is refreshed if no local cache exists. This means a reliable way to force a refresh of CFEngine's internal package cache is to simply delete the local cache:
            $(sys.statedir)/packages_installed_<package_module>.lmdb*
History: Introduced in CFEngine 3.6
See also: packageupdatesmatching().
'''



'''
processexists
Table of Contents
Prototype: processexists(regex)
Return type: boolean
The return value is cached.
Description: Return whether a process matches the given regular expression regex.
This function searches for the given regular expression in the process table. Use .*sherlock.* to find all the processes that match sherlock. Use .*\bsherlock\b.* to exclude partial matches like sherlock123 (\b matches a word boundary).
Arguments:
regex: regular expression, in the range: .*
The process table is usually obtained with something like ps -eo user,pid,ppid,pgid,%cpu,%mem,vsize,ni,rss,stat,nlwp,stime,time,args, and the CMD or COMMAND field (args) is used to match against. However the exact data used may change per platform and per CFEngine release.
Example:
    classes:
      # the class "holmes" will be set if a process line contains the word "sherlock"
      "holmes" expression => processexists(".*sherlock.*");
History: Introduced in CFEngine 3.9
See also: processes findprocesses().
'''


'''
readjson
Table of Contents
Prototype: readjson(filename, maxbytes)
Return type: data
Description: Parses JSON data from the file filename and returns the result as a data variable. maxbytes is optional, if specified, only the first maxbytes bytes are read from filename.
Arguments:
filename: string, in the range: "?(/.*)
maxbytes: int, in the range: 0,99999999999
Example:
    vars:

      "loadthis"

         data =>  readjson("/tmp/data.json", 4000);
See also: readdata(), parsejson(), storejson(), parseyaml(), readyaml(), mergedata(), and data documentation.
'''


'''
registryvalue
Table of Contents
Prototype: registryvalue(key, valueid)
Return type: string
Description: Returns the value of valueid in the Windows registry key key.
This function applies only to Windows-based systems. The value is parsed as a string.
Arguments:
key: string, in the range: .*
valueid: string, in the range: .*
Example:
body common control
{
      bundlesequence => { "reg" };
}

bundle agent reg
{
  vars:
    windows::
      "value" string => registryvalue("HKEY_LOCAL_MACHINE\SOFTWARE\CFEngine AS\CFEngine","value3");
    !windows::
      "value" string => "Sorry, no registry data is available";

  reports:
      "Value extracted: $(value)";

}
Output:
R: Value extracted: Sorry, no registry data is available
Notes: Currently values of type REG_SZ (string), REG_EXPAND_SZ (expandable string) and REG_DWORD (double word) are supported.
'''


'''
readfile
Table of Contents
Prototype: readfile(filename, maxbytes)
Return type: string
Description: Returns the first maxbytes bytes from file filename. When maxbytes is 0, the maximum possible bytes will be read from the file (but see Notes below).
Arguments:
filename: string, in the range: "?(/.*)
maxbytes: int, in the range: 0,99999999999
Example:
Prepare:
echo alpha > /tmp/cfe_hostlist
echo beta >> /tmp/cfe_hostlist
echo gamma >> /tmp/cfe_hostlist
Run:
body common control
{
      bundlesequence => { "example" };
}

bundle agent example
{
  vars:

      "xxx"
      string => readfile( "/tmp/cfe_hostlist" , "5" );
  reports:
      "first 5 characters of /tmp/cfe_hostlist: $(xxx)";
}
Output:
R: first 5 characters of /tmp/cfe_hostlist: alpha
Notes:
To reliably read files located within /proc or /sys directories, maxsize has to be set to 0.
At the moment, only 4095 bytes can fit into a string variable. This limitation may be removed in the future. If this should happen, a warning will be printed.
If you request more bytes than CFEngine can read into a string variable (e.g. 999999999), a warning will also be printed.
If either because you specified a large value, or you specified 0, more bytes are read than will fit in a string, the string is truncated to the maximum.
On Windows, the file will be read in text mode, which means that CRLF line endings will be converted to LF line endings in the resulting variable. This can make the variable length shorter than the size of the file being read.
History: Warnings about the size limit and the special 0 value were introduced in 3.6.0
'''



'''
readcsv
Table of Contents
Description: Parses CSV data from the first 1 MB of file filename and returns the result as a data variable.
While it may seem similar to data_readstringarrayidx() and data_readstringarray(), the readcsv() function is more capable because it follows RFC 4180, especially regarding quoting. This is not possible if you just split strings on a regular expression delimiter.
The returned data is in the same format as data_readstringarrayidx(), that is, a data container that holds a JSON array of JSON arrays.
Example:
Prepare:
echo -n 1,2,3 > /tmp/csv
Run:
bundle agent main
{
  vars:

      # note that the CSV file has to have ^M (DOS) EOL terminators
      # thus the prep step uses `echo -n` and just one line, so it will work on Unix
      "csv" data => readcsv("/tmp/csv");
      "csv_str" string => format("%S", csv);

  reports:

      "From /tmp/csv, got data $(csv_str)";

}
Output:
R: From /tmp/csv, got data [["1","2","3"]]
Note: CSV files formatted according to RFC 4180 must end with the CRLF sequence. Thus a text file created on Unix with standard Unix tools like vi will not, by default, have those line endings.
See also: readdata(), data_readstringarrayidx(),data_readstringarray(), parsejson(), storejson(), mergedata(), and data documentation.
History: Was introduced in 3.7.0.
'''



'''
returnszero
Table of Contents
Prototype: returnszero(command, shell)
Return type: boolean
The return value is cached.
Description: Runs command and returns whether it has returned with exit status zero.
This is the complement of execresult(), but it returns a class result rather than the output of the command.
Arguments:
command: string, in the range: .+
shell: one of
noshell
useshell
powershell
Example:
body common control
{
      bundlesequence => { "example" };
}

bundle agent example
{
  classes:

      "my_result" expression => returnszero("/usr/local/bin/mycommand","noshell");

  reports:

    !my_result::

      "Command failed";

}
Output:
2014-08-18T14:13:28+0100 error: Proposed executable file '/usr/local/bin/mycommand' doesn't exist
2014-08-18T14:13:28+0100 error: returnszero '/usr/local/bin/mycommand' is assumed to be executable but isn't
R: Command failed
Notes: you should never use this function to execute commands that make changes to the system, or perform lengthy computations. Such an operation is beyond CFEngine's ability to guarantee convergence, and on multiple passes and during syntax verification these function calls are executed, resulting in system changes that are covert. Calls to execresult should be for discovery and information extraction only. Effectively calls to this function will be also repeatedly executed by cf-promises when it does syntax checking, which is highly undesirable if the command is expensive. Consider using commands promises instead, which have locking and are not evaluated by cf-promises.
See also: execresult().
'''



'''
readyaml
Table of Contents
Prototype: readyaml(filename, maxbytes)
Return type: data
Description: Parses YAML data from the file filename and returns the result as a data variable. maxbytes is optional, if specified, only the first maxbytes bytes are read from filename.
Arguments:
filename: string, in the range: "?(/.*)
maxbytes: int, in the range: 0,99999999999
Example:
    vars:

      "loadthis"

         data =>  readyaml("/tmp/data.yaml", 4000);
See also: readdata(), parsejson(), parseyaml(), storejson(), mergedata(), and data documentation.
'''


'''
readdata
Table of Contents
Prototype: readdata(filename, filetype)
Return type: data
Description: Parses CSV, JSON, or YAML data from file filename and returns the result as a data variable.
When filetype is auto, the file type is guessed from the extension (ignoring case): .csv means CSV; .json means JSON; .yaml means YAML. If the file doesn't match any of those names, JSON is used.
When filetype is CSV, this function behaves exactly like readcsv() and returns the same data structure.
When filetype is JSON, this function behaves exactly like readjson() and returns the same data structure, except there is no data size limit (maxbytes is inf).
When filetype is YAML, this function behaves exactly like readyaml() and returns the same data structure, except there is no data size limit (maxbytes is inf).
Arguments:
filename: string, in the range: "?(/.*)
filetype: one of
CSV
YAML
JSON
auto
Example:
Prepare:
echo -n 1,2,3 > /tmp/file.csv
echo -n '{ "x": 200 }' > /tmp/file.json
echo '- a' > /tmp/file.yaml
echo '- b' >> /tmp/file.yaml
Run:
bundle agent main
{
  vars:

      "csv" data => readdata("/tmp/file.csv", "auto"); # or file type "CSV"
      "json" data => readdata("/tmp/file.json", "auto"); # or file type "JSON"

      "csv_str" string => format("%S", csv);
      "json_str" string => format("%S", json);

    feature_yaml:: # we can only test YAML data if libyaml is compiled in
      "yaml" data => readdata("/tmp/file.yaml", "auto"); # or file type "YAML"
      "yaml_str" string => format("%S", yaml);
  reports:

      "From /tmp/file.csv, got data $(csv_str)";
      "From /tmp/file.json, got data $(json_str)";
    feature_yaml::
      "From /tmp/file.yaml, we would get data $(yaml_str)";
    !feature_yaml:: # show the output anyway
      'From /tmp/file.yaml, we would get data ["a","b"]';

}
Output:
R: From /tmp/file.csv, got data [["1","2","3"]]
R: From /tmp/file.json, got data {"x":200}
R: From /tmp/file.yaml, we would get data ["a","b"]
See also: readcsv(), readyaml(), readjson(), and data documentation.
History: Was introduced in 3.7.0.
'''



'''
readstringarrayidx
Table of Contents
Prototype: readstringarrayidx(array, filename, comment, split, maxentries, maxbytes)
Return type: int
Description: Populates the two-dimensional array array with up to maxentries fields from the first maxbytes bytes of file filename.
One dimension is separated by the regex split, the other by the lines in the file. The array arguments are both integer indexes, allowing for non-identifiers at first field (e.g. duplicates or names with spaces), unlike readstringarray.
The comment field is a multiline regular expression and will strip out unwanted patterns from the file being read, leaving unstripped characters to be split into fields. Using the empty string ("") indicates no comments.
Returns an integer number of keys in the array (i.e., the number of lines matched). If you only want the fields in the first matching line (e.g., to mimic the behavior of the getpwnam(3) on the file /etc/passwd), use getfields(), instead.
Arguments:
array: string, in the range: [a-zA-Z0-9_$(){}\[\].:]+
filename: string, in the range: "?(/.*)
comment: string, in the range: .*
split: string, in the range: .*
maxentries: int, in the range: 0,99999999999
maxbytes: int, in the range: 0,99999999999
Example:
    vars:

      "dim_array"

         int =>  readstringarrayidx("array_name","/tmp/array","\s*#[^\n]*",":",10,4000);
Input example:
     at spaced:x:25:25:Batch jobs daemon:/var/spool/atjobs:/bin/bash
     duplicate:x:103:105:User for Avahi:/var/run/avahi-daemon:/bin/false    # Disallow login
     beagleindex:x:104:106:User for Beagle indexing:/var/cache/beagle:/bin/bash
     duplicate:x:1:1:bin:/bin:/bin/bash
     # Daemon has the default shell
     daemon:x:2:2:Daemon:/sbin:
Results in a systematically indexed map of the file:
     array_name[0][0]       at spaced
     array_name[0][1]       x
     array_name[0][2]       25
     array_name[0][3]       25
     array_name[0][4]       Batch jobs daemon
     array_name[0][5]       /var/spool/atjobs
     array_name[0][6]       /bin/bash
     array_name[1][0]       duplicate
     array_name[1][1]       x
     array_name[1][2]       103
     array_name[1][3]       105
     array_name[1][4]       User for Avahi
     array_name[1][5]       /var/run/avahi-daemon
     array_name[1][6]       /bin/false
     ...

'''

import socket

from opsbro.misc.IPy import IP
from opsbro.evaluater import export_evaluater_function


@export_evaluater_function
def ip_is_in_range(ip, range):
    """**ip_is_in_range(ip, range)** -> return True if the ip is in the ip range, False otherwise.

 * ip:     (string) ip (v4 or v6) to check
 * range:  (string) ip range that the ip must be in


<code>
    Example:
        ip_is_in_range('172.16.0.30', '172.16.0.0/24')
    Returns:
        True
</code>
    """
    
    ip_range = IP(range)
    return ip in ip_range


@export_evaluater_function
def check_tcp(host, port, timeout=10):
    """**check_tcp(host, port, timeout=10)** -> return True if the TCP connection can be established, False otherwise.

 * host: (string) ip/fqdn of the host to connect to.
 * port: (integer) TCP port to connect to
 * timeout [optionnal] (integer) timeout to use for the connection test.

<code>
 Example:
     check_tcp('www.google.com', 80)

 Returns:
     True
</code>

    """
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
        sock.close()
        return True
    except socket.error:
        sock.close()
        return False


@export_evaluater_function
def ip_to_host(ip):
    """**ip_to_host(ip)** -> return the hostname if the ip is founded in the DNS server, '' otherwise.

 * ip: (string) ip of the host to get hostname from reverse DNS.

<code>
 Example:
     ip_to_host('172.217.23.35')

 Returns:
     'lhr35s02-in-f35.1e100.net'
</code>

    """
    try:
        hname, tmp = socket.gethostbyaddr(ip)
        # clean the last . if there is one
        if hname.endswith('.'):
            return hname[:-1]
    except socket.error:
        return ''


@export_evaluater_function
def host_to_ip(hname):
    """**host_to_ip(hname)** -> return the ip if founded, '' otherwise.

 * hname: (string) name of the host to get IP from DNS.

<code>
 Example:
     host_to_ip('www.google.com')

 Returns:
     '74.125.206.147'
</code>

    """
    try:
        ip = socket.gethostbyname(hname)
        return ip
    except socket.error:
        return ''





'''
network_connections
Table of Contents
Prototype: network_connections(regex)
Return type: data
Description: Return the list of current network connections.
This function looks in /proc/net to find the current network connections.
The returned data container has four keys:
tcp has all the TCP connections over IPv4
tcp6 has all the TCP connections over IPv6
udp has all the UDP connections over IPv4
udp6 has all the UDP connections over IPv6
Under each key, there's an array of connection objects that all look like this:
      {
        "local": {
          "address": "...source address...",
          "port": "...source port..."
        },
        "remote": {
          "address": "...remote address...",
          "port": "...remote port..."
        },
        "state": "...connection state..."
      }
All the data is collected from the files /proc/net/tcp, /proc/net/tcp6, /proc/net/udp, and /proc/net/udp6.
The address will be either IPv4 or IPv6 as appropriate. The port will be an integer stored as a string. The state will be a string like UNKNOWN.
On Linux, usually a state of UNKNOWN and a remote address 0.0.0.0 or 0:0:0:0:0:0:0:0 with port 0 mean this is a listening IPv4 and IPv6 server. In addition, usually a local address of 0.0.0.0 or 0:0:0:0:0:0:0:0 means the server is listening on every IPv4 or IPv6 interface, while 127.0.0.1 (the IPv4 localhost address) or 0:100:0:0:0:0:0:0 means the server is only listening to connections coming from the same machine.
A state of ESTABLISHED usually means you're looking at a live connection.
Example:
    vars:
      "connections" data => network_connections();
Output:
The SSH daemon:
   {
     "tcp": [
      {
        "local": {
          "address": "0.0.0.0",
          "port": "22"
        },
        "remote": {
          "address": "0.0.0.0",
          "port": "0"
        },
        "state": "UNKNOWN"
      }
    ]
   }
The printer daemon listening only to local IPv6 connections on port 631:
    "tcp6": [
      {
        "local": {
          "address": "0:100:0:0:0:0:0:0",
          "port": "631"
        },
        "remote": {
          "address": "0:0:0:0:0:0:0:0",
          "port": "0"
        },
        "state": "UNKNOWN"
      }
   ]
An established connection on port 2200:
     "tcp": [
      {
        "local": {
          "address": "192.168.1.33",
          "port": "2200"
        },
        "remote": {
          "address": "1.2.3.4",
          "port": "8533"
        },
        "state": "ESTABLISHED"
      }
    ]
History: Introduced in CFEngine 3.9
See also: sys.inet, sys.inet6.
'''


'''
selectservers
Table of Contents
Prototype: selectservers(hostlist, port, query, regex, maxbytes, array)
Return type: int
Description: Returns the number of tcp servers from hostlist which respond with a reply matching regex to a query send to port, and populates array with their names.
The regular expression is anchored. If query is empty, then no reply checking is performed (any server reply is deemed to be satisfactory), otherwise at most maxbytes bytes are read from the server and matched.
This function allows discovery of all the TCP ports that are active and functioning from an ordered list, and builds an array of their names. This allows maintaining a list of pretested failover alternatives.
Arguments:
hostlist: string, in the range: @[(][a-zA-Z0-9_$(){}\[\].:]+[)]
port: string, in the range: .*
query: string, in the range: .*
regex: regular expression, in the range: .*
maxbyes: int, in the range: 0,99999999999
array: string, in the range: [a-zA-Z0-9_$(){}\[\].:]+
Example:
    bundle agent example
    {
    vars:

     "hosts" slist => { "slogans.iu.hio.no", "eternity.iu.hio.no", "nexus.iu.hio.no" };
     "fhosts" slist => { "www.cfengine.com", "www.cfengine.org" };

     "up_servers" int =>  selectservers("@(hosts)","80","","","100","alive_servers");
     "has_favicon" int =>
            selectservers(
                "@(hosts)", "80",
            "GET /favicon.ico HTTP/1.0$(const.n)Host: www.cfengine.com$(const.n)$(const.n)",
            "(?s).*OK.*",
            "200", "favicon_servers");

    classes:

      "someone_alive" expression => isgreaterthan("$(up_servers)","0");

      "has_favicon" expression => isgreaterthan("$(has_favicon)","0");

    reports:
        "Number of active servers $(up_servers)";

      someone_alive::
        "First server $(alive_servers[0]) fails over to $(alive_servers[1])";

      has_favicon::
        "At least $(favicon_servers[0]) has a favicon.ico";

    }
If there is a multi-line response from the server, special care must be taken to ensure that newlines are matched, too. Note the use of (?s) in the example, which allows . to also match newlines in the multi-line HTTP response.
'''


'''
url_get
Table of Contents
Prototype: url_get(url, options_container)
Return type: data
Description: Retrieves the contents of a url using options from a data container. The data is returned in a data container.
NOTE that the options_container can be specified as inline JSON
This function can accept many types of data parameters.
Currently only file, http, and ftp URLs are supported. Internally, libcurl is used.
url_get() caches its results. To invalidate the cache, use a different set of options, e.g. by modifying an unused key with the system time.
If the libcurl integration is not available, the function will exit with an error and the variable will remain undefined. If the libcurl initialization fails, the function will also exit with an error. In every other normal case, the function will return a valid data container. In official CFEngine packages, libcurl integration is always provided.
The available options currently are:
url.max_content: if present, specifies the maximum number of content bytes to retrieve.
url.max_headers: if present, specifies the maximum number of response headers to retrieve.
url.verbose: if 1, libcurl will be more verbose while retrieving the content
url.timeout: if present, libcurl will time out the request after that many seconds
url.referer: if present, libcurl will set the Referer to this
url.user-agent: if present, libcurl will set the User-Agent to this
url.headers: an array of strings in the format Foo: bar specifying headers for the request
The returned data container will have the following keys:
returncode: the HTTP response code, e.g. 200.
rc: the libcurl integer result code, either 0 for success or something else for failure
error_message: when present, indicates the request was unsuccessful and explains why
success: a boolean. When success is false, the result code was not 0 and the request was unsuccessful.
content: the response content as a string
headers: the response headers as a string
Arguments:
url: string, in the range: .*
options_container: string, in the range: .*
Example:
This example retrieves two URLs using one set of options. The options are specified in JSON and parsed into a data container options. That data container is then passed to each invocation of url_get.
bundle agent main
{
  vars:
      "options_str" string => '
{
  "url.max_content": 512,
  "url.verbose": 0,
  "url.headers": [ "Foo: bar" ]
}';
      "options" data => parsejson($(options_str));
      "url" string => "http://cfengine.com";
      "res" data => url_get($(url), options);
      "out" string => format("%S", res);

      "url2" string => "http://nosuchcfenginehost.com";
      "res2" data => url_get($(url2), options);
      "out2" string => format("%S", res2);

  reports:
      "$(this.bundle): from $(url) with options $(options_str) we got $(out)";
      "$(this.bundle): from $(url2) with options $(options_str) we got $(out2)";
}
Output:
R: main: from http://cfengine.com with options
{
  "cfengine.max_content": 512,
  "curl.verbose": 0,
  "curl.headers": [ "Foo: bar" ]
} we got {"returncode":200,"rc":0,"success":true,"content":"\n<!DOCTYPE html>\n<!--[if lt IE 7]>\n<html class=\"no-js lt-ie9 lt-ie8 lt-ie7\" lang=\"en-US\" prefix=\"og: http://ogp.me/ns#\"> <![endif]-->\n<!--[if IE 7]>\n<html class=\"no-js lt-ie9 lt-ie8\" lang=\"en-US\" prefix=\"og: http://ogp.me/ns#\"> <![endif]-->\n<!--[if IE 8]>\n<html class=\"no-js lt-ie9\" lang=\"en-US\" prefix=\"og: http://ogp.me/ns#\"> <![endif]-->\n<!--[if gt IE 8]><!-->\n<html class=\"no-js\" lang=\"en-US\" prefix=\"og: http://ogp.me/ns#\"> <!--<![endif]-->\n<head>\n\n    \n    <meta charset=\"utf-8\">\n\n    <title>\n        CFEng","headers":"HTTP/1.1 200 OK\r\nDate: Fri, 27 Mar 2015 18:13:01 GMT\r\nServer: Apache\r\nX-Powered-By: PHP/5.3.3\r\nX-Pingback: http://cfengine.com/xmlrpc.php\r\nConnection: close\r\nTransfer-Encoding: chunked\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"}

R: main: from http://nosuchcfenginehost.com with options
{
  "cfengine.max_content": 512,
  "curl.verbose": 0,
  "curl.headers": [ "Foo: bar" ]
} we got {"returncode":0,"rc":6,"success":false,"content":"","headers":""}
History: Introduced in CFEngine 3.8. The collecting function behavior was added in 3.9.
See also: readtcp(), mergedata(), parsejson(), about collecting functions, and data documentation.

'''


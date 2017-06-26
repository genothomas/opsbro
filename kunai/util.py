import os
import sys
import shutil
import glob
import socket
import struct

try:
    import fcntl
except ImportError:
    fcntl = None

try:
    import requests as rq
except ImportError:
    rq = None

from kunai.misc.windows import windowser
from kunai.log import logger
from kunai.httpclient import HTTP_EXCEPTIONS


def make_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def copy_dir(source_item, destination_item):
    if os.path.isdir(source_item):
        make_dir(destination_item)
        sub_items = glob.glob(source_item + '/*')
        for sub_item in sub_items:
            copy_dir(sub_item, destination_item + '/' + sub_item.split('/')[-1])
    else:
        shutil.copy(source_item, destination_item)


def to_best_int_float(val):
    try:
        i = int(float(val))
        f = float(val)
    except ValueError:
        return None
        # If the f is a .0 value,
        # best match is int
    if i == f:
        return i
    return f


# get a dict but with key as lower
def lower_dict(d):
    r = {}
    for (k, v) in d.iteritems():
        r[k.lower()] = v
    return r


def _sort_local_addresses(addr1, addr2):
    addr1_is_192 = addr1.startswith('192.')
    addr2_is_192 = addr2.startswith('192.')
    addr1_is_10 = addr1.startswith('10.')
    addr2_is_10 = addr2.startswith('10.')
    addr1_is_172 = addr1.startswith('172.')
    addr2_is_172 = addr2.startswith('172.')
    addr1_is_127 = addr1.startswith('127.')
    addr2_is_127 = addr2.startswith('127.')
    
    # lower is better
    addr1_order = 4
    if addr1_is_192:
        addr1_order = 1
    elif addr1_is_172:
        addr1_order = 2
    elif addr1_is_10:
        addr1_order = 3
    if addr1_is_127:
        addr1_order = 5
    addr2_order = 4
    if addr2_is_192:
        addr2_order = 1
    elif addr2_is_172:
        addr2_order = 2
    elif addr2_is_10:
        addr2_order = 3
    if addr2_is_127:
        addr2_order = 5
    
    print "Address order: %s:%d %s:%d" % (addr1, addr1_order, addr2, addr2_order)
    if addr1_order > addr2_order:
        return 1
    elif addr1_order < addr2_order:
        return -1
    return 0


def _get_linux_local_addresses():
    stdin, stdout = os.popen2('hostname -I')
    buf = stdout.read().strip()
    stdin.close()
    stdout.close()
    res = [s.strip() for s in buf.split(' ') if s.strip()]
    res.sort(_sort_local_addresses)
    return res


def _is_valid_local_addr(addr):
    if not addr:
        return False
    if addr.startswith('127.0.0.'):
        return False
    if addr.startswith('169.254.'):
        return False
    # we can check the address is localy available
    if sys.platform == 'linux2':
        _laddrs = _get_linux_local_addresses()
        if addr not in _laddrs:
            return False
    return True


# On EC2 need to get public IP from http://169.254.169.254/latest/meta-data/public-ipv4
def _get_ec2_public_ip():
    uri = 'http://169.254.169.254/latest/meta-data/public-ipv4'
    if rq is None:
        logger.error('Cannot load the python-requests lib. It is need to get public IP on your EC2 server. Exiting')
        sys.exit(2)
    try:
        r = rq.get(uri)
        addr = r.text
    except HTTP_EXCEPTIONS, exp:
        logger.error('Cannot get pubic IP for your EC2 instance from %s. Error: %s.Exiting' % (uri, exp))
        sys.exit(2)
    return addr
    

# Only works in linux
def get_public_address():
    # Special case: EC2, local public IP is useless, need public IP
    if os.path.exists('/sys/hypervisor/version/extra'):
        with open('/sys/hypervisor/version/extra') as f:
            buf = f.read().strip()
            if buf == '.amazon':
                # EC2 case: need to get from special IP
                addr = _get_ec2_public_ip()
                return addr
    # If I am in the DNS or in my /etc/hosts, I win
    try:
        addr = socket.gethostbyname(socket.gethostname())
        if _is_valid_local_addr(addr):
            return addr
    except Exception, exp:
        pass
    
    if sys.platform == 'linux2':
        '''
        for prefi in ['bond', 'eth']:
            for i in xrange(0, 10):
                ifname = '%s%d' % (prefi, i)
                try:
                    addr = get_ip_address(ifname)
                    if _is_valid_local_addr(addr):
                        return addr
                except IOError:  # no such interface
                    pass
        '''
        addrs = _get_linux_local_addresses()
        if len(addrs) > 0:
            return addrs[0]
    
    # On windows also loop over the interfaces
    if os.name == 'nt':
        c = windowser.get_wmi()
        for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=1):
            for addr in interface.IPAddress:
                if _is_valid_local_addr(addr):
                    return addr
    
    return None


# Get the ip address in a linux system
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


# recursivly change a dict with pure bytes
def byteify(input):
    if isinstance(input, dict):
        return dict([(byteify(key), byteify(value)) for key, value in input.iteritems()])
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, str):
        return input.decode('utf8', 'ignore')
    else:
        return input

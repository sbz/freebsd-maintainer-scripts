import os
import shlex
import subprocess


template = r"""%s
 +--------------------------------------+           ,        ,
 |        Welcome to %s           |          /(        )`
 |                                      |          \ \___   / |
 |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|          /- _  `-/  '
 |                                      |         (/\/ \ \   /\
 |  kern.hostname: %.8s               |         / /   | `    \
 |    kern.ostype: %s              |         O O   ) /    |
 | kern.osrelease: %s          |         `-^--'`<     '
 |       hw.model: %.20s |        (_.)  _  )   /
 |     hw.machine: %s                |         `.___/`    /
 |        hw.ncpu: %s                    |           `-----' /
 | dev.cpu.0.freq: %s                <----.     __ / __   \
 |     hw.physmem: %s         <----|====O)))==) \) /====
 |           inet: %s        <----'    `--' `.__,' \
 |                                      |           |        |
 |          admin: %s         |            \       /
 |                                      |       ______( (_  / \______
 |                                      |     ,'  ,-----'   |        \
 +--------------------------------------+     `--{__________)        \/
"""


def run_command(cmd: str) -> str:
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    try:
        out, err = p.communicate(timeout=10)

    except subprocess.TimeoutExpired:
        p.kill()
        out, _ = p.communicate()

    return out.strip()


def sysctl_get(oid_string: str) -> str:
    result = ""
    try:
        import freebsd
        result = freebsd.sysctl('%s' % oid_string)
    except ImportError:
        cmd = 'sysctl -n {0}'.format(oid_string)
        result = run_command(cmd)
    finally:
        return str(result, 'utf-8')


uname = " ".join(" ".join(os.uname()[:4]).split(' ')[:13])
fqdn = "6dev.net"
admin = "%s@%s" % (os.environ['USER'], fqdn)
inet = os.popen("ifconfig|grep 'inet .* broad*'").read().split()[1]

oids = ["kern.hostname", "kern.osrelease", "kern.ostype", "hw.model",
        "hw.machine", "hw.ncpu", "dev.cpu.0.freq", "hw.physmem"]

for oid in oids:
    locals()[oid.replace('.', '_')] = sysctl_get(oid)

hw_physmem = "%.1fGB" % float(int(hw_physmem)/1000000000.0)

print(template % (uname, fqdn,
                  kern_hostname.split('.')[0], kern_ostype, kern_osrelease,
                  hw_model, hw_machine, hw_ncpu,
                  dev_cpu_0_freq, hw_physmem, inet, admin))

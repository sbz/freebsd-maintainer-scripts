import os

template="""%s
 +--------------------------------------+           ,        ,
 |        Welcome to %s           |          /(        )`
 |                                      |          \ \___   / |
 |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|          /- _  `-/  '
 |                                      |         (/\/ \ \   /\\
 |  kern.hostname: %.8s               |         / /   | `    \\
 |    kern.ostype: %s              |         O O   ) /    |
 | kern.osrelease: %s     |         `-^--'`<     '
 |       hw.model: %.20s |        (_.)  _  )   /
 |     hw.machine: %s                |         `.___/`    /
 |        hw.ncpu: %s                    |           `-----' /
 | dev.cpu.0.freq: %s                <----.     __ / __   \\
 |     hw.physmem: %s         <----|====O)))==) \) /====
 |           inet: %s        <----'    `--' `.__,' \\
 |                                      |           |        |
 |          admin: %s         |            \       /
 |                                      |       ______( (_  / \______
 |                                      |     ,'  ,-----'   |        \\
 +--------------------------------------+     `--{__________)        \/
"""

def sysctl_get(oid_string):
    result=""
    try:
        import freebsd
        result=freebsd.sysctl('%s' % oid_string)
    except:
        result=os.popen('sysctl -n %s' % oid_string).read().strip()
    finally:
        return result

uname = " ".join(" ".join(os.uname()[:4]).split(' ')[:13])
fqdn = "6dev.net"
admin = "%s@%s" % (os.environ['USER'], fqdn)
inet = os.popen("ifconfig|grep 'inet .* broad*'").read().split()[1]

oids = ["kern.hostname", "kern.osrelease", "kern.ostype", "hw.model", "hw.machine",
"hw.ncpu", "dev.cpu.0.freq", "hw.physmem"]

for oid in oids:
    locals()[oid.replace('.','_')] = sysctl_get(oid)

print(template % (uname, fqdn, kern_hostname.split('.')[0], kern_ostype, kern_osrelease, hw_model,
        hw_machine, hw_ncpu, dev_cpu_0_freq, "%.1fGB" %
        float(int(hw_physmem)/1000000000.0), inet, admin))

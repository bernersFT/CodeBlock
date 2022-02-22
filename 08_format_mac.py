import re


def format_mac(mac):
    mac_re = re.compile(r'''
		(^([0-9A-F]{1,2}[-]){5}([0-9A-F]{1,2})$
		|^([0-9A-F]{1,2}[:]){5}([0-9A-F]{1,2})$
		|^([0-9A-F]{1,2}[.]){5}([0-9A-F]{1,2})$
		|^([0-9A-F]{1,4}[-]){2}([0-9A-F]{1,4})$
		|^([0-9A-F]{1,4}[:]){2}([0-9A-F]{1,4})$
		|^([0-9A-F]{1,4}[.]){2}([0-9A-F]{1,4})$
		)''', re.VERBOSE | re.IGNORECASE)
    if re.match(mac_re, mac):
        if mac.count(":") == 5 or mac.count("-") == 5 or mac.count(".") == 5:
            sep = mac[2]
            mac_fm = mac.replace(sep, ':')
            return mac_fm
        elif mac.count(".") == 2 or mac.count("-") == 2 or mac.count(":") == 2:
            sep = mac[4]
            mac_fm = mac.replace(sep, '')
            return (
                    mac_fm[0:2]
                    + ":"
                    + mac_fm[2:4]
                    + ":"
                    + mac_fm[4:6]
                    + ":"
                    + mac_fm[6:8]
                    + ":"
                    + mac_fm[8:10]
                    + ":"
                    + mac_fm[10:]
            )

# support format for MAC as below, and return like 12:12:12:12:12:12
print(format_mac('1212:1212:1212'))
print(format_mac('1212-1212-1212'))
print(format_mac('1212.1212.1212'))
print(format_mac('12-12-12-12-12-12'))
print(format_mac('12:12:12:12:12:12'))
print(format_mac('12.12.12.12.12.12'))

import os.path
from python_hosts import Hosts, HostsEntry
from shutil import copyfile

dirs = ['data/mysql57db', 'data/redisdb', 'log/cron_log', 'log/httpd_log', 'log/nginx_log', 'log/node_log',
'log/php_log', 'log/pm2_log', 'web_src/cmc.com']
                                     
for newpath in dirs:
    if not os.path.exists(newpath):
        os.makedirs(newpath)

#hosts = Hosts(path='c:\\windows\\system32\\drivers\\etc\\hosts')
if os.name == 'nt':
    hosts = Hosts(path='c:\\windows\\system32\\drivers\\etc\\hosts')
    new_entry = HostsEntry(entry_type='ipv4', address='127.0.0.1', names=['cmc.com'])
    addResult = hosts.add([new_entry])

    if addResult['duplicate_count'] > 0:
        print('Host record already exists')
    else:
	print('Host record added!');
		hosts.write()

copyfile('./.env.example', './.env')
print('Done!');
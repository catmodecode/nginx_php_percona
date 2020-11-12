import os
import os.path
import re
from python_hosts import Hosts, HostsEntry
from dotenv import load_dotenv

load_dotenv()
domainTamplate = os.getenv("DOMAIN_TEMPLATE")

web_src = "web_src/"

def create_config(dirname, domain):
    try:
        tpl = open("etc/"+dirname+"/tpl/domain.tpl")
        tpldata = tpl.read()

    finally:
        tpl.close()

    tpldata = tpldata.replace("#domain#", domain)

    tpl = open("etc/"+dirname+"/sites-enabled/"+domain+".conf", "w")
    tpl.write(tpldata)
    tpl.close()

def delete_config(dirname, domain):
    delpath = "etc/"+dirname+"/sites-enabled/"+domain+".conf"
    if os.path.exists(delpath):
        os.remove(delpath)

def create_domain():
    domain = input("Enter 3rd level domain name(real domain will be " + domainTamplate.replace("%domain%", "yourdomain") + "): ")
    domain_regex = r'^[a-z][a-z0-9]{2,15}$'

    domain_regex = '{0}$'.format(domain_regex)
    valid_domain_name_regex = re.compile(domain_regex)

    if re.match(valid_domain_name_regex, domain ):
        domain = domainTamplate.replace("%domain%", domain)
        newpath = web_src + domain

        if not os.path.exists(newpath):
            os.makedirs(newpath)
            #generate httpd configs
            create_config("httpd", domain)

            #generate nginx configs
            create_config("nginx", domain)

            if os.name == 'nt':
                hosts = Hosts(path='c:\\windows\\system32\\drivers\\etc\\hosts')

                new_entry = HostsEntry(entry_type='ipv4', address='127.0.0.1', names=[domain])
                addResult = hosts.add([new_entry])
                if addResult['duplicate_count'] > 0:
                    print('Host record already exists')
                else:
                    print('Host record added!');
                    hosts.write()
                
            restartWeb()

            do_database = input('Create database(Y/N) default:Y: ')
            if(do_database == 'Y' or do_database == ''):
                create_database();

            print('Done');
            return;

        else:
            print('This domain already exists!');
            return;

    else:
        print('Invalid domain');
        return;

def delete_domain():
    domain = input("Enter 3rd level domain name(real domain will be " + domainTamplate.replace("%domain%", "yourdomain") + "): ")
    domain_regex = r'^[a-z][a-z0-9]{2,15}$'

    domain_regex = '{0}$'.format(domain_regex)
    valid_domain_name_regex = re.compile(domain_regex)

    if re.match(valid_domain_name_regex, domain ):
        domain = domainTamplate.replace("%domain%", domain)
        newpath = web_src + domain

        if not os.path.exists(newpath):
            print('This domain not found!');
            return;

        else:
            delete_config("httpd", domain)
            delete_config("nginx", domain)

            if os.name == 'nt':
                hosts = Hosts(path='c:\\windows\\system32\\drivers\\etc\\hosts')

                removeResult = hosts.remove_all_matching(name=domain)
                hosts.write()
            
            restartWeb()
            
            print('Configs deleted.');
            return;

    else:
        print('Invalid domain');
        return;

def create_database():
    database = input("Enter database name: ")
    database_regex = r'^[a-z][a-z0-9]{2,15}$'
    database_regex = '{0}$'.format(database_regex)
    valid_database_name_regex = re.compile(database_regex)
    if re.match(valid_database_name_regex, database ):
        os.system('docker exec db mysql -uroot -proot -e "CREATE DATABASE ' + database + '; GRANT ALL PRIVILEGES ON ' + database + '.* TO \'bitrix\'@\'localhost\' IDENTIFIED BY \'bitrix\'; FLUSH PRIVILEGES;"')
        print('Database "' + database + '" created, user: "bitrix" password: "bitrix"')
    else:
        print('invalid database name')
    return

def restartWeb():
    os.system('docker exec -it nginx nginx -s reload')
    os.system('docker exec -it apache apachectl restart')

answer = input("1. Create domain\r\n2. Delete domain\r\n3. Create database\r\nSelect item: ")
if answer == '1':
    create_domain()
elif answer == '2':
    delete_domain()
elif answer == '3':
    create_database()
else:
    print('Bye!')

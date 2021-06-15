import platform, os, sys

#import pathlib
#from os.path import expanduser

import ac
import acsys 
import configparser
from collections import defaultdict
import queue

# Teste p/ pasta Documentos
#from win32com.shell import shell, shellcon 
#  doc_folder = shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0)

# Esse Trecho abaixo vou verificar caso seja necessário
"""
if platform.architecture()[0] == "64bit":
    dllfolder = "stdlib64"
else:
    dllfolder = "stdlib"
cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(cwd, dllfolder))
os.environ['PATH'] = os.environ['PATH'] + ";."
#import ctypes from ctypes import wintypes """

LABELS = {
	"cabecarioConfig"      :["Lista de Setups, selecione p/ comparar ",
	"List of Setups, selec for comparison"],

	"descSetupbase"        :["Arquivo-Setup-base","File-Setup-base"],
	
	"descSetupCompare1"    :["Arquivo-Setup-compare1","File-Setup-compare1"],	

	"instrucao1"  :["Para efetuar o comparação e necessario 2 ou mais SETUPS.", 
	                "For comparasion it's necessary 2 or more SETUPS "],

	"instrucao2"  :["Você pode comparar seu SETUP com o SETUP padrão do carro, mas,", 
	                "You can compare your SETUP with default SETUP but, "],

	"instrucao3"  :["para isso é necessário salva-lo.", 
	                "for this it's necessary to save it"],

	"instrucao4"  :["Para SALVAR o SETUP padrão é necessario voltar para menu de SETUPS,", 
	                "For save default SETUP it's necessary come back to menu SETUPS"],

	"instrucao5"  :["Apos resetar (botão abaixo), escolhe um nome p/ o SETUP padrão e salve", 
	                "After reset (button under), choose a name for default SETUP and save"], 	 	
		
	}

COLORS = {
	"white"      : [1, 1, 1, 1],
	"yellow"     : [1, 1, 0, 1],
	"green"      : [0, 1, 0, 1],
	"red"        : [1, 0, 0, 1],  
	"blue"       : [0, 0, 1, 1],  
	"clearblue"  : [0, 1, 1, 1],
	"pink"       : [1, 0, 1, 1],
  "black"      : [0, 0, 0, 1]
}

DOISPONTOS= ': ' 
PASTA_ENGRENAGEM=  "content/gui/pitstop/operating_repair.png"
PASTA_RESETSETUP=  "content/gui/setupIO/reset_button_ON.png"
PASTA_SAVE= "content/gui/setupIO/btn_save_ON.png"


LINHAINICIALCAMPOSSETUP=63
COLUNAINICIALCAMPOSSETUP=50

QTDCAMPOSTELASETUP=7
DIFCAMPOSLINHASETUP=30
DIFCAMPOSCOLUNASETUP=100
DIFCAMPOSCOLUNAPRIMEIROVALOR=200
QTDCAMPOSDIFERENTESSETUP=2

idiomaApp = 1

def acMain(ac_version):
	appWindow = ac.newApp("CompareSetups")
	ac.setSize(appWindow, 500, 500)

	instructionWindow = ac.newApp("instructionWindow")
	ac.setSize(instructionWindow, 550, 350)

	#settingsWindow = ac.newApp("settingsWindow")
	#ac.setSize(settingsWindow, 500, 500)

	#ac.setBackgroundColor(appWindow, *rgb(COLORS["black"]))

	#versaoteste1(appWindow)		
		
	pathSetup =  'C:/Users/user/Documents/Assetto Corsa/setups'
	pathSetupCar = '/mclaren_mp412c_gt3/spa'
	fileSetupCar = 'mp4-gt3_setup_for_spa.ini'
	file1 = pathSetup+pathSetupCar+ '/'+fileSetupCar
	file2 = 'C:/Users/user/Documents/Assetto Corsa/setups/mclaren_mp412c_gt3/spa/'+'default.ini'

	listaArqSetups = arquivosSetup(2)

	criarCamposInstrucao(instructionWindow)

	if listaArqSetups.__len__() > 1:
		invisivelTelaCompareSetups = False
		invisivelTelaInstrucao = True
		invisivelTelaConfig = True
	else:
		invisivelTelaInstrucao = True

	config1 = lerArquivo(file1)
	config2 = lerArquivo(file2)

	#listSetupDif = separaDiferencaSetups(config1, config2)
		
 	#Retirar
	listSetupDif = listaDiferencaQuebraGalho()
	
	if listSetupDif.__len__() > 0:
		listaCamposSetupDif = criaCamposSetup(appWindow, listSetupDif)		

		# alimenta a primeira lista novamente
		listaCamposSetupDif = posicionaCamposSetup(configuraCoresCamposSetup(listaCamposSetupDif), defineLinhasColunasSetup())

		# Se retirar a copia desta rotina e tirar o retorna termina com lista vazia
		#posicionaCamposSetup(configuraCoresCamposSetup(listaCamposSetupDif), defineLinhasColunasSetup())
	
	return "CompareSetups"

def criarCamposInstrucao(instructionWindow):
	
	# Cabeçario Tela de Instrução
	l_cabecarioInstrucao1 = ac.addLabel(instructionWindow, LABELS ["instrucao1"][idiomaApp])
	ac.setPosition(l_cabecarioInstrucao1, 40,43)

	l_cabecarioInstrucao2 = ac.addLabel(instructionWindow, LABELS ["instrucao2"][idiomaApp])
	ac.setPosition(l_cabecarioInstrucao2, 40,63)

	l_cabecarioInstrucao3 = ac.addLabel(instructionWindow, LABELS ["instrucao3"][idiomaApp])
	ac.setPosition(l_cabecarioInstrucao3, 40,83)

	l_cabecarioInstrucao4 = ac.addLabel(instructionWindow, LABELS ["instrucao4"][idiomaApp])
	ac.setPosition(l_cabecarioInstrucao4, 40,123)

	# Icone engrenagem 
	b_engrenagem = ac.addButton(instructionWindow, "")
	ac.setPosition(b_engrenagem, 80, 143)
	ac.setSize(b_engrenagem, 46 , 46)
	ac.drawBorder(b_engrenagem, 0)
	ac.setBackgroundTexture(b_engrenagem, PASTA_ENGRENAGEM)
	ac.setBackgroundOpacity(b_engrenagem, 0)	

	l_cabecarioInstrucao5 = ac.addLabel(instructionWindow, LABELS ["instrucao5"][idiomaApp])
	ac.setPosition(l_cabecarioInstrucao5, 40,223)

	# Icone Reset Setup
	b_reset = ac.addButton(instructionWindow, "")
	ac.setPosition(b_reset, 70, 243)
	ac.setSize(b_reset, 66 , 66)
	ac.drawBorder(b_reset, 0)
	ac.setBackgroundTexture(b_reset, PASTA_RESETSETUP)
	ac.setBackgroundOpacity(b_reset, 0)		

	# Icone Save Setup
	b_save = ac.addButton(instructionWindow, "")
	ac.setPosition(b_save, 460, 243)
	ac.setSize(b_save, 66 , 66)
	ac.drawBorder(b_save, 0)
	ac.setBackgroundTexture(b_save, PASTA_SAVE)
	ac.setBackgroundOpacity(b_save, 0)	
		

def criarCamposConfig(settingsWindow):
	
	# Cabeçario Tela de Configuraçao Setups
	l_cabecarioConfig = ac.addLabel(settingsWindow, LABELS ["cabecarioConfig"][idiomaApp])
	ac.setPosition(l_cabecarioConfig, 40,43)

	# Descriçãos da legenda da lista de setups a comparar
	l_descSetupbase = ac.addLabel(settingsWindow, LABELS ["descSetupbase"][idiomaApp])	
	ac.setFontColor(l_descSetupbase, *rgb(COLORS["green"]))
	ac.setPosition(l_descSetupbase, 50,63)

	# Descriçãos da legenda da lista de setups a comparar
	l_descSetupCompare1 = ac.addLabel(settingsWindow, LABELS ["descSetupCompare1"][idiomaApp])	
	ac.setFontColor(l_descSetupCompare1, *rgb(COLORS["red"]))
	ac.setPosition(l_descSetupCompare1, 75,63)

	
def pastaArquivoSetup():

	trackName = ac.getTrackName(0)
	#trackConfiguration = ac.getTrackConfiguration(0)
	carName = ac.getCarName(0)

	# Funciona em python > 3.3
	#home = pathlib.Path.home()
	
	# Somente retorna user/user
	#home = expanduser("~")
	#ConsoleLog('pasta home1: '+home)	
	
	home = os.path.expanduser('~/Documents')	

	# funciona em python > 3.3
	#path = pathlib.join(home, 'Assetto Corsa', 'setups', carName, trackName)

	path = os.path.join(home, 'Assetto Corsa', 'setups', carName, trackName)

	return path


def arquivosSetup(qtdMaxArqRetornados):

	pasta = pastaArquivoSetup()
	listaArqs = os.listdir(pasta)

	arqsIni = []	
	contaIni = 0
	for ini in listaArqs:
		if (ini.endswith('.ini')) and (contaIni < qtdMaxArqRetornados):
			arqsIni.append(ini)	
			contaIni += 1
		if contaIni == qtdMaxArqRetornados: break

	return arqsIni


def lerArquivo(file):
	
	config = configparser.ConfigParser()

	try:
		config.read_file(open(file,'r'))
	except configparser.ParsingError as e:
		ConsoleLog('Ignoring parsing errors1:\n' + str(e))
		
	return config


def separaDiferencaSetups(config1, config2):

	listSetupDif =  defaultdict(list)
	"""for each_section in config1.sections():
		if (config2.has_section(each_section)):			 
			for (each_key, each_val) in config1.items(each_section):
				ConsoleLog('\nTESTETETSTETETSTETETDSGH&: '+each_section+each_key+each_val)  				
				#ConsoleLog('\nTESTE: '+config2.get(str(each_section),str([each_section][each_key]),1))	
				sec = config2.__getitem__(each_section)				

				
				key = sec.get(each_key[0])				
				key.__getnewargs__()

				ConsoleLog('\nTESTE: ' + sec.name + ', ') 
				if(not each_val.__eq__ (config2[each_section][each_key])):
					listSetupDif[each_section].append(config1[each_section][each_key])
					listSetupDif[each_section].append(config2[each_section][each_key])	"""

	return listSetupDif


def criaCamposSetup(appWindow, listSetupDif):
	#listaCamposSetupDif =  []
	listaCamposSetupDif =  queue.Queue()

	l=0
	while l < QTDCAMPOSTELASETUP:		
		key,value = listSetupDif.popitem()
		
		#listaCamposSetupDif.append(ac.addLabel(appWindow, key))
		listaCamposSetupDif.put(ac.addLabel(appWindow, key))
		
		c=0
		while c < QTDCAMPOSDIFERENTESSETUP:			
			#listaCamposSetupDif.append(ac.addLabel(appWindow, value[0][c]))
			listaCamposSetupDif.put(ac.addLabel(appWindow, value[0][c]))
			c += 1
		l = l+1
	
	return listaCamposSetupDif


def defineLinhasColunasSetup():

	l=0
	posicoesCamposSetup = []
	
	linha = LINHAINICIALCAMPOSSETUP	
	while l < QTDCAMPOSTELASETUP:

		
		# Descricao do campo
		coluna = COLUNAINICIALCAMPOSSETUP
		colunaLinha = []
		colunaLinha.append(coluna)
		colunaLinha.append(linha)
		posicoesCamposSetup.append(colunaLinha)

		# Primeiro valor
		coluna += DIFCAMPOSCOLUNAPRIMEIROVALOR
		colunaLinha = []
		colunaLinha.append(coluna)
		colunaLinha.append(linha)
		posicoesCamposSetup.append(colunaLinha)


		# Segundo valor
		coluna += DIFCAMPOSCOLUNASETUP
		colunaLinha = []
		colunaLinha.append(coluna)
		colunaLinha.append(linha)
		posicoesCamposSetup.append(colunaLinha)

		linha +=DIFCAMPOSLINHASETUP
		l += 1

	return posicoesCamposSetup


def configuraCoresCamposSetup(filaQ):
	filaQCopia = queue.Queue()
	
	i=0
	while not filaQ.empty():
		item = filaQ.get()

		if i == 1:
			ac.setFontColor(item, *rgb(COLORS["green"]))
			i += 1
		elif i == 2:
			ac.setFontColor(item, *rgb(COLORS["red"]))
			i = 0
		else:
			i += 1
		
		filaQCopia.put(item)
	return filaQCopia


def posicionaCamposSetup(listaQ, posicoesCamposSetup):
	
	ordemCampos=0
	listaQCopia = queue.Queue()

	while not listaQ.empty():		
		item = listaQ.get()
		ac.setPosition(item, *separaPosicaoCampos(posicoesCamposSetup[ordemCampos]))	
		listaQCopia.put(item)		
		ordemCampos += 1
	
	return listaQCopia


def separaPosicaoCampos(posicoesCamposSetup):

	posicaoCampoSetup=[]
	posicaoCampoSetup = posicoesCamposSetup
	coluna = posicaoCampoSetup[0]
	linha = posicaoCampoSetup[1]	

	return coluna, linha


def rgb(COLORS):
	cor =[]		
	cor = COLORS
	r = cor[0] 
	g = cor[1] 		
	b = cor[2]
	a = cor[3]
	return r,g,b,a

def ConsoleLog(message):
  ac.console(message)
  ac.log(message)  


def listaDiferencaQuebraGalho():

	lista =  defaultdict(list)

	listaFixa = {'INTERNAL_GEAR_2': ['3', '1'], 'INTERNAL_GEAR_3': ['5', '3'], 'INTERNAL_GEAR_4': ['5', '3'], 'INTERNAL_GEAR_5': ['5', '4'], 
	'INTERNAL_GEAR_6': ['3', '2'], 'INTERNAL_GEAR_7': ['6', '7'], 'FINAL_RATIO': ['5', '7'], 'TYRES': ['0', '1'], 'PRESSURE_LF': ['19', '16'], 
	'PRESSURE_RF': ['19', '16'], 'PRESSURE_LR': ['19', '16'], 'PRESSURE_RR': ['19', '16'], 'TRACTION_CONTROL': ['4', '3'], 'WING_2': ['2', '5'], 
	'CAMBER_LF': ['-45', '-39'], 'TOE_OUT_LF': ['11', '7'], 'CAMBER_RF': ['-45', '-39'], 'TOE_OUT_RF': ['11', '7'], 'CAMBER_LR': ['-29', '-28'], 
	'TOE_OUT_LR': ['5', '9'], 'CAMBER_RR': ['-29', '-28'], 'TOE_OUT_RR': ['5', '9'], 'DAMP_FAST_BUMP_LF': ['12', '10'], 'DAMP_BUMP_LF': ['12', '9'], 
	'DAMP_FAST_REBOUND_LF': ['34', '38'], 'DAMP_REBOUND_LF': ['4', '8'], 'DAMP_FAST_BUMP_RF': ['11', '10'], 'DAMP_BUMP_RF': ['12', '9'], 
	'DAMP_FAST_REBOUND_RF': ['34', '38'], 'DAMP_REBOUND_RF': ['4', '8'], 'DAMP_FAST_BUMP_LR': ['25', '22'], 'DAMP_BUMP_LR': ['11', '9'], 
	'DAMP_FAST_REBOUND_LR': ['18', '23'], 'DAMP_REBOUND_LR': ['9', '13'], 'DAMP_FAST_BUMP_RR': ['25', '22'], 'DAMP_BUMP_RR': ['11', '9'], 
	'DAMP_FAST_REBOUND_RR': ['18', '23'], 'DAMP_REBOUND_RR': ['9', '13'], 'FRONT_BIAS': ['68', '69'], 'ARB_FRONT': ['6', '5'], 
	'ARB_REAR': ['1', '2'], 'SPRING_RATE_LF': ['130', '120'], 'ROD_LENGTH_LF': ['25', '24'], 'SPRING_RATE_RF': ['130', '120'], 'ROD_LENGTH_RF': ['25', '24'], 
	'SPRING_RATE_LR': ['120', '140'], 'ROD_LENGTH_LR': ['30', '24'], 'SPRING_RATE_RR': ['120', '140'], 'ROD_LENGTH_RR': ['30', '24'], 
	'PACKER_RANGE_LF': ['62', '54'], 'PACKER_RANGE_RF': ['62', '54'], 'PACKER_RANGE_LR': ['62', '54'], 'PACKER_RANGE_RR': ['62', '54'], 
	'DIFF_POWER': ['30', '65']}
	
	for k,v in listaFixa.items():
		lista[k].append([v[0],v[1]])

	return lista

def versaoteste1 (appWindow):
	l_descCampo1 = ac.addLabel(appWindow, "Camber Lf{}".format(DOISPONTOS))
	ac.setPosition(l_descCampo1, 50,63)

	l_value1Campo1 = ac.addLabel(appWindow, "0.1")	
	ac.setFontColor(l_value1Campo1, *rgb(COLORS["green"]))
	ac.setPosition(l_value1Campo1, 150,63)

	l_value2Campo1 = ac.addLabel(appWindow, "0.2")	
	ac.setFontColor(l_value2Campo1, *rgb(COLORS["yellow"]))
	ac.setPosition(l_value2Campo1, 250,63)

	l_value3Campo1 = ac.addLabel(appWindow, "0.3")	
	ac.setFontColor(l_value3Campo1, *rgb(COLORS["red"]))
	ac.setPosition(l_value3Campo1, 350,63)
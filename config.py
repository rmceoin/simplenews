
import yaml

configFile="config.yaml"

def readConfig():
	print "Reading config"
	with open(configFile, 'r') as ymlfile:
		cfg = yaml.load(ymlfile)
	return cfg

if __name__ == "__main__":
	cfg = readConfig()
	print(cfg)

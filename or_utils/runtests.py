import ConfigParser
import subprocess 
import os 
import sys
import os.path 

def runTest(log, rule, alert, decoder, section, name, negate=False, debug=False):
    formated = "%s:%s:%s"%(rule,alert,decoder)
    p = subprocess.Popen(['sudo', '/var/ossec/bin/ossec-logtest', '-U',formated],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            shell=False)
    std_out = p.communicate(log)[0]
    if (p.returncode != 0 and not negate) or (p.returncode == 0 and negate):
        print "" 
        print "-" * 60
        print "Failed: Exit code = %s"%(p.returncode) 
        print "        Alert     = %s"%(alert) 
        print "        Rule      = %s"%(rule)
        print "        Decoder   = %s"%(decoder)
        print "        Section   = %s"%(section)
        print "        line name = %s"%(name)
        print " " 
        print std_out 
    elif debug:
        print "Exit code= %s"%(p.returncode) 
        print std_out
    else:
        sys.stdout.write(".")

def run(tpath="./tests"):
    debug = False
    for aFile in os.listdir(tpath):
        aFile = os.path.join(tpath, aFile)
        print "- [ File = %s ] ---------"%(aFile)
        if aFile.endswith(".ini"):
            tGroup = ConfigParser.ConfigParser()
            tGroup.read([aFile])
            tSections = tGroup.sections()
            for t in tSections:
                rule = tGroup.get(t, "rule")
                alert = tGroup.get(t, "alert")
                decoder = tGroup.get(t, "decoder")
                for (name, value) in tGroup.items(t):
                    if name.startswith("log "):
                        if debug: 
                            print "-"* 60
                        if name.endswith("pass"):
                            neg = False 
                        elif name.endswith("fail"):
                            neg = True
                        else:
                            neg = False 
                        runTest(value, rule, alert, decoder, t, name, negate=neg)
            print ""

if __name__ == "__main__":
    run()
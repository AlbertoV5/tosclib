from tosclib import tosc
import argparse, re

def CopyScripts(input : str, output : str, source : str = "source", target : str = "target"):
    """Find the script in source and copy it to all children in target"""
    
    script = tosc.pullValueFromKey(
                        inputFile = input,
                        key = "name",
                        value = source,
                        targetKey = "script")
                        
    root = tosc.load(input)
    main = tosc.ElementTOSC(root[0])

    for primary in main.children:
        primary = tosc.ElementTOSC(primary)

        if re.fullmatch(primary.getPropertyValue("name").text, target):
            continue
        
        for secondary in primary.children:
            secondary = tosc.ElementTOSC(secondary)
            secondary.createProperty("s", "script", script)
 
        tosc.write(root, output)

        return print(f"\nWrote: \n{script}\nTo file: {output}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--Input", help = ".tosc input file", required = True)
    parser.add_argument("-o", "--Output", help = ".tosc input file", required = True)
    parser.add_argument("-s", "--Source", help = "Tosc object source name")
    parser.add_argument("-t", "--Target", help = "Tosc object target name")

    args = parser.parse_args()

    # For testing purposes
    args.Source = "source" if args.Source == None else args.Source
    args.Target = "target" if args.Target == None else args.Target

    CopyScripts(args.Input, args.Output, args.Source, args.Target)

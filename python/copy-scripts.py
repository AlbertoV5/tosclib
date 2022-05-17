from tosclib import tosc
import argparse

def CopyScripts(
                    inputFile : str, 
                    outputFile : str, 
                    source : str = "source", 
                    target : str = "target") -> bool:
    """Find the script in source and copy it to all children in target"""
    
    script = tosc.Property.pullValueFromKey(
                        inputFile = inputFile,
                        key = "name",
                        value = source,
                        targetKey = "script")
                        
    root = tosc.load(inputFile)
    main = tosc.Node.getMainElements(root[0])

    for child in main["children"]:
        
        if not tosc.Property.getValueFromKey(child, "name") == target:
            continue
        target = tosc.Node.getMainElements(child)

        for box in target["children"]:
            tosc.Property.create(box, "s", "script", script)
        
        tosc.write(root, outputFile)
        return print(f"\nWrote: \n{script}\nTo file: {outputFile}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--Input", help = ".tosc file")
    parser.add_argument("-o", "--Output", help = ".tosc file")
    parser.add_argument("-s", "--Source", help = "Source name")
    parser.add_argument("-t", "--Target", help = "Target name")

    args = parser.parse_args()

    args.Output = args.Input if args.Output == None else args.Output
    args.Source = "source" if args.Source == None else args.Source
    args.Target = "target" if args.Target == None else args.Target

    print(args)
    
    CopyScripts(args.Input, args.Output, args.Source, args.Target)
    
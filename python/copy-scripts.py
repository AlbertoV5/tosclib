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
    main = tosc.node.getMainElements(root[0])

    for child in main["children"]:
        
        if not tosc.Property.getValueFromKey(child, "name") == target:
            continue
        target = tosc.node.getMainElements(child)

        for box in target["children"]:
            tosc.Property.create(box, "s", "script", script)
        
        return tosc.write(root, outputFile)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--Input", help = ".tosc file")
    parser.add_argument("-o", "--Output", help = ".tosc file")
    parser.add_argument("-s", "--Source", help = "Source name")
    parser.add_argument("-t", "--Target", help = "Target name")

    args = parser.parse_args()

    args.Output = args.Input if args.Output == None else args.Output
    
    CopyScripts(args.Input, args.Output, args.Source, args.Target)
    print(f"\nWrote to file: {args.Output}")
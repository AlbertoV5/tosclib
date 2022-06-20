import tosclib as tosc
import re


def main(inputFile, outputFile, sourceName, targetName):

    # Find the script string with a streaming parser
    script = tosc.pullValueFromKey(
        inputFile=inputFile, key="name", value=sourceName, targetKey="script"
    )

    root = tosc.load(inputFile)
    main = tosc.ElementTOSC(root[0])

    for group in main.children:
        group = tosc.ElementTOSC(group)

        # Move on if the Property is not the target
        if re.fullmatch(group.get_prop("name")[1], targetName) is None:
            continue

        # Assuming the Element is the target, iterate through children
        for box in group.children:
            box = tosc.ElementTOSC(box)
            if box.has_prop("script"):
                box.set_prop(("script", script))
            else:
                box.add_prop(("script", script))

        tosc.write(root, outputFile)

        return print(f"Wrote:\n \n{script}\n\nTo file: {outputFile}")


if __name__ == "__main__":

    main("docs/demos/files/test.tosc", "docs/demos/files/out.tosc", "source", "target")

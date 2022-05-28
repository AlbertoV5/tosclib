import tosclib as tosc
import argparse


def addProperty(args):

    root = tosc.load(args.Input)
    parent = tosc.ElementTOSC(root[0])

    # Set the property to the parent node, not root
    parent.createProperty(type=args.Type, key=args.Property, text=args.Value)

    print("Added Property: ")
    parent.showProperty(args.Property)
    tosc.write(root, args.Output)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--Input", help=".tosc input file", required=True)
    parser.add_argument("-o", "--Output", help=".tosc output file", required=True)
    parser.add_argument("-p", "--Property", help="Name of the Property")
    parser.add_argument("-v", "--Value", help="Contents of the Property")
    parser.add_argument(
        "-t",
        "--Type",
        help="Type of the property. Best is 's'.",
        choices=["s", "b", "c", "r"],
    )

    args = parser.parse_args()

    # For testing purposes
    args.Property = "CustomProperty" if args.Property == None else args.Property
    args.Value = "Update" if args.Value == None else args.Value
    args.Type = "s" if args.Type == None else args.Type

    addProperty(args)

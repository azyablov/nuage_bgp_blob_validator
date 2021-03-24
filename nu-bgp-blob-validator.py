from lxml import etree
import os
import argparse
import sys


if __name__ == '__main__':
    """
    Main entry point
    """
    # Parsing arguments
    argp_desc = sys.argv[0] + ' BGP BLOB validation'
    arg_par = argparse.ArgumentParser(prog='nf_pg', description=argp_desc)
    arg_par.add_argument('-p', help='validate against BGP policy schema', action='store_true',
                         required=False)
    arg_par.add_argument('-n', help='validate against BGP neighbor schema', action='store_true',
                         required=False)
    arg_par.add_argument('-x', help='XML file', action='store', required=True)
    args = arg_par.parse_args()
    if ( args.n and args.p ) or ( not args.n and not args.p ):
        print("Schema option is not provided OR should be one only: -p OR -n")
        exit(1)
    if args.p:
        schema_file = "./xsd/bgp-routing-policies.xsd"
    elif args.n:
        schema_file = "./xsd/bgp-routing-neighbor.xsd"

    if os.path.exists(args.x) and os.access(args.x, os.R_OK):
        try:
            with open(args.x, mode='r', encoding='utf-8') as xfh:
                xml_str = xfh.read()
                xml_par = etree.XMLParser(ns_clean=True, encoding='utf-8', remove_blank_text=True)
                xdata: etree._Element = etree.fromstring(bytes(xml_str, encoding='utf-8'), parser=xml_par)
        except OSError as ose:
            print("Unable to open XML file!")
    else:
        print("File does not exist OR access rights preventing reading the file.")
        exit(2)
    # Validate against XML schema
    try:
        bgp_schema = etree.XMLSchema(file=schema_file)
        v_res = bgp_schema.validate(xdata)
        if not v_res:
            print("XML document is invalid!")
            print(bgp_schema.error_log)
            exit(3)
        print("ok ;)")
    except etree.XMLSchemaParseError as spe:
        raise
    exit(0)

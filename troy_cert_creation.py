import os
import sys
import argparse

CERT_TOP_PART = "/usr/local/pitt_scripts/certs/top_part.txt"
CERT_MIDDLE_PART = "/usr/local/pitt_scripts/certs/middle.txt"


def sanity_check(output):
    """Check to make sure that top_part.txt and middle.txt files exist in
    correct path. Check that we can write to destination directory
    
    Program will exit if any checks fail
    """
    if not os.path.exists(CERT_TOP_PART):
        print("SANITY CHECK: File {} does not exist!".format(CERT_TOP_PART))
        sys.exit(1)

    if not os.path.exists(CERT_MIDDLE_PART):
        print("SANITY CHECK: File {} does not exist!".format(CERT_MIDDLE_PART))
        sys.exit(1)

    if not os.access(output, os.W_OK):
        print("SANITY CHECK: Cannot write to {} !".format(output))
        sys.exit(1)


def build_arg_parser():
    """Builds a standard argument parser for output of cert files"""
    parser = argparse.ArgumentParser(
            description='Standard arguments for building a cert')

    parser.add_argument('-o', '--output',
                        required=True,
                        action='store',
                        help='Directory to output files to')

    parser.add_argument('-c', '--common-name',
                        required=False,
                        action='store',
                        help='Common Name for cert')

    parser.add_argument('-s', '--sans',
                        required=False,
                        action='store',
                        help='Filename containing list of SANs for CN')

    return parser.parse_args()


def build_config(cn, names):
    """Build the .cfg file that will be used to generate the cert"""
    new_cfg = open(cn + ".cfg", "w+")

    with open(CERT_TOP_PART, 'r') as f:
        new_cfg.write(f.read())

    new_cfg.write('commonName_default = ' + cn + '\n')

    with open(CERT_MIDDLE_PART, 'r') as f:
        new_cfg.write(f.read())

    for n in names:
        new_cfg.write(n + '\n')

    new_cfg.close()

    return cn + ".cfg"


def sans():
    names = []
    print("Please enter the SANs")
    for i in range(2000):
        z = raw_input()
        t = i + 1
        if z != "":
            names.append("DNS." + str(t) + " = " + z.strip())
        else:
            return names


def main():
    args = build_arg_parser()

    # For saftey's sake!
    sanity_check(args.output)

    # We are able to write to the directory that the user
    # provided for output, so switch our working directory to there
    os.chdir(args.output)

    cn = raw_input("Please enter the common name ")
    cn = cn.strip()

    names = sans()

    new_cfg = build_config(cn, names)

    create_csr_key = os.system('openssl req -out ' + cn + '.csr -new -newkey rsa:2048 -nodes -keyout ' + cn + '.key -sha256 -config ' + cn + '.cfg' + '\n' + '\n' + '\n' + '\n' + '\n')

    print create_csr_key

    csr_name = cn + '.csr'
    key_name = cn + '.key'

    print os.getcwd() + "/" + csr_name
    print os.getcwd() + "/" + key_name
    print os.getcwd() + "/" + new_cfg


# Run
if __name__ == "__main__":
    main()

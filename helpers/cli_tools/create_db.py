import argparse
import sqlite3

def main(create_path, db_type, output_path):


    # Read the create script
    with open(create_path, 'r') as f:
        create_script = f.read()
    
    # Create the database
    if db_type == 'sqlite':
        conn = sqlite3.connect(output_path)
        cursor = conn.cursor()
        cursor.executescript(create_script)
        conn.commit()
        conn.close()
    else:
        print('Only sqlite is supported for now')
        return


if __name__ == '__main__':
    # Create script is required to be run from the command line
    
    parser = argparse.ArgumentParser(description='Create a database')
    
    # Add creat script argument
    parser.add_argument('create_script_path', type=str, help='Path to the create script')

    # db_type is optional, default is sqlite (only permitted option for now)
    parser.add_argument('db_type', type=str, help='Type of database to create', default='sqlite')

    # Add output path argument, only to be used with sqlite
    parser.add_argument('output_path', type=str, help='Path to the output database file', default='db.sqlite')

    # add overwrite argument should be called as --overwrite, default is False
    parser.add_argument('--overwrite', action='store_true', help='Overwrite the database if it exists', default=False)


    args = parser.parse_args()

    # Validate db_type
    if args.db_type != 'sqlite':
        print('Only sqlite is supported for now')
        exit(1)

    # If db_type is sqlite, output_path is required
    if args.db_type == 'sqlite' and args.output_path == 'db.sqlite':
        print('Output path is required for sqlite')
        exit(1)

    # Validate overwrite
    if args.overwrite and not args.output_path:
        print('Output path is required to overwrite')
        exit(1)
    elif args.overwrite and args.output_path:
        print('Overwriting the database')
        # Delete the database
        import os
        os.remove(args.output_path)
        
    main(args.create_script_path, args.db_type, args.output_path)
#![deny(
    warnings,
    unsafe_code,
    unused_import_braces,
    unused_qualifications,
    trivial_casts,
    trivial_numeric_casts
)]

use std::path::PathBuf;
use std::io::{self, Read, Write};
use std::fs::File;
use clap::{App, Arg, ArgMatches, SubCommand};
use liblox::keyring::get_os_keyring;
use liblox::{KeyRing, KeyRingSecret};
use zeroize::Zeroize;
use colored::Colorize;

use std::collections::BTreeMap;

#[cfg(target_os = "macos")]
use liblox::keyring::macos::MacOsKeyRing as OsKeyRing;

#[cfg(target_os = "linux")]
use liblox::keyring::linux::LinuxOsKeyRing as OsKeyRing;

#[cfg(target_os = "windows")]
use liblox::keyring::windows::WindowsOsKeyRing as OsKeyRing;

fn main() {
    let matches = App::new("Lox")
        .version("0.1")
        .author("Michael Lodder")
        .about("Lox is a platform independent program for storing and retrieving information from secure enclaves or keyrings")
        .subcommand(SubCommand::with_name("get")
            .about("Retrieve a secret identified by ID. If no ID is specified or ID is '-', input is received from STDIN")
            .arg(Arg::with_name("SERVICE")
                .help("The service name to use for associating with this secret. The reason a service name is required is if no service name is specified, the default name would be the current calling process name. This sort of behavior has been known to lead to privilege escalation when used incorrectly so it is preferred to specify a service name.")
                .required(true)
                .index(1))
            .arg(Arg::with_name("ID")
                .help("The ID to retrieve. If no ID is specified or ID is '-', input is received from STDIN")
                .required(false)
                .index(2)))
        .subcommand(SubCommand::with_name("set")
            .about("Save a secret identified by ID. If no ID is specified or ID is '-', input is received from STDIN")
            .arg(Arg::with_name("SERVICE")
                .help("The service name to use for associating with this secret. The reason a service name is required is if no service name is specified, the default name would be the current calling process name. This sort of behavior has been known to lead to privilege escalation when used incorrectly so it is preferred to specify a service name.")
                .required(true)
                .index(1))
            .arg(Arg::with_name("ID")
                .help("The ID to retrieve.")
                .required(true)
                .index(2))
            .arg(Arg::with_name("SECRET")
                .help("The SECRET to be saved. If no SECRET is specified, input is received from STDIN")
                .required(false)
                .index(3)))
        .subcommand(SubCommand::with_name("delete")
            .about("Delete a secret identified by ID. If no ID is specified or ID is '-', input is received from STDIN")
            .arg(Arg::with_name("SERVICE")
                .help("The service name to use for associating with this secret. The reason a service name is required is if no service name is specified, the default name would be the current calling process name. This sort of behavior has been known to lead to privilege escalation when used incorrectly so it is preferred to specify a service name. Use the keyword 'kind' to designate which type of secret to look for on OSX. 'kind' can be either internet or generic. If 'kind' is not specified, Lox will try whichever type can be searched based on the other criteria provided")
                .required(true)
                .index(1))
            .arg(Arg::with_name("ID")
                .help("The ID to retrieve. If no ID is specified or ID is '-', input is received from STDIN")
                .required(false)
                .index(2)))
        .subcommand(SubCommand::with_name("peek")
            .about("Look up a secret identified by ID that is not managed by Lox. If no ID is specified or ID is '-', input is received from STDIN")
            .arg(Arg::with_name("ID")
                .help("The ID to retrieve. If no ID is specified or ID is '-', input is received from STDIN. The ID if formatted by using name-value pairs comma separated. For example, if you wanted to peek at any ID in the keyring with two attributes service and account, it would look like service=lox,account=api. Lox returns any items that it finds matching the search criteria")
                .required(false)
                .index(1)))
        .subcommand(SubCommand::with_name("list")
            .about("List all the secret names in the keychain.")
        ).get_matches();

    if let Some(matches) = matches.subcommand_matches("get") {
        get(matches);
    } else if let Some(matches) = matches.subcommand_matches("set") {
        set(matches);
    } else if let Some(matches) = matches.subcommand_matches("delete") {
        delete(matches)
    } else if let Some(matches) = matches.subcommand_matches("peek") {
        peek(matches)
    } else if let Some(_) = matches.subcommand_matches("list") {
        list()
    }
    else {
        die::<()>("Please specify a command to run [get | set | delete | peek | list]");
    }
}

fn get(matches: &ArgMatches) {
    let mut keyring = get_keyring(matches);
    let id = get_id(matches, true);

    let secret = keyring.get_secret(&id).unwrap_or_else(|e| die::<KeyRingSecret>(&e));
    io::stdout().write_all(secret.as_slice()).unwrap();
    io::stdout().flush().unwrap();
}

fn peek(matches: &ArgMatches) {
    let id = get_id(matches, false);

    let secrets = OsKeyRing::peek_secret(&id).unwrap_or_else(|e| die::<Vec<(String, KeyRingSecret)>>(&e));

    if secrets.len() == 1 && !id.is_empty() {
        io::stdout().write_all(secrets[0].1.as_slice()).unwrap();
        io::stdout().flush().unwrap();
        println!("");
    } else {
        for s in secrets {
            print!("{} -> ", s.0);
            io::stdout().write_all(s.1.as_slice()).unwrap();
            println!("");
            io::stdout().flush().unwrap();
        }
    }
}

fn list() {
    let secret_names = OsKeyRing::list_secrets().unwrap_or_else(|e| die::<Vec<BTreeMap<String, String>>>(&e));
    for s in secret_names {
        println!("{:?}", s);
    }
}

fn delete(matches: &ArgMatches) {
    let mut keyring = get_keyring(matches);
    let id = get_id(matches, true);

    keyring.delete_secret(&id).unwrap_or_else(|e| die::<()>(&e));
    println!("{}", "Success".green());
}

fn set(matches: &ArgMatches) {
    let mut keyring = get_keyring(matches);
    let id = matches.value_of("ID").unwrap();
    let mut secret = read_input(matches, "SECRET", true);

    keyring.set_secret(&id, &secret).unwrap_or_else(|e| die::<()>(&format!("Failed: {}", e)));
    secret.zeroize();
    println!("{}", "Success".green());
}

fn get_id(matches: &ArgMatches, read_stdin: bool) -> String {
    let id = read_input(matches, "ID", read_stdin);
    let mut id_str = String::new();
    if let Ok(s) = String::from_utf8(id).map_err(|e| format!("{}", e)) {
        id_str = s.to_string();
    } else {
        die::<()>("ID cannot be read properly");
    }
    id_str
}

fn get_keyring(matches: &ArgMatches) -> OsKeyRing {
    let service = matches.value_of("SERVICE").unwrap();
    match get_os_keyring(&service) {
        Ok(keyring) => keyring,
        Err(e) => die::<OsKeyRing>(&format!("Unable to get OS keyring: {}", e.as_str()))
    }
}

fn read_input(matches: &ArgMatches, name: &str, read_stdin: bool) -> Vec<u8> {
    match matches.value_of(name) {
        Some(text) => {
            match get_file(text) {
                Some(file) => {
                    match File::open(file.as_path()) {
                        Ok(mut f) => {
                            read_stream(&mut f)
                        },
                        Err(_) => {
                            die::<Vec<u8>>(&format!("Unable to read file {}", file.to_str().unwrap()))
                        }
                    }
                }
                None => {
                    text.as_bytes().to_vec()
                }
            }
        }
        None => {
            if atty::is(atty::Stream::Stdin) {
                if read_stdin {
                    rpassword::read_password_from_tty(Some("Enter Secret: ")).unwrap().as_bytes().to_vec()
                } else {
                    Vec::new()
                }
            } else {
                let mut f = io::stdin();
                read_stream(&mut f)
            }
        }
    }
}

fn read_stream<R: Read>(f: &mut R) -> Vec<u8> {
    let mut bytes = Vec::new();
    let mut buffer = [0u8; 4096];

    let mut read = f.read(&mut buffer);
    while read.is_ok() {
        let n = read.unwrap();

        if n == 0 {
            break;
        }

        bytes.extend_from_slice(&buffer[..n]);

        read = f.read(&mut buffer);
    }

    bytes
}

fn get_file(name: &str) -> Option<PathBuf> {
    let mut file = PathBuf::new();
    file.push(name);
    if file.as_path().is_file() {
        let metadata = file
            .as_path()
            .symlink_metadata()
            .expect("symlink_metadata call failed");
        if metadata.file_type().is_symlink() {
            match file.as_path().read_link() {
                Ok(f) => file = f,
                Err(_) => die::<()>(&format!("Can't read the symbolic link: {}", name))
            }
        }
        Some(file)
    } else {
        None
    }
}

fn die<R: Sized>(final_message: &str) -> R {
    eprintln!("{}", final_message.red());
    std::process::exit(1);
}

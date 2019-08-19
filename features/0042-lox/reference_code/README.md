# Lox

A command line tool for accessing various keychains or secure enclaves.

## The problem

Applications use several credentials today to secure data locally and during transmitted.
However, bad habits happen when safeguarding these credentials. For example, when creating an API token for Amazon's AWS, Amazon generates
a secret key on a user's behalf and is downloaded to a CSV file. Programmers do not know how to best
sure these downloaded credentials because they must be used in a program to make API calls.
They don't which of the following is the best option. They can:

- Put these credentials directly in the program like most do as constant variables but this is a terrible option because attackers can analyze the code and extract it.
- Use environment variables. If so, should it passed as at the command level or put in a global variable registry? Both are susceptible to sniffing memory or process information.
- Read a config file that contains the credentials but must rely on the security of the operating system to manage access control.
- Use secure enclaves to store the credentials but this just shifts to another problem as secure enclaves rely on yet another set of credentials to ensure the application has the correct authorization. These come as hardware security modules (HSM) or trusted execution environments (TEE)
- Require interaction with a user or group to supply the credential for each use or cache it for a period of time. This is usually done with passwords, pins, cyber tokens, and biometrics.

Where to put the credential that is directly used by applications or people is called the top level credential problem.

There are services like [LeakLooker](https://github.com/woj-ciech/LeakLooker) that browse the internet looking for credentials that can be scrapped and unfortunately but often [succeed](https://hackernoon.com/leaklooker-v2-find-more-open-servers-and-source-code-leaks-25e671700e41?mc_cid=47325dd839&mc_eid=0ff0c85eaf).
Some projects have documented how to test credentials to see if they have been revealed. See [keyhacks](https://github.com/streaak/keyhacks).

These document aims to provide guidance and aid in adopting best practices and developing code to address the top level credential problem–-the credential used to protect all others–the keys to the kingdom–or a secret that is used directly by a program that if compromised would yield disastrous consequences.

## The solution

*Lox* is a layer that is designed to be a command line tool or API library for storing secrets.
The default is to use the operating system keychain. The goal is to add to *Lox* to allow for 
many different enclaves that are optimal for storing the keys to the kingdom like YubiKey, Intel SGX, or Arm Trustzone.
In principle, a system's secure enclave should be able to keep some credentials away from `root` (as in, the attacker can *use* the credential as long as they have access, but they can't extract the credential for persistence), and assuming no other attacks like [Foreshadow](https://foreshadowattack.eu/).

Mac OS X, Linux, and Android have built-in keychains that are guarded by the operating system.
iOS and Android come with hardware secure enclaves or trusted execution environments for managing the secrets stored in the keychain.

This first iteration uses the OS keychain or an equivalent and uses the command line or is a C callable API.
Future work could allow for communication over unix or tcp sockets with *Lox* running as a daemon process.

Currently Mac OS X offers support for a [CLI tool](https://www.netmeister.org/blog/keychain-passwords.html) and [libraries](https://developer.apple.com/documentation/security) but they are complex to understand and can be prone to misuse due to misunderstandings.
*Lox* removes the complexity by choosing secure defaults so developers can focus on their job. 

*Lox* is written in Rust and has no external dependencies to do its job except DBus on linux.

The program can be compiled from any OS to run on any OS. Lox-CLI is the command line tool while Lox is the library.

## Run the program

Basic Usage

Requires dbus library on linux.

On ubuntu, this is libdbus-1-3 when running.
On redhat, this is dbus when running.

Gnome-keyring or KWallet must also be installed on Linux.

*Lox* can be run either using **cargo run -- \<args\>** or if it is already built from [source](#build-from-source)
using *./lox*.

*Lox* tries to determine if input is a file or text. If a file exists that matches the entered text, *Lox* will
read the contents. Otherwise, it will prompt the user for either the id of the secret or to enter a secret.

*Lox* stores secrets based on a service name and an ID. The service name is the name of the program or process that only is allowed to access the secret with ID.
Secrets can be retrieved, stored, or deleted.

When secrets are stored, care should be given to not pass the value over the command line as it could be stored in the command line history.
For this reason, either put the value in a file or *Lox* will read it from STDIN. After *Lox* stores the secret, Lox will securely wipe it from memory.

## Caveat
One remaining problem is how to solve the service name provided to *Lox*.  Ideally *Lox* could compute it instead of supplied from the calling endpoint which can lie about the name.
We can imagine an attacker who wants access to the aws credentials in the keychain just needs to know the service name and the id of the secret to request it. Access is still blocked by
the operating system if the attacker doesn't know the keychain credentials similar to a password vault. If *Lox* could compute the service name then this makes it harder for an attacker
to retrieve targeted secrets. However, this is better than the secrets existing in plaintext in code, config files, or environment variables.

## Examples 
*Lox* takes at least two arguments: service_name and ID.
When storing a secret, an additional parameter is needed. If omitted (the preferred method) the value is read from STDIN.

### Storing a secret
```bash
lox set aws 1qwasdrtyuhjnjyt987yh
prompt> ...<Return>
Success
``` 

### Retrieve a secret
```bash
lox get aws 1qwasdrtyuhjnjyt987yh
<Secret Value>
```

### Delete a secret
```bash
lox delete aws 1qwasdrtyuhjnjyt987yh
```

### List all secrets
*Lox* can read all values stored in the keyring. List will just list the name
of all the values in the keyring without retrieving their actual values.
```bash
lox list
``` 

```
{"application": "lox", "id": "apikey", "service": "aws", "username": "mike", "xdg:schema": "org.freedesktop.Secret.Generic"}
{"application": "lox", "id": "walletkey", "service": "indy", "username": "mike", "xdg:schema": "org.freedesktop.Secret.Generic"}
```

### Peek secrets
*Lox* can retrieve all or a subset of secrets in the keyring. Peek without
any arguments will pull out all keyring names and their values. Because Lox
encrypts values before storing them in the keyring if it can, those values
will be returned as hex values instead of their associated plaintext.
Peek filtering is different based on the operating system. 

For OSX, filtering
is based on the **kind** that should be read. It can be __generic__ or __internet__ passwords.
__generic__ only requires the *service* and *account* labels. __internet__ requires the *server*, *account*, *protocol*, *authentication_type* values.
Filters are supplied as name value pairs separated by = and multiple pairs separated by a comma.
```bash
lox peek service=aws,account=apikey
```

For Linux, filtering is based on a subset of name value pairs of the attributes that match.
For example, if the attributes in the keyring were like this
```
{"application": "lox", "id": "apikey", "service": "aws", "username": "mike", "xdg:schema": "org.freedesktop.Secret.Generic"}
{"application": "lox", "id": "walletkey", "service": "indy", "username": "mike", "xdg:schema": "org.freedesktop.Secret.Generic"}
```
To filter based on *id*, run
```bash
lox peek id=apikey
```
To filter based on *username* AND *service*, run 
```bash
lox peek username=mike,service=aws
```

For Windows, filtering is based on the credentials targetname and globbing.
For example, if *list* returned
```
{"targetname": "MicrosoftAccount:target=SSO_POP_Device"}
{"targetname": "WindowsLive:target=virtualapp/didlogical"}
{"targetname": "LegacyGeneric:target=IEUser:aws:apikey"}
```
then filtering searches everything after ":target=". In this case, if the value
to be peeked is IEUser:aws:apikey, the following will return just that result
```bash
lox.exe peek IE*
lox.exe peek IE*apikey
lox.ece peek IEUser:aws:apikey
```

## Build from source
[build-from-source]: # build-from-source

To make a distributable executable, run the following commands:

1. On Linux install dbus library. On a debian based OS this is libdbus-1-dev. On a Redhat based OS this is dbus-devel.
1. **curl https://sh.rustup.rs -sSf | sh -s -- -y** - installs the run compiler
1. **cd reference_code/**
1. **cargo build --release** - when this is finished the executable is *target/release/lox*.
1. For \*nix users **cp target/release/lox /usr/local/lib** and **chmod +x /usr/local/lib/lox**
1. For Windows users copy **target/release/lox.exe** to a folder and add that folder to your %PATH variable.

Liblox is the library that can be linked to programs to manage secrets.
Use the library for the underlying operating system that meets your needs

1. **liblox.dll** - Windows
1. **liblox.so** - Linux
1. **liblox.dylib** - Mac OS X


## FUTURE WORK

Allow for other enclaves like Hashicorp vault, LastPass, 1Password.
Allow for steganography methods like using images or Microsoft Office files for storing the secrets.
